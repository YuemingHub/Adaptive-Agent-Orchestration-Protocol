---
name: end-to-end-delivery
description: Coordinate a non-technical or novice developer from a rough idea or partial implementation through a verified application release by sequencing existing AAOP routes. This is not a seventh route or a new workflow engine; use it when the user's goal spans multiple route transitions such as idea -> build -> iterate -> release.
---

# End-to-End Delivery Journey

Use this Skill when the user's desired outcome is broader than one engineering task: for example, “I have an idea; help me make it into a real app and get it online,” or “this partially built app needs to become a real released product.”

This Skill does **not** replace AAOP routes. It coordinates them over time.

## Core contract

The user supplies goals, domain truth, material product decisions, credentials/authorization when needed, and production approval.

AAOP owns the engineering process:

- inspect before asking;
- infer the **current** route from present evidence rather than Journey position;
- choose the smallest evidence-bearing next step;
- make ordinary reversible engineering decisions autonomously;
- verify before claiming completion;
- reroute only when evidence changes the problem;
- preserve resumable Journey checkpoints without treating them as current truth;
- do not make a novice choose frameworks, databases, Agent topology, MCP servers, or deployment machinery unless a real user-owned constraint requires it.

The default experience is one natural-language surface. The user should be able to begin with:

> I want to build …

and continue without learning AAOP's internal vocabulary.

## Canonical definition and checkpoint

The canonical Journey definition lives at `../../journeys/idea-to-production.json`.

For a long-running Journey, maintain a lightweight continuity checkpoint with:

```bash
python .aaop/tools/journey.py status idea-to-production --json
python .aaop/tools/journey.py start idea-to-production --goal "<long-horizon product outcome>" --route <current-route>
python .aaop/tools/journey.py checkpoint idea-to-production ...
```

The checkpoint lives under `.aaop/runtime/journeys/` and is preserved across AAOP upgrades. It records the original goal, current gate/route, evidence, blockers, route history, and next action.

**It is not a workflow engine or source of truth.** At the start of a new session, reconcile the saved checkpoint against current repository/runtime/target evidence and project instructions. If they disagree, current evidence wins and the checkpoint must be updated rather than forcing the old plan.

Do not overwrite an existing Journey checkpoint merely because a new conversation started.

## Journey shape

A common greenfield sequence is:

```text
rough idea
  -> idea-to-build
  -> first real slice
  -> feature-change / bug-fix loops as evidence demands
  -> release candidate
  -> release-operations
  -> deployed + directly verified target outcome
  -> next evidence-driven loop
```

But this is **not** a mandatory route order.

- An existing trustworthy implementation may start at `feature-change`, `bug-fix`, `understand-review`, or `release-operations`.
- `repo-recovery` may interrupt whenever the current repository cannot be trusted.
- `understand-review` is used when a material decision must be made before mutation, not as ceremonial review after every change.
- A Journey gate may be skipped when current evidence already proves its exit condition.

Do not force an existing project back through greenfield discovery simply because the long-horizon goal is “take it all the way online.”

## Gate 0 — Intake without a questionnaire

Load `../developer-intake/SKILL.md`.

Resolve, from the user's words and accessible evidence:

- who the first actor is;
- the concrete situation;
- the long-horizon observable improvement;
- hard constraints versus preferences versus solution hypotheses;
- the immediate problem/uncertainty that determines the **current route**.

Ask at most one concrete question at a time, and only when inspection cannot resolve an outcome-blocking user-owned fact.

Do not ask the user what stack to use.

After selecting the current route, create the Journey checkpoint if one does not already exist. If it exists, reconcile it instead of restarting the Journey.

## Gate 1 — First evidence-bearing slice, only when needed

Enter `idea-to-build` **only when there is no trustworthy existing slice from which to continue**.

Define a first slice that:

- serves one actor in one situation;
- has an observable acceptance path;
- explicitly excludes non-essential scope;
- reduces at least one material product or execution uncertainty;
- can be implemented with the minimum reversible technical shape.

A generated scaffold is not sufficient unless the scaffold itself tests a real uncertainty.

If an existing application already has a trustworthy usable slice, skip this gate and route from the actual current delta instead of pretending the project is greenfield.

For novice usability, keep the internal task queue small. Prefer one current outcome and one next executable task over a large speculative roadmap.

## Gate 2 — Project/bootstrap readiness

Before implementation, determine what already exists.

- If there is no trustworthy implementation, create only the minimum project shape needed by the first slice.
- If an existing repository is contradictory or its baseline cannot be trusted, reroute to `repo-recovery`.
- Reuse repository-native scripts, tests, CI, deployment configuration, and host capabilities before adding tooling.
- Environment problems are blockers, not automatic reasons to install an agent runtime.
- Reconcile the Journey checkpoint with the current project baseline before resuming mutation.

Historical source: the former `solo-dev-autopilot` environment-detect/env-setup/project-scaffold practices informed this gate, but AAOP keeps the decision at route/capability level rather than requiring a fixed scaffold workflow.

## Gate 3 — Implementation loop

For each coherent change:

1. re-read the current baseline and relevant project rules;
2. prove the current delta still exists;
3. implement the smallest coherent change;
4. run the strongest practical local verification;
5. classify failures before retrying;
6. stop repeated blind retries and re-diagnose when evidence is not changing;
7. inspect the diff for unrelated changes and sensitive data;
8. checkpoint meaningful new evidence and the next decision.

Prefer project-declared validation commands. Where applicable, use the familiar sequence:

```text
format -> lint -> typecheck -> build -> tests -> runtime/acceptance check
```

Skip irrelevant steps; do not invent checks merely to satisfy ceremony.

This absorbs the useful core of `solo-dev-autopilot`'s dev-loop/test-runner/code-review practices without forcing its old fixed Skill topology.

## Gate 4 — Evidence-driven iteration and anti-thrash

After the first slice is real, do not automatically expand the roadmap.

Use evidence to choose the next route:

- observed defect -> `bug-fix`;
- desired behavior change -> `feature-change`;
- contradictory/untrustworthy project state -> `repo-recovery`;
- decision-only request -> `understand-review`;
- deployment/release becomes the immediate blocker -> `release-operations`.

A route change must correspond to materially new evidence or a changed blocker classification. The checkpoint tool requires a reason and evidence when changing from one established route to another.

**Do not use rerouting as a substitute for diagnosis.** If the Journey begins bouncing between routes while the underlying evidence is unchanged, stop, classify the blocker, record it, and identify the smallest legitimate unblock condition.

The system should repeatedly ask internally:

> What is the smallest next change that materially improves the user's outcome or reduces the next important uncertainty?

## Gate 5 — Specialist capability only when justified

Default to one capable agent.

Only split responsibility when specialization, context isolation, safe parallel independence, adversarial review, or a permission boundary materially improves execution.

Before adding a specialist:

1. check the main agent's native ability;
2. check repository scripts/libraries/tests;
3. check existing Skills and host tools;
4. check already connected tools/providers;
5. identify the exact missing specialization.

`agent-bundles` is an optional curated specialist-agent source. It is **not** part of the default stack and must not be installed because “more agents sounds better.” Load its Integration Recipe only when a bounded specialist role is genuinely missing.

Agent-role prompts do not create missing APIs, tools, credentials, network access, or runtime capabilities.

## Gate 6 — Release-candidate proof

Do not equate “tests passed” with “ready for production.”

Before entering production execution, establish a release candidate with evidence appropriate to the project, such as:

- acceptance path works;
- relevant regression tests pass;
- build/type/lint gates pass where configured;
- CI state is known;
- no unintended diff or exposed secret is present;
- production configuration requirements are identified;
- migrations/data changes are understood;
- observability/health checks are sufficient for the blast radius;
- rollback/restore path exists before consequential writes.

Thresholds such as fixed coverage percentages are project policy, not universal AAOP law. Use the project's own risk and acceptance baseline.

This gate absorbs the durable lessons from `solo-dev-autopilot` production-preflight while removing project-specific hard-coded thresholds.

## Gate 7 — Production authorization and deployment

Enter `release-operations` when release/deployment is the current problem.

Before a consequential production write:

- identify the exact target environment;
- obtain direct target/runtime evidence where possible;
- know the current target revision/precondition;
- verify the authorized access path;
- define rollback/restore;
- revalidate the material target precondition immediately before the write;
- stop and reconcile if the target moved;
- require user authorization for production writes unless an already-established policy explicitly grants that authority.

Never bypass missing credentials, network restrictions, external dependency outages, or authorization by installing alternate providers or widening access.

Historical source: this preserves the core safety boundary from `solo-dev-autopilot` deploy-gate while using AAOP's risk-based autonomy policy rather than a separate permission system.

## Gate 8 — Observe the actual target outcome

A deployment event is not the finish line.

Verify the deployed behavior against the intended outcome using the strongest practical **target-environment** evidence:

- version/revision identity;
- health/readiness;
- representative user path;
- logs/error signals;
- browser smoke check when material;
- data/migration result when material.

Local Git state, local tests, or CI success cannot substitute for target evidence.

If target evidence is unavailable, preserve production state as unknown, checkpoint the exact blocker, and keep the Journey **blocked/not-complete**. Do not convert “unknown but probably deployed” into a completed release.

If failure thresholds are crossed, execute the prepared rollback when authorized, then reroute using the observed failure.

The Journey checkpoint may be marked `complete` only after direct target verification; `.aaop/tools/journey.py` enforces this invariant.

## Gate 9 — Learning loop

After a real use, release, failure, or near-miss:

- preserve the new evidence;
- distinguish product learning from engineering learning;
- promote a Pressure Guard only when the failure pattern is repeatable and route-relevant;
- update the next outcome rather than expanding process for its own sake.

The old `creating-forward` repository is historical lineage for requirement baseline, task/evidence discipline, authorization boundaries, and interruption recovery. Its interruption-recovery lesson is represented here by a persisted but non-authoritative Journey checkpoint. It remains archived and should not be installed as a second protocol beside AAOP.

## Beginner-facing interaction contract

The user should usually see:

- what we are trying to make true now;
- what was learned or changed;
- whether it is verified;
- what genuinely blocks progress;
- the one material decision/authorization they actually own, if any.

The user should **not** be asked to operate:

- route names;
- Journey checkpoint mechanics;
- Agent counts;
- Skill selection;
- MCP/provider selection;
- branch choreography;
- CI mechanics;
- framework/database choice;
- release checklists that can be derived and executed by the system.

A novice is the product owner of intent, not the scheduler of the engineering machine.

## Completion criterion

The end-to-end Journey is complete for the current release only when:

- a real user-visible application slice is deployed to the intended target;
- the deployed target revision/state is directly verified with target-environment evidence;
- the intended acceptance path is proven in the target context where practical;
- rollback/recovery status is known;
- material residual risks are visible;
- and the next product decision can be made from real evidence rather than speculative architecture.

A safely blocked Journey is a correct execution state, but it is **not complete**. If direct target verification cannot be obtained, record the blocker and exact unblock condition and stop short of completion.
