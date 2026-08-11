#!/usr/bin/env python3
"""Regression validation for AAOP autonomous project continuation."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROUTE_PATH = ROOT / ".aaop" / "routes" / "repo-recovery.json"
JOURNEY_PATH = ROOT / ".aaop" / "journeys" / "idea-to-production.json"
PRESSURE_PATH = ROOT / "tests" / "pressure" / "blocked-priority-must-not-stop-project.json"
GUARD_ID = "scoped-blocker-recompute-frontier"
BANNED_PROJECT_TOKENS = ("Family Space", "MingOS", "aaop-family", "/admin")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load(path: Path) -> dict:
    require(path.is_file(), f"missing continuation surface: {path.relative_to(ROOT)}")
    payload = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(payload, dict), f"{path}: expected JSON object")
    return payload


def main() -> int:
    route = load(ROUTE_PATH)
    journey = load(JOURNEY_PATH)
    pressure = load(PRESSURE_PATH)

    guards = route.get("pressure_guards")
    require(isinstance(guards, list), "repo-recovery pressure_guards must be a list")
    guard = next(
        (item for item in guards if isinstance(item, dict) and item.get("id") == GUARD_ID),
        None,
    )
    require(isinstance(guard, dict), f"repo-recovery missing {GUARD_ID}")
    rule = str(guard.get("rule", ""))
    lower_rule = rule.lower()
    for phrase in (
        "affected delta",
        "project-level executable frontier",
        "route completion",
        "continue",
        "no safe authorized",
    ):
        require(phrase in lower_rule, f"continuation guard missing invariant: {phrase}")

    routing = journey.get("routing_policy")
    require(isinstance(routing, dict), "Journey routing_policy must be an object")
    require(
        routing.get("blocked_delta_scopes_only_affected_work") is True,
        "Journey must scope a blocker to affected work",
    )
    require(
        routing.get("route_completion_recomputes_project_frontier") is True,
        "Journey must recompute project frontier after route completion",
    )

    completion = journey.get("completion_policy")
    require(isinstance(completion, dict), "Journey completion_policy must be an object")
    require(
        completion.get("single_blocker_does_not_end_journey") is True,
        "Journey must reject single-blocker completion",
    )

    transition_rules = journey.get("route_transition_rules")
    require(isinstance(transition_rules, list), "Journey route_transition_rules must be a list")
    serialized_rules = "\n".join(str(item) for item in transition_rules).lower()
    for phrase in (
        "blocked delta",
        "recompute",
        "executable frontier",
        "continue",
    ):
        require(phrase in serialized_rules, f"Journey transition rules missing continuation phrase: {phrase}")

    require(pressure.get("expected_route") == "repo-recovery", "pressure case must start in repo-recovery")
    require(pressure.get("expected_blocker_class") == "authorization", "pressure case blocker must be authorization")
    required_guards = pressure.get("required_guard_ids")
    require(isinstance(required_guards, list) and GUARD_ID in required_guards, "pressure case must bind continuation guard")
    serialized_pressure = json.dumps(pressure, ensure_ascii=False).lower()
    for phrase in (
        "highest-priority current delta",
        "safe, authorized",
        "recompute the project-level executable frontier",
        "skip unrelated executable work",
        "second planner",
    ):
        require(phrase in serialized_pressure, f"pressure case missing real-project lesson: {phrase}")

    combined = (rule + "\n" + serialized_pressure).lower()
    for token in BANNED_PROJECT_TOKENS:
        require(token.lower() not in combined, f"continuation invariant leaked consumer-specific token: {token}")

    print(
        "PASS autonomous continuation: scoped blockers do not end project takeover; route completion and blocked deltas "
        "recompute the project executable frontier and continue until no safe authorized work remains"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
