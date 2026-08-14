#!/usr/bin/env python3
"""Regression validation for project frontier reconciliation and bounded verification debt."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROUTE_PATH = ROOT / ".aaop" / "routes" / "repo-recovery.json"
JOURNEY_PATH = ROOT / ".aaop" / "journeys" / "idea-to-production.json"
POLICY_PATH = ROOT / ".aaop" / "policies" / "pre-mutation-reconciliation.md"
PRESSURE_PATH = ROOT / "tests" / "pressure" / "green-local-checkout-with-active-project-frontier.json"
VERIFICATION_DEBT_PRESSURE_PATH = ROOT / "tests" / "pressure" / "verification-debt-must-not-compound-unbounded.json"
GUARD_ID = "project-frontier-before-project-noop"
SCOPED_BLOCKER_GUARD_ID = "scoped-blocker-frontier-continuation"
BANNED_CONSUMER_TOKENS = ("Family Space", "Family-Space", "MingOS", "aaop-family", "Jiaming")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load(path: Path) -> dict[str, object]:
    require(path.is_file(), f"missing project-frontier surface: {path.relative_to(ROOT)}")
    payload = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(payload, dict), f"expected JSON object: {path.relative_to(ROOT)}")
    return payload


def main() -> int:
    route = load(ROUTE_PATH)
    journey = load(JOURNEY_PATH)
    pressure = load(PRESSURE_PATH)
    verification_debt_pressure = load(VERIFICATION_DEBT_PRESSURE_PATH)
    policy = POLICY_PATH.read_text(encoding="utf-8")

    require(route.get("route_id") == "repo-recovery", "frontier reconciliation must strengthen repo-recovery")

    guards = route.get("pressure_guards")
    require(isinstance(guards, list), "repo-recovery pressure_guards must be a list")
    guard = next(
        (item for item in guards if isinstance(item, dict) and item.get("id") == GUARD_ID),
        None,
    )
    require(isinstance(guard, dict), f"repo-recovery missing {GUARD_ID}")
    rule = str(guard.get("rule") or "")
    lower_rule = rule.lower()
    for phrase in (
        "project-level pause",
        "current work topology",
        "unmet acceptance evidence",
        "green tests",
        "local-no-mutation",
        "project-no-frontier",
        "merely open",
        "do not manufacture",
    ):
        require(phrase in lower_rule, f"project-frontier guard missing invariant: {phrase}")

    scoped_blocker_guard = next(
        (item for item in guards if isinstance(item, dict) and item.get("id") == SCOPED_BLOCKER_GUARD_ID),
        None,
    )
    require(isinstance(scoped_blocker_guard, dict), f"repo-recovery missing {SCOPED_BLOCKER_GUARD_ID}")

    stages = route.get("stages")
    require(isinstance(stages, list), "repo-recovery stages must be a list")
    serialized_stages = json.dumps(stages, ensure_ascii=False).lower()
    for phrase in (
        "project-declared current work topology",
        "accepted outcome versus current acceptance evidence",
        "another current work target",
        "local-no-mutation",
        "project-no-frontier",
    ):
        require(phrase in serialized_stages, f"repo-recovery stages missing project-frontier behavior: {phrase}")

    verification = route.get("verification")
    require(isinstance(verification, list), "repo-recovery verification must be a list")
    serialized_verification = "\n".join(str(item) for item in verification).lower()
    for phrase in (
        "green tests",
        "scoped verification evidence",
        "local-no-mutation",
        "project-no-frontier",
        "merely open or historical",
    ):
        require(phrase in serialized_verification, f"repo-recovery verification missing frontier distinction: {phrase}")

    routing = journey.get("routing_policy")
    require(isinstance(routing, dict), "canonical Journey routing_policy must be an object")
    require(
        routing.get("project_frontier_reconciled_before_project_pause") is True,
        "canonical Journey must reconcile project frontier before project pause",
    )
    completion = journey.get("completion_policy")
    require(isinstance(completion, dict), "canonical Journey completion_policy must be an object")
    require(completion.get("local_no_mutation_is_not_project_no_frontier") is True, "Journey must separate local no-mutation from project no-frontier")
    require(completion.get("green_checks_are_not_project_completion") is True, "Journey must reject green checks as project completion proof")
    serialized_journey = json.dumps(journey, ensure_ascii=False).lower()
    for phrase in (
        "material project-declared current candidate/pr/branch/issue/handoff/predecessor-successor evidence",
        "green checks or no-local-mutation",
        "scope-relative",
        "execution-continuity",
        "provider selection",
    ):
        require(phrase in serialized_journey, f"Journey missing project-frontier/continuity invariant: {phrase}")

    require(
        pressure.get("expected_route") == "repo-recovery",
        "project-frontier pressure must begin with repo-recovery",
    )
    required = pressure.get("required_guard_ids")
    require(isinstance(required, list) and GUARD_ID in required, "pressure case must bind project-frontier guard")
    serialized_pressure = json.dumps(pressure, ensure_ascii=False).lower()
    for phrase in (
        "green project-native tests",
        "merge-authoritative release-candidate chain",
        "local-no-mutation",
        "project-no-frontier",
        "random open pull requests",
        "tests verify declared contracts",
    ):
        require(phrase in serialized_pressure, f"project-frontier pressure missing real-project lesson: {phrase}")

    # The inverse failure mode of scoped continuation is unbounded verification debt:
    # continuing work is correct, but later dependent mutations must not treat an
    # unverified delta as a trusted baseline indefinitely.
    lower_policy = policy.lower()
    for phrase in (
        "## verification debt containment",
        "unverified mutation",
        "dependency-aware scope",
        "keep the dependent unverified chain **bounded**",
        "critical-control, migration, release, deployment, shared-runtime",
        "retire all material verification debt",
        "monetary cost remains an authorization boundary",
    ):
        require(phrase in lower_policy, f"pre-mutation policy missing verification-debt invariant: {phrase}")

    require(
        verification_debt_pressure.get("expected_route") == "repo-recovery",
        "verification-debt pressure must begin with repo-recovery",
    )
    debt_guards = verification_debt_pressure.get("required_guard_ids")
    require(
        isinstance(debt_guards, list) and SCOPED_BLOCKER_GUARD_ID in debt_guards,
        "verification-debt pressure must preserve scoped-blocker continuation",
    )
    serialized_debt_pressure = json.dumps(verification_debt_pressure, ensure_ascii=False).lower()
    for phrase in (
        "exact-head aggregate execution remains unavailable",
        "unverified mutation",
        "continue genuinely independent",
        "bounded verification debt",
        "retired before merge",
    ):
        require(phrase in serialized_debt_pressure, f"verification-debt pressure missing lesson: {phrase}")

    combined = (
        f"{json.dumps(route, ensure_ascii=False)}\n"
        f"{json.dumps(journey, ensure_ascii=False)}\n"
        f"{json.dumps(pressure, ensure_ascii=False)}\n"
        f"{policy}"
    ).lower()
    for token in BANNED_CONSUMER_TOKENS:
        require(token.lower() not in combined, f"project-frontier invariant leaked consumer-specific token: {token}")

    print(
        "PASS project frontier reconciliation: local green/no-mutation evidence stays scope-relative; "
        "current project work topology is reconciled before project pause; blockers preserve independent frontier; "
        "dependent unverified mutations remain bounded verification debt until exact acceptance evidence retires it"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
