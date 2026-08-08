# Claude Code Adapter

Purpose: map AAOP onto Claude Code's native instruction, Skill, subagent, team, permission, and MCP features.

## Bootstrap

Claude Code loads project `CLAUDE.md`. AAOP's root `CLAUDE.md` points to `AGENTS.md` and `.aaop/ORCHESTRATOR.md`.

## Native Skills

Claude Code project Skills live under `.claude/skills/<skill-name>/SKILL.md` and use the Agent Skills format.

AAOP keeps canonical source Skills under `.aaop/skills/` to remain host-neutral. For native discovery, copy or symlink each desired canonical skill into `.claude/skills/` while preserving its directory name and `SKILL.md` content.

Do not automatically duplicate every Skill into every project if it is not needed. Progressive disclosure is part of the design.

## Subagents

Claude Code project subagents can be defined under `.claude/agents/` with YAML frontmatter controlling description, tools, model, skills, MCP access, permissions, and related behavior.

Generate a project-specific subagent **only after** AAOP capability planning shows a stable responsibility worth isolating. Avoid maintaining generic “frontend/backend/QA” agents by default.

A generated agent should map AAOP fields approximately as:

```text
AAOP objective              → agent prompt/body
AAOP responsibilities       → prompt constraints
AAOP skills                 → `skills:` preloads when appropriate
AAOP tools                  → `tools:` / `disallowedTools:`
AAOP MCP providers          → `mcpServers:`
AAOP permission boundary    → `permissionMode` + project settings
AAOP independent work       → optional worktree isolation
```

Subagents are appropriate for isolated work that returns a result to the lead. Use agent teams only when peers need shared task coordination/direct communication and the current Claude Code environment supports that feature.

## Permissions

Do not use permissive modes merely to eliminate prompts. Map AAOP's risk-based autonomy onto Claude Code permissions:

- allow routine low-risk project operations;
- restrict tools for specialist/read-only reviewers;
- keep consequential external/destructive operations behind the project's intended permission boundary.

## MCP

A Claude Code subagent can be scoped to selected MCP servers. Apply least privilege rather than inheriting every integration. If a server is missing, follow `.aaop/policies/mcp-and-tools.md` rather than guessing an install command.

## Important context behavior

Treat subagents as isolated contexts. Pass the task, required project constraints, expected outputs, and acceptance evidence explicitly. Do not assume they inherit the parent conversation's full working context.
