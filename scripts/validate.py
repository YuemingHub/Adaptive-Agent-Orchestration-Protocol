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
    ".aaop/registries/capabilities.json",
    ".aaop/schemas/environment-profile.schema.json",
    ".aaop/schemas/project-profile.schema.json",
    ".aaop/schemas/capability-matrix.schema.json",
    ".aaop/schemas/team-plan.schema.json",
    ".aaop/schemas/execution-plan.schema.json",
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


def validate_json(path: Path, errors: list[str]) -> None:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001 - validator should report all parse failures
        error(errors, f"{path}: invalid JSON: {exc}")
        return
    if path.name.endswith(".schema.json") and "$schema" not in payload:
        error(errors, f"{path}: schema file missing $schema")


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

    skill_root = root / ".aaop" / "skills"
    skills = sorted(skill_root.glob("*/SKILL.md")) if skill_root.exists() else []
    if not skills:
        error(errors, "no canonical Skills found under .aaop/skills")
    for path in skills:
        validate_skill(path, errors)

    expected_skills = {
        "project-discovery",
        "capability-planning",
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
