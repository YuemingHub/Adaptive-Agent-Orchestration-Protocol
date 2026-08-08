# AAOP Bootstrap

This repository uses the Adaptive Agent Orchestration Protocol (AAOP).

## Mandatory startup

For any non-trivial developer request:

1. read `.aaop/ORCHESTRATOR.md`;
2. use `.aaop/skills/developer-intake/SKILL.md` to understand the user's situation before capability/provider planning;
3. route internally using `.aaop/registries/routes.json` when useful.

The user should be able to speak in ordinary language. Do not require them to choose a workflow, Agent type, Skill, MCP server, runtime, or framework.

Do not begin by inventing a fixed team. First understand the developer situation, available assets, desired observable outcome, environment/project evidence, constraints, and required capabilities.

## Operating rules

1. **Situation before machinery.** Determine whether this is an idea, repo recovery, bug, feature, understanding/review, or release/operations problem before choosing tools/agents.
2. **Read before asking.** If the workspace/repo/logs/issues can answer a question, inspect them instead of making the user restate the evidence.
3. **One primary route.** For mixed requests, choose the route that unlocks the user's most immediate outcome and queue secondary intents.
4. **Project before plan.** Inspect relevant repository instructions, architecture, code, tests, CI, deployment, issues/roadmap, and recent history before broad changes.
5. **Capabilities before roles.** Derive what abilities are required, then decide whether one agent or multiple agents should own them.
6. **Minimum sufficient team.** Do not create agents for ceremony. Split only for context isolation, meaningful specialization, independent review, permission boundaries, or safe parallelism.
7. **Skill ≠ Agent ≠ Tool.** Skills encode repeatable know-how. Agents own responsibilities. Tools/MCP provide access to real systems.
8. **Reuse before install.** Prefer current native tools, existing Skills, repository scripts, and connected MCP before adding dependencies or external servers.
9. **Autonomy is risk-based.** Automatically perform low-risk, reversible work. Ask only for material product choices, unavailable user-only information, credentials, cost, high-impact external writes, or irreversible actions.
10. **Never request secrets in chat when a safer host-supported secret mechanism exists.** Never commit secrets.
11. **Verification is mandatory.** Define evidence that proves the requested outcome, execute relevant checks, and report limitations precisely.
12. **Replan from evidence.** If assumptions fail, tests fail, tools disappear, or review finds a direction error, diagnose and change the route/plan rather than repeating the same attempt.
13. **Graceful degradation.** If native subagents/teams are unavailable, preserve responsibility boundaries with sequential task contexts.
14. **User is not the scheduler.** Do not repeatedly ask “continue?” for ordinary next steps. Continue until the goal is complete or a real decision/permission boundary is reached.
15. **Outcome over activity.** Optimize for the user's intended result, reliability, and explainability—not number of agents, files, commits, or lines of code.

## Canonical orchestration skills

Use these when relevant:

- `.aaop/skills/developer-intake/SKILL.md` — turn minimal natural language into the correct development route and provisional observable outcome.
- `.aaop/skills/project-discovery/SKILL.md` — build a grounded environment/project profile before broad planning.
- `.aaop/skills/capability-planning/SKILL.md` — convert the routed outcome into required capabilities and dependencies.
- `.aaop/skills/provider-selection/SKILL.md` — add a mature provider only after a concrete capability gap is proven.
- `.aaop/skills/team-construction/SKILL.md` — create the minimum sufficient ownership structure.
- `.aaop/skills/tool-resolution/SKILL.md` — resolve missing tools/MCP safely and with least privilege.
- `.aaop/skills/verification-loop/SKILL.md` — define acceptance evidence, review independently, and replan on failure.

## Runtime outputs

When useful, maintain derived state under `.aaop/runtime/` using the schemas in `.aaop/schemas/`, including `intake-envelope.json`. Runtime files may remain uncommitted unless intentionally promoted to project documentation.

## Precedence

1. Explicit user instruction
2. Safety, security, legal, and host permission boundaries
3. More specific repository/directory instructions
4. `.aaop/ORCHESTRATOR.md`
5. This bootstrap
6. Generic host defaults

If rules conflict, follow the higher-precedence rule and record the consequence when material.
