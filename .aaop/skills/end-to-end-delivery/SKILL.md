---
name: end-to-end-delivery
description: Coordinate a non-technical or novice developer from a rough idea through a verified application release by sequencing existing AAOP routes. This is not a seventh route or a new workflow engine; use it when the user's goal spans multiple route transitions such as idea -> build -> iterate -> release.
---

# End-to-End Delivery Journey

Use this Skill when the user's desired outcome is broader than one engineering task: for example, “I have an idea; help me make it into a real app and get it online.”

This Skill does **not** replace AAOP routes. It coordinates them over time.

## Core contract

The user supplies goals, domain truth, material product decisions, credentials/authorization when needed, and production approval.

AAOP owns the engineering process:

- inspect before asking;
- infer the current route;
- choose the smallest evidence-bearing next step;
- make ordinary reversible engineering decisions autonomously;
- verify before claiming completion;
- reroute when evidence changes the problem;
- do not make a novice choose frameworks, databases, Agent topology, MCP servers, or deployment machinery unless a real user-owned constraint requires it.

The default experience is one natural-language surface. The user should be able to begin with:

> I want to build …

and continue without learning AAOP's internal vocabulary.

## Journey state machine

The canonical journey definition lives at `../../journeys/idea-to-production.json`.

The normal route sequence is:

```text
rough idea
  -> idea-to-build
  -> first real slice
  -> feature-change / bug-fix loops as evidence demands
  -> release candidate
  -> release-operations
  -> deployed + observed outcome
  -> next evidence-driven loop
```

`repo-recovery` may interrupt whenever the current repository cannot be trusted.
`understand-review` is used when a material decision must be made before mutation, not as ceremonial review after every change.

Do not force every project through every route.

## Gate 0 — Intake without a questionnaire

Load `../developer-intake/SKILL.md`.

Resolve, from the user's words and accessible evidence:

- who the first actor is;
- the concrete situation;
- the observable improvement;
- hard constraints versus preferences versus solution hypotheses;
- the riskiest assumption worth testing first.

Ask at most one concrete question at a time, and only when inspection cannot resolve an outcome-blocking user-owned fact.

Do not ask the user what stack to use.

## Gate 1 — First evidence-bearing slice

Enter `idea-to-build`.

Define a first slice that:

- serves one actor in one situation;
- has an observable acceptance path;
- explicitly excludes non-essential scope;
- reduces at least one material product or execution uncertainty;
- can be implemented with the minimum reversible technical shape.

A generated scaffold is not sufficient unless the scaffold itself tests a real uncertainty.

For novice usability, keep an internal task queue small. Prefer one current outcome and one next executable task over a large speculative roadmap.

## Gate 2 — Project/bootstrap readiness

Before implementation, determine what already exists.

- If there is no trustworthy implementation, create only the minimum project shape needed by the first slice.
- If an existing repository is contradictory or its baseline cannot be trusted, reroute to `repo-recovery`.
- Reuse repository-native scripts, tests, CI, deployment configuration, and host capabilities before adding tooling.
- Environment problems are blockers, not automatic reasons to install an agent runtime.

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
8. update the next decision from evidence.

Prefer project-declared validation commands. Where applicable, use the familiar sequence:

```text
format -> lint -> typecheck -> build -> tests -> runtime/acceptance check
```

Skip irrelevant steps; do not invent checks merely to satisfy ceremony.

This absorbs the useful core of `solo-dev-autopilot`'s dev-loop/test-runner/code-review practices without forcing its old fixed Skill topology.

## Gate 4 — Evidence-driven iteration

After the first slice is real, do not automatically expand the roadmap.

Use evidence to choose the next route:

- observed defect -> `bug-fix`;
- desired behavior change -> `feature-change`;
- contradictory/untrustworthy project state -> `repo-recovery`;
- decision-only request -> `understand-review`;
- deployment/release becomes the immediate blocker -> `release-operations`.

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

Enter `release-operations`.

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

## Gate 8 — Observe the actual outcome

A deployment event is not the finish line.

Verify the deployed behavior against the intended outcome using the strongest practical target evidence:

- version/revision identity;
- health/readiness;
- representative user path;
- logs/error signals;
- browser smoke check when material;
- data/migration result when material.

If target evidence is unavailable, preserve production state as unknown instead of promoting local/CI evidence into a production claim.

If failure thresholds are crossed, execute the prepared rollback when authorized, then reroute using the observed failure.

## Gate 9 — Learning loop

After a real use, release, failure, or near-miss:

- preserve the new evidence;
- distinguish product learning from engineering learning;
- promote a Pressure Guard only when the failure pattern is repeatable and route-relevant;
- update the next outcome rather than expanding process for its own sake.

The old `creating-forward` repository is historical lineage for requirement baseline, task/evidence discipline, authorization boundaries, and interruption recovery. It is archived and should not be installed as a second protocol beside AAOP.

## Beginner-facing interaction contract

The user should usually see:

- what we are trying to make true now;
- what was learned or changed;
- whether it is verified;
- what genuinely blocks progress;
- the one material decision/authorization they actually own, if any.

The user should **not** be asked to operate:

- route names;
- Agent counts;
- Skill selection;
- MCP/provider selection;
- branch choreography;
- CI mechanics;
- framework/database choice;
- release checklists that can be derived and executed by the system.

A novice is the product owner of intent, not the scheduler of the engineering machine.

## Completion criterion

The end-to-end journey is complete for the current release when:

- a real user-visible application slice is deployed to the intended target;
- the deployed target state is directly verified or explicitly marked unknown if evidence is blocked;
- the intended acceptance path is proven in the target context where practical;
- rollback/recovery status is known;
- material residual risks are visible;
- and the next product decision can be made from real evidence rather than speculative architecture.
