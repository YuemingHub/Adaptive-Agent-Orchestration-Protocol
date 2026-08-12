#!/usr/bin/env python3
"""Validate human-forward intake, salvage-first recovery, and model-independent capability orchestration."""

from __future__ import annotations

import json
import sys
from pathlib import Path

GREENFIELD_CASE = "tests/pressure/nontechnical-domain-owner-greenfield.json"
BROWNFIELD_CASE = "tests/pressure/nontechnical-owner-messy-existing-project.json"
CAPABILITY_CASE = "tests/pressure/single-model-is-not-the-execution-system.json"
COMPOSITION_CASE = "tests/pressure/provider-capabilities-exist-but-cannot-compose.json"


def load(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def require_text(errors: list[str], text: str, phrase: str, label: str) -> None:
    if phrase not in text:
        errors.append(f"{label}: missing phrase {phrase!r}")


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    errors: list[str] = []

    idea_path = root / ".aaop/routes/idea-to-build.json"
    idea = load(idea_path)
    if not isinstance(idea, dict):
        errors.append(f"{idea_path}: expected object")
    else:
        guards = {
            item.get("id"): item.get("rule", "")
            for item in idea.get("pressure_guards", [])
            if isinstance(item, dict)
        }
        human_rule = guards.get("human-context-is-product-evidence", "")
        for phrase in (
            "Do not infer product/domain authority from technical fluency",
            "lived experience",
            "testable first slice",
        ):
            require_text(errors, human_rule, phrase, str(idea_path))
        evidence = "\n".join(
            item
            for stage in idea.get("stages", [])
            if isinstance(stage, dict)
            for item in stage.get("evidence", [])
            if isinstance(item, str)
        )
        require_text(errors, evidence, "lived/domain experience", str(idea_path))

    capabilities_path = root / ".aaop/registries/capabilities.json"
    capabilities = load(capabilities_path)
    if not isinstance(capabilities, dict):
        errors.append(f"{capabilities_path}: expected object")
    else:
        policy = "\n".join(capabilities.get("resolution_policy", []))
        for phrase in (
            "language model is one reasoning provider, not the whole execution system",
            "verbal confidence is not capability proof",
            "meaningfully different failure mode",
            "Only a proven unresolved capability gap justifies adding a new provider",
        ):
            require_text(errors, policy, phrase, str(capabilities_path))

    planning_path = root / ".aaop/skills/capability-planning/SKILL.md"
    planning_text = planning_path.read_text(encoding="utf-8")
    for phrase in (
        "Close the composition path, not only the capability list.",
        "Capability composability and transfer closure",
        "exact-head repository execution is still partial/missing",
        "revision continuity",
        "composition_edges",
        "Do not install an orchestration framework merely because two existing tools cannot exchange one artifact.",
    ):
        require_text(errors, planning_text, phrase, str(planning_path))

    matrix_path = root / ".aaop/schemas/capability-matrix.schema.json"
    matrix = load(matrix_path)
    if not isinstance(matrix, dict):
        errors.append(f"{matrix_path}: expected object")
    else:
        properties = matrix.get("properties", {})
        if not isinstance(properties, dict) or "composition_edges" not in properties:
            errors.append(f"{matrix_path}: missing composition_edges")
        else:
            edges = properties.get("composition_edges")
            items = edges.get("items", {}) if isinstance(edges, dict) else {}
            required = set(items.get("required", [])) if isinstance(items, dict) else set()
            if not {"from", "to", "status", "transfer"} <= required:
                errors.append(f"{matrix_path}: composition_edges must require from/to/status/transfer")
            edge_props = items.get("properties", {}) if isinstance(items, dict) else {}
            for field in (
                "identity_requirement",
                "provenance_requirement",
                "authorization_requirement",
                "evidence",
                "gap_resolution",
            ):
                if not isinstance(edge_props, dict) or field not in edge_props:
                    errors.append(f"{matrix_path}: composition_edges missing {field!r}")

    provider_path = root / ".aaop/skills/provider-selection/SKILL.md"
    provider_text = provider_path.read_text(encoding="utf-8")
    for phrase in (
        "If no gap is proven, select **no additional provider**.",
        "current host native capability",
        "Composition closure before provider escalation",
        "exact-head execution remains partial",
        "smallest compatible bridge/shared workspace/provider-native transfer",
        "verify the original capability gap is actually closed",
    ):
        require_text(errors, provider_text, phrase, str(provider_path))

    orchestrator_path = root / ".aaop/ORCHESTRATOR.md"
    orchestrator = orchestrator_path.read_text(encoding="utf-8")
    for phrase in (
        "map each required capability against",
        "Only unresolved technical abilities become candidate capability gaps",
        "Only `capability-gap` directly justifies provider selection",
        "Default to one agent",
    ):
        require_text(errors, orchestrator, phrase, str(orchestrator_path))

    cases = {
        GREENFIELD_CASE: {
            "route": "idea-to-build",
            "guards": {"human-context-is-product-evidence", "user-does-not-own-stack-choice"},
            "facts": ["domain experience", "software requirements jargon"],
        },
        BROWNFIELD_CASE: {
            "route": "repo-recovery",
            "guards": {"preserve-conflicting-evidence", "prove-delta-before-mutation"},
            "facts": ["duplicated implementations", "validated behavior"],
        },
        CAPABILITY_CASE: {
            "route": "feature-change",
            "guards": {"reconcile-current-baseline-before-mutation", "verification-harness-integrity"},
            "facts": ["browser-visible behavior", "builder model judging its own"],
        },
        COMPOSITION_CASE: {
            "route": "repo-recovery",
            "guards": {"scoped-blocker-frontier-continuation"},
            "facts": ["repository provider", "local runtime", "exact-head repository execution"],
        },
    }

    for rel, expected in cases.items():
        path = root / rel
        payload = load(path)
        if not isinstance(payload, dict):
            errors.append(f"{path}: expected object")
            continue
        if payload.get("expected_route") != expected["route"]:
            errors.append(f"{path}: expected_route must be {expected['route']!r}")
        guards = set(payload.get("required_guard_ids", []))
        missing = expected["guards"] - guards
        if missing:
            errors.append(f"{path}: missing required guards {sorted(missing)}")
        facts = "\n".join(payload.get("known_facts", []))
        for phrase in expected["facts"]:
            require_text(errors, facts, phrase, str(path))

    composition = load(root / COMPOSITION_CASE)
    if isinstance(composition, dict):
        lessons = "\n".join(composition.get("lessons", []))
        for phrase in (
            "Capability availability is not capability composability",
            "revision continuity",
            "end-to-end capability graph",
            "smallest missing bridge",
        ):
            require_text(errors, lessons, phrase, COMPOSITION_CASE)
        if composition.get("expected_blocker_class") != "capability-composability":
            errors.append(f"{COMPOSITION_CASE}: expected_blocker_class must be 'capability-composability'")

    recovery_path = root / ".aaop/routes/repo-recovery.json"
    recovery = load(recovery_path)
    if isinstance(recovery, dict):
        guards = {
            item.get("id"): item.get("rule", "")
            for item in recovery.get("pressure_guards", [])
            if isinstance(item, dict)
        }
        for guard_id in (
            "preserve-conflicting-evidence",
            "prove-delta-before-mutation",
            "default-autonomous-takeover",
            "scoped-blocker-frontier-continuation",
        ):
            if guard_id not in guards:
                errors.append(f"{recovery_path}: missing brownfield recovery guard {guard_id!r}")
        stabilize = "\n".join(
            str(stage.get("purpose", ""))
            for stage in recovery.get("stages", [])
            if isinstance(stage, dict)
        )
        for phrase in ("before broad refactoring", "do not manufacture a diff"):
            require_text(errors, stabilize, phrase, str(recovery_path))
    else:
        errors.append(f"{recovery_path}: expected object")

    if errors:
        print("AAOP human-forward capability fabric validation failed:", file=sys.stderr)
        for item in errors:
            print(f"  - {item}", file=sys.stderr)
        return 1

    print("AAOP human-forward capability fabric validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
