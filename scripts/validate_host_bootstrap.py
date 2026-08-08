#!/usr/bin/env python3
"""Validate AAOP's static cross-host bootstrap contract.

This cannot prove proprietary hosts actually loaded repository instructions at
runtime. It protects AAOP's side of the contract: canonical paths, compact host
bridges, documented first-party sources, and avoidance of duplicated bootstraps.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERIFIED_DATE = "2026-08-08"


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def load_installer():
    path = ROOT / "scripts" / "install.py"
    spec = importlib.util.spec_from_file_location("aaop_installer_for_validation", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def meaningful_lines(text: str) -> list[str]:
    return [line.strip() for line in text.splitlines() if line.strip()]


def require_refs(errors: list[str], label: str, text: str) -> None:
    for required in (
        ".aaop/ORCHESTRATOR.md",
        ".aaop/skills/developer-intake/SKILL.md",
        ".aaop/skills/route-execution/SKILL.md",
        ".aaop/routes/<route-id>.json",
    ):
        if required not in text:
            fail(errors, f"{label}: missing canonical startup reference {required}")


def validate_adapter(
    errors: list[str],
    filename: str,
    required_urls: tuple[str, ...],
    required_phrases: tuple[str, ...] = (),
) -> None:
    path = ROOT / "adapters" / filename
    if not path.exists():
        fail(errors, f"missing adapter: {path}")
        return
    text = path.read_text(encoding="utf-8")
    if f"Host behavior last verified: **{VERIFIED_DATE}**" not in text:
        fail(errors, f"{path}: missing current host verification date {VERIFIED_DATE}")
    for url in required_urls:
        if url not in text:
            fail(errors, f"{path}: missing first-party source {url}")
    for phrase in required_phrases:
        if phrase not in text:
            fail(errors, f"{path}: missing conformance statement {phrase!r}")


def main() -> int:
    errors: list[str] = []
    installer = load_installer()

    agents = installer.AGENTS_BLOCK
    claude = installer.CLAUDE_BLOCK
    begin = installer.AAOP_BEGIN
    end = installer.AAOP_END

    for label, block in (("AGENTS_BLOCK", agents), ("CLAUDE_BLOCK", claude)):
        if block.count(begin) != 1 or block.count(end) != 1:
            fail(errors, f"{label}: expected exactly one AAOP marker pair")
        require_refs(errors, label, block)

    agents_lines = meaningful_lines(agents)
    claude_lines = meaningful_lines(claude)
    if len(agents_lines) < 12:
        fail(errors, "AGENTS_BLOCK: common bootstrap unexpectedly too small to carry routing guardrails")
    if len(claude_lines) >= len(agents_lines) * 0.55:
        fail(
            errors,
            f"CLAUDE_BLOCK: host bridge is no longer thin ({len(claude_lines)} lines vs {len(agents_lines)} common lines)",
        )
    if "This block is intentionally small" not in claude:
        fail(errors, "CLAUDE_BLOCK: missing explicit anti-duplication boundary")
    if "common cross-host bootstrap guidance lives in `AGENTS.md`" not in claude:
        fail(errors, "CLAUDE_BLOCK: common AGENTS ownership boundary is unclear")

    source_claude = (ROOT / "CLAUDE.md").read_text(encoding="utf-8")
    require_refs(errors, "root CLAUDE.md", source_claude)
    if len(meaningful_lines(source_claude)) > 24:
        fail(errors, "root CLAUDE.md: source bridge has grown beyond the thin-host role")
    if "deliberately a thin Claude-specific bridge" not in source_claude:
        fail(errors, "root CLAUDE.md: missing thin-bridge design statement")

    validate_adapter(
        errors,
        "codex.md",
        (
            "https://openai.com/index/unrolling-the-codex-agent-loop/",
            "https://openai.com/index/introducing-codex/",
        ),
        ("root `AGENTS.md` marked block as the **common cross-host bootstrap**",),
    )
    validate_adapter(
        errors,
        "claude-code.md",
        ("https://docs.anthropic.com/en/docs/claude-code/memory",),
        ("**thin Claude-specific bridge**",),
    )
    validate_adapter(
        errors,
        "cursor.md",
        (
            "https://docs.cursor.com/context/rules-for-ai",
            "https://docs.cursor.com/en/cli/using",
        ),
        (
            "Cursor CLI also reads root `AGENTS.md` **and** root `CLAUDE.md`",
            "no generated `.cursor/rules` file is required",
        ),
    )

    doc = ROOT / "docs" / "HOST_BOOTSTRAP_CONFORMANCE.md"
    if not doc.exists():
        fail(errors, f"missing conformance documentation: {doc}")
    else:
        text = doc.read_text(encoding="utf-8")
        if VERIFIED_DATE not in text:
            fail(errors, f"{doc}: missing verification date")
        for host in ("Codex", "Claude Code", "Cursor"):
            if f"## {host}" not in text:
                fail(errors, f"{doc}: missing {host} section")
        if "Static CI cannot prove" not in text:
            fail(errors, f"{doc}: missing runtime-proof limitation")

    if errors:
        print("AAOP host bootstrap validation failed:", file=sys.stderr)
        for item in errors:
            print(f"  - {item}", file=sys.stderr)
        return 1

    print(
        "AAOP host bootstrap validation passed "
        f"(AGENTS={len(agents_lines)} meaningful lines, CLAUDE={len(claude_lines)}; "
        "hosts=codex,claude-code,cursor)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
