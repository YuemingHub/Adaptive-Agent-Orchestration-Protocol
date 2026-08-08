# AAOP for Claude Code

This repository uses the Adaptive Agent Orchestration Protocol.

For substantive developer work:

1. read `.aaop/ORCHESTRATOR.md`;
2. start with `.aaop/skills/developer-intake/SKILL.md`;
3. after routing, load `.aaop/skills/route-execution/SKILL.md` and only the current `.aaop/routes/<route-id>.json`;
4. if AAOP integrity is uncertain, use `python .aaop/tools/health.py . --json` before repair (`source-tree` is expected in this repository);
5. use `adapters/claude-code.md` only when Claude-specific Skills, subagents, permissions, or MCP behavior matters.

Prefer current project evidence and existing Claude Code/native capability before adding providers. Keep reviews read-only unless mutation is explicitly requested, and do not turn early technology vocabulary into requirements before the outcome proves the need.

This file is deliberately a thin Claude-specific bridge. Canonical orchestration policy lives in `.aaop/ORCHESTRATOR.md`; common cross-host startup guidance lives in `AGENTS.md`. Keeping this file small avoids duplicating the full AAOP bootstrap in hosts such as Cursor CLI that read both root instruction files.
