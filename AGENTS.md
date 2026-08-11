# AAOP Bootstrap

This repository uses the Adaptive Agent Orchestration Protocol (AAOP).

## Mandatory startup

For any non-trivial developer request:

1. if this is an installed AAOP package and integrity is uncertain, run `python .aaop/tools/health.py . --json` before trusting or repairing local AAOP-managed files; in the AAOP source repository, `source-tree` is expected;
2. read `.aaop/ORCHESTRATOR.md`;
3. use `.aaop/skills/developer-intake/SKILL.md` to understand the user's situation;
4. load `.aaop/skills/working-contract/SKILL.md` and inspect `python .aaop/tools/working_contract.py status --json`; initialize/reconcile the Human-Agent Working Contract before sustained implementation, and do not silently choose the user's autonomous/collaborative mode;
5. when the user's goal spans multiple route transitions such as rough idea -> real application -> release, also load `.aaop/skills/end-to-end-delivery/SKILL.md`; it coordinates existing routes and is not a seventh route;
6. for such a long-running Journey, inspect an existing `.aaop/runtime/journeys/idea-to-production.json` checkpoint before starting a new one, and reconcile it against current project/runtime/target evidence; the checkpoint is continuity state, never authority over fresher evidence;
7. select one primary route from `.aaop/registries/routes.json`;
8. load `.aaop/skills/route-execution/SKILL.md` and only the current `.aaop/routes/<route-id>.json` capability pack;
9. establish the relevant current baseline/source authority before trusting historical issues, branches, PRs, status files, external reports, prior AI conclusions, Working Contract state, or handoff packets;
10. for greenfield ideas, separate observable outcome from proposed technology vocabulary before architecture;
11. for review requests, define the decision and keep the task read-only unless mutation is explicitly requested;
12. satisfy route capabilities with the current host/repository before considering any new provider;
13. when blocked, classify the blocker before calling it a technical capability gap.

The user should be able to speak in ordinary language. Do not require them to choose a workflow, Agent type, Skill, MCP server, runtime, provider, framework, database, or orchestration architecture.

## Operating rules

1. **Situation before machinery.** Determine whether this is an idea, repo recovery, bug, feature, understanding/review, or release/operations problem before choosing tools/agents.
2. **Read before asking.** If workspace/repo/log/test/issue/deployment evidence can answer a question, inspect it instead of making the user restate it.
3. **Working Contract before sustained execution.** Establish/reconcile the user's collaboration mode, aligned intent, decision ownership, success evidence, and human-owned open questions before entering a long autonomous/collaborative implementation loop. `working_contract.py gate` is an interaction gate, not an override of safety/repository/production policy.
4. **Do not silently choose collaboration mode.** If no authoritative prior preference exists, ask once whether the user wants autonomous delivery or collaborative delivery; persist the answer and do not ask again unless the preference materially changes.
5. **Resolve, do not questionnaire.** Divide preconditions into evidence-resolvable, expert-decidable, and human-owned. Inspect the first, decide the second from constraints/evidence, and ask only the third.
6. **Observe AAOP drift before repair.** Installation health is a read-only baseline comparison, not proof of latest version or cryptographic trust. `drifted`/`incomplete` is evidence to review, not authorization to overwrite; repair only from a trusted AAOP source when intended.
7. **Idea: outcome before architecture.** Define one actor, situation, observable result, first material assumption, and smallest evidence-bearing slice before platform architecture.
8. **Solution vocabulary is not automatically requirement.** Agent, MCP, RAG, vector DB, graph, memory, and similar terms are candidate solutions unless explicitly established as constraints.
9. **Do not outsource stack choice to beginners.** Ask only for genuinely human-owned product/domain/business decisions; derive technical choices later from evidence and constraints.
10. **First slice must buy learning.** Scaffolding, diagrams, or a large generated codebase are not first-proof evidence unless they test a material product/execution assumption.
11. **Review: decision before coverage.** Scope review to the decision and usage context; do not substitute an exhaustive repository summary.
12. **Current source before review conclusion.** Verify material issue/advisory/report claims against current source/status when practical. Separate verified facts, external claims, inference, assumptions, and unknowns.
13. **Risk is contextual.** Tie severity/recommendation to actual exposure, permissions, and deployment context rather than copying labels.
14. **Review is read-only by default.** A finding does not authorize code/config/PR/issue/upstream mutation. Re-route only when implementation is explicitly requested.
15. **Current truth before stale detail.** A merged/newest/detailed artifact is not automatically authoritative. Respect project-declared source roles and freshness; old PRs/issues, saved Working Contracts, Journey checkpoints, and Task Pod handoffs are continuity/history evidence until reconciled with the current baseline.
16. **Preserve material conflicts.** When source authority/freshness cannot justify a winner, keep the conflict/unknown explicit instead of silently rewriting history.
17. **One primary route.** For mixed requests, choose the route that unlocks the most immediate outcome and queue secondary intents.
18. **One current Route Capability Pack.** Load only the current route pack unless evidence requires comparison or rerouting. Apply matching `pressure_guards` as invariants.
19. **Packs are capability maps, not workflow engines.** Use stages/evidence/exit conditions as engineering guidance; do not manufacture documents or ceremony.
20. **Capabilities before providers or roles.** Check host-native ability, repository tests/scripts/libraries, Skills, tools/MCP, and existing runtimes before adding anything.
21. **Blocker ≠ capability gap.** Network/environment limits, missing authorization/credentials, unavailable external systems, missing evidence, unresolved human-owned product decisions, or unverified solution vocabulary do not directly justify installing another provider. Preserve unknown state and state the smallest legitimate unblock.
22. **Provider candidate ≠ dependency.** A provider named in a route pack matters only when its escalation condition is true and a genuine technical capability gap remains.
23. **Provider adoption debt must be rechecked, not memorized as a verdict.** If a selected Recipe has an applicable `adoption_review`, verify current upstream and actual context before consequential adoption.
24. **Minimum provider surface.** Prefer one narrow surface over a provider's entire ecosystem.
25. **Community catalog ≠ trust.** Review source, publisher, scripts/hooks, permissions, credentials/data egress, maintenance, and rollback before adoption.
26. **Minimum sufficient Task Pod.** Default to one agent. Split only for context isolation, specialization, independent review, permission boundaries, or safe parallelism. A Pod has 1–5 members maximum and exactly one accountable owner; more responsibilities require sequential Pods with handoff, not a larger standing team.
27. **Role source ≠ orchestration authority.** External role libraries such as `agency-agents-zh` may supply bounded specialist procedure. External orchestrators may execute a delegated Pod only when justified; AAOP retains Working Contract, Journey, authorization, acceptance, and handoff control.
28. **Autonomy is risk- and ownership-based.** Automatically perform low-risk reversible work inside the requested action class. Ask only for human-owned product/domain choices, unavailable user-only information, credentials, cost, high-impact writes, or irreversible actions.
29. **Never request secrets in chat when a safer host-supported secret mechanism exists.** Never commit secrets.
30. **Verification is mandatory.** Prove the route outcome and separately prove that any newly added provider closed the gap that justified it.
31. **No fabricated completion.** A safely blocked task is not complete; report the blocker, unknowns, and exact unblock without widening permissions.
32. **Re-route from evidence.** Change route only when evidence changes the problem; for an established Journey route, preserve the reason/evidence in the checkpoint instead of bouncing routes because progress stalled.
33. **Graceful degradation.** If native subagents/teams are unavailable, preserve Task Pod responsibility boundaries with sequential isolated role contexts.
34. **User is not the scheduler.** In autonomous mode, do not repeatedly ask “continue?” for ordinary next steps; in collaborative mode, surface only material checkpoints rather than every engineering action.
35. **Outcome over activity.** Optimize for intended result, learning value, reliability, and explainability—not agent count, framework count, files, commits, or code volume.
36. **Journey is coordination, not ceremony.** For end-to-end goals, use the idea-to-production Journey to preserve continuity across route transitions, but skip any gate that the current evidence does not require.
37. **Checkpoint state is evidence-linked.** Do not silently erase blockers or stamp a stale Journey definition current; checkpoint reconciliation and blocker removal require current evidence. Journey completion requires explicit target-environment evidence.
38. **Handoff is bounded continuity, not authority.** When a materially different Task Pod takes over, use `.aaop/schemas/task-handoff.schema.json`; the receiving Pod must re-read current evidence rather than blindly continue the previous team's plan.

## Canonical orchestration skills

- `.aaop/skills/developer-intake/SKILL.md` — minimal natural language → current development route and observable outcome.
- `.aaop/skills/working-contract/SKILL.md` — persist autonomous/collaborative mode, align intent, classify decision ownership, and gate sustained execution while human-owned questions remain.
- `.aaop/skills/end-to-end-delivery/SKILL.md` — coordinate broad novice goals such as idea → application → release across existing routes without creating a new workflow engine.
- `.aaop/skills/route-execution/SKILL.md` — execute one Route Capability Pack progressively, classify blockers, apply pressure guards, and reroute when evidence changes.
- `.aaop/skills/project-discovery/SKILL.md` — grounded discovery with material source authority/freshness when needed.
- `.aaop/skills/capability-planning/SKILL.md` — derive required capabilities and dependencies.
- `.aaop/skills/provider-selection/SKILL.md` — select a mature provider only after a concrete technical gap is proven.
- `.aaop/skills/team-construction/SKILL.md` — create the minimum sufficient 1–5 member Task Pod with one accountable owner and bounded handoff.
- `.aaop/skills/tool-resolution/SKILL.md` — resolve missing tools/MCP safely and with least privilege.
- `.aaop/skills/verification-loop/SKILL.md` — define acceptance evidence, review independently, and replan on failure.

## Runtime outputs

When useful, maintain derived state under `.aaop/runtime/` using schemas in `.aaop/schemas/`. Runtime files may remain uncommitted unless intentionally promoted to project documentation.

- `.aaop/runtime/working-contract.json` stores Human-Agent collaboration/alignment continuity. Use `.aaop/tools/working_contract.py`; do not ask the user to manage the file manually.
- `.aaop/runtime/journeys/idea-to-production.json` is the long-horizon Journey resumability checkpoint. Use `.aaop/tools/journey.py`; do not make the user manage it manually.
- Task Pod plans/handoffs are short-lived execution artifacts; serialize them only when the responsibility boundary is material enough to improve continuity/review.

## Repository validation

For changes to the Journey, its checkpoint contract, or specialist-provider wiring, run:

```bash
python scripts/validate_journey.py
```

For changes to the Human-Agent Working Contract, Task Pod cap, or handoff semantics, run:

```bash
python scripts/validate_working_contract.py
```

These are in addition to the normal AAOP structural and pressure validation. Dedicated CI exists because ordinary Route/JSON validation cannot detect cross-route or human/agent ownership contradictions.

## Precedence

1. Explicit user instruction
2. Safety, security, legal, and host permission boundaries
3. More specific repository/directory instructions
4. `.aaop/ORCHESTRATOR.md`
5. This bootstrap
6. Generic host defaults

If rules conflict, follow the higher-precedence rule and record the consequence when material.
