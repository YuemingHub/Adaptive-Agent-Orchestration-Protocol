---
name: capability-planning
description: Convert a user outcome and project profile into required capabilities, dependencies, acceptance evidence, and a capability matrix before choosing agents. Use for multi-step work, unfamiliar tasks, or whenever the right team/tools are not obvious.
license: Apache-2.0
metadata:
  aaop-version: "0.1.0"
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
6. Add dependencies between capabilities. Mark which can run independently.
7. For each capability, inspect providers in this order:
   - main agent native ability;
   - available Skill;
   - native host tool;
   - connected MCP/app;
   - repository script/test harness;
   - existing specialist/subagent;
   - missing.
8. Mark provider fit as `available`, `partial`, `missing`, or `blocked`.
9. For missing/partial capabilities, state the smallest gap that must be resolved. Do not choose a new MCP yet unless resolution truly requires one.

## Output

Use `.aaop/schemas/capability-matrix.schema.json` when serializing.

A useful matrix answers:

- What capability is required?
- Why is it required?
- What existing provider can satisfy it?
- What is missing?
- What does it depend on?
- What evidence will later prove it worked?

## Anti-patterns

Do not:

- produce “PM / frontend / backend / QA” simply from habit;
- map every capability to a different agent;
- add external tools when a local/native capability is sufficient;
- confuse a Skill with permission to access an external system;
- continue planning around a provider that the current host cannot actually use.

## Completion condition

Planning is sufficient when every required capability has either:

1. an available provider;
2. a concrete low-risk gap-resolution path; or
3. an explicit blocker that requires user action.
