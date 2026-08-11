#!/usr/bin/env python3
"""Regression validation for stale consumer AAOP control-plane freshness."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROUTE_PATH = ROOT / ".aaop" / "routes" / "repo-recovery.json"
PRESSURE_PATH = ROOT / "tests" / "pressure" / "stale-consumer-control-plane-claims-ready.json"
BOOTSTRAP_PATH = ROOT / "scripts" / "bootstrap.py"
README_PATH = ROOT / "README.md"
GUARD_ID = "consumer-integration-freshness"
BANNED_PROJECT_TOKENS = (
    "Family Space",
    "MingOS",
    "aaop-family",
    "/admin",
    "codex/no-parent-visible-fallbacks",
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_json(path: Path) -> dict:
    require(path.is_file(), f"missing consumer-freshness surface: {path.relative_to(ROOT)}")
    payload = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(payload, dict), f"{path}: expected JSON object")
    return payload


def main() -> int:
    route = load_json(ROUTE_PATH)
    pressure = load_json(PRESSURE_PATH)
    bootstrap = BOOTSTRAP_PATH.read_text(encoding="utf-8")
    readme = README_PATH.read_text(encoding="utf-8")

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
        "health/ready/version",
        "installation integrity",
        "current control-plane compatibility",
        "stable-managed",
        "canonical state-preserving stable bootstrap",
        "exact-frozen",
        "do not silently replace the pin",
        "verified-no-op",
        "keep freshness unknown",
        "do not build a second updater",
    ):
        require(phrase in lower_rule, f"consumer-integration guard missing invariant: {phrase}")

    require(
        'DEFAULT_REF = "stable"' in bootstrap,
        "canonical bootstrap must retain stable as the production/default source",
    )
    for phrase in (
        "Re-running the same stable install command upgrades",
        "--ref main",
        "Use an exact commit ref",
        "run_installer(source, target, mode)",
        "run_provenance(target, provenance_kind, provenance_ref)",
    ):
        require(phrase in bootstrap, f"existing bootstrap lifecycle missing reusable surface: {phrase}")

    for phrase in (
        "Run the current `stable` bootstrap command again",
        "intentionally pinned to an exact commit",
        "not automatically wrong merely because upstream moved",
        "concrete compatibility, safety, or capability delta",
    ):
        require(phrase in readme, f"README missing stable/exact consumer lifecycle boundary: {phrase}")

    require(pressure.get("expected_route") == "repo-recovery", "pressure case must begin with repo-recovery")
    require(
        pressure.get("expected_blocker_class") == "missing-evidence",
        "pressure case must preserve unresolved compatibility as missing-evidence until proven",
    )
    required_guards = pressure.get("required_guard_ids")
    require(
        isinstance(required_guards, list)
        and GUARD_ID in required_guards
        and "default-autonomous-takeover" in required_guards
        and "scoped-blocker-frontier-continuation" in required_guards,
        "pressure case must bind freshness, takeover, and continuation guards",
    )

    serialized = json.dumps(pressure, ensure_ascii=False).lower()
    for phrase in (
        "health and ready as passing",
        "package version string alone",
        "stable-managed",
        "exact-frozen",
        "rather than verified-no-op",
        "follow main merely because it is newer",
        "second updater",
    ):
        require(phrase in serialized, f"pressure case missing consumer-freshness lesson: {phrase}")

    combined = (rule + "\n" + serialized).lower()
    for token in BANNED_PROJECT_TOKENS:
        require(token.lower() not in combined, f"consumer freshness invariant leaked project-specific token: {token}")

    print(
        "PASS consumer integration freshness: local health/ready/version cannot certify current takeover semantics; "
        "stable-managed consumers reuse the canonical state-preserving bootstrap, exact-frozen consumers retain "
        "reproducibility, and stale control planes cannot manufacture verified-no-op conclusions"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
