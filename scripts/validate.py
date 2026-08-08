#!/usr/bin/env python3
"""Zero-dependency structural validation for AAOP."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SKILL_NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

REQUIRED = [
    "AGENTS.md",
    "CLAUDE.md",
    ".aaop/ORCHESTRATOR.md",
    ".aaop/policies/autonomy.md",
    ".aaop/policies/mcp-and-tools.md",
    ".aaop/policies/progressive-integration.md",
    ".aaop/registries/capabilities.json",
    ".aaop/registries/providers.json",
    ".aaop/registries/adoption-profiles.json",
    ".aaop/schemas/environment-profile.schema.json",
    ".aaop/schemas/project-profile.schema.json",
    ".aaop/schemas/capability-matrix.schema.json",
    ".aaop/schemas/team-plan.schema.json",
    ".aaop/schemas/execution-plan.schema.json",
    ".aaop/schemas/integration-plan.schema.json",
    ".aaop/tools/doctor.py",
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
    except Exception as exc:  # noqa: BLE001 - validator should report all parse failures
        error(errors, f"{path}: invalid JSON: {exc}")
        return None


def validate_json(path: Path, errors: list[str]) -> None:
    payload = load_json(path, errors)
    if payload is None:
        return
    if path.name.endswith(".schema.json") and (not isinstance(payload, dict) or "$schema" not in payload):
        error(errors, f"{path}: schema file missing $schema")


def validate_provider_model(root: Path, errors: list[str]) -> None:
    providers_path = root / ".aaop/registries/providers.json"
    profiles_path = root / ".aaop/registries/adoption-profiles.json"
    providers_payload = load_json(providers_path, errors)
    profiles_payload = load_json(profiles_path, errors)
    if not isinstance(providers_payload, dict) or not isinstance(profiles_payload, dict):
        return

    provider_rows = providers_payload.get("providers")
    if not isinstance(provider_rows, list) or not provider_rows:
        error(errors, f"{providers_path}: providers must be a non-empty list")
        return

    provider_ids: set[str] = set()
    for row in provider_rows:
        if not isinstance(row, dict):
            error(errors, f"{providers_path}: every provider must be an object")
            continue
        provider_id = row.get("id")
        if not isinstance(provider_id, str) or not SKILL_NAME_RE.fullmatch(provider_id):
            error(errors, f"{providers_path}: invalid provider id {provider_id!r}")
            continue
        if provider_id in provider_ids:
            error(errors, f"{providers_path}: duplicate provider id {provider_id!r}")
        provider_ids.add(provider_id)
        level = row.get("adoption_level")
        if not isinstance(level, int) or not 1 <= level <= 5:
            error(errors, f"{providers_path}: {provider_id} adoption_level must be 1..5")

    profiles = profiles_payload.get("profiles")
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
                if provider_id not in provider_ids:
                    error(errors, f"{profiles_path}: unknown provider reference {provider_id!r}")


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

    validate_provider_model(root, errors)

    skill_root = root / ".aaop" / "skills"
    skills = sorted(skill_root.glob("*/SKILL.md")) if skill_root.exists() else []
    if not skills:
        error(errors, "no canonical Skills found under .aaop/skills")
    for path in skills:
        validate_skill(path, errors)

    expected_skills = {
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

    print(f"AAOP validation passed ({len(skills)} Skills, root={root})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
