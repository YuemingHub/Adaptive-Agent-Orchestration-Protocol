#!/usr/bin/env python3
"""Validate AAOP's verification-harness integrity invariant."""

from __future__ import annotations

import json
import sys
from pathlib import Path

GUARD_ID = "verification-harness-integrity"
ROUTES = ("repo-recovery", "bug-fix", "feature-change", "release-operations")
PRESSURE_CASE = "tests/pressure/custom-verification-harness-false-green.json"


def load(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    errors: list[str] = []

    policy_path = root / ".aaop/policies/pre-mutation-reconciliation.md"
    policy = policy_path.read_text(encoding="utf-8")
    for phrase in (
        "## Verification harness integrity",
        "distinct checks cannot collide",
        "failure exit codes and failure states propagate",
        "downgrade its green result to provisional/unknown evidence",
    ):
        if phrase not in policy:
            errors.append(f"{policy_path}: missing verification-harness policy phrase {phrase!r}")

    for route_id in ROUTES:
        path = root / ".aaop/routes" / f"{route_id}.json"
        payload = load(path)
        if not isinstance(payload, dict):
            errors.append(f"{path}: route must be an object")
            continue
        guards = payload.get("pressure_guards", [])
        guard = next(
            (item for item in guards if isinstance(item, dict) and item.get("id") == GUARD_ID),
            None,
        )
        if guard is None:
            errors.append(f"{path}: missing {GUARD_ID!r} pressure guard")
            continue
        rule = guard.get("rule", "")
        for phrase in (
            "do not trust a green aggregate",
            "discovered distinctly",
            "failures propagate",
            "provisional/unknown evidence",
        ):
            if phrase not in rule:
                errors.append(f"{path}: {GUARD_ID} rule missing phrase {phrase!r}")

    journey_path = root / ".aaop/journeys/idea-to-production.json"
    journey = load(journey_path)
    if not isinstance(journey, dict):
        errors.append(f"{journey_path}: journey must be an object")
    else:
        completion = journey.get("completion_policy", {})
        if not isinstance(completion, dict) or completion.get(
            "green_aggregate_requires_trustworthy_verification_harness"
        ) is not True:
            errors.append(
                f"{journey_path}: completion policy must require a trustworthy verification harness"
            )
        transition_text = "\n".join(journey.get("route_transition_rules", []))
        if "green custom test/validation/CI aggregate" not in transition_text:
            errors.append(
                f"{journey_path}: route transitions must keep untrusted green aggregates provisional"
            )

    pressure_path = root / PRESSURE_CASE
    pressure = load(pressure_path)
    if not isinstance(pressure, dict):
        errors.append(f"{pressure_path}: pressure case must be an object")
    else:
        if pressure.get("expected_route") != "repo-recovery":
            errors.append(f"{pressure_path}: expected route must be repo-recovery")
        guards = pressure.get("required_guard_ids", [])
        if GUARD_ID not in guards:
            errors.append(f"{pressure_path}: must require {GUARD_ID!r}")
        facts = "\n".join(pressure.get("known_facts", []))
        for phrase in ("bare module basename", "sys.path", "no current GitHub Actions workflow"):
            if phrase not in facts:
                errors.append(f"{pressure_path}: missing evidence phrase {phrase!r}")

    if errors:
        print("AAOP verification-harness integrity validation failed:", file=sys.stderr)
        for item in errors:
            print(f"  - {item}", file=sys.stderr)
        return 1

    print("AAOP verification-harness integrity validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
