#!/usr/bin/env python3
"""Install AAOP into another project without external dependencies.

Usage:
    python scripts/install.py /path/to/project
    python scripts/install.py /path/to/project --force

The installer copies the canonical `.aaop` package and adds compact bootstrap
blocks to AGENTS.md and CLAUDE.md without replacing existing project rules.
It installs no third-party runtime, Skill collection, MCP server, route provider,
or workspace.
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

AAOP_BEGIN = "<!-- AAOP:BEGIN -->"
AAOP_END = "<!-- AAOP:END -->"

AGENTS_BLOCK = f"""{AAOP_BEGIN}
## Adaptive Agent Orchestration Protocol (AAOP)

For non-trivial developer work, read `.aaop/ORCHESTRATOR.md` and begin with
`.aaop/skills/developer-intake/SKILL.md`. Infer the user's current situation and
one primary development route from ordinary language plus available project
evidence. Then load `.aaop/skills/route-execution/SKILL.md` and only the matching
`.aaop/routes/<route-id>.json` capability pack.

Do not make the user choose an Agent, workflow, Skill, MCP server, provider, or
runtime. Read accessible repository/log/test evidence before asking questions.
Satisfy route capabilities with the current host/repository first. A provider
candidate in a route pack is not a dependency: add the smallest provider surface
only after a concrete capability gap is proven. Apply risk-based autonomy,
verify the route outcome, and reroute when evidence changes the situation.

Canonical orchestration Skills live under `.aaop/skills/`.
{AAOP_END}
"""

CLAUDE_BLOCK = f"""{AAOP_BEGIN}
## Adaptive Agent Orchestration Protocol (AAOP)

Read `AGENTS.md`, `.aaop/ORCHESTRATOR.md`, and start developer requests with
`.aaop/skills/developer-intake/SKILL.md`. After routing, load
`.aaop/skills/route-execution/SKILL.md` and only the current
`.aaop/routes/<route-id>.json` capability pack. Accept natural language, inspect
the workspace before asking for technical facts already present, and prefer
existing Claude Code/native capabilities. Do not create a fixed team or add a
provider merely because a route pack lists it; prove the capability gap first.
{AAOP_END}
"""


def append_block(path: Path, block: str) -> str:
    if path.exists():
        text = path.read_text(encoding="utf-8")
        if AAOP_BEGIN in text:
            return "already-present"
        separator = "" if not text or text.endswith("\n\n") else "\n\n"
        path.write_text(text + separator + block, encoding="utf-8")
        return "appended"
    path.write_text(block, encoding="utf-8")
    return "created"


def copy_package(source: Path, target: Path, force: bool) -> str:
    destination = target / ".aaop"
    if destination.exists():
        if not force:
            raise SystemExit(
                f"Refusing to overwrite existing {destination}. Re-run with --force after review."
            )
        shutil.rmtree(destination)
    shutil.copytree(source / ".aaop", destination, ignore=shutil.ignore_patterns("runtime"))
    return str(destination)


def main() -> int:
    parser = argparse.ArgumentParser(description="Install AAOP into a project")
    parser.add_argument("target", type=Path, help="Target project directory")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Replace an existing .aaop package. Bootstrap blocks are never duplicated.",
    )
    args = parser.parse_args()

    source = Path(__file__).resolve().parents[1]
    target = args.target.expanduser().resolve()
    target.mkdir(parents=True, exist_ok=True)

    required = source / ".aaop" / "ORCHESTRATOR.md"
    if not required.exists():
        raise SystemExit(f"AAOP source package is incomplete: missing {required}")

    package_path = copy_package(source, target, args.force)
    agents_status = append_block(target / "AGENTS.md", AGENTS_BLOCK)
    claude_status = append_block(target / "CLAUDE.md", CLAUDE_BLOCK)

    print("AAOP installation complete")
    print(f"  package: {package_path}")
    print(f"  AGENTS.md: {agents_status}")
    print(f"  CLAUDE.md: {claude_status}")
    print("  third-party providers installed: none")
    print("  secrets requested: none")
    print("Optional inventory: python .aaop/tools/doctor.py .")
    print("Optional route packs: python .aaop/tools/route.py list")
    print("Optional provider recipes: python .aaop/tools/recipe.py list")
    print("Next: open the target project in your existing AI host and describe what you want in ordinary language.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
