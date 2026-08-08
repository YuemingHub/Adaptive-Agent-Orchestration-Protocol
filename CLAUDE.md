# AAOP for Claude Code

This project is governed by the Adaptive Agent Orchestration Protocol.

Before substantive work, read:

1. `AGENTS.md`
2. `.aaop/ORCHESTRATOR.md`
3. the relevant Skill(s) under `.aaop/skills/`
4. `adapters/claude-code.md` when native Claude Code subagents, skills, MCP, or permissions are involved

Do not create subagents merely because the host supports them. Derive required capabilities first, then use subagents when context isolation, specialization, independent review, or parallelism provides a concrete benefit.

When native project Skills are desired, follow `adapters/claude-code.md` to install or mirror the canonical AAOP Skills into `.claude/skills/` without changing their meaning.

For external MCP access, apply `.aaop/policies/mcp-and-tools.md`. Prefer already-connected capabilities and least privilege. Never commit credentials.
