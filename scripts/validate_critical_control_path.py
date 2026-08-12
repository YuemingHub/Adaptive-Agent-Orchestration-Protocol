#!/usr/bin/env python3
"""Validate AAOP's effective critical-control enforcement invariant."""

from __future__ import annotations

import json
import sys
from pathlib import Path

CASE = "tests/pressure/declared-critical-control-not-on-active-path.json"


def load(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    errors: list[str] = []

    policy_path = root / ".aaop/policies/pre-mutation-reconciliation.md"
    policy = policy_path.read_text(encoding="utf-8")
    for phrase in (
        "## Effective critical-control enforcement",
        "presence of that control is not evidence",
        "representative protected entrypoint actually reaches the intended control",
        "does not silently fail open",
        "keep the control status unknown",
    ):
        if phrase not in policy:
            errors.append(f"{policy_path}: missing critical-control policy phrase {phrase!r}")

    case_path = root / CASE
    case = load(case_path)
    if not isinstance(case, dict):
        errors.append(f"{case_path}: pressure case must be an object")
    else:
        if case.get("expected_route") != "repo-recovery":
            errors.append(f"{case_path}: expected route must be repo-recovery")
        guards = case.get("required_guard_ids", [])
        if "reconcile-current-baseline-before-mutation" not in guards:
            errors.append(
                f"{case_path}: must retain reconcile-current-baseline-before-mutation as the owning route guard"
            )
        facts = "\n".join(case.get("known_facts", []))
        for phrase in (
            "authentication helper",
            "without invoking the authentication helper",
            "network-error fallback",
            "0.0.0.0",
        ):
            if phrase not in facts:
                errors.append(f"{case_path}: missing evidence phrase {phrase!r}")
        must_not = "\n".join(case.get("must_not", []))
        if "specific security product for every AAOP consumer" not in must_not:
            errors.append(f"{case_path}: must preserve project-specific control selection")

    if errors:
        print("AAOP critical-control path validation failed:", file=sys.stderr)
        for item in errors:
            print(f"  - {item}", file=sys.stderr)
        return 1

    print("AAOP critical-control path validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
