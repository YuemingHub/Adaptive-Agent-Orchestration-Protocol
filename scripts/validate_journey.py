#!/usr/bin/env python3
"""Validate AAOP's multi-route Journey invariants without external dependencies.

The main AAOP validator intentionally focuses on the route/provider package model.
This validator protects cross-route semantics that can otherwise look structurally
valid while producing incorrect end-to-end behavior.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROUTES = {
    "idea-to-build",
    "repo-recovery",
    "bug-fix",
    "feature-change",
    "understand-review",
    "release-operations",
}
ROUTE_SELECTIONS = {"developer-intake", "current-route"}
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$")
ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

REQUIRED_FILES = {
    ".aaop/journeys/idea-to-production.json",
    ".aaop/schemas/journey.schema.json",
    ".aaop/schemas/journey-state.schema.json",
    ".aaop/skills/end-to-end-delivery/SKILL.md",
    ".aaop/skills/developer-intake/SKILL.md",
    ".aaop/tools/journey.py",
    ".aaop/recipes/agent-bundles.json",
}


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def load(path: Path, errors: list[str]) -> dict[str, Any] | None:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        fail(errors, f"{path}: invalid JSON: {exc}")
        return None
    if not isinstance(payload, dict):
        fail(errors, f"{path}: expected JSON object")
        return None
    return payload


def nonempty_string_list(path: Path, field: str, value: object, errors: list[str]) -> None:
    if not isinstance(value, list) or not value:
        fail(errors, f"{path}: {field} must be a non-empty list")
        return
    for item in value:
        if not isinstance(item, str) or not item.strip():
            fail(errors, f"{path}: {field} must contain non-empty strings")


def validate_schema_file(path: Path, errors: list[str]) -> None:
    payload = load(path, errors)
    if payload is not None and "$schema" not in payload:
        fail(errors, f"{path}: schema missing $schema")


def validate_state_schema(root: Path, errors: list[str]) -> None:
    path = root / ".aaop/schemas/journey-state.schema.json"
    payload = load(path, errors)
    if payload is None:
        return
    required = payload.get("required")
    required_set = set(required) if isinstance(required, list) else set()
    expected = {
        "cycle",
        "target_verified",
        "target_evidence",
        "route_history",
        "release_history",
        "completed_at",
    }
    missing = expected - required_set
    if missing:
        fail(errors, f"{path}: release-cycle checkpoint schema missing required fields: {', '.join(sorted(missing))}")

    properties = payload.get("properties")
    if not isinstance(properties, dict):
        fail(errors, f"{path}: properties must be an object")
        return

    route_history = properties.get("route_history")
    if not isinstance(route_history, dict):
        fail(errors, f"{path}: route_history schema missing")
    else:
        items = route_history.get("items")
        route_required = set(items.get("required", [])) if isinstance(items, dict) else set()
        if "cycle" not in route_required:
            fail(errors, f"{path}: route_history entries must identify their release cycle")

    release_history = properties.get("release_history")
    if not isinstance(release_history, dict):
        fail(errors, f"{path}: release_history schema missing")
    else:
        items = release_history.get("items")
        release_required = set(items.get("required", [])) if isinstance(items, dict) else set()
        expected_release = {"cycle", "completed_at", "outcome", "target_evidence"}
        if not expected_release <= release_required:
            fail(errors, f"{path}: release_history entries must preserve completed cycle target evidence")


def validate_journey(root: Path, errors: list[str]) -> None:
    path = root / ".aaop/journeys/idea-to-production.json"
    payload = load(path, errors)
    if payload is None:
        return

    journey_id = payload.get("journey_id")
    if journey_id != "idea-to-production":
        fail(errors, f"{path}: journey_id must be 'idea-to-production'")
    if not isinstance(journey_id, str) or not ID_RE.fullmatch(journey_id):
        fail(errors, f"{path}: invalid journey_id {journey_id!r}")

    version = payload.get("version")
    if not isinstance(version, str) or not SEMVER_RE.fullmatch(version):
        fail(errors, f"{path}: version must be SemVer")

    for field in ("objective", "status"):
        value = payload.get(field)
        if not isinstance(value, str) or not value.strip():
            fail(errors, f"{path}: {field} must be a non-empty string")

    routing = payload.get("routing_policy")
    required_routing = {
        "intake_selects_current_route": True,
        "greenfield_gates_are_conditional": True,
        "reroute_requires_new_evidence": True,
        "stale_checkpoint_never_overrides_current_evidence": True,
        "completed_cycle_must_reopen_explicitly": True,
    }
    if not isinstance(routing, dict):
        fail(errors, f"{path}: routing_policy must be an object")
    else:
        for key, expected in required_routing.items():
            if routing.get(key) is not expected:
                fail(errors, f"{path}: routing_policy.{key} must be {expected!r}")

    completion_policy = payload.get("completion_policy")
    required_completion = {
        "blocked_is_complete": False,
        "target_verification_required": True,
        "target_verification_is_cycle_scoped": True,
        "local_or_ci_evidence_cannot_substitute_for_target_evidence": True,
    }
    if not isinstance(completion_policy, dict):
        fail(errors, f"{path}: completion_policy must be an object")
    else:
        for key, expected in required_completion.items():
            if completion_policy.get(key) is not expected:
                fail(errors, f"{path}: completion_policy.{key} must be {expected!r}")

    state = payload.get("state_contract")
    expected_state = {
        "runtime_file": ".aaop/runtime/journeys/idea-to-production.json",
        "schema": ".aaop/schemas/journey-state.schema.json",
        "checkpoint_tool": ".aaop/tools/journey.py",
    }
    if not isinstance(state, dict):
        fail(errors, f"{path}: state_contract must be an object")
    else:
        for key, expected in expected_state.items():
            if state.get(key) != expected:
                fail(errors, f"{path}: state_contract.{key} must be {expected!r}")
        authority = state.get("authority")
        if not isinstance(authority, str) or not authority.strip():
            fail(errors, f"{path}: state_contract.authority must be explicit")
        elif "historical" not in authority.lower():
            fail(errors, f"{path}: state_contract.authority must state that completed release evidence becomes historical")

    for field in ("entry_conditions", "user_owns", "system_owns", "route_transition_rules", "completion"):
        nonempty_string_list(path, field, payload.get(field), errors)

    gates = payload.get("gates")
    if not isinstance(gates, list) or not gates:
        fail(errors, f"{path}: gates must be a non-empty list")
        return

    seen: set[str] = set()
    gate_map: dict[str, dict[str, Any]] = {}
    for gate in gates:
        if not isinstance(gate, dict):
            fail(errors, f"{path}: every gate must be an object")
            continue
        gate_id = gate.get("id")
        if not isinstance(gate_id, str) or not ID_RE.fullmatch(gate_id):
            fail(errors, f"{path}: invalid gate id {gate_id!r}")
            continue
        if gate_id in seen:
            fail(errors, f"{path}: duplicate gate id {gate_id!r}")
        seen.add(gate_id)
        gate_map[gate_id] = gate

        route = gate.get("primary_route")
        selector = gate.get("route_selection")
        if route is None and selector is None:
            fail(errors, f"{path}: gate {gate_id!r} needs primary_route or route_selection")
        if route is not None and route not in ROUTES:
            fail(errors, f"{path}: gate {gate_id!r} has invalid primary_route {route!r}")
        if selector is not None and selector not in ROUTE_SELECTIONS:
            fail(errors, f"{path}: gate {gate_id!r} has invalid route_selection {selector!r}")
        reroutes = gate.get("possible_reroutes", [])
        if not isinstance(reroutes, list):
            fail(errors, f"{path}: gate {gate_id!r} possible_reroutes must be a list")
        else:
            for reroute in reroutes:
                if reroute not in ROUTES:
                    fail(errors, f"{path}: gate {gate_id!r} has invalid reroute {reroute!r}")
        goal = gate.get("goal")
        if not isinstance(goal, str) or not goal.strip():
            fail(errors, f"{path}: gate {gate_id!r} needs a goal")
        nonempty_string_list(path, f"gate {gate_id}.exit_evidence", gate.get("exit_evidence"), errors)

    intake = gate_map.get("intake")
    if not intake or intake.get("route_selection") != "developer-intake" or "primary_route" in intake:
        fail(errors, f"{path}: intake must let developer-intake select the current route instead of forcing greenfield")

    first_slice = gate_map.get("first-slice")
    if not first_slice:
        fail(errors, f"{path}: missing first-slice gate")
    else:
        if first_slice.get("primary_route") != "idea-to-build":
            fail(errors, f"{path}: first-slice must use idea-to-build when it applies")
        if not isinstance(first_slice.get("applies_when"), str) or not first_slice.get("applies_when", "").strip():
            fail(errors, f"{path}: first-slice must be explicitly conditional")
        if not isinstance(first_slice.get("skip_when"), str) or not first_slice.get("skip_when", "").strip():
            fail(errors, f"{path}: first-slice must define the existing-implementation skip condition")

    deploy = gate_map.get("deploy-observe")
    if not deploy or deploy.get("primary_route") != "release-operations":
        fail(errors, f"{path}: deploy-observe must run under release-operations")
    elif not any("current release cycle" in str(item).lower() for item in deploy.get("exit_evidence", [])):
        fail(errors, f"{path}: deploy-observe target evidence must be scoped to the current release cycle")


def validate_skill_wiring(root: Path, errors: list[str]) -> None:
    end_to_end = root / ".aaop/skills/end-to-end-delivery/SKILL.md"
    intake = root / ".aaop/skills/developer-intake/SKILL.md"
    journey_tool = root / ".aaop/tools/journey.py"
    end_text = end_to_end.read_text(encoding="utf-8") if end_to_end.exists() else ""
    intake_text = intake.read_text(encoding="utf-8") if intake.exists() else ""
    tool_text = journey_tool.read_text(encoding="utf-8") if journey_tool.exists() else ""

    for required in (
        ".aaop/tools/journey.py",
        "blocked/not-complete",
        "existing",
        "current evidence wins",
        "release cycle",
    ):
        if required not in end_text:
            fail(errors, f"{end_to_end}: missing hardened Journey contract phrase {required!r}")
    if "--start-next-cycle" not in end_text:
        fail(errors, f"{end_to_end}: completed releases are not wired to an explicit next-cycle boundary")
    if "end-to-end-delivery" not in intake_text:
        fail(errors, f"{intake}: broad goals are not wired to end-to-end-delivery")
    for required in ("--start-next-cycle", "release_history", "target_evidence", "complete and immutable"):
        if required not in tool_text:
            fail(errors, f"{journey_tool}: missing release-cycle safeguard {required!r}")


def validate_agent_bundles_detection(root: Path, errors: list[str]) -> None:
    path = root / ".aaop/recipes/agent-bundles.json"
    payload = load(path, errors)
    if payload is None:
        return
    detect = payload.get("detect")
    if detect != {}:
        fail(
            errors,
            f"{path}: detection must remain empty until agent-bundles provides provider-specific ownership evidence; generic host agent files are false positives",
        )


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    errors: list[str] = []

    for relative in sorted(REQUIRED_FILES):
        if not (root / relative).exists():
            fail(errors, f"missing required Journey file: {relative}")

    validate_schema_file(root / ".aaop/schemas/journey.schema.json", errors)
    validate_schema_file(root / ".aaop/schemas/journey-state.schema.json", errors)
    validate_state_schema(root, errors)
    validate_journey(root, errors)
    validate_skill_wiring(root, errors)
    validate_agent_bundles_detection(root, errors)

    if errors:
        print("AAOP Journey validation failed:", file=sys.stderr)
        for item in errors:
            print(f"  - {item}", file=sys.stderr)
        return 1

    print("AAOP Journey validation passed (routing, completion, resumability, release-cycle isolation, specialist detection)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
