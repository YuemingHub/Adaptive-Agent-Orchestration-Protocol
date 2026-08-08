# Claude Code Adapter

Purpose: map AAOP onto Claude Code's native instruction, Skill, subagent, permission, and MCP features without making Claude-specific behavior normative.

Host behavior last verified: **2026-08-08**

Official source:

- https://docs.anthropic.com/en/docs/claude-code/memory

## Bootstrap

Claude Code automatically loads project `CLAUDE.md` memory/instructions and can discover more-specific `CLAUDE.md` files as work enters nested subtrees. Claude `CLAUDE.md` also supports `@path` imports, but AAOP does not require an import chain for its core startup.

AAOP therefore keeps root `CLAUDE.md` as a **thin Claude-specific bridge**, not a second copy of the common `AGENTS.md` bootstrap.

The installed Claude block should only ensure that Claude Code:

1. reads `.aaop/ORCHESTRATOR.md` for non-trivial work;
2. starts with `.aaop/skills/developer-intake/SKILL.md`;
3. loads `.aaop/skills/route-execution/SKILL.md` and only the current route pack after routing;
4. respects project-specific `CLAUDE.md` text outside the AAOP marker block;
5. uses existing Claude Code/native capabilities before adding providers.

Why keep it thin? Cursor CLI currently reads both root `AGENTS.md` **and** root `CLAUDE.md`. Duplicating the full AAOP bootstrap in both files wastes context and can create needless repetition. The canonical policy remains `.aaop/ORCHESTRATOR.md` either way.

## Native Skills

Claude Code project Skills live under `.claude/skills/<skill-name>/SKILL.md` and use the Agent Skills format.

AAOP keeps canonical source Skills under `.aaop/skills/` to remain host-neutral. For native discovery, copy or symlink only desired canonical Skills into `.claude/skills/` while preserving directory name and `SKILL.md` meaning.

Do not automatically duplicate every Skill into every project. Progressive disclosure is part of the design.

## Subagents

Generate a project-specific subagent **only after** AAOP capability planning shows a stable responsibility worth isolating. Avoid maintaining generic “frontend/backend/QA” agents by default.

A generated agent should map AAOP fields approximately as:

```text
AAOP objective              → agent prompt/body
AAOP responsibilities       → prompt constraints
AAOP skills                 → skill preload when appropriate
AAOP tools                  → allowed/disallowed tools
AAOP MCP providers          → scoped MCP access
AAOP permission boundary    → Claude permission settings
AAOP independent work       → optional isolated worktree/context
```

Use subagents when context isolation, specialization, independent review, permission boundaries, or safe parallelism materially helps the task—not because Claude Code happens to expose the primitive.

## Permissions

Do not use permissive modes merely to eliminate prompts. Map AAOP's risk-based autonomy onto Claude Code permissions:

- allow routine low-risk project operations;
- restrict tools for specialist/read-only reviewers;
- keep consequential external/destructive operations behind the project's intended permission boundary.

## MCP

Scope Claude Code MCP access to what the current responsibility needs. If a server is missing, follow `.aaop/policies/mcp-and-tools.md` instead of guessing an install command.

## Conformance boundary

AAOP depends on Claude Code's documented `CLAUDE.md` project-memory surface, not on an AAOP-specific Claude plugin. If Claude changes discovery/import behavior, update this adapter and host-bootstrap conformance evidence rather than leaking vendor rules into the host-neutral Orchestrator.
