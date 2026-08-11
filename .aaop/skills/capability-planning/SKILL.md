---
name: capability-planning
description: Convert a user outcome and project profile into required capabilities, dependencies, acceptance evidence, and a capability matrix before choosing agents. Use for multi-step work, unfamiliar tasks, or whenever the right team/tools are not obvious.
license: Apache-2.0
---

# Capability Planning

## Goal

Describe what must be possible to achieve the outcome before deciding who should do it.

## Workflow

1. Write the `stated_request` and the best-grounded `underlying_outcome`.
2. List concrete deliverables/state changes.
3. Identify hard constraints and decision boundaries.
4. Define acceptance evidence before implementation.
5. Decompose the outcome into **capabilities**, not job titles. Prefer verb/noun ability labels such as `repository-analysis`, `browser-validation`, `data-migration`, `security-review`.
6. For work expected to span many turns, sessions, agent contexts, or external waits, decide whether `execution-continuity` is a real capability requirement. Use that label only when the project needs one or more of:
   - a bounded executable frontier that survives fresh sessions;
   - durable todo ownership/evidence/handoff rather than transcript memory;
   - an explicit run/wait/gate/quiet decision before another model turn;
   - scheduler/monitor wake semantics for external waits;
   - recovery from interruption without reopening already-resolved human-owned questions.
   A large task does **not** automatically require this capability. First inspect whether the current host plus AAOP Working Contract/Journey already provides sufficient continuity.
7. Add dependencies between capabilities. Mark which can run independently.
8. For each capability, inspect providers in this order:
   - main agent native ability;
   - available Skill;
   - native host tool;
   - connected MCP/app;
   - repository script/test harness;
   - existing specialist/subagent;
   - existing runtime/control-plane capability already installed and authorized;
   - missing.
9. Mark provider fit as `available`, `partial`, `missing`, or `blocked`.
10. For missing/partial capabilities, state the smallest gap that must be resolved. Do not choose a new MCP/runtime/control plane yet unless resolution truly requires one.

## Execution-continuity boundary

Keep these separate when planning:

- **implementation capability** — can an Agent actually edit, reason, test, or operate the project?
- **execution-continuity capability** — can bounded work continue safely across turns/sessions/waits with durable evidence and stop conditions?
- **team-execution capability** — does a justified Task Pod need explicit parallel/dependency/resume machinery?
- **organizational governance capability** — do multiple humans/runtimes need shared approvals, audit, permissions, and ownership?

A weakness in one class is not evidence to install a provider aimed at another class.

Examples:

- Agent can code/test but repeatedly wakes with stale context and no durable wait/no-progress state → `execution-continuity` gap.
- Current host cannot sustain the long-horizon reasoning/tool runtime itself → runtime gap, not merely continuity.
- One bounded Pod needs explicit multi-role dependency execution → team-execution gap.
- Several people/agents require shared audit/approval/routing → governance gap.

Provider choice belongs to `provider-selection`; capability planning only proves which class is actually missing.

## Output

Use `.aaop/schemas/capability-matrix.schema.json` when serializing.

A useful matrix answers:

- What capability is required?
- Why is it required?
- What existing provider can satisfy it?
- What is missing?
- What does it depend on?
- What evidence will later prove it worked?

For `execution-continuity`, acceptance evidence should name the actual property to prove, for example:

- fresh-session resume reconstructs the same bounded frontier;
- unchanged external wait causes no unnecessary model turn;
- repeated unchanged failure becomes a durable blocker/quiet state;
- handoff preserves compact evidence and responsibility;
- validation failure cannot be recorded as successful completion.

Do not use “LoopX is installed” or “the scheduler ran” as acceptance evidence. Installation is not the outcome.

## Anti-patterns

Do not:

- produce “PM / frontend / backend / QA” simply from habit;
- map every capability to a different agent;
- add external tools when a local/native capability is sufficient;
- confuse a Skill with permission to access an external system;
- continue planning around a provider that the current host cannot actually use;
- declare `execution-continuity` missing only because the task is long;
- collapse runtime ability, continuity control, Task Pod execution, and organizational governance into one vague “need orchestration” gap.

## Completion condition

Planning is sufficient when every required capability has either:

1. an available provider;
2. a concrete low-risk gap-resolution path; or
3. an explicit blocker that requires user action.

For any proposed external runtime/control-plane escalation, the matrix must identify the exact missing capability class and evidence proving lower layers are insufficient before provider selection begins.
