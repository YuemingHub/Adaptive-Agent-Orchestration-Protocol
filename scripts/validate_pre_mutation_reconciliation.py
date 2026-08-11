#!/usr/bin/env python3
"""Regression guard for project-independent pre-mutation reconciliation."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / ".aaop" / "policies" / "pre-mutation-reconciliation.md"
ROUTES = ROOT / ".aaop" / "routes"
PRESSURE_CASE = ROOT / "tests" / "pressure" / "stale-project-assumption-drift.json"
MUTATING_EXISTING_ROUTES = ("bug-fix", "feature-change", "repo-recovery", "release-operations")
GUARD_ID = "reconcile-current-baseline-before-mutation"
DERIVED_GUARD_ID = "derived-control-surface-no-shadow-truth"
BANNED_PROJECT_TOKENS = ("Family Space", "MingOS", "aaop-family", "chat-first")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_json(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(payload, dict), f"{path}: expected JSON object")
    return payload


def main() -> int:
    require(POLICY.is_file(), "missing pre-mutation reconciliation policy")
    require(PRESSURE_CASE.is_file(), "missing stale-project assumption pressure case")

    policy = POLICY.read_text(encoding="utf-8")
    lower_policy = policy.lower()
    for phrase in (
        "existing",
        "authority and freshness",
        "unknown",
        "stale-derived-evidence",
        "material-conflict",
        "verified-no-op",
        "test is evidence",
        "not a project-specific onboarding flow",
        "derived control surface truth boundary",
        "second source of truth",
        "provenance/source linkage",
        "consumer-local regression",
        "does not require every project",
    ):
        require(phrase.lower() in lower_policy, f"policy missing invariant: {phrase}")

    for token in BANNED_PROJECT_TOKENS:
        require(token.lower() not in lower_policy, f"AAOP policy leaked consumer-specific token: {token}")

    for route_id in MUTATING_EXISTING_ROUTES:
        payload = load_json(ROUTES / f"{route_id}.json")
        guards = payload.get("pressure_guards")
        require(isinstance(guards, list), f"{route_id}: pressure_guards must be a list")
        guard = next(
            (row for row in guards if isinstance(row, dict) and row.get("id") == GUARD_ID),
            None,
        )
        require(isinstance(guard, dict), f"{route_id}: missing {GUARD_ID}")
        rule = str(guard.get("rule", "")).lower()
        for concept in ("current", "authority", "unknown", "historical", "test"):
            require(concept in rule, f"{route_id}: reconciliation guard missing concept {concept!r}")
        for token in BANNED_PROJECT_TOKENS:
            require(token.lower() not in rule, f"{route_id}: guard leaked consumer-specific token: {token}")

    recovery = load_json(ROUTES / "repo-recovery.json")
    recovery_guards = recovery.get("pressure_guards", [])
    derived_guard = next(
        (row for row in recovery_guards if isinstance(row, dict) and row.get("id") == DERIVED_GUARD_ID),
        None,
    )
    require(isinstance(derived_guard, dict), f"repo-recovery: missing {DERIVED_GUARD_ID}")
    derived_rule = str(derived_guard.get("rule", "")).lower()
    for concept in ("consumer", "source of truth", "unknown", "provenance", "local regression"):
        require(concept in derived_rule, f"repo-recovery: derived-control guard missing concept {concept!r}")
    for token in BANNED_PROJECT_TOKENS:
        require(token.lower() not in derived_rule, f"repo-recovery: derived-control guard leaked consumer-specific token: {token}")

    case = load_json(PRESSURE_CASE)
    require(case.get("expected_route") == "repo-recovery", "pressure case must route contradictory broad continuation to repo-recovery")
    required_guards = case.get("required_guard_ids", [])
    require(GUARD_ID in required_guards, "pressure case must require reconciliation guard")
    require(DERIVED_GUARD_ID in required_guards, "pressure case must require derived-control truth-boundary guard")
    serialized_case = json.dumps(case, ensure_ascii=False).lower()
    for phrase in ("shadow source", "consumer-local regression", "unknown semantics"):
        require(phrase in serialized_case, f"pressure case must retain repaired-consumer lesson: {phrase}")
    for token in BANNED_PROJECT_TOKENS:
        require(token.lower() not in serialized_case, f"pressure case must remain anonymized: {token}")

    print(
        "PASS pre-mutation reconciliation: existing-project mutation routes require a "
        "project-independent current-baseline trust gate; derived control surfaces cannot "
        "become shadow truth; stale evidence, conflicts, and unknowns remain distinct"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
