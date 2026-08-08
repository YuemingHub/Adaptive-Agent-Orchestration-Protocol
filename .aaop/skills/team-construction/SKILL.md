---
name: team-construction
description: Build the minimum sufficient main-agent/subagent ownership structure from a capability matrix. Use when work may benefit from specialization, context isolation, independent review, parallel execution, or distinct permissions.
license: Apache-2.0
---

# Team Construction

## Goal

Assign ownership only after required capabilities and providers are known.

## Default

Start from **one agent**. Add another owner only when separation has a measurable benefit.

## Split criteria

Create a separate subagent/task owner when at least one applies:

- specialist knowledge/context is materially different;
- exploration would consume excessive main-context space;
- a workstream is independent and safe to parallelize;
- independent adversarial review would improve reliability;
- permission/tool access should be narrower than the main agent's;
- implementation isolation (for example a worktree) reduces collision risk.

Prefer an agent **team** over isolated subagents only when peers need direct coordination, shared task state, or mutual challenge. Otherwise subagents returning summaries are simpler.

## Merge criteria

Keep capabilities under one owner when:

- they share the same context and tools;
- handoff overhead exceeds specialization benefit;
- tasks must edit the same state sequentially;
- the task is small enough for a single coherent context;
- the host does not support isolation and simulation would add no value.

## Owner contract

For each owner define:

- `id` — stable local identifier;
- `role` — responsibility, not status title;
- `objective` — measurable result;
- `responsibilities` — bounded scope;
- `inputs` — context/artifacts required;
- `outputs` — artifacts/evidence returned;
- `skills` — only necessary reusable workflows;
- `tools` — least-privilege concrete access;
- `dependencies` — upstream owners/tasks;
- `completion_criteria` — evidence required before handoff.

Use `.aaop/schemas/team-plan.schema.json` when serializing.

## Reviewer separation

For consequential work, prefer a reviewer context that did not implement the change. The reviewer checks:

- user outcome, not merely spec compliance;
- governing project principles;
- regression and boundary conditions;
- security/privacy implications;
- unnecessary complexity;
- whether tests/evidence actually prove the claim.

## Host degradation

If native subagents/teams are unavailable:

1. keep the ownership plan;
2. execute owners as sequential isolated roles in the main agent;
3. explicitly reset the role objective and evidence expectations at each boundary;
4. preserve independent review by reviewing from the acceptance criteria rather than the implementation narrative.

Lack of native multi-agent capability is never, by itself, a reason to ask the user to switch tools.
