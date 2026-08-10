#!/usr/bin/env python3
"""Static contract checks for Journey state recovery wiring."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def require(text: str, marker: str, path: Path) -> None:
    if marker not in text:
        raise SystemExit(f"{path} missing Journey recovery contract marker: {marker!r}")


def main() -> int:
    state_path = ROOT / ".aaop/tools/journey_state.py"
    tool_path = ROOT / ".aaop/tools/journey.py"
    intake_path = ROOT / ".aaop/skills/developer-intake/SKILL.md"

    for path in (state_path, tool_path, intake_path):
        if not path.is_file():
            raise SystemExit(f"missing Journey recovery surface: {path}")

    state = state_path.read_text(encoding="utf-8")
    tool = tool_path.read_text(encoding="utf-8")
    intake = intake_path.read_text(encoding="utf-8")

    for marker in (
        'CURRENT_STATE_SCHEMA_VERSION = "0.3.2"',
        'LEGACY_STATE_SCHEMA_VERSION = "0.3.1"',
        "FutureCheckpointSchema",
        "last-good recovery snapshot",
        "corrupt_archive_root",
    ):
        require(state, marker, state_path)

    for marker in (
        "recover_checkpoint_unlocked",
        'sub.add_parser(\n        "recover"',
        "Recovery with an older tool is forbidden",
        "Stale Journey checkpoint revision",
    ):
        require(tool, marker, tool_path)

    for marker in (
        "do not interpret the failure as “there is no Journey.”",
        "journey.py recover idea-to-production",
        "future/unsupported checkpoint schema",
        "do **not** run old recovery",
        "a valid current checkpoint continues through ordinary reconciliation + revision CAS",
    ):
        require(intake, marker, intake_path)

    print("PASS Journey recovery contract wiring")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
