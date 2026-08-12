#!/usr/bin/env python3
"""Validate AAOP's verification-harness integrity invariant."""

from __future__ import annotations

import json
import sys
from pathlib import Path

GUARD_ID = "verification-harness-integrity"
ROUTES = ("repo-recovery", "bug-fix", "feature-change", "release-operations")
PRESSURE_CASES = (
    "tests/pressure/custom-verification-harness-false-green.json",
    "tests/pressure/self-judging-behavioral-eval-is-provisional.json",
    "tests/pressure/verification-target-shadow-implementation.json",
)


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
        "generator self-assessment is not silently promoted into independent verification",
        "same-turn self-judgment as independent proof",
        "observed **actual** value has a causal path",
        "shadow implementation proves only that the local test/spec representation is self-consistent",
        "representative mutation-sensitive path",
        "evidence-target fidelity",
        "downgrade the affected green result to provisional/unknown evidence",
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

    runner_case_path = root / PRESSURE_CASES[0]
    runner_case = load(runner_case_path)
    if not isinstance(runner_case, dict):
        errors.append(f"{runner_case_path}: pressure case must be an object")
    else:
        if runner_case.get("expected_route") != "repo-recovery":
            errors.append(f"{runner_case_path}: expected route must be repo-recovery")
        guards = runner_case.get("required_guard_ids", [])
        if GUARD_ID not in guards:
            errors.append(f"{runner_case_path}: must require {GUARD_ID!r}")
        facts = "\n".join(runner_case.get("known_facts", []))
        for phrase in ("bare module basename", "sys.path", "no current GitHub Actions workflow"):
            if phrase not in facts:
                errors.append(f"{runner_case_path}: missing evidence phrase {phrase!r}")

    eval_case_path = root / PRESSURE_CASES[1]
    eval_case = load(eval_case_path)
    if not isinstance(eval_case, dict):
        errors.append(f"{eval_case_path}: pressure case must be an object")
    else:
        if eval_case.get("expected_route") != "repo-recovery":
            errors.append(f"{eval_case_path}: expected route must be repo-recovery")
        guards = eval_case.get("required_guard_ids", [])
        for guard_id in (GUARD_ID, "scoped-blocker-frontier-continuation"):
            if guard_id not in guards:
                errors.append(f"{eval_case_path}: must require {guard_id!r}")
        facts = "\n".join(eval_case.get("known_facts", []))
        for phrase in ("same model response", "dry run", "does not execute this behavioral runner"):
            if phrase not in facts:
                errors.append(f"{eval_case_path}: missing evidence phrase {phrase!r}")

    target_case_path = root / PRESSURE_CASES[2]
    target_case = load(target_case_path)
    if not isinstance(target_case, dict):
        errors.append(f"{target_case_path}: pressure case must be an object")
    else:
        if target_case.get("expected_route") != "repo-recovery":
            errors.append(f"{target_case_path}: expected route must be repo-recovery")
        guards = target_case.get("required_guard_ids", [])
        if GUARD_ID not in guards:
            errors.append(f"{target_case_path}: must require {GUARD_ID!r}")
        facts = "\n".join(target_case.get("known_facts", []))
        for phrase in (
            "actual_dims = expected_dims",
            "expected_steps == STEPS_BY_MODE[mode]",
            "QUICK_SCAN and ALL_FM locally",
            "no implementation-path evidence",
        ):
            if phrase not in facts:
                errors.append(f"{target_case_path}: missing evidence phrase {phrase!r}")
        lessons = "\n".join(target_case.get("lessons", []))
        for phrase in ("evidence-target fidelity", "causal dependency", "mutation-sensitive"):
            if phrase not in lessons:
                errors.append(f"{target_case_path}: missing generic lesson phrase {phrase!r}")

    if errors:
        print("AAOP verification-harness integrity validation failed:", file=sys.stderr)
        for item in errors:
            print(f"  - {item}", file=sys.stderr)
        return 1

    print("AAOP verification-harness integrity validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
