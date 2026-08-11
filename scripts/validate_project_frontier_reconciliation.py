#!/usr/bin/env python3
"""Regression validation for project-wide frontier reconciliation before project no-op."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROUTE_PATH = ROOT / ".aaop" / "routes" / "repo-recovery.json"
PRESSURE_PATH = ROOT / "tests" / "pressure" / "green-local-checkout-with-active-project-frontier.json"
GUARD_ID = "project-frontier-before-project-noop"
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
    pressure = load(PRESSURE_PATH)

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

    combined = f"{json.dumps(route, ensure_ascii=False)}\n{json.dumps(pressure, ensure_ascii=False)}".lower()
    for token in BANNED_CONSUMER_TOKENS:
        require(token.lower() not in combined, f"project-frontier invariant leaked consumer-specific token: {token}")

    print(
        "PASS project frontier reconciliation: local green/no-mutation evidence stays scope-relative; "
        "current project work topology and unmet acceptance evidence are reconciled before project no-op/pause"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
