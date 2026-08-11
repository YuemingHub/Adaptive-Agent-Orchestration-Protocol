---
name: team-construction
description: Build the minimum sufficient 1-5 member Task Pod from the aligned outcome and capability gaps. Use only when specialization, context isolation, independent review, safe parallelism, or permission boundaries create measurable value; otherwise keep one accountable agent.
license: Apache-2.0
---

# Team Construction / Task Pods

## Goal

Turn one aligned, bounded outcome into the **smallest sufficient ownership structure**. A Task Pod is temporary: it exists for one evidence-bearing outcome, proves that outcome, produces a handoff when needed, then dissolves.

AAOP remains the orchestration control plane. A role library or external multi-agent runtime may supply specialist roles/execution primitives, but it does not own the Journey, Working Contract, authorization policy, or current source of truth.

## Hard limits

1. Default to **one capable agent**.
2. A Task Pod has **1–5 members maximum**. Five is a ceiling, never a target.
3. Every Pod has exactly **one accountable owner** responsible for the Pod outcome and final evidence integration.
4. Add members only for a concrete responsibility boundary.
5. For consequential work, prefer an independent reviewer who did not implement the change.
6. If more than five responsibility boundaries appear necessary, split the work into sequential Pods with explicit handoff rather than creating a larger standing team.

Serialize material Pod plans with `.aaop/schemas/team-plan.schema.json`.

## Preconditions

Before creating more than one owner:

1. load/reconcile `.aaop/skills/working-contract/SKILL.md`;
2. confirm the current outcome is aligned or independently well-defined by authoritative project evidence;
3. identify the exact capability/responsibility gap a second context would solve;
4. check host-native ability, repository scripts, local Skills/tools and existing agents first;
5. do not use more agents to bypass a product decision, missing credential, network/environment restriction, unavailable external system, or authorization blocker.

## Split criteria

Create a separate specialist/task owner only when at least one applies:

- specialist knowledge/context is materially different;
- exploration would consume excessive main-context space;
- a workstream is independent and safe to parallelize;
- independent adversarial review materially improves reliability;
- permission/tool access should be narrower than the accountable owner's;
- implementation isolation reduces collision risk.

Prefer an `agent-team` only when peers genuinely need shared coordination. Otherwise bounded subagents returning evidence to the accountable owner are simpler and safer.

## Merge criteria

Keep work under one owner when:

- responsibilities share the same context and tools;
- handoff overhead exceeds specialization benefit;
- tasks must mutate the same state sequentially;
- the task is small enough for one coherent context;
- a second role would mostly repeat the same reasoning;
- the host has no useful isolation and role simulation adds no evidence value.

## Accountable owner contract

The accountable owner:

- owns the Pod outcome, not every implementation action;
- integrates specialist evidence and resolves ordinary technical tradeoffs;
- prevents simultaneous conflicting writers;
- re-reads current project/Journey/Working Contract evidence before consequential mutation;
- decides whether acceptance criteria are genuinely proved;
- serializes Journey/Working Contract state updates where required;
- produces the handoff packet when the next materially different Pod will take over.

Specialists do **not** independently become Journey or Working Contract state owners.

## Member contract

For each member define:

- `id` — stable local identifier;
- `kind` — `accountable-owner`, `specialist`, or `reviewer`;
- `role` — responsibility, not prestige/title;
- `objective` — measurable bounded result;
- `responsibilities` — what this context owns and does not own;
- `inputs` — evidence/artifacts required;
- `outputs` — artifacts/findings/tests returned;
- `skills` — only necessary procedures;
- `tools` — least-privilege concrete access;
- `dependencies` — true data/work dependencies;
- `completion_criteria` — evidence required before return/handoff.

The top-level Pod also declares `outcome`, `accountable_owner`, and objective `acceptance_criteria`.

## Role-source policy

Use role sources progressively:

1. host-native/main-agent capability;
2. project-local agent/Skill definitions;
3. an already-reviewed specialist source;
4. only then a new external role provider.

`agency-agents-zh` may be selected as an optional specialist-role source when one of its bounded expert responsibilities materially improves the current Pod. Treat its role files as procedural inputs, not authority over product truth, project policy, tools, credentials, or the AAOP Working Contract.

Do **not** install or expose its full role catalog merely because it exists. Select the minimum justified role subset and record the concrete upstream revision when the role content materially affects a consequential decision.

`agency-orchestrator` may be considered only when the host genuinely lacks the multi-role execution/DAG/resume primitive needed for a justified Pod. Do not run its DAG as a second top-level Journey/control plane beside AAOP. AAOP owns the goal, authorization, acceptance and handoff; the provider, if selected, executes a bounded delegated Pod.

## Reviewer separation

For consequential work, prefer a reviewer context that did not implement the change. The reviewer checks:

- intended user outcome, not merely implementation-plan compliance;
- governing project principles and Working Contract;
- regression and boundary conditions;
- security/privacy implications;
- unnecessary complexity;
- whether tests/evidence actually prove the acceptance criteria.

A reviewer returns findings to the accountable owner. The reviewer does not silently expand scope or seize ownership of the Pod/Journey.

## Handoff between Pods

A new Pod should start from **current evidence**, not blindly inherit the prior team's narrative.

When a materially different Pod will take over, serialize a handoff using `.aaop/schemas/task-handoff.schema.json` containing:

- long-horizon goal;
- current bounded outcome;
- current baseline;
- material decisions + decision owner + reason;
- what was actually delivered;
- evidence proving delivery;
- residual risks and blockers;
- unresolved human-owned questions;
- next outcome;
- concrete references such as commit/PR/test/runtime/artifact identifiers.

The receiving Pod must re-read the current project, Working Contract and Journey evidence and reconcile the handoff. **Current reality outranks the handoff.**

Do not hand off a giant speculative plan. Hand off the smallest state required for the next bounded outcome.

## Host degradation

If native subagents/teams are unavailable:

1. keep the same Pod responsibility plan;
2. execute owners as sequential isolated role contexts in the main agent;
3. explicitly reset objective/inputs/completion criteria at each responsibility boundary;
4. keep one logical accountable owner;
5. preserve independent review by reviewing from acceptance criteria and current diff/evidence rather than the implementation narrative.

Lack of native multi-agent capability is never, by itself, a reason to ask the user to switch tools.

## Completion criterion

Task Pod construction is complete when:

- one bounded outcome and acceptance criteria are explicit;
- the minimum number of owners (1–5) is justified;
- exactly one accountable owner is identifiable;
- each specialist exists for a concrete responsibility boundary;
- tools/permissions are least privilege;
- provider use, if any, is narrower than the whole provider ecosystem;
- consequential work has independent review where practical;
- the Pod can finish, prove its outcome, and hand off without making the human schedule the internal team.
