#!/usr/bin/env python3
"""Persist AAOP multi-route Journey checkpoints without becoming a workflow engine.

This tool stores only continuity state under ``.aaop/runtime/journeys``. It does
not select routes, execute tasks, install providers, or decide whether evidence
is trustworthy. Current project/runtime/target evidence always outranks a saved
checkpoint when the two disagree.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
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
STATUSES = {"active", "blocked", "complete"}
STATE_SCHEMA_VERSION = "0.2.0"


def package_root() -> Path:
    return Path(__file__).resolve().parents[1]


def journey_root() -> Path:
    return package_root() / "journeys"


def state_root() -> Path:
    return package_root() / "runtime" / "journeys"


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SystemExit(f"AAOP Journey file not found: {path}") from exc
    except Exception as exc:  # noqa: BLE001
        raise SystemExit(f"AAOP Journey file is invalid JSON: {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise SystemExit(f"AAOP Journey JSON must be an object: {path}")
    return payload


def load_definition(journey_id: str) -> dict[str, Any]:
    path = journey_root() / f"{journey_id}.json"
    payload = load_json(path)
    if payload.get("journey_id") != journey_id:
        raise SystemExit(f"AAOP Journey id mismatch in {path}")
    return payload


def state_path(journey_id: str) -> Path:
    return state_root() / f"{journey_id}.json"


def load_state(journey_id: str) -> dict[str, Any]:
    return load_json(state_path(journey_id))


def save_state(journey_id: str, payload: dict[str, Any]) -> None:
    path = state_path(journey_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def gate_ids(definition: dict[str, Any]) -> set[str]:
    result: set[str] = set()
    for gate in definition.get("gates", []):
        if isinstance(gate, dict) and isinstance(gate.get("id"), str):
            result.add(gate["id"])
    return result


def ensure_gate(definition: dict[str, Any], gate: str) -> None:
    if gate not in gate_ids(definition):
        available = ", ".join(sorted(gate_ids(definition)))
        raise SystemExit(f"Unknown Journey gate {gate!r}. Available: {available}")


def append_unique(values: list[str], additions: list[str]) -> list[str]:
    result = list(values)
    seen = set(result)
    for value in additions:
        cleaned = value.strip()
        if cleaned and cleaned not in seen:
            result.append(cleaned)
            seen.add(cleaned)
    return result


def render_state(state: dict[str, Any], definition: dict[str, Any]) -> None:
    print(f"journey: {state['journey_id']}")
    print(f"goal: {state['goal']}")
    print(f"status: {state['status']}")
    print(f"gate: {state['current_gate']}")
    print(f"route: {state.get('current_route') or '-'}")
    print(f"target verified: {'yes' if state.get('target_verified') else 'no'}")
    print(f"target evidence: {len(state.get('target_evidence', []))}")
    print(f"next: {state.get('next_action') or '-'}")
    print(f"updated: {state['updated_at']}")
    if state.get("journey_version") != definition.get("version"):
        print(
            "checkpoint: RECONCILE REQUIRED "
            f"(saved definition={state.get('journey_version')}, current={definition.get('version')})"
        )
    blockers = state.get("blockers", [])
    if blockers:
        print("blockers:")
        for blocker in blockers:
            print(f"  - {blocker}")


def command_show(journey_id: str, as_json: bool) -> int:
    definition = load_definition(journey_id)
    if as_json:
        print(json.dumps(definition, ensure_ascii=False, indent=2))
    else:
        print(f"journey: {definition['journey_id']}")
        print(f"version: {definition['version']}")
        print(f"objective: {definition['objective']}")
        print("gates:")
        for gate in definition.get("gates", []):
            selector = gate.get("primary_route") or gate.get("route_selection") or "-"
            print(f"  - {gate['id']}: {selector} — {gate['goal']}")
    return 0


def command_start(journey_id: str, goal: str, gate: str, route: str | None, reason: str) -> int:
    definition = load_definition(journey_id)
    ensure_gate(definition, gate)
    path = state_path(journey_id)
    if path.exists():
        raise SystemExit(
            f"Journey checkpoint already exists at {path}. Read status and reconcile it; do not overwrite continuity state."
        )
    timestamp = now_utc()
    history: list[dict[str, Any]] = []
    if route:
        history.append({"from": None, "to": route, "reason": reason.strip() or "initial intake", "at": timestamp})
    state: dict[str, Any] = {
        "schema_version": STATE_SCHEMA_VERSION,
        "journey_id": journey_id,
        "journey_version": definition["version"],
        "goal": goal.strip(),
        "status": "active",
        "current_gate": gate,
        "current_route": route,
        "current_outcome": None,
        "next_action": None,
        "target_verified": False,
        "target_evidence": [],
        "evidence": [],
        "blockers": [],
        "route_history": history,
        "last_checkpoint_reason": reason.strip() or "initial intake",
        "updated_at": timestamp,
    }
    if not state["goal"]:
        raise SystemExit("Journey goal must not be empty")
    save_state(journey_id, state)
    render_state(state, definition)
    return 0


def command_status(journey_id: str, as_json: bool) -> int:
    definition = load_definition(journey_id)
    state = load_state(journey_id)
    if as_json:
        payload = dict(state)
        payload["definition_version_current"] = definition.get("version")
        payload["checkpoint_needs_reconcile"] = state.get("journey_version") != definition.get("version")
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        render_state(state, definition)
    return 0


def command_checkpoint(args: argparse.Namespace) -> int:
    definition = load_definition(args.journey_id)
    state = load_state(args.journey_id)

    version_changed = state.get("journey_version") != definition.get("version")
    if version_changed and (not args.reason.strip() or not args.evidence):
        raise SystemExit(
            "Journey definition changed since this checkpoint. Reconciliation requires --reason and at least one --evidence item from the current project/runtime state."
        )

    if args.gate:
        ensure_gate(definition, args.gate)
        state["current_gate"] = args.gate

    previous_route = state.get("current_route")
    if args.route and args.route != previous_route:
        if previous_route is not None and not args.reason.strip():
            raise SystemExit("Changing Journey route requires --reason with the evidence-backed reclassification.")
        if previous_route is not None and not args.evidence:
            raise SystemExit("Changing Journey route requires at least one --evidence item; lack of progress alone is not a reroute signal.")
        timestamp = now_utc()
        state.setdefault("route_history", []).append(
            {
                "from": previous_route,
                "to": args.route,
                "reason": args.reason.strip() or "initial route selection",
                "at": timestamp,
            }
        )
        state["current_route"] = args.route

    if args.outcome is not None:
        state["current_outcome"] = args.outcome.strip() or None
    if args.next_action is not None:
        state["next_action"] = args.next_action.strip() or None

    state["evidence"] = append_unique(list(state.get("evidence", [])), args.evidence)

    existing_blockers = list(state.get("blockers", []))
    if args.clear_blockers and existing_blockers:
        if not args.reason.strip() or not args.evidence:
            raise SystemExit(
                "Clearing Journey blockers requires --reason and at least one --evidence item proving the blocker changed or was resolved."
            )
        state["blockers"] = []
    state["blockers"] = append_unique(list(state.get("blockers", [])), args.blocker)

    state["target_evidence"] = append_unique(list(state.get("target_evidence", [])), args.target_evidence)
    if args.target_evidence:
        state["target_verified"] = True

    requested_status = args.status or state.get("status", "active")
    if requested_status not in STATUSES:
        raise SystemExit(f"Invalid Journey status: {requested_status}")

    if requested_status == "blocked" and not state.get("blockers"):
        raise SystemExit("A blocked Journey checkpoint requires at least one blocker.")

    if requested_status == "complete":
        completion_policy = definition.get("completion_policy", {})
        if completion_policy.get("blocked_is_complete") is not False:
            raise SystemExit("Journey definition does not prove that blocked state is non-complete.")
        if state.get("blockers"):
            raise SystemExit("Journey cannot be complete while blockers remain; clear only blockers that current evidence proves resolved.")
        if completion_policy.get("target_verification_required") and not state.get("target_verified"):
            raise SystemExit("Journey cannot be complete without direct target verification. Keep it active/blocked and record the exact unblock.")
        if completion_policy.get("target_verification_required") and not state.get("target_evidence"):
            raise SystemExit("Journey completion requires explicit target-environment evidence, not only a completion flag.")
        if state.get("current_gate") not in {"deploy-observe", "learning-loop"}:
            raise SystemExit("Journey completion is only valid after deploy-observe (or the post-deploy learning gate).")

    state["status"] = requested_status
    state["schema_version"] = STATE_SCHEMA_VERSION
    state["journey_version"] = definition["version"]
    state["last_checkpoint_reason"] = args.reason.strip() or state.get("last_checkpoint_reason")
    state["updated_at"] = now_utc()
    save_state(args.journey_id, state)
    render_state(state, definition)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect and checkpoint AAOP multi-route Journeys")
    sub = parser.add_subparsers(dest="command", required=True)

    show = sub.add_parser("show", help="Show one Journey definition")
    show.add_argument("journey_id")
    show.add_argument("--json", action="store_true")

    start = sub.add_parser("start", help="Create a resumable Journey checkpoint")
    start.add_argument("journey_id")
    start.add_argument("--goal", required=True)
    start.add_argument("--gate", default="intake")
    start.add_argument("--route", choices=sorted(ROUTES))
    start.add_argument("--reason", default="initial intake")

    status = sub.add_parser("status", help="Read the current Journey checkpoint")
    status.add_argument("journey_id")
    status.add_argument("--json", action="store_true")

    checkpoint = sub.add_parser("checkpoint", help="Update continuity state after meaningful evidence")
    checkpoint.add_argument("journey_id")
    checkpoint.add_argument("--gate")
    checkpoint.add_argument("--route", choices=sorted(ROUTES))
    checkpoint.add_argument("--status", choices=sorted(STATUSES))
    checkpoint.add_argument("--outcome")
    checkpoint.add_argument("--next-action")
    checkpoint.add_argument("--evidence", action="append", default=[])
    checkpoint.add_argument("--target-evidence", action="append", default=[])
    checkpoint.add_argument("--blocker", action="append", default=[])
    checkpoint.add_argument("--clear-blockers", action="store_true")
    checkpoint.add_argument("--reason", default="")

    args = parser.parse_args()
    if args.command == "show":
        return command_show(args.journey_id, args.json)
    if args.command == "start":
        return command_start(args.journey_id, args.goal, args.gate, args.route, args.reason)
    if args.command == "status":
        return command_status(args.journey_id, args.json)
    if args.command == "checkpoint":
        return command_checkpoint(args)
    parser.error(f"Unknown command {args.command!r}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
