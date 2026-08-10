#!/usr/bin/env python3
"""Regression tests for AAOP lifecycle transactionality and manifest trust boundaries."""

from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_PACKAGE = ROOT / ".aaop"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


installer = load_module("aaop_install", ROOT / "scripts" / "install.py")
bootstrap = load_module("aaop_bootstrap", ROOT / "scripts" / "bootstrap.py")


def file_bytes(path: Path) -> bytes | None:
    return path.read_bytes() if path.is_file() else None


def capture_install_state(target: Path) -> dict[str, bytes | None]:
    manifest = json.loads((target / ".aaop" / installer.MANIFEST_NAME).read_text(encoding="utf-8"))
    result: dict[str, bytes | None] = {
        "manifest": file_bytes(target / ".aaop" / installer.MANIFEST_NAME),
        "AGENTS.md": file_bytes(target / "AGENTS.md"),
        "CLAUDE.md": file_bytes(target / "CLAUDE.md"),
    }
    for relative in manifest["files"]:
        result[f"aaop:{relative}"] = file_bytes(target / ".aaop" / relative)
    return result


def assert_install_state(target: Path, expected: dict[str, bytes | None]) -> None:
    current = capture_install_state(target)
    assert current == expected, "installation state changed across failed transaction"


def health(target: Path) -> dict[str, object]:
    command = [
        sys.executable,
        str(target / ".aaop" / "tools" / "health.py"),
        str(target),
        "--json",
    ]
    completed = subprocess.run(command, check=True, text=True, capture_output=True)
    return json.loads(completed.stdout)


def assert_healthy(target: Path) -> None:
    report = health(target)
    assert report["state"] == "healthy", report


def install_clean(target: Path) -> None:
    mode, *_ = installer.install_or_upgrade(SOURCE_PACKAGE, target, upgrade=False)
    assert mode == "installed"
    assert not (target / installer.TRANSACTION_DIR_NAME).exists()
    assert_healthy(target)


def expect_system_exit(callable_, contains: str) -> None:
    try:
        callable_()
    except SystemExit as exc:
        assert contains in str(exc), (contains, exc)
    else:
        raise AssertionError(f"expected SystemExit containing {contains!r}")


def test_fresh_install_failure_rolls_back() -> None:
    with tempfile.TemporaryDirectory(prefix="aaop-install-fresh-failure-") as tmp:
        target = Path(tmp) / "project"
        target.mkdir()
        (target / "AGENTS.md").write_text("KEEP\n", encoding="utf-8")
        before_agents = (target / "AGENTS.md").read_bytes()

        original = installer.atomic_copy_file
        calls = 0
        failed = False

        def flaky(source: Path, destination: Path) -> None:
            nonlocal calls, failed
            calls += 1
            if not failed and calls == 3:
                failed = True
                raise OSError("injected fresh-install promotion failure")
            original(source, destination)

        installer.atomic_copy_file = flaky
        try:
            try:
                installer.install_or_upgrade(SOURCE_PACKAGE, target, upgrade=False)
            except OSError as exc:
                assert "injected fresh-install" in str(exc)
            else:
                raise AssertionError("expected injected fresh-install failure")
        finally:
            installer.atomic_copy_file = original

        assert not (target / ".aaop").exists(), "failed fresh install left a partial package"
        assert not (target / installer.TRANSACTION_DIR_NAME).exists(), "rolled-back transaction journal remained active"
        assert (target / "AGENTS.md").read_bytes() == before_agents


def test_upgrade_failure_rolls_back() -> None:
    with tempfile.TemporaryDirectory(prefix="aaop-install-upgrade-failure-") as tmp:
        target = Path(tmp) / "project"
        target.mkdir()
        (target / "AGENTS.md").write_text("PROJECT-RULE\n", encoding="utf-8")
        install_clean(target)
        before = capture_install_state(target)

        original = installer.atomic_copy_file
        calls = 0
        failed = False

        def flaky(source: Path, destination: Path) -> None:
            nonlocal calls, failed
            # begin_transaction snapshots use shutil.copy2, so these calls are promotion/rollback only.
            calls += 1
            if not failed and calls == 3:
                failed = True
                raise OSError("injected upgrade promotion failure")
            original(source, destination)

        installer.atomic_copy_file = flaky
        try:
            try:
                installer.install_or_upgrade(SOURCE_PACKAGE, target, upgrade=True)
            except OSError as exc:
                assert "injected upgrade" in str(exc)
            else:
                raise AssertionError("expected injected upgrade failure")
        finally:
            installer.atomic_copy_file = original

        assert not (target / installer.TRANSACTION_DIR_NAME).exists()
        assert_install_state(target, before)
        assert_healthy(target)


def test_uninstall_failure_rolls_back() -> None:
    with tempfile.TemporaryDirectory(prefix="aaop-install-uninstall-failure-") as tmp:
        target = Path(tmp) / "project"
        target.mkdir()
        install_clean(target)
        before = capture_install_state(target)

        original = installer.remove_block
        failed = False

        def flaky(path: Path) -> str:
            nonlocal failed
            if not failed:
                failed = True
                raise OSError("injected uninstall bootstrap failure")
            return original(path)

        installer.remove_block = flaky
        try:
            try:
                installer.transactional_uninstall(target)
            except OSError as exc:
                assert "injected uninstall" in str(exc)
            else:
                raise AssertionError("expected injected uninstall failure")
        finally:
            installer.remove_block = original

        assert not (target / installer.TRANSACTION_DIR_NAME).exists()
        assert_install_state(target, before)
        assert_healthy(target)


def test_future_manifest_is_fail_closed() -> None:
    with tempfile.TemporaryDirectory(prefix="aaop-install-future-manifest-") as tmp:
        target = Path(tmp) / "project"
        target.mkdir()
        install_clean(target)
        manifest_path = target / ".aaop" / installer.MANIFEST_NAME
        original = manifest_path.read_bytes()
        payload = json.loads(original)
        payload["schema_version"] = installer.MANIFEST_SCHEMA_VERSION + 100
        manifest_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

        expect_system_exit(
            lambda: installer.install_or_upgrade(SOURCE_PACKAGE, target, upgrade=True),
            "newer than this installer",
        )
        report = health(target)
        assert report["state"] == "unsupported-manifest", report
        manifest_path.write_bytes(original)
        assert_healthy(target)


def test_manifest_path_cannot_escape_package() -> None:
    with tempfile.TemporaryDirectory(prefix="aaop-install-manifest-path-") as tmp:
        target = Path(tmp) / "project"
        target.mkdir()
        install_clean(target)
        sentinel = target / "DO-NOT-DELETE.txt"
        sentinel.write_text("safe\n", encoding="utf-8")
        manifest_path = target / ".aaop" / installer.MANIFEST_NAME
        original = manifest_path.read_bytes()
        payload = json.loads(original)
        any_hash = next(iter(payload["files"].values()))
        payload["files"]["../../DO-NOT-DELETE.txt"] = any_hash
        manifest_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

        expect_system_exit(
            lambda: installer.transactional_uninstall(target),
            "unsafe managed path",
        )
        assert sentinel.read_text(encoding="utf-8") == "safe\n"
        report = health(target)
        assert report["state"] == "invalid-manifest", report
        manifest_path.write_bytes(original)
        assert_healthy(target)


def test_interrupted_journal_blocks_and_recovers() -> None:
    with tempfile.TemporaryDirectory(prefix="aaop-install-interrupted-") as tmp:
        target = Path(tmp) / "project"
        target.mkdir()
        install_clean(target)
        before = capture_install_state(target)
        manifest = json.loads((target / ".aaop" / installer.MANIFEST_NAME).read_text(encoding="utf-8"))
        planned = set(manifest["files"])
        transaction, metadata = installer.begin_transaction(target, planned, "upgrade")

        victim = next(iter(sorted(planned)))
        victim_path = target / ".aaop" / victim
        victim_path.write_text("INTERRUPTED-MIXED-VERSION\n", encoding="utf-8")

        report = health(target)
        assert report["state"] == "interrupted-install", report
        expect_system_exit(lambda: bootstrap.target_mode(target), "interrupted lifecycle transaction")
        expect_system_exit(
            lambda: installer.install_or_upgrade(SOURCE_PACKAGE, target, upgrade=True),
            "interrupted transaction exists",
        )

        archive = installer.recover_interrupted_transaction(target)
        assert archive.exists(), archive
        assert not transaction.exists()
        assert_install_state(target, before)
        assert_healthy(target)
        interrupted_backup = archive / "interrupted-current" / "aaop" / victim
        assert interrupted_backup.is_file(), interrupted_backup
        assert "INTERRUPTED-MIXED-VERSION" in interrupted_backup.read_text(encoding="utf-8")


def main() -> int:
    tests = [
        test_fresh_install_failure_rolls_back,
        test_upgrade_failure_rolls_back,
        test_uninstall_failure_rolls_back,
        test_future_manifest_is_fail_closed,
        test_manifest_path_cannot_escape_package,
        test_interrupted_journal_blocks_and_recovers,
    ]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    print(f"PASS installer transaction/manifest hardening: {len(tests)}/{len(tests)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
