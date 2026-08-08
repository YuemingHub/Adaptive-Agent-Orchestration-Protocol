#!/usr/bin/env python3
"""Install AAOP into another project without external dependencies.

Usage:
    python scripts/install.py /path/to/project
    python scripts/install.py /path/to/project --force

The installer copies the canonical `.aaop` package and adds compact bootstrap
blocks to AGENTS.md and CLAUDE.md without replacing existing project rules.
It installs no third-party runtime, Skill collection, MCP server, or workspace.
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

AAOP_BEGIN = "<!-- AAOP:BEGIN -->"
AAOP_END = "<!-- AAOP:END -->"

AGENTS_BLOCK = f"""{AAOP_BEGIN}
## Adaptive Agent Orchestration Protocol (AAOP)

For non-trivial work, read `.aaop/ORCHESTRATOR.md` before substantive changes.
Start from capabilities already present in this project/host. Derive required
capabilities before creating agents or adding integrations. Install nothing new
unless a concrete capability gap is proven; then select the smallest justified
Skill, MCP, discovery standard, runtime, or workspace. Apply risk-based autonomy
and verify the requested outcome before declaring completion.

Canonical orchestration Skills live under `.aaop/skills/`.
{AAOP_END}
"""

CLAUDE_BLOCK = f"""{AAOP_BEGIN}
## Adaptive Agent Orchestration Protocol (AAOP)

Read `AGENTS.md` and `.aaop/ORCHESTRATOR.md` for non-trivial work. Load only the
relevant `.aaop/skills/*/SKILL.md` procedures. Prefer existing Claude Code/native
capabilities. Do not create a fixed team or add MCP/runtime dependencies by
default; prove the capability gap first and use progressive integration.
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
    print("Next: open the target project in your existing AI host and state the desired outcome.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
