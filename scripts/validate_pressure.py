#!/usr/bin/env python3
"""Validate AAOP real-project pressure cases against route pressure guards."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from validate_pre_mutation_reconciliation import main as validate_pre_mutation_reconciliation
from validate_autonomous_takeover import main as validate_autonomous_takeover
from validate_consumer_integration_freshness import main as validate_consumer_integration_freshness
from validate_project_frontier_reconciliation import main as validate_project_frontier_reconciliation
from validate_source_freshness import main as validate_source_freshness
from validate_pressure_promotion import main as validate_pressure_promotion
from validate_team_execution_patterns import main as validate_team_execution_patterns
from validate_verification_harness_integrity import main as validate_verification_harness_integrity
from validate_critical_control_path import main as validate_critical_control_path
from validate_human_forward_capability_fabric import main as validate_human_forward_capability_fabric

ROUTES = {
    "idea-to-build",
    "repo-recovery",
    "bug-fix",
    "feature-change",
    "understand-review",
    "release-operations",
}
ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
REQUIRED_FIELDS = {
    "version",
    "id",
    "provenance",
    "developer_request",
    "expected_route",
    "known_facts",
    "expected_first_moves",
    "must_preserve",
    "must_not",
    "required_guard_ids",
    "lessons",
}
REQUIRED_SCHEMA = ".aaop/schemas/pressure-case.schema.json"


def load(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def route_guards(root: Path, errors: list[str]) -> dict[str, set[str]]:
    result: dict[str, set[str]] = {}
    for route in ROUTES:
        path = root / ".aaop" / "routes" / f"{route}.json"
        try:
            payload = load(path)
        except Exception as exc:  # noqa: BLE001
            fail(errors, f"{path}: cannot read route: {exc}")
            continue
        if not isinstance(payload, dict):
            fail(errors, f"{path}: route must be an object")
            continue
        guards = payload.get("pressure_guards", [])
        ids: set[str] = set()
        if guards is not None and not isinstance(guards, list):
            fail(errors, f"{path}: pressure_guards must be a list")
            continue
        for item in guards or []:
            if not isinstance(item, dict):
                fail(errors, f"{path}: pressure guard must be an object")
                continue
            guard_id = item.get("id")
            rule = item.get("rule")
            if not isinstance(guard_id, str) or not ID_RE.fullmatch(guard_id):
                fail(errors, f"{path}: invalid pressure guard id {guard_id!r}")
                continue
            if guard_id in ids:
                fail(errors, f"{path}: duplicate pressure guard {guard_id!r}")
            if not isinstance(rule, str) or not rule.strip():
                fail(errors, f"{path}: pressure guard {guard_id!r} needs a rule")
            ids.add(guard_id)
        result[route] = ids
    return result


def validate_case(path: Path, payload: object, guards: dict[str, set[str]], errors: list[str]) -> None:
    if not isinstance(payload, dict):
        fail(errors, f"{path}: case must be an object")
        return

    missing = REQUIRED_FIELDS - payload.keys()
    if missing:
        fail(errors, f"{path}: missing fields: {', '.join(sorted(missing))}")
        return

    case_id = payload.get("id")
    if not isinstance(case_id, str) or not ID_RE.fullmatch(case_id):
        fail(errors, f"{path}: invalid case id {case_id!r}")
    elif path.stem != case_id:
        fail(errors, f"{path}: case id must match filename")

    route = payload.get("expected_route")
    if route not in ROUTES:
        fail(errors, f"{path}: invalid expected_route {route!r}")
        return

    for field in ("known_facts", "expected_first_moves", "must_not", "required_guard_ids", "lessons"):
        value = payload.get(field)
        if not isinstance(value, list) or not value:
            fail(errors, f"{path}: {field} must be a non-empty list")

    preserve = payload.get("must_preserve")
    if not isinstance(preserve, list):
        fail(errors, f"{path}: must_preserve must be a list")

    required_guards = payload.get("required_guard_ids", [])
    if isinstance(required_guards, list):
        for guard_id in required_guards:
            if not isinstance(guard_id, str) or not ID_RE.fullmatch(guard_id):
                fail(errors, f"{path}: invalid required guard id {guard_id!r}")
            elif guard_id not in guards.get(route, set()):
                fail(errors, f"{path}: route {route!r} missing required pressure guard {guard_id!r}")

    provenance = payload.get("provenance")
    if not isinstance(provenance, dict):
        fail(errors, f"{path}: provenance must be an object")
        return
    privacy = provenance.get("privacy")
    kind = provenance.get("kind")
    if privacy == "anonymized":
        if kind != "anonymized-real-project":
            fail(errors, f"{path}: anonymized case must use anonymized-real-project provenance")
        if provenance.get("repository") or provenance.get("reference"):
            fail(errors, f"{path}: anonymized case must not publish repository/reference identifiers")
    elif privacy == "public":
        if kind not in {"public-repository", "public-issue"}:
            fail(errors, f"{path}: public case must use public-repository or public-issue provenance")
        if not provenance.get("repository") or not provenance.get("reference"):
            fail(errors, f"{path}: public case must identify its public repository/reference")
    else:
        fail(errors, f"{path}: invalid provenance privacy {privacy!r}")


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    errors: list[str] = []

    schema_path = root / REQUIRED_SCHEMA
    if not schema_path.exists():
        fail(errors, f"missing required pressure schema: {REQUIRED_SCHEMA}")
    else:
        try:
            schema = load(schema_path)
            if not isinstance(schema, dict) or "$schema" not in schema:
                fail(errors, f"{schema_path}: invalid pressure schema")
        except Exception as exc:  # noqa: BLE001
            fail(errors, f"{schema_path}: invalid JSON: {exc}")

    guards = route_guards(root, errors)
    case_root = root / "tests" / "pressure"
    cases = sorted(case_root.glob("*.json"))
    if len(cases) < 7:
        fail(errors, f"{case_root}: expected at least 7 real-project pressure cases")

    seen: set[str] = set()
    covered_routes: set[str] = set()
    for path in cases:
        try:
            payload = load(path)
        except Exception as exc:  # noqa: BLE001
            fail(errors, f"{path}: invalid JSON: {exc}")
            continue
        if isinstance(payload, dict):
            case_id = payload.get("id")
            if isinstance(case_id, str):
                if case_id in seen:
                    fail(errors, f"{path}: duplicate pressure case id {case_id!r}")
                seen.add(case_id)
            route = payload.get("expected_route")
            if isinstance(route, str) and route in ROUTES:
                covered_routes.add(route)
        validate_case(path, payload, guards, errors)

    missing_routes = ROUTES - covered_routes
    if missing_routes:
        fail(errors, f"pressure suite missing route coverage: {', '.join(sorted(missing_routes))}")

    for label, validator in (
        ("default autonomous takeover", validate_autonomous_takeover),
        ("consumer integration freshness", validate_consumer_integration_freshness),
        ("project frontier reconciliation", validate_project_frontier_reconciliation),
        ("stable source freshness", validate_source_freshness),
        ("team execution pattern", validate_team_execution_patterns),
        ("pre-mutation reconciliation", validate_pre_mutation_reconciliation),
        ("verification harness integrity", validate_verification_harness_integrity),
        ("critical control path", validate_critical_control_path),
        ("human-forward capability fabric", validate_human_forward_capability_fabric),
        ("real-project pressure promotion", validate_pressure_promotion),
    ):
        try:
            result = validator()
            if result != 0:
                fail(errors, f"{label} validation returned {result}")
        except Exception as exc:  # noqa: BLE001
            fail(errors, f"{label} validation failed: {exc}")

    if errors:
        print("AAOP pressure validation failed:", file=sys.stderr)
        for item in errors:
            print(f"  - {item}", file=sys.stderr)
        return 1

    print(f"AAOP pressure validation passed ({len(cases)} cases; routes={','.join(sorted(covered_routes))})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
