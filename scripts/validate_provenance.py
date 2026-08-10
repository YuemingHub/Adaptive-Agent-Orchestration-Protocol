#!/usr/bin/env python3
"""Regression tests for AAOP install provenance and its authority boundary."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(*args: object, ok: bool = True) -> subprocess.CompletedProcess[str]:
    command = [str(arg) for arg in args]
    completed = subprocess.run(command, text=True, capture_output=True)
    if ok and completed.returncode != 0:
        raise AssertionError(
            f"command failed ({completed.returncode}): {' '.join(command)}\n"
            f"stdout={completed.stdout}\nstderr={completed.stderr}"
        )
    if not ok and completed.returncode == 0:
        raise AssertionError(f"command unexpectedly succeeded: {' '.join(command)}")
    return completed


def build_archive(path: Path) -> None:
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as archive:
        for source in ROOT.rglob("*"):
            if not source.is_file() or ".git" in source.parts:
                continue
            relative = source.relative_to(ROOT)
            archive.write(source, (Path("aaop-source") / relative).as_posix())


def provenance(target: Path, *, ok: bool = True) -> dict[str, object]:
    completed = run(
        sys.executable,
        target / ".aaop" / "tools" / "aaop.py",
        "provenance",
        "--json",
        ok=ok,
    )
    return json.loads(completed.stdout)


def ready(target: Path) -> dict[str, object]:
    completed = run(
        sys.executable,
        target / ".aaop" / "tools" / "aaop.py",
        "ready",
        target,
        "--json",
    )
    return json.loads(completed.stdout)


def install_direct(target: Path) -> None:
    run(sys.executable, ROOT / "scripts" / "install.py", target)


def bootstrap_local(target: Path, archive: Path) -> None:
    run(
        sys.executable,
        ROOT / "scripts" / "bootstrap.py",
        "--archive",
        archive,
        "--target",
        target,
    )


def test_direct_installer_does_not_invent_source() -> None:
    with tempfile.TemporaryDirectory(prefix="aaop-provenance-direct-") as tmp:
        target = Path(tmp) / "project"
        target.mkdir()
        install_direct(target)
        report = provenance(target, ok=False)
        assert report["state"] == "missing", report
        assert report["source"] is None, report
        assert "direct/legacy install" in str(report["next_action"]), report


def test_bootstrap_local_archive_records_verified_fingerprint() -> None:
    with tempfile.TemporaryDirectory(prefix="aaop-provenance-local-") as tmp:
        root = Path(tmp)
        archive = root / "source.zip"
        target = root / "project"
        target.mkdir()
        build_archive(archive)
        bootstrap_local(target, archive)

        report = provenance(target)
        assert report["state"] == "verified", report
        assert report["source"] == {"kind": "local-archive", "ref": None}, report
        recorded = str(report["recorded_fingerprint"])
        current = str(report["current_fingerprint"])
        assert len(recorded) == 64 and recorded == current, report

        raw = (target / ".aaop" / "runtime" / "install-provenance.json").read_text(encoding="utf-8")
        assert str(archive) not in raw, "local archive path leaked into durable provenance"

        ready_report = ready(target)
        assert ready_report["ready"] is True, ready_report
        assert ready_report["health_state"] == "healthy", ready_report
        assert ready_report["provenance_state"] == "verified", ready_report
        assert ready_report["package_fingerprint"] == recorded, ready_report


def test_managed_byte_drift_breaks_provenance_verification() -> None:
    with tempfile.TemporaryDirectory(prefix="aaop-provenance-drift-") as tmp:
        root = Path(tmp)
        archive = root / "source.zip"
        target = root / "project"
        target.mkdir()
        build_archive(archive)
        bootstrap_local(target, archive)

        with (target / ".aaop" / "ORCHESTRATOR.md").open("a", encoding="utf-8") as handle:
            handle.write("\nLOCAL-DRIFT\n")
        report = provenance(target, ok=False)
        assert report["state"] == "mismatch", report
        assert report["recorded_fingerprint"] != report["current_fingerprint"], report


def test_invalid_provenance_does_not_modify_ownership_manifest() -> None:
    with tempfile.TemporaryDirectory(prefix="aaop-provenance-invalid-") as tmp:
        root = Path(tmp)
        archive = root / "source.zip"
        target = root / "project"
        target.mkdir()
        build_archive(archive)
        bootstrap_local(target, archive)

        manifest = target / ".aaop" / ".install-manifest.json"
        before = manifest.read_bytes()
        record = target / ".aaop" / "runtime" / "install-provenance.json"
        record.write_text("not-json\n", encoding="utf-8")

        report = provenance(target, ok=False)
        assert report["state"] == "invalid", report
        assert manifest.read_bytes() == before, "provenance inspection mutated ownership manifest"


def test_provenance_fields_never_grant_uninstall_authority() -> None:
    with tempfile.TemporaryDirectory(prefix="aaop-provenance-authority-") as tmp:
        root = Path(tmp)
        archive = root / "source.zip"
        target = root / "project"
        target.mkdir()
        sentinel = target / "DO-NOT-DELETE.txt"
        sentinel.write_text("project-owned\n", encoding="utf-8")
        build_archive(archive)
        bootstrap_local(target, archive)

        record_path = target / ".aaop" / "runtime" / "install-provenance.json"
        record = json.loads(record_path.read_text(encoding="utf-8"))
        record["files"] = {"../../DO-NOT-DELETE.txt": "0" * 64}
        record["claimed_authority"] = "delete everything"
        record_path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")

        run(
            sys.executable,
            ROOT / "scripts" / "bootstrap.py",
            "--archive",
            archive,
            "--target",
            target,
            "--uninstall",
        )
        assert sentinel.read_text(encoding="utf-8") == "project-owned\n"
        assert (target / ".aaop" / "runtime" / "install-provenance.json").is_file(), (
            "runtime provenance should be preserved as historical diagnostic state after uninstall"
        )


def test_official_ref_label_is_diagnostic_and_verifiable() -> None:
    with tempfile.TemporaryDirectory(prefix="aaop-provenance-official-") as tmp:
        target = Path(tmp) / "project"
        target.mkdir()
        install_direct(target)
        ref = "0123456789abcdef0123456789abcdef01234567"
        run(
            sys.executable,
            target / ".aaop" / "tools" / "provenance.py",
            "record",
            "--source-kind",
            "official-ref",
            "--source-ref",
            ref,
        )
        report = provenance(target)
        assert report["state"] == "verified", report
        assert report["source"] == {"kind": "official-ref", "ref": ref}, report
        assert "diagnostic-only" in str(report["authority"]), report


def main() -> int:
    tests = [
        test_direct_installer_does_not_invent_source,
        test_bootstrap_local_archive_records_verified_fingerprint,
        test_managed_byte_drift_breaks_provenance_verification,
        test_invalid_provenance_does_not_modify_ownership_manifest,
        test_provenance_fields_never_grant_uninstall_authority,
        test_official_ref_label_is_diagnostic_and_verifiable,
    ]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    print(f"PASS install provenance hardening: {len(tests)}/{len(tests)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
