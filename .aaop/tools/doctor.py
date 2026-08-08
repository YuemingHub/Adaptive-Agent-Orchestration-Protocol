#!/usr/bin/env python3
"""Inspect an AAOP-enabled project without installing anything.

The doctor reports what is already present so the orchestrator can start from the
lowest integration surface. It intentionally does not install, connect, or modify
providers.
"""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

HOST_COMMANDS = {
    "codex": "Codex CLI",
    "claude": "Claude Code",
    "cursor": "Cursor CLI",
    "agent-router": "AgentSpace AgentRouter",
    "auto": "AutoAgent CLI",
}

MCP_CONFIGS = [
    ".mcp.json",
    ".cursor/mcp.json",
    ".claude/mcp.json",
]

SKILL_PATHS = [
    ".aaop/skills",
    ".agents/skills",
    ".claude/skills",
    ".cursor/skills",
]

INSTRUCTION_FILES = [
    "AGENTS.md",
    "CLAUDE.md",
    ".github/copilot-instructions.md",
]


def existing_paths(root: Path, candidates: list[str]) -> list[str]:
    return [item for item in candidates if (root / item).exists()]


def command_inventory() -> dict[str, str]:
    found: dict[str, str] = {}
    for command, label in HOST_COMMANDS.items():
        path = shutil.which(command)
        if path:
            found[command] = path
    return found


def count_skills(root: Path, paths: list[str]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for relative in paths:
        directory = root / relative
        if directory.exists():
            counts[relative] = len(list(directory.glob("*/SKILL.md")))
    return counts


def infer_surface(mcp: list[str], skills: dict[str, int], commands: dict[str, str]) -> int:
    # This is an environment hint, not a claim that higher layers are required.
    if "agent-router" in commands:
        return 5
    if "auto" in commands:
        return 4
    if mcp or any(value > 0 for value in skills.values()):
        return 2
    if any(command in commands for command in ("codex", "claude", "cursor")):
        return 1
    return 0


def inspect(root: Path) -> dict[str, object]:
    instructions = existing_paths(root, INSTRUCTION_FILES)
    mcp = existing_paths(root, MCP_CONFIGS)
    skill_dirs = existing_paths(root, SKILL_PATHS)
    skills = count_skills(root, skill_dirs)
    commands = command_inventory()
    surface = infer_surface(mcp, skills, commands)

    return {
        "project_root": str(root),
        "instruction_files": instructions,
        "mcp_configs": mcp,
        "skill_counts": skills,
        "available_commands": commands,
        "observed_surface_level": surface,
        "policy": "Do not upgrade based on this inventory alone. Start with what is present; prove a capability gap before adding a provider.",
        "next_action": "State the desired project outcome and let AAOP perform project/capability discovery before any installation decision.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect the current AAOP integration surface")
    parser.add_argument("root", nargs="?", type=Path, default=Path.cwd())
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    args = parser.parse_args()

    root = args.root.expanduser().resolve()
    report = inspect(root)

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0

    print("AAOP environment doctor")
    print(f"  project: {report['project_root']}")
    print(f"  observed surface: Level {report['observed_surface_level']}")
    print(f"  instructions: {', '.join(report['instruction_files']) or 'none detected'}")
    print(f"  MCP configs: {', '.join(report['mcp_configs']) or 'none detected'}")
    skill_counts = report["skill_counts"]
    if isinstance(skill_counts, dict) and skill_counts:
        rendered = ", ".join(f"{key}={value}" for key, value in skill_counts.items())
    else:
        rendered = "none detected"
    print(f"  skills: {rendered}")
    commands = report["available_commands"]
    if isinstance(commands, dict):
        print(f"  runtime/host CLIs: {', '.join(commands) or 'none detected'}")
    print("  decision: do not install anything from this report alone")
    print(f"  next: {report['next_action']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
