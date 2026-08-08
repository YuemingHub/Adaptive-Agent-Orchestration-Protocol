#!/usr/bin/env python3
"""Validate AAOP real-project pressure cases against route pressure guards."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

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

    required_guards = payload.get("required_guard_ids", [])
    if isinstance(required_guards, list):
        for guard_id in required_guards:
            if guard_id not in guards.get(route, set()):
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
        if not provenance.get("repository") or not provenance.get("reference"):
            fail(errors, f"{path}: public case must identify its public repository/reference")
    else:
        fail(errors, f"{path}: invalid provenance privacy {privacy!r}")


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    errors: list[str] = []
    guards = route_guards(root, errors)
    case_root = root / "tests" / "pressure"
    cases = sorted(case_root.glob("*.json"))
    if len(cases) < 4:
        fail(errors, f"{case_root}: expected at least 4 real-project pressure cases")

    seen: set[str] = set()
    for path in cases:
        try:
            payload = load(path)
        except Exception as exc:  # noqa: BLE001
            fail(errors, f"{path}: invalid JSON: {exc}")
            continue
        if isinstance(payload, dict) and isinstance(payload.get("id"), str):
            if payload["id"] in seen:
                fail(errors, f"{path}: duplicate pressure case id {payload['id']!r}")
            seen.add(payload["id"])
        validate_case(path, payload, guards, errors)

    if errors:
        print("AAOP pressure validation failed:", file=sys.stderr)
        for item in errors:
            print(f"  - {item}", file=sys.stderr)
        return 1

    covered_routes = sorted({load(path)["expected_route"] for path in cases if isinstance(load(path), dict)})
    print(f"AAOP pressure validation passed ({len(cases)} cases; routes={','.join(covered_routes)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
