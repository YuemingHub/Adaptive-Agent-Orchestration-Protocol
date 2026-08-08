# AAOP Bootstrap

This repository uses the Adaptive Agent Orchestration Protocol (AAOP).

## Mandatory startup

For any non-trivial user request, read `.aaop/ORCHESTRATOR.md` before making substantive changes.

Do not begin by inventing a fixed team. First understand the environment, project, requested outcome, constraints, and required capabilities.

## Operating rules

1. **Project before plan.** Inspect relevant repository instructions, architecture, code, tests, CI, deployment, issues/roadmap, and recent history before changing a project.
2. **Capabilities before roles.** Derive what abilities are required, then decide whether one agent or multiple agents should own them.
3. **Minimum sufficient team.** Do not create agents for ceremony. Split only for context isolation, meaningful specialization, independent review, or safe parallelism.
4. **Skill ≠ Agent ≠ Tool.** Skills encode repeatable know-how. Agents own responsibilities. Tools/MCP provide access to real systems.
5. **Reuse before install.** Prefer current native tools, existing Skills, repository scripts, and connected MCP before adding dependencies or external servers.
6. **Autonomy is risk-based.** Automatically perform low-risk, reversible work. Ask only for material product choices, unavailable user-only information, credentials, cost, high-impact external writes, or irreversible actions.
7. **Never request secrets in chat when a safer host-supported secret mechanism exists.** Never commit secrets.
8. **Verification is mandatory.** Define evidence that proves the requested outcome, execute the relevant checks, and report limitations precisely.
9. **Replan from evidence.** If assumptions fail, tests fail, tools disappear, or review finds a direction error, diagnose and change the plan rather than repeating the same attempt.
10. **Graceful degradation.** If native subagents/teams are unavailable, simulate role isolation using sequential task contexts. Lack of multi-agent support is not a blocker.
11. **User is not the scheduler.** Do not repeatedly ask “continue?” for ordinary next steps. Continue until the goal is complete or a real decision/permission boundary is reached.
12. **Outcome over activity.** Optimize for the user's intended result, reliability, and explainability—not number of agents, files, commits, or lines of code.

## Canonical orchestration skills

Use these when relevant:

- `.aaop/skills/project-discovery/SKILL.md` — build a grounded environment/project profile before planning.
- `.aaop/skills/capability-planning/SKILL.md` — convert the requested outcome into required capabilities and dependencies.
- `.aaop/skills/team-construction/SKILL.md` — create the minimum sufficient ownership structure.
- `.aaop/skills/tool-resolution/SKILL.md` — resolve missing tools/MCP safely and with least privilege.
- `.aaop/skills/verification-loop/SKILL.md` — define acceptance evidence, review independently, and replan on failure.

## Runtime outputs

When useful, maintain derived state under `.aaop/runtime/` using the schemas in `.aaop/schemas/`. Runtime files may remain uncommitted unless they are intentionally part of project documentation.

## Precedence

1. Explicit user instruction
2. Safety, security, legal, and host permission boundaries
3. More specific repository/directory instructions
4. `.aaop/ORCHESTRATOR.md`
5. This bootstrap
6. Generic host defaults

If rules conflict, follow the higher-precedence rule and record the consequence when material.
