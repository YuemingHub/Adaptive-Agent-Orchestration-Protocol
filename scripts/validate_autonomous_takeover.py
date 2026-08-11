#!/usr/bin/env python3
"""Regression validation for AAOP's default autonomous takeover composition."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def text(relative: str) -> str:
    path = ROOT / relative
    require(path.is_file(), f"missing takeover contract surface: {relative}")
    return path.read_text(encoding="utf-8")


def main() -> int:
    orchestrator = text(".aaop/ORCHESTRATOR.md")
    intake = text(".aaop/skills/developer-intake/SKILL.md")
    contract = text(".aaop/skills/working-contract/SKILL.md")
    journey_skill = text(".aaop/skills/end-to-end-delivery/SKILL.md")
    quickstart = text("docs/QUICKSTART.md")
    entrypoint = text("docs/DEVELOPER_ENTRYPOINT.md")
    route = json.loads(text(".aaop/routes/repo-recovery.json"))
    journey = json.loads(text(".aaop/journeys/idea-to-production.json"))
    pressure = json.loads(text("tests/pressure/default-autonomous-takeover.json"))

    for phrase in (
        "Default autonomous takeover",
        "ultimate intent",
        "current development goal",
        "highest-value evidence-backed",
        "Technical ambiguity",
        "do not create a parallel plan ledger",
    ):
        require(phrase in orchestrator, f"orchestrator missing takeover invariant: {phrase}")

    for phrase in (
        "Default autonomous takeover request",
        "Ultimate intent",
        "Current development goal",
        "Choose the current goal without making the user schedule",
        "After each verified delta",
    ):
        require(phrase in intake, f"developer intake missing takeover behavior: {phrase}")

    for phrase in (
        "explicit takeover request",
        "Ordinary technical uncertainty is agent-owned",
    ):
        require(phrase in contract, f"working contract missing novice-boundary invariant: {phrase}")

    for phrase in (
        "Default takeover next-delta loop",
        "not a second planner, workflow engine, state database, or default Provider",
        "Journey completion still requires",
    ):
        require(phrase in journey_skill, f"Journey skill missing takeover continuity: {phrase}")

    require("AAOP: take over this project." in quickstart, "Quick Start must expose the minimal takeover entrypoint")
    require("Default autonomous takeover" in entrypoint, "developer entrypoint must document autonomous takeover")

    routing = journey.get("routing_policy")
    require(
        isinstance(routing, dict)
        and routing.get("autonomous_takeover_reconstructs_intent_and_selects_current_goal") is True,
        "canonical Journey must declare autonomous takeover intent/current-goal reconstruction",
    )
    system_owns = journey.get("system_owns")
    require(
        isinstance(system_owns, list)
        and "intent reconstruction and current-goal selection from current project evidence" in system_owns,
        "Journey must retain agent ownership of intent reconstruction/current-goal selection",
    )

    guards = route.get("pressure_guards")
    guard_ids = {item.get("id") for item in guards if isinstance(item, dict)} if isinstance(guards, list) else set()
    require("default-autonomous-takeover" in guard_ids, "repo-recovery must guard default autonomous takeover")
    require(pressure.get("expected_route") == "repo-recovery", "takeover pressure must begin with repo recovery")
    required_guards = pressure.get("required_guard_ids")
    require(
        isinstance(required_guards, list) and "default-autonomous-takeover" in required_guards,
        "takeover pressure must bind its guard",
    )
    must_not = pressure.get("must_not")
    require(
        isinstance(must_not, list)
        and any("workflow engine" in item for item in must_not if isinstance(item, str)),
        "takeover pressure must preserve the no-duplicate-engine boundary",
    )

    print(
        "PASS autonomous takeover: minimal entrypoint, intent reconstruction, agent-owned current-goal selection, "
        "next-delta continuity, novice boundaries, and repo-recovery pressure regression"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
