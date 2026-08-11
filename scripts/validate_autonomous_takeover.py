#!/usr/bin/env python3
"""Regression validation for AAOP's default autonomous takeover and project continuation."""

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
    blocked_pressure = json.loads(text("tests/pressure/blocked-highest-priority-must-not-stop-project.json"))

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
    require(isinstance(routing, dict), "canonical Journey routing_policy must be an object")
    for key in (
        "autonomous_takeover_reconstructs_intent_and_selects_current_goal",
        "route_completion_is_not_project_completion",
        "blocked_delta_is_scoped_and_frontier_recomputed",
        "bounded_execution_end_is_handoff_not_completion",
    ):
        require(routing.get(key) is True, f"canonical Journey missing autonomous continuation routing invariant: {key}")

    completion = journey.get("completion_policy")
    require(isinstance(completion, dict), "canonical Journey completion_policy must be an object")
    for key in (
        "single_blocker_cannot_block_project_when_other_executable_delta_exists",
        "project_pause_requires_no_meaningful_authorized_executable_frontier_or_bounded_run_end",
    ):
        require(completion.get(key) is True, f"canonical Journey missing scoped-blocker completion invariant: {key}")

    system_owns = journey.get("system_owns")
    require(
        isinstance(system_owns, list)
        and "intent reconstruction and current-goal selection from current project evidence" in system_owns,
        "Journey must retain agent ownership of intent reconstruction/current-goal selection",
    )
    require(
        isinstance(system_owns, list)
        and any("executable-frontier recomputation" in item for item in system_owns if isinstance(item, str)),
        "Journey must retain system ownership of scoped blocker handling/frontier recomputation",
    )

    transition_rules = journey.get("route_transition_rules")
    require(isinstance(transition_rules, list), "Journey route_transition_rules must be a list")
    serialized_transitions = "\n".join(item for item in transition_rules if isinstance(item, str)).lower()
    for phrase in (
        "route completion",
        "blocked delta",
        "unrelated authorized deltas remain executable",
        "no other meaningful authorized executable delta remains",
        "bounded host execution window",
    ):
        require(phrase in serialized_transitions, f"Journey missing project-continuation transition rule: {phrase}")

    guards = route.get("pressure_guards")
    guard_ids = {item.get("id") for item in guards if isinstance(item, dict)} if isinstance(guards, list) else set()
    require("default-autonomous-takeover" in guard_ids, "repo-recovery must guard default autonomous takeover")
    require(
        "scoped-blocker-frontier-continuation" in guard_ids,
        "repo-recovery must guard scoped blocker frontier continuation",
    )

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

    require(
        blocked_pressure.get("expected_route") == "repo-recovery",
        "scoped-blocker pressure must start from repo recovery",
    )
    require(
        blocked_pressure.get("expected_blocker_class") == "authorization",
        "scoped-blocker pressure must preserve the actual authorization boundary",
    )
    blocked_required = blocked_pressure.get("required_guard_ids")
    require(
        isinstance(blocked_required, list)
        and "scoped-blocker-frontier-continuation" in blocked_required
        and "default-autonomous-takeover" in blocked_required,
        "scoped-blocker pressure must bind takeover and frontier-continuation guards",
    )
    serialized_blocked = json.dumps(blocked_pressure, ensure_ascii=False).lower()
    for phrase in (
        "blocked only within its exact scope",
        "recompute the project frontier",
        "continue implementation or verification",
        "whole project must stop",
        "ask the novice to choose",
        "second planner",
    ):
        require(phrase in serialized_blocked, f"scoped-blocker pressure missing real-project invariant: {phrase}")

    print(
        "PASS autonomous takeover: minimal entrypoint, intent reconstruction, agent-owned current-goal selection, "
        "scoped blockers, route-vs-project completion, executable-frontier recomputation, bounded-run handoff, "
        "novice boundaries, and real-project pressure regressions"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
