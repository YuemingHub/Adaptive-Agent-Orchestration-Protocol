#!/usr/bin/env python3
"""Cross-platform regression tests for AAOP Journey state version/recovery safety."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JOURNEY_ID = "idea-to-production"


def run(*args: object, ok: bool = True) -> subprocess.CompletedProcess[str]:
    command = [str(arg) for arg in args]
    completed = subprocess.run(command, text=True, capture_output=True)
    if ok and completed.returncode != 0:
        raise AssertionError(
            f"command failed ({completed.returncode}): {' '.join(command)}\nstdout={completed.stdout}\nstderr={completed.stderr}"
        )
    if not ok and completed.returncode == 0:
        raise AssertionError(f"command unexpectedly succeeded: {' '.join(command)}\n{completed.stdout}")
    return completed


def install_target(root: Path) -> tuple[Path, Path]:
    target = root / "project"
    run(sys.executable, ROOT / "scripts" / "install.py", target)
    journey = target / ".aaop" / "tools" / "journey.py"
    run(
        sys.executable,
        journey,
        "start",
        JOURNEY_ID,
        "--goal",
        "turn the existing partial app into a verified online release",
        "--route",
        "feature-change",
        "--reason",
        "journey recovery regression",
    )
    return target, journey


def state_path(target: Path) -> Path:
    return target / ".aaop" / "runtime" / "journeys" / f"{JOURNEY_ID}.json"


def recovery_path(target: Path) -> Path:
    return target / ".aaop" / "runtime" / "journeys" / ".recovery" / f"{JOURNEY_ID}.last-good.json"


def status(journey: Path, *, ok: bool = True) -> subprocess.CompletedProcess[str]:
    return run(sys.executable, journey, "status", JOURNEY_ID, "--json", ok=ok)


def revision(journey: Path) -> int:
    return int(json.loads(status(journey).stdout)["revision"])


def checkpoint(journey: Path, expected: int, *extra: object, ok: bool = True) -> subprocess.CompletedProcess[str]:
    return run(
        sys.executable,
        journey,
        "checkpoint",
        JOURNEY_ID,
        "--expected-revision",
        expected,
        *extra,
        ok=ok,
    )


def test_last_good_snapshot_tracks_successful_state() -> None:
    with tempfile.TemporaryDirectory(prefix="aaop-journey-last-good-") as tmp:
        target, journey = install_target(Path(tmp))
        snapshot = recovery_path(target)
        assert snapshot.is_file(), snapshot
        first = json.loads(state_path(target).read_text(encoding="utf-8"))
        recovered = json.loads(snapshot.read_text(encoding="utf-8"))
        assert recovered == first

        rev = revision(journey)
        checkpoint(
            journey,
            rev,
            "--reason",
            "record a successful checkpoint",
            "--evidence",
            "successful evidence",
            "--next-action",
            "continue from the successful evidence",
        )
        current = json.loads(state_path(target).read_text(encoding="utf-8"))
        recovered = json.loads(snapshot.read_text(encoding="utf-8"))
        assert recovered == current
        assert current["revision"] == rev + 1


def test_future_schema_is_fail_closed_everywhere() -> None:
    with tempfile.TemporaryDirectory(prefix="aaop-journey-future-") as tmp:
        target, journey = install_target(Path(tmp))
        path = state_path(target)
        payload = json.loads(path.read_text(encoding="utf-8"))
        payload["schema_version"] = "9.0.0"
        path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        before = path.read_bytes()

        result = status(journey, ok=False)
        assert "newer state reader" in (result.stdout + result.stderr)

        result = checkpoint(
            journey,
            1,
            "--reason",
            "old tool must not downgrade future state",
            "--evidence",
            "future schema exists",
            ok=False,
        )
        assert "newer state reader" in (result.stdout + result.stderr)
        assert path.read_bytes() == before

        result = run(sys.executable, journey, "recover", JOURNEY_ID, ok=False)
        assert "newer" in (result.stdout + result.stderr).lower()
        assert path.read_bytes() == before


def test_current_schema_missing_revision_is_not_legacy() -> None:
    with tempfile.TemporaryDirectory(prefix="aaop-journey-missing-revision-") as tmp:
        target, journey = install_target(Path(tmp))
        path = state_path(target)
        payload = json.loads(path.read_text(encoding="utf-8"))
        assert payload["schema_version"] == "0.3.2"
        payload.pop("revision")
        path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

        result = status(journey, ok=False)
        combined = result.stdout + result.stderr
        assert "invalid revision" in combined
        assert "recover" in combined.lower()


def test_known_legacy_schema_migrates_from_revision_zero() -> None:
    with tempfile.TemporaryDirectory(prefix="aaop-journey-legacy-") as tmp:
        target, journey = install_target(Path(tmp))
        path = state_path(target)
        payload = json.loads(path.read_text(encoding="utf-8"))
        payload["schema_version"] = "0.3.1"
        payload.pop("revision")
        path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

        legacy = json.loads(status(journey).stdout)
        assert legacy["revision"] == 0, legacy
        checkpoint(
            journey,
            0,
            "--reason",
            "explicitly migrate known legacy checkpoint",
            "--evidence",
            "legacy checkpoint reconciled with current project state",
        )
        migrated = json.loads(status(journey).stdout)
        assert migrated["schema_version"] == "0.3.2", migrated
        assert migrated["revision"] == 1, migrated
        snapshot = json.loads(recovery_path(target).read_text(encoding="utf-8"))
        assert snapshot["schema_version"] == "0.3.2"
        assert snapshot["revision"] == 1


def test_corrupt_json_recovers_explicitly_and_invalidates_stale_writer() -> None:
    with tempfile.TemporaryDirectory(prefix="aaop-journey-corrupt-") as tmp:
        target, journey = install_target(Path(tmp))
        rev1 = revision(journey)
        checkpoint(
            journey,
            rev1,
            "--reason",
            "establish last good revision",
            "--evidence",
            "last-good evidence survives recovery",
            "--next-action",
            "resume after recovery",
        )
        stale = revision(journey)
        assert stale == 2
        path = state_path(target)
        path.write_text('{"schema_version":"0.3.2","broken":', encoding="utf-8")
        damaged_bytes = path.read_bytes()

        result = status(journey, ok=False)
        combined = result.stdout + result.stderr
        assert "invalid JSON" in combined
        assert "journey.py recover" in combined

        recovered = run(sys.executable, journey, "recover", JOURNEY_ID)
        assert "recovered explicitly" in recovered.stdout
        state = json.loads(status(journey).stdout)
        assert state["revision"] == stale + 1, state
        assert "last-good evidence survives recovery" in state["evidence"]
        assert state["next_action"] == "resume after recovery"

        corrupt_root = target / ".aaop" / "runtime" / "journeys" / ".recovery" / JOURNEY_ID / "corrupt"
        archives = list(corrupt_root.glob("*.json"))
        assert len(archives) == 1, archives
        assert archives[0].read_bytes() == damaged_bytes

        result = checkpoint(
            journey,
            stale,
            "--reason",
            "stale writer tries to continue after recovery",
            "--evidence",
            "stale evidence must not land",
            ok=False,
        )
        assert "Stale Journey checkpoint revision" in (result.stdout + result.stderr)
        after = json.loads(status(journey).stdout)
        assert "stale evidence must not land" not in after["evidence"]


def test_corrupt_recovery_snapshot_never_overwrites_current_damage() -> None:
    with tempfile.TemporaryDirectory(prefix="aaop-journey-corrupt-recovery-") as tmp:
        target, journey = install_target(Path(tmp))
        path = state_path(target)
        path.write_text("not-json-current\n", encoding="utf-8")
        before = path.read_bytes()
        recovery_path(target).write_text("not-json-recovery\n", encoding="utf-8")

        result = run(sys.executable, journey, "recover", JOURNEY_ID, ok=False)
        combined = result.stdout + result.stderr
        assert "recovery refused" in combined.lower()
        assert "invalid JSON" in combined
        assert path.read_bytes() == before


def test_valid_checkpoint_cannot_be_replaced_by_recovery() -> None:
    with tempfile.TemporaryDirectory(prefix="aaop-journey-valid-recovery-") as tmp:
        target, journey = install_target(Path(tmp))
        before = state_path(target).read_bytes()
        result = run(sys.executable, journey, "recover", JOURNEY_ID, ok=False)
        assert "current Journey checkpoint is valid" in (result.stdout + result.stderr)
        assert state_path(target).read_bytes() == before


def main() -> int:
    tests = [
        test_last_good_snapshot_tracks_successful_state,
        test_future_schema_is_fail_closed_everywhere,
        test_current_schema_missing_revision_is_not_legacy,
        test_known_legacy_schema_migrates_from_revision_zero,
        test_corrupt_json_recovers_explicitly_and_invalidates_stale_writer,
        test_corrupt_recovery_snapshot_never_overwrites_current_damage,
        test_valid_checkpoint_cannot_be_replaced_by_recovery,
    ]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    print(f"PASS Journey state version/recovery hardening: {len(tests)}/{len(tests)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
