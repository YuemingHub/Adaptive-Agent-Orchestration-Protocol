# AAOP for Claude Code

This project is governed by the Adaptive Agent Orchestration Protocol.

Before substantive developer work, read:

1. `AGENTS.md`
2. `.aaop/ORCHESTRATOR.md`
3. `.aaop/skills/developer-intake/SKILL.md`
4. after routing, `.aaop/skills/route-execution/SKILL.md` and only the current `.aaop/routes/<route-id>.json`
5. other relevant `.aaop/skills/*/SKILL.md` only as the route requires them
6. `adapters/claude-code.md` when native Claude Code subagents, skills, MCP, or permissions are involved

Accept ordinary developer language. Inspect the workspace/repository before asking the user for technical facts already present in project evidence.

Prefer Claude Code/native project capability first. A provider candidate in a Route Capability Pack is not a dependency. Prove the capability gap before adding a Skill, MCP server, development harness, or external runtime, and select only the minimum provider surface that closes the gap.

Do not create subagents merely because the host supports them. Derive required capabilities first, then use subagents when context isolation, specialization, independent review, permission boundaries, or safe parallelism provides concrete value.

When native project Skills are desired, follow `adapters/claude-code.md` to install or mirror canonical AAOP Skills into `.claude/skills/` without changing their meaning.

For external MCP/tool access, apply `.aaop/policies/mcp-and-tools.md`. Prefer already-connected capabilities and least privilege. Treat community catalogs as discovery rather than trust. Never commit credentials.
