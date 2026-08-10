# Unified Idea-to-Production Pipeline

Status: canonical design for the four-repository consolidation
Date: 2026-08-10

## 1. Decision

The four repositories should not survive as four parallel products.

The canonical product becomes **AAOP as the control plane**, with one end-to-end developer journey layered on top of the existing situation routes.

```text
User: “I have an idea …”
        ↓
AAOP developer intake
        ↓
End-to-End Delivery Journey
        ↓
current situation route
        ↓
smallest evidence-bearing execution
        ↓
verify / reroute / continue
        ↓
release candidate
        ↓
release-operations
        ↓
authorized deploy + target verification
        ↓
real-world evidence -> next loop
```

This is a consolidation by **responsibility**, not by copying every file into one directory.

## 2. What happens to each repository

### Adaptive-Agent-Orchestration-Protocol — canonical home

Keep and extend.

It owns:

- natural-language developer intake;
- situation/route selection;
- evidence authority and freshness;
- capability matching;
- blocker classification;
- progressive provider selection;
- autonomy/permission boundaries;
- verification and rerouting;
- the new multi-route idea-to-production Journey.

AAOP is the only protocol a target project should need to install.

### solo-dev-autopilot — implementation lessons absorbed, not copied wholesale

Do not preserve its 21-Skill topology as a second orchestration system.

Absorb the durable practices:

| Solo Dev Autopilot capability | Unified AAOP destination |
| --- | --- |
| novice bootstrap / “tell me your idea” | `developer-intake` + `end-to-end-delivery` |
| creating-forward requirement baseline | `idea-to-build` outcome/behavior gates |
| task-planner / anti-drift | one current outcome + smallest executable delta |
| env-detect / env-setup | project discovery + blocker classification |
| project-scaffold | minimum reversible technical shape in `idea-to-build` |
| context-map / memory | evidence discovery + project-owned state when useful |
| dev-loop | implementation verification loop |
| test-runner | route-specific acceptance/regression verification |
| code-review | diff/risk verification or `understand-review` when decision-only |
| commit-helper | host-native integration step, not a user-facing workflow |
| production-preflight | `release-operations` preflight-and-rollback |
| deploy-gate | AAOP risk-based autonomy + explicit production authorization |
| observability | target evidence / post-change validation |
| closed-loop feedback | Pressure Guards + next evidence-driven outcome |

The important change is that these are no longer mandatory fixed stages. AAOP invokes only the capabilities justified by the current route and evidence.

### creating-forward — archived protocol lineage

Do not install beside AAOP.

Its durable concepts are already represented by AAOP and the unified Journey:

- requirement baseline;
- task/evidence discipline;
- authorization boundary;
- interruption recovery;
- “no evidence, no completion.”

Keep the repository archived as historical lineage and migration evidence. Do not evolve it as a parallel Core.

### agent-bundles — optional specialist supply

Keep it small and external to the default AAOP install.

Its role becomes:

> When AAOP proves that a bounded specialist responsibility materially improves the current task, agent-bundles can supply curated expert role prompts for the current host.

It is not:

- a default multi-agent layer;
- a technical capability provider for missing APIs/tools;
- a reason to install more agents when one capable agent is enough.

AAOP includes an Integration Recipe for this provider.

## 3. The novice experience

The novice should not see the architecture above.

The intended interaction is:

```text
User:
I want to make an app that …

System:
understands the idea and existing evidence
-> asks one material question only if necessary
-> defines the first real outcome
-> chooses the technical shape
-> builds the smallest slice
-> verifies it
-> keeps iterating from evidence
-> prepares release
-> asks only for credentials/material product choices/production authorization when genuinely required
-> deploys when authorized
-> verifies the actual target
```

The novice does not need to select:

- frontend/backend framework;
- database;
- MCP servers;
- Skills;
- Agent roles/count;
- test framework;
- CI structure;
- branch strategy;
- deployment provider;
- orchestration runtime.

Those are engineering decisions inferred from the outcome and the real environment unless the user has a hard constraint.

## 4. Canonical gates

### Gate 0 — Intake

Goal: translate a rough idea into one observable outcome.

Evidence:

- first actor;
- concrete situation;
- desired improvement;
- real constraints;
- first important uncertainty.

Failure to avoid: turning the first conversation into a requirements questionnaire.

### Gate 1 — First evidence-bearing slice

Goal: build the smallest thing that teaches something important.

Evidence:

- acceptance path;
- non-goals;
- working artifact;
- uncertainty reduced.

Failure to avoid: spending days on architecture/scaffolding that tests no product assumption.

### Gate 2 — Trustworthy project baseline

Goal: know what exists and what can be safely changed.

Evidence:

- relevant project rules;
- current source baseline;
- available tests/build commands;
- environment blockers;
- current write preconditions.

Failure to avoid: treating an environment/credential problem as a reason to add a new runtime.

### Gate 3 — Development loop

Goal: one coherent change at a time, verified before the next claim.

Typical validation sequence when relevant:

```text
format -> lint -> typecheck -> build -> tests -> runtime/acceptance
```

But project-native evidence wins. No universal checklist exists for every stack.

Failure to avoid: “code written = task complete.”

### Gate 4 — Evidence-driven iteration

Goal: let observed evidence choose the next route.

```text
defect                     -> bug-fix
new/changed behavior       -> feature-change
untrustworthy repository   -> repo-recovery
decision-only assessment   -> understand-review
deployment now blocks goal -> release-operations
```

Failure to avoid: following a stale roadmap after evidence changes the problem.

### Gate 5 — Specialist composition only if justified

Goal: keep one-agent simplicity unless a real responsibility boundary earns another specialist.

A specialist is justified by:

- material specialization;
- context isolation;
- safe parallel independence;
- adversarial review;
- permission boundary.

Only then consider agent-bundles or another provider.

Failure to avoid: assuming more agents means more capability.

### Gate 6 — Release candidate

Goal: prove the application is ready to enter operational preflight.

Evidence is risk-dependent and can include:

- acceptance/regression tests;
- build/type/lint checks;
- CI state;
- secret/sensitive-data review;
- production configuration needs;
- migration impact;
- observability/health checks;
- rollback prerequisites.

Failure to avoid: hard-coding a universal threshold such as “80% coverage means production ready.” Project risk and policy determine the threshold.

### Gate 7 — Release preflight

Goal: know the target before touching it.

Evidence:

- target environment identity;
- current deployed/runtime state or explicit unknown;
- authorized access path;
- preflight result;
- rollback/restore path;
- target revision/precondition;
- required production authorization.

Failure to avoid: inferring production truth from local Git/CI evidence.

### Gate 8 — Deploy and observe

Goal: make only the authorized operational change and verify the real target.

Immediately before the write:

- revalidate target revision/precondition;
- stop/reconcile if it moved;
- execute within the granted scope;
- verify version, health, representative user path, logs and data impact as material.

Failure to avoid: forcing a stale plan over concurrent target changes.

### Gate 9 — Learning loop

Goal: make the next decision from real use, failure or release evidence.

Only promote new protocol/Pressure Guards when a real repeatable failure pattern has been demonstrated.

Failure to avoid: adding process after every one-off incident.

## 5. What “fully online” means

For this pipeline, “application complete and online” does **not** mean “the repository has code and CI passed.”

The current release is complete when:

1. a real user-visible application slice exists;
2. it is deployed to the intended target;
3. the target revision/state is directly verified, or explicitly left unknown when direct evidence is blocked;
4. the intended target acceptance path is proven where practical;
5. rollback/recovery status is known;
6. material residual risks are visible;
7. the next product decision can be based on real evidence.

## 6. One product, three internal layers

The consolidated system is easiest to understand as three layers:

```text
Layer A — Protocol / Control Plane
AAOP intake, routes, evidence, policy, capability matching, reroute

Layer B — Delivery Journey
idea-to-production multi-route state machine for novice end-to-end delivery

Layer C — Capability Providers
host-native tools first; then Skills/MCP/specialists/runtimes only when justified
(agent-bundles is one optional specialist source)
```

This avoids two opposite failures:

- a rigid monolithic autopilot that forces every project through the same workflow;
- a loose collection of Skills/Agents/MCP servers that makes the novice assemble the system manually.

## 7. Migration rule

Going forward:

- new protocol decisions land in AAOP;
- new end-to-end delivery behavior lands in the AAOP Journey/Route system;
- reusable external specialist sourcing remains in agent-bundles;
- creating-forward remains archived lineage;
- solo-dev-autopilot should be treated as a migration/reference source until its remaining unique assets are either absorbed, referenced, or explicitly retired.

Do not introduce a fifth orchestration repository.
