#!/usr/bin/env python3
"""Zero-dependency structural validation for AAOP."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SKILL_NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
ROUTE_IDS = {
    "idea-to-build",
    "repo-recovery",
    "bug-fix",
    "feature-change",
    "understand-review",
    "release-operations",
}

REQUIRED = [
    "AGENTS.md",
    "CLAUDE.md",
    ".aaop/ORCHESTRATOR.md",
    ".aaop/policies/autonomy.md",
    ".aaop/policies/mcp-and-tools.md",
    ".aaop/policies/progressive-integration.md",
    ".aaop/registries/routes.json",
    ".aaop/registries/capabilities.json",
    ".aaop/registries/providers.json",
    ".aaop/registries/adoption-profiles.json",
    ".aaop/schemas/intake-envelope.schema.json",
    ".aaop/schemas/route-capability-pack.schema.json",
    ".aaop/schemas/environment-profile.schema.json",
    ".aaop/schemas/project-profile.schema.json",
    ".aaop/schemas/capability-matrix.schema.json",
    ".aaop/schemas/team-plan.schema.json",
    ".aaop/schemas/execution-plan.schema.json",
    ".aaop/schemas/integration-plan.schema.json",
    ".aaop/schemas/integration-recipe.schema.json",
    ".aaop/recipes/README.md",
    ".aaop/tools/doctor.py",
    ".aaop/tools/route.py",
    ".aaop/tools/recipe.py",
]


def error(errors: list[str], message: str) -> None:
    errors.append(message)


def parse_frontmatter(path: Path, errors: list[str]) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        error(errors, f"{path}: missing opening YAML frontmatter delimiter")
        return {}
    try:
        end = lines[1:].index("---") + 1
    except ValueError:
        error(errors, f"{path}: missing closing YAML frontmatter delimiter")
        return {}

    values: dict[str, str] = {}
    for raw in lines[1:end]:
        if not raw or raw[0].isspace() or ":" not in raw:
            continue
        key, value = raw.split(":", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def validate_skill(path: Path, errors: list[str]) -> None:
    values = parse_frontmatter(path, errors)
    name = values.get("name", "")
    description = values.get("description", "")

    if not name:
        error(errors, f"{path}: missing skill name")
    elif not SKILL_NAME_RE.fullmatch(name):
        error(errors, f"{path}: invalid Agent Skills name {name!r}")
    elif len(name) > 64:
        error(errors, f"{path}: name exceeds 64 characters")
    elif path.parent.name != name:
        error(errors, f"{path}: name must match parent directory {path.parent.name!r}")

    if not description:
        error(errors, f"{path}: missing skill description")
    elif len(description) > 1024:
        error(errors, f"{path}: description exceeds 1024 characters")

    if len(path.read_text(encoding="utf-8").splitlines()) > 500:
        error(errors, f"{path}: SKILL.md exceeds recommended 500 lines")


def load_json(path: Path, errors: list[str]) -> object | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        error(errors, f"{path}: invalid JSON: {exc}")
        return None


def validate_json(path: Path, errors: list[str]) -> None:
    payload = load_json(path, errors)
    if payload is None:
        return
    if path.name.endswith(".schema.json") and (not isinstance(payload, dict) or "$schema" not in payload):
        error(errors, f"{path}: schema file missing $schema")


def validate_routes(root: Path, errors: list[str]) -> None:
    path = root / ".aaop/registries/routes.json"
    payload = load_json(path, errors)
    if not isinstance(payload, dict):
        return
    rows = payload.get("routes")
    if not isinstance(rows, list):
        error(errors, f"{path}: routes must be a list")
        return

    found: set[str] = set()
    for row in rows:
        if not isinstance(row, dict):
            error(errors, f"{path}: every route must be an object")
            continue
        route_id = row.get("id")
        if route_id not in ROUTE_IDS:
            error(errors, f"{path}: unknown route id {route_id!r}")
            continue
        if route_id in found:
            error(errors, f"{path}: duplicate route id {route_id!r}")
        found.add(route_id)
        for field in ("situation", "use_when", "first_moves", "avoid", "completion_shape"):
            if field not in row:
                error(errors, f"{path}: {route_id} missing field {field!r}")

    missing = ROUTE_IDS - found
    if missing:
        error(errors, f"{path}: missing routes: {', '.join(sorted(missing))}")


def provider_ids(root: Path, errors: list[str]) -> set[str]:
    path = root / ".aaop/registries/providers.json"
    payload = load_json(path, errors)
    if not isinstance(payload, dict):
        return set()
    rows = payload.get("providers")
    if not isinstance(rows, list) or not rows:
        error(errors, f"{path}: providers must be a non-empty list")
        return set()

    ids: set[str] = set()
    for row in rows:
        if not isinstance(row, dict):
            error(errors, f"{path}: every provider must be an object")
            continue
        provider_id = row.get("id")
        if not isinstance(provider_id, str) or not SKILL_NAME_RE.fullmatch(provider_id):
            error(errors, f"{path}: invalid provider id {provider_id!r}")
            continue
        if provider_id in ids:
            error(errors, f"{path}: duplicate provider id {provider_id!r}")
        ids.add(provider_id)
        level = row.get("adoption_level")
        if not isinstance(level, int) or not 1 <= level <= 5:
            error(errors, f"{path}: {provider_id} adoption_level must be 1..5")
    return ids


def validate_provider_model(root: Path, errors: list[str], ids: set[str]) -> None:
    profiles_path = root / ".aaop/registries/adoption-profiles.json"
    payload = load_json(profiles_path, errors)
    if not isinstance(payload, dict):
        return
    profiles = payload.get("profiles")
    if not isinstance(profiles, list) or not profiles:
        error(errors, f"{profiles_path}: profiles must be a non-empty list")
        return

    for profile in profiles:
        if not isinstance(profile, dict):
            error(errors, f"{profiles_path}: every profile must be an object")
            continue
        level = profile.get("level")
        if not isinstance(level, int) or not 0 <= level <= 5:
            error(errors, f"{profiles_path}: profile level must be 0..5")
        for key in ("requires", "optional", "choose_one_or_few"):
            refs = profile.get(key, [])
            if not isinstance(refs, list):
                error(errors, f"{profiles_path}: {key} must be a list")
                continue
            for provider_id in refs:
                if provider_id not in ids:
                    error(errors, f"{profiles_path}: unknown provider reference {provider_id!r}")


def validate_recipes(root: Path, errors: list[str], ids: set[str]) -> set[str]:
    recipe_root = root / ".aaop/recipes"
    recipes = sorted(recipe_root.glob("*.json")) if recipe_root.exists() else []
    if not recipes:
        error(errors, "no integration recipes found under .aaop/recipes")
        return set()

    recipe_ids: set[str] = set()
    for path in recipes:
        payload = load_json(path, errors)
        if not isinstance(payload, dict):
            continue
        recipe_id = payload.get("id")
        provider_id = payload.get("provider_id")
        if not isinstance(recipe_id, str) or not SKILL_NAME_RE.fullmatch(recipe_id):
            error(errors, f"{path}: invalid recipe id {recipe_id!r}")
            continue
        if path.stem != recipe_id:
            error(errors, f"{path}: recipe id must match filename stem")
        if recipe_id in recipe_ids:
            error(errors, f"{path}: duplicate recipe id {recipe_id!r}")
        recipe_ids.add(recipe_id)
        if provider_id not in ids:
            error(errors, f"{path}: unknown provider_id {provider_id!r}")
        for required in ("last_verified", "source_of_truth", "selection", "detect", "install", "verify", "rollback"):
            if required not in payload:
                error(errors, f"{path}: missing required field {required!r}")
        install = payload.get("install")
        if not isinstance(install, dict) or "mode" not in install:
            error(errors, f"{path}: install.mode is required")
    return recipe_ids


def validate_route_packs(root: Path, errors: list[str], providers: set[str], recipes: set[str]) -> None:
    pack_root = root / ".aaop/routes"
    found: set[str] = set()
    for path in sorted(pack_root.glob("*.json")) if pack_root.exists() else []:
        payload = load_json(path, errors)
        if not isinstance(payload, dict):
            continue
        route_id = payload.get("route_id")
        if route_id not in ROUTE_IDS:
            error(errors, f"{path}: unknown route_id {route_id!r}")
            continue
        if path.stem != route_id:
            error(errors, f"{path}: route_id must match filename stem")
        if route_id in found:
            error(errors, f"{path}: duplicate route capability pack {route_id!r}")
        found.add(route_id)

        for required in ("version", "objective", "stages", "escalations", "verification", "reroute_signals"):
            if required not in payload:
                error(errors, f"{path}: missing required field {required!r}")

        stages = payload.get("stages")
        if not isinstance(stages, list) or not stages:
            error(errors, f"{path}: stages must be a non-empty list")
        else:
            stage_ids: set[str] = set()
            for stage in stages:
                if not isinstance(stage, dict):
                    error(errors, f"{path}: every stage must be an object")
                    continue
                stage_id = stage.get("id")
                if not isinstance(stage_id, str) or not stage_id:
                    error(errors, f"{path}: stage id is required")
                elif stage_id in stage_ids:
                    error(errors, f"{path}: duplicate stage id {stage_id!r}")
                else:
                    stage_ids.add(stage_id)
                for field in ("purpose", "required_capabilities", "evidence", "exit_when"):
                    if field not in stage:
                        error(errors, f"{path}: stage {stage_id!r} missing field {field!r}")

        escalations = payload.get("escalations", [])
        if not isinstance(escalations, list):
            error(errors, f"{path}: escalations must be a list")
            continue
        for item in escalations:
            if not isinstance(item, dict):
                error(errors, f"{path}: escalation must be an object")
                continue
            for field in ("when", "capability_gap", "provider_candidates", "selection_rule"):
                if field not in item:
                    error(errors, f"{path}: escalation missing field {field!r}")
            candidates = item.get("provider_candidates", [])
            if not isinstance(candidates, list):
                error(errors, f"{path}: provider_candidates must be a list")
                continue
            for provider_id in candidates:
                if provider_id not in providers:
                    error(errors, f"{path}: unknown provider candidate {provider_id!r}")
                elif provider_id not in recipes:
                    error(errors, f"{path}: provider candidate {provider_id!r} has no integration recipe")

    missing = ROUTE_IDS - found
    if missing:
        error(errors, f"{pack_root}: missing route capability packs: {', '.join(sorted(missing))}")
    extra = found - ROUTE_IDS
    if extra:
        error(errors, f"{pack_root}: unexpected route capability packs: {', '.join(sorted(extra))}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate AAOP repository/package structure")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="AAOP root to validate")
    parser.add_argument(
        "--package-only",
        action="store_true",
        help="Validate an installed package without requiring repository adapters/docs.",
    )
    args = parser.parse_args()
    root = args.root.resolve()
    errors: list[str] = []

    for relative in REQUIRED:
        if not (root / relative).exists():
            error(errors, f"missing required file: {relative}")

    for path in (root / ".aaop").rglob("*.json") if (root / ".aaop").exists() else []:
        validate_json(path, errors)

    validate_routes(root, errors)
    providers = provider_ids(root, errors)
    validate_provider_model(root, errors, providers)
    recipes = validate_recipes(root, errors, providers)
    validate_route_packs(root, errors, providers, recipes)

    skill_root = root / ".aaop" / "skills"
    skills = sorted(skill_root.glob("*/SKILL.md")) if skill_root.exists() else []
    if not skills:
        error(errors, "no canonical Skills found under .aaop/skills")
    for path in skills:
        validate_skill(path, errors)

    expected_skills = {
        "developer-intake",
        "route-execution",
        "project-discovery",
        "capability-planning",
        "provider-selection",
        "team-construction",
        "tool-resolution",
        "verification-loop",
    }
    actual_skills = {path.parent.name for path in skills}
    missing_skills = expected_skills - actual_skills
    if missing_skills:
        error(errors, f"missing core Skills: {', '.join(sorted(missing_skills))}")

    if not args.package_only:
        for relative in [
            "README.md",
            "docs/DEVELOPER_ENTRYPOINT.md",
            "docs/ROUTE_CAPABILITY_PACKS.md",
            "docs/PROGRESSIVE_ADOPTION.md",
            "docs/ECOSYSTEM_MAP.md",
            "adapters/codex.md",
            "adapters/claude-code.md",
            "adapters/cursor.md",
            "adapters/generic.md",
            "scripts/install.py",
        ]:
            if not (root / relative).exists():
                error(errors, f"missing repository file: {relative}")

    if errors:
        print("AAOP validation failed:", file=sys.stderr)
        for item in errors:
            print(f"  - {item}", file=sys.stderr)
        return 1

    print(
        f"AAOP validation passed ({len(skills)} Skills, {len(ROUTE_IDS)} route packs, "
        f"{len(recipes)} recipes, root={root})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
