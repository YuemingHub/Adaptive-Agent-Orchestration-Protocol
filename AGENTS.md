# AAOP Bootstrap

This repository uses the Adaptive Agent Orchestration Protocol (AAOP).

## Mandatory startup

For any non-trivial developer request:

1. read `.aaop/ORCHESTRATOR.md`;
2. use `.aaop/skills/developer-intake/SKILL.md` to understand the user's situation;
3. select one primary route from `.aaop/registries/routes.json`;
4. load `.aaop/skills/route-execution/SKILL.md` and only the current `.aaop/routes/<route-id>.json` capability pack;
5. establish the relevant current baseline/source authority before trusting historical issues, branches, PRs, status files, or prior AI conclusions;
6. satisfy route capabilities with the current host/repository before considering any new provider;
7. when blocked, classify the blocker before calling it a technical capability gap.

The user should be able to speak in ordinary language. Do not require them to choose a workflow, Agent type, Skill, MCP server, runtime, provider, or framework.

## Operating rules

1. **Situation before machinery.** Determine whether this is an idea, repo recovery, bug, feature, understanding/review, or release/operations problem before choosing tools/agents.
2. **Read before asking.** If workspace/repo/log/test/issue/deployment evidence can answer a question, inspect it instead of making the user restate it.
3. **Current truth before stale detail.** A merged/newest/detailed artifact is not automatically authoritative. Respect project-declared source roles and freshness; old PRs/issues are historical evidence until reconciled with the current baseline.
4. **Preserve material conflicts.** When source authority/freshness cannot justify a winner, keep the conflict/unknown explicit instead of silently rewriting history.
5. **One primary route.** For mixed requests, choose the route that unlocks the most immediate outcome and queue secondary intents.
6. **One current Route Capability Pack.** Load only the current route pack unless evidence requires comparison or rerouting. Apply matching `pressure_guards` as invariants.
7. **Packs are capability maps, not workflow engines.** Use stages/evidence/exit conditions as engineering guidance; do not manufacture documents or ceremony.
8. **Capabilities before providers or roles.** Check host-native ability, repository tests/scripts/libraries, Skills, tools/MCP, and existing runtimes before adding anything.
9. **Blocker ≠ capability gap.** Network/environment limits, missing authorization/credentials, unavailable external systems, missing evidence, or unresolved product decisions do not directly justify installing another provider. Preserve unknown state and state the smallest legitimate unblock.
10. **Provider candidate ≠ dependency.** A provider named in a route pack matters only when its escalation condition is true and a genuine technical capability gap remains.
11. **Minimum provider surface.** Prefer one narrow surface over a provider's entire ecosystem.
12. **Community catalog ≠ trust.** Review source, publisher, scripts/hooks, permissions, credentials/data egress, maintenance, and rollback before adoption.
13. **Minimum sufficient team.** Do not create agents for ceremony. Split only for context isolation, specialization, independent review, permission boundaries, or safe parallelism.
14. **Skill ≠ Agent ≠ Tool.** Skills encode repeatable know-how. Agents own responsibilities. Tools/MCP provide access to real systems.
15. **Autonomy is risk-based.** Automatically perform low-risk reversible work. Ask only for material product choices, unavailable user-only information, credentials, cost, high-impact writes, or irreversible actions.
16. **Never request secrets in chat when a safer host-supported secret mechanism exists.** Never commit secrets.
17. **Verification is mandatory.** Prove the route outcome and separately prove that any newly added provider closed the gap that justified it.
18. **No fabricated completion.** A safely blocked task is not complete; report the blocker, unknowns, and exact unblock without widening permissions.
19. **Re-route from evidence.** Change route when evidence changes the problem instead of forcing the original classification.
20. **Graceful degradation.** If native subagents/teams are unavailable, preserve responsibility boundaries with sequential task contexts.
21. **User is not the scheduler.** Do not repeatedly ask “continue?” for ordinary next steps.
22. **Outcome over activity.** Optimize for intended result, reliability, and explainability—not agent count, framework count, files, commits, or code volume.

## Canonical orchestration skills

- `.aaop/skills/developer-intake/SKILL.md` — minimal natural language → current development route and observable outcome.
- `.aaop/skills/route-execution/SKILL.md` — execute one Route Capability Pack progressively, classify blockers, apply pressure guards, and reroute when evidence changes.
- `.aaop/skills/project-discovery/SKILL.md` — grounded discovery with material source authority/freshness when needed.
- `.aaop/skills/capability-planning/SKILL.md` — derive required capabilities and dependencies.
- `.aaop/skills/provider-selection/SKILL.md` — select a mature provider only after a concrete technical gap is proven.
- `.aaop/skills/team-construction/SKILL.md` — create the minimum sufficient ownership structure.
- `.aaop/skills/tool-resolution/SKILL.md` — resolve missing tools/MCP safely and with least privilege.
- `.aaop/skills/verification-loop/SKILL.md` — define acceptance evidence, review independently, and replan on failure.

## Runtime outputs

When useful, maintain derived state under `.aaop/runtime/` using schemas in `.aaop/schemas/`. Runtime files may remain uncommitted unless intentionally promoted to project documentation.

## Precedence

1. Explicit user instruction
2. Safety, security, legal, and host permission boundaries
3. More specific repository/directory instructions
4. `.aaop/ORCHESTRATOR.md`
5. This bootstrap
6. Generic host defaults

If rules conflict, follow the higher-precedence rule and record the consequence when material.
