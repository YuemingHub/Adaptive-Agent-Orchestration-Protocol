#!/usr/bin/env python3
"""Regression guard for AAOP team-execution patterns absorbed from external reviews."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEAM = ROOT / ".aaop" / "skills" / "team-construction" / "SKILL.md"
FEATURE = ROOT / ".aaop" / "routes" / "feature-change.json"
PROVIDERS = ROOT / ".aaop" / "registries" / "providers.json"
REVIEW = ROOT / "docs" / "CLAUDE_STANDARD_DEV_TEAM_REVIEW.md"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), f"{path}: expected JSON object")
    return value


def main() -> int:
    for path in (TEAM, FEATURE, PROVIDERS, REVIEW):
        require(path.is_file(), f"missing team-pattern surface: {path.relative_to(ROOT)}")

    team = TEAM.read_text(encoding="utf-8")
    review = REVIEW.read_text(encoding="utf-8")
    feature = load_json(FEATURE)
    providers = load_json(PROVIDERS)

    # Preserve AAOP's minimum-team topology instead of importing a standing 12-role team.
    require("Default to **one capable agent**" in team, "one-agent default must remain explicit")
    require("1–5 members maximum" in team, "Task Pod 1-5 ceiling must remain explicit")
    require("exactly **one accountable owner**" in team, "one accountable owner must remain explicit")

    # New execution mechanisms must remain present.
    require("Contract fan-out and evidence invalidation" in team, "missing contract fan-out rule")
    require("Builder–verifier pair for consequential slices" in team, "missing builder-verifier pattern")
    require("Parallelism and verification-baseline coupling" in team, "missing verification-baseline coupling rule")
    require("Interruption and partial-delivery recovery" in team, "missing partial-delivery recovery rule")
    require("do not blindly replay the original task" in team, "interruption recovery must reject blind replay")
    require("execution-continuity" in team and "LoopX" in team, "partial recovery must route a proven continuity gap instead of creating duplicate state")
    require("do not assume a delegated/subagent context can itself create or schedule peer subagents" in team.lower(), "host topology discovery/degradation rule missing")

    guards = feature.get("pressure_guards", [])
    require(isinstance(guards, list), "feature-change pressure_guards must be a list")
    guard = next((row for row in guards if isinstance(row, dict) and row.get("id") == "contract-fanout-evidence-invalidation"), None)
    require(isinstance(guard, dict), "feature-change missing contract-fanout-evidence-invalidation guard")
    guard_rule = str(guard.get("rule", "")).lower()
    require("invalidate evidence" in guard_rule, "contract guard must invalidate stale evidence")
    require("consumers" in guard_rule, "contract guard must discover current consumers")
    require("affected" in guard_rule or "classify" in guard_rule, "contract guard must classify the affected surface")

    # The reviewed repository is a pattern source, never a new top-level Provider/runtime.
    provider_rows = providers.get("providers", [])
    require(isinstance(provider_rows, list), "providers must be a list")
    provider_ids = {row.get("id") for row in provider_rows if isinstance(row, dict)}
    require("claude-standard-dev-team" not in provider_ids, "reviewed fixed-team repository must not become an AAOP Provider")

    # Preserve explicit rejection of accidental topology/policy.
    for phrase in (
        "Fixed 12-agent team",
        "Fixed 11-phase workflow",
        "Default NEEDS WORK",
        "Ban on browser automation",
        "Hard-coded subpath deployment conventions",
        "absorb the invariant, retire the accidental topology",
    ):
        require(phrase in review, f"review must retain rejection rationale: {phrase}")

    require("d1aa5006d6b6ecb7430950a966b1d31cd6574a39" in review, "review must pin the inspected upstream commit")
    require("MIT" in review, "review must retain upstream license provenance")

    print(
        "PASS team execution patterns: minimum Task Pod preserved; contract fan-out, "
        "independent verification, interruption salvage, baseline-aware parallelism, "
        "and host-topology degradation are guarded without a new fixed-team Provider"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
