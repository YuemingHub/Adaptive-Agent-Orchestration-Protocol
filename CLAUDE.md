# AAOP for Claude Code

This project is governed by the Adaptive Agent Orchestration Protocol.

Before substantive developer work, read:

1. `AGENTS.md`
2. if this is an installed AAOP package and integrity is uncertain, run `python .aaop/tools/health.py . --json`; `source-tree` is expected inside the AAOP source repository
3. `.aaop/ORCHESTRATOR.md`
4. `.aaop/skills/developer-intake/SKILL.md`
5. after routing, `.aaop/skills/route-execution/SKILL.md` and only the current `.aaop/routes/<route-id>.json`
6. other relevant `.aaop/skills/*/SKILL.md` only as the route requires them
7. `adapters/claude-code.md` when native Claude Code subagents, skills, MCP, or permissions are involved

Accept ordinary developer language. Inspect the workspace/repository before asking the user for technical facts already present in project evidence.

Installation health is a read-only local baseline comparison. It does not prove that AAOP is the latest upstream release and it is not a tamper-proof security root. If it reports `drifted` or `incomplete`, review the listed differences before any canonical repair; do not silently overwrite local AAOP-managed changes.

For greenfield ideas, do not turn Agent/MCP/RAG/vector DB/graph/memory or other early solution vocabulary into architecture requirements by default. Establish the user-visible outcome and an evidence-bearing first slice before selecting the technical shape. Do not make a non-technical user choose a stack Claude Code can derive later.

For review/adoption/audit requests, define the decision first, verify material external claims against current source/status when practical, separate fact from inference/unknown, contextualize risk to the usage environment, and remain read-only unless implementation is explicitly requested.

Prefer Claude Code/native project capability first. A provider candidate in a Route Capability Pack is not a dependency. Prove the capability gap before adding a Skill, MCP server, development harness, or external runtime, and select only the minimum provider surface that closes the gap. If a selected Recipe has an applicable `adoption_review`, re-check it against current upstream and actual context instead of treating it as a permanent provider verdict.

Do not create subagents merely because the host supports them. Derive required capabilities first, then use subagents when context isolation, specialization, independent review, permission boundaries, or safe parallelism provides concrete value.

When native project Skills are desired, follow `adapters/claude-code.md` to install or mirror canonical AAOP Skills into `.claude/skills/` without changing their meaning.

For external MCP/tool access, apply `.aaop/policies/mcp-and-tools.md`. Prefer already-connected capabilities and least privilege. Treat community catalogs as discovery rather than trust. Never commit credentials.
