# Cursor Adapter

Purpose: map AAOP onto Cursor rules, Agent/CLI behavior, and MCP without making Cursor-specific configuration normative.

Host behavior last verified: **2026-08-08**

Official sources:

- https://docs.cursor.com/context/rules-for-ai
- https://docs.cursor.com/en/cli/using

## Bootstrap

Cursor supports root `AGENTS.md` as simple project instructions. Cursor CLI also reads root `AGENTS.md` **and** root `CLAUDE.md` alongside `.cursor/rules`.

AAOP therefore uses this host strategy:

- `AGENTS.md` = common cross-host bootstrap;
- `CLAUDE.md` = thin Claude-specific bridge only;
- no generated `.cursor/rules` file is required for baseline AAOP activation.

This matters because copying the full AAOP bootstrap into both root files causes duplicated persistent context in Cursor CLI. Keep the common instructions in `AGENTS.md` and the canonical policy/procedures under `.aaop/`.

For stronger Cursor-native integration, create focused project rules under `.cursor/rules/` only when the project truly needs Cursor-specific scoping. Point those rules back to canonical AAOP/project sources rather than copying the whole protocol.

Example project rule:

```md
---
description: Apply AAOP orchestration for non-trivial multi-step project tasks
globs:
alwaysApply: true
---
Read `AGENTS.md` and `.aaop/ORCHESTRATOR.md` before substantive multi-step work. Load only the relevant `.aaop/skills/*/SKILL.md` procedures.
```

Do not create an always-applied Cursor rule that merely duplicates root `AGENTS.md`.

## Agents / parallelism

Cursor host capabilities can vary by IDE/CLI version. Discover what the current environment exposes. If there is no native subagent primitive suitable for AAOP's ownership plan, use sequential role isolation and/or separate sessions/worktrees when available.

Do not make multi-agent support a prerequisite.

## MCP

Project MCP configuration may be provided through `.cursor/mcp.json`; global configuration may also exist outside the repository.

AAOP does **not** commit a populated MCP config because required services are project-specific and credentials must not be embedded. When a capability gap requires MCP:

1. prefer an already configured server;
2. evaluate first-party/official sources;
3. create only the minimal configuration required;
4. reference credentials through environment variables or OAuth rather than literal secrets;
5. verify the server/tools are visible before depending on them.

## Non-interactive automation

Cursor Agent CLI can run non-interactively. Broader write autonomy increases the importance of AAOP's verification and external-side-effect policy; a non-interactive host mode does not override `.aaop/policies/autonomy.md`.

## Conformance boundary

AAOP relies on Cursor's documented rules/project-instruction surfaces, not a proprietary AAOP Cursor plugin. If Cursor changes which root instruction files it loads, update this adapter and host-bootstrap conformance tests; do not add duplicated rule layers speculatively.
