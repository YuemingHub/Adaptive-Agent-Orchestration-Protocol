# AAOP Bootstrap

This repository uses the Adaptive Agent Orchestration Protocol (AAOP).

## Mandatory startup

For any non-trivial developer request:

1. if this is an installed AAOP package and integrity is uncertain, run `python .aaop/tools/health.py . --json` before trusting or repairing local AAOP-managed files; in the AAOP source repository, `source-tree` is expected;
2. read `.aaop/ORCHESTRATOR.md`;
3. use `.aaop/skills/developer-intake/SKILL.md` to understand the user's situation;
4. select one primary route from `.aaop/registries/routes.json`;
5. load `.aaop/skills/route-execution/SKILL.md` and only the current `.aaop/routes/<route-id>.json` capability pack;
6. establish the relevant current baseline/source authority before trusting historical issues, branches, PRs, status files, external reports, or prior AI conclusions;
7. for greenfield ideas, separate observable outcome from proposed technology vocabulary before architecture;
8. for review requests, define the decision and keep the task read-only unless mutation is explicitly requested;
9. satisfy route capabilities with the current host/repository before considering any new provider;
10. when blocked, classify the blocker before calling it a technical capability gap.

The user should be able to speak in ordinary language. Do not require them to choose a workflow, Agent type, Skill, MCP server, runtime, provider, framework, database, or orchestration architecture.

## Operating rules

1. **Situation before machinery.** Determine whether this is an idea, repo recovery, bug, feature, understanding/review, or release/operations problem before choosing tools/agents.
2. **Read before asking.** If workspace/repo/log/test/issue/deployment evidence can answer a question, inspect it instead of making the user restate it.
3. **Observe AAOP drift before repair.** Installation health is a read-only baseline comparison, not proof of latest version or cryptographic trust. `drifted`/`incomplete` is evidence to review, not authorization to overwrite; repair only from a trusted AAOP source when intended.
4. **Idea: outcome before architecture.** Define one actor, situation, observable result, first material assumption, and smallest evidence-bearing slice before platform architecture.
5. **Solution vocabulary is not automatically requirement.** Agent, MCP, RAG, vector DB, graph, memory, and similar terms are candidate solutions unless explicitly established as constraints.
6. **Do not outsource stack choice to beginners.** Ask only for genuinely user-owned product decisions; derive technical choices later from evidence and constraints.
7. **First slice must buy learning.** Scaffolding, diagrams, or a large generated codebase are not first-proof evidence unless they test a material product/execution assumption.
8. **Review: decision before coverage.** Scope review to the decision and usage context; do not substitute an exhaustive repository summary.
9. **Current source before review conclusion.** Verify material issue/advisory/report claims against current source/status when practical. Separate verified facts, external claims, inference, assumptions, and unknowns.
10. **Risk is contextual.** Tie severity/recommendation to actual exposure, permissions, and deployment context rather than copying labels.
11. **Review is read-only by default.** A finding does not authorize code/config/PR/issue/upstream mutation. Re-route only when implementation is explicitly requested.
12. **Current truth before stale detail.** A merged/newest/detailed artifact is not automatically authoritative. Respect project-declared source roles and freshness; old PRs/issues are historical evidence until reconciled with the current baseline.
13. **Preserve material conflicts.** When source authority/freshness cannot justify a winner, keep the conflict/unknown explicit instead of silently rewriting history.
14. **One primary route.** For mixed requests, choose the route that unlocks the most immediate outcome and queue secondary intents.
15. **One current Route Capability Pack.** Load only the current route pack unless evidence requires comparison or rerouting. Apply matching `pressure_guards` as invariants.
16. **Packs are capability maps, not workflow engines.** Use stages/evidence/exit conditions as engineering guidance; do not manufacture documents or ceremony.
17. **Capabilities before providers or roles.** Check host-native ability, repository tests/scripts/libraries, Skills, tools/MCP, and existing runtimes before adding anything.
18. **Blocker ≠ capability gap.** Network/environment limits, missing authorization/credentials, unavailable external systems, missing evidence, unresolved product decisions, or unverified solution vocabulary do not directly justify installing another provider. Preserve unknown state and state the smallest legitimate unblock.
19. **Provider candidate ≠ dependency.** A provider named in a route pack matters only when its escalation condition is true and a genuine technical capability gap remains.
20. **Provider adoption debt must be rechecked, not memorized as a verdict.** If a selected Recipe has an applicable `adoption_review`, verify current upstream and actual context before consequential adoption.
21. **Minimum provider surface.** Prefer one narrow surface over a provider's entire ecosystem.
22. **Community catalog ≠ trust.** Review source, publisher, scripts/hooks, permissions, credentials/data egress, maintenance, and rollback before adoption.
23. **Minimum sufficient team.** Do not create agents for ceremony. Split only for context isolation, specialization, independent review, permission boundaries, or safe parallelism.
24. **Autonomy is risk-based.** Automatically perform low-risk reversible work inside the requested action class. Ask only for material product choices, unavailable user-only information, credentials, cost, high-impact writes, or irreversible actions.
25. **Never request secrets in chat when a safer host-supported secret mechanism exists.** Never commit secrets.
26. **Verification is mandatory.** Prove the route outcome and separately prove that any newly added provider closed the gap that justified it.
27. **No fabricated completion.** A safely blocked task is not complete; report the blocker, unknowns, and exact unblock without widening permissions.
28. **Re-route from evidence.** Change route when evidence changes the problem instead of forcing the original classification.
29. **Graceful degradation.** If native subagents/teams are unavailable, preserve responsibility boundaries with sequential task contexts.
30. **User is not the scheduler.** Do not repeatedly ask “continue?” for ordinary next steps.
31. **Outcome over activity.** Optimize for intended result, learning value, reliability, and explainability—not agent count, framework count, files, commits, or code volume.

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
