# Cursor Adapter

Purpose: map AAOP onto Cursor rules, Agent/CLI behavior, and MCP without making Cursor-specific configuration normative.

## Bootstrap

Cursor supports root `AGENTS.md` as project instructions, and Cursor CLI also reads root `AGENTS.md` / `CLAUDE.md`. AAOP therefore works in direct protocol mode without a generated Cursor rule.

For stronger Cursor-native integration, create focused project rules under `.cursor/rules/` that point back to the canonical AAOP files rather than copying the whole protocol into a large rule.

Example project rule:

```md
---
description: Apply AAOP orchestration for non-trivial multi-step project tasks
globs:
alwaysApply: true
---
Read `AGENTS.md` and `.aaop/ORCHESTRATOR.md` before substantive multi-step work. Load only the relevant `.aaop/skills/*/SKILL.md` procedures.
```

Keep Cursor rules focused and composable. Do not duplicate the entire orchestrator in `.cursor/rules`.

## Agents / parallelism

Cursor host capabilities can vary by IDE/CLI version. Discover what the current environment exposes. If there is no native subagent primitive suitable for AAOP's team plan, use sequential role isolation and/or separate background sessions/worktrees when available.

Do not make multi-agent support a prerequisite.

## MCP

Project MCP configuration may be provided through `.cursor/mcp.json`; global configuration may also exist outside the repository.

AAOP does **not** commit a populated MCP config because required services are project-specific and credentials must not be embedded. When a capability gap requires MCP:

1. prefer an already configured server;
2. evaluate first-party/official sources;
3. create only the minimal `mcpServers` entry required;
4. reference credentials through environment variables or OAuth rather than literal secrets;
5. verify the server/tools are visible before depending on them.

## Non-interactive automation

When Cursor Agent CLI is used non-interactively, remember that broader write autonomy increases the importance of AAOP's explicit verification and external-side-effect policy. A non-interactive host mode does not override `.aaop/policies/autonomy.md`.
