# Unified Idea-to-Production Pipeline

Status: canonical design for the four-repository consolidation
Date: 2026-08-10

## 1. Decision

The four repositories should not survive as four parallel products.

The canonical product is **AAOP as the control plane**, with one resumable end-to-end delivery Journey layered on top of the existing situation routes.

```text
User: “I have an idea …” or “this half-built app needs to become real”
        ↓
AAOP developer intake
        ↓
End-to-End Delivery Journey
        ↓
select the CURRENT route from present evidence
        ↓
smallest evidence-bearing execution
        ↓
verify / checkpoint / reroute only when evidence changes
        ↓
release candidate
        ↓
release-operations
        ↓
authorized deploy + DIRECT target verification
        ↓
real-world evidence -> next loop
```

This is consolidation by **responsibility**, not by copying every file into one directory.

The Journey is not a seventh Route and not another workflow runtime. It preserves the long-horizon product goal while AAOP continues to select exactly one current Route at a time.

## 2. What happens to each repository

### Adaptive-Agent-Orchestration-Protocol — canonical home

AAOP owns:

- natural-language developer intake;
- current-situation Route selection;
- evidence authority and freshness;
- capability matching;
- blocker classification;
- progressive provider selection;
- autonomy/permission boundaries;
- verification and rerouting;
- the multi-route idea-to-production Journey;
- lightweight Journey checkpoints for interruption recovery.

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
| context-map / memory | current project evidence + Journey checkpoint when continuity matters |
| dev-loop | implementation verification loop |
| test-runner | route-specific acceptance/regression verification |
| code-review | diff/risk verification or `understand-review` when decision-only |
| commit-helper | host-native integration step, not a user-facing workflow |
| production-preflight | `release-operations` preflight-and-rollback |
| deploy-gate | AAOP risk-based autonomy + explicit production authorization |
| observability | direct target evidence / post-change validation |
| closed-loop feedback | Pressure Guards + next evidence-driven outcome |

These are no longer mandatory fixed stages. AAOP invokes only the capabilities justified by the current Route and evidence.

### creating-forward — archived protocol lineage

Do not install it beside AAOP.

Its durable concepts are represented by AAOP and the unified Journey:

- requirement baseline;
- task/evidence discipline;
- authorization boundary;
- interruption recovery;
- “no evidence, no completion.”

Interruption recovery is now represented by a persisted Journey checkpoint under `.aaop/runtime/journeys/`. That checkpoint is deliberately **non-authoritative**: a new session must reconcile it against current repository/runtime/target evidence before continuing.

### agent-bundles — optional specialist supply

Keep it small and external to the default AAOP install.

Its role is:

> When AAOP proves that a bounded specialist responsibility materially improves the current task, agent-bundles can supply curated expert role prompts for the current host.

It is not:

- a default multi-agent layer;
- a technical capability provider for missing APIs/tools;
- a reason to install more agents when one capable agent is enough.

AAOP intentionally does **not** detect agent-bundles from generic `.claude/agents/*.md`, `.cursor/agents/*.md`, or similar files. Those may be project-owned agents and do not prove provider ownership. Until agent-bundles exposes a provider-specific marker, its Recipe detection remains empty and adoption is explicit.

## 3. The novice experience

The intended interaction is:

```text
User:
I want to make an app that …

System:
understands the idea AND any existing implementation
-> selects the current Route from evidence
-> asks one material question only if necessary
-> creates/reconciles a Journey checkpoint
-> chooses the next technical step
-> builds or fixes the smallest coherent delta
-> verifies it
-> reroutes only when evidence changes the problem
-> prepares release
-> asks only for credentials/material product choices/production authorization when genuinely required
-> deploys when authorized
-> directly verifies the actual target
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
- orchestration runtime;
- Journey gate or checkpoint commands.

Those are engineering decisions inferred from outcome and evidence unless the user has a hard constraint.

## 4. Critical invariants discovered by failure review

The initial consolidated Journey exposed several failure modes that must remain regression-protected.

### 4.1 Journey position must not force the current Route

A long-horizon goal may begin from:

- a rough idea;
- a trustworthy partial application;
- a reproducible bug;
- an untrustworthy repository;
- a release candidate;
- a blocked deployment.

Therefore **developer intake selects the current Route**. The Journey does not force every entry through `idea-to-build`.

`idea-to-build` is used for the first evidence-bearing slice only when no trustworthy existing slice already exists.

### 4.2 Blocked is not complete

AAOP's core protocol already states that a safely blocked task is not complete. The Journey follows the same rule.

If direct target verification is unavailable after a deployment attempt:

```text
target state = unknown
Journey status = blocked / not complete
next = exact legitimate unblock condition
```

Never reinterpret this as “probably deployed, therefore complete.”

### 4.3 Current evidence outranks saved Journey state

A checkpoint exists to survive interruptions, not to freeze history.

At every resumed session:

```text
saved Journey checkpoint
        +
current repository/runtime/target/project rules
        ↓
reconcile
        ↓
current evidence wins
```

A stale checkpoint may trigger a Route change, but the transition must be recorded from new evidence rather than silently forcing the old plan.

### 4.4 Rerouting must not become route thrashing

A Route change requires materially new evidence or a changed blocker classification.

If execution starts bouncing between `bug-fix`, `repo-recovery`, `feature-change`, or another Route while the underlying evidence is unchanged, stop and re-diagnose. Lack of progress is not itself a reason to choose another Route.

### 4.5 Generic local Agent files do not prove provider ownership

A project can already contain `.claude/agents/*.md` or similar files without ever using `agent-bundles`.

Provider presence must be based on provider-specific evidence. Until such evidence exists, AAOP must return “not detected” instead of claiming agent-bundles is present.

## 5. Canonical gates

### Gate 0 — Intake

Goal: understand the long-horizon outcome and select the **current** Route from present evidence.

Evidence:

- actor and situation;
- desired observable improvement;
- real constraints;
- current asset/project state;
- immediate uncertainty/blocker;
- current Route.

Failure to avoid: assuming “idea-to-production” means the project is greenfield.

### Gate 1 — First evidence-bearing slice, conditional

Use only when no trustworthy existing slice already exists.

Goal: build the smallest thing that teaches something important.

Evidence:

- acceptance path;
- non-goals;
- working artifact;
- uncertainty reduced.

Failure to avoid: rebuilding product discovery/scaffolding around an already-working partial app.

### Gate 2 — Trustworthy project baseline

Goal: know what exists and what can be safely changed.

Evidence:

- relevant project rules;
- current source baseline;
- available tests/build commands;
- environment blockers;
- current write preconditions;
- Journey checkpoint reconciled with current evidence.

Failure to avoid: letting stale remembered state outrank the repository or target.

### Gate 3 — Development loop

Goal: one coherent change at a time, verified before the next claim.

Typical validation sequence when relevant:

```text
format -> lint -> typecheck -> build -> tests -> runtime/acceptance
```

Project-native evidence wins. No universal checklist exists for every stack.

Failure to avoid: “code written = task complete.”

### Gate 4 — Evidence-driven iteration

Goal: let observed evidence choose the next Route.

```text
defect                     -> bug-fix
new/changed behavior       -> feature-change
untrustworthy repository   -> repo-recovery
decision-only assessment   -> understand-review
deployment now blocks goal -> release-operations
```

Every established Route transition should carry a reason and new evidence. Repeated oscillation without new evidence is a diagnosis failure, not progress.

### Gate 5 — Specialist composition only if justified

Goal: keep one-agent simplicity unless a real responsibility boundary earns another specialist.

A specialist is justified by:

- material specialization;
- context isolation;
- safe parallel independence;
- adversarial review;
- permission boundary.

Only then consider agent-bundles or another provider.

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

Failure to avoid: hard-coding universal thresholds such as “80% coverage means production ready.”

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

Unknown target state is acceptable as a **blocked preflight state**, not as completion evidence.

### Gate 8 — Deploy and observe

Goal: make only the authorized operational change and verify the real target.

Immediately before the write:

- revalidate target revision/precondition;
- stop/reconcile if it moved;
- execute within the granted scope;
- verify target revision, health, representative user path, logs and data impact as material.

Local Git, local tests, and CI cannot substitute for direct target evidence.

### Gate 9 — Learning loop

Goal: make the next decision from real use, failure or release evidence.

Only promote new protocol/Pressure Guards when a repeatable failure pattern has been demonstrated.

## 6. Resumability without building a workflow engine

The Journey checkpoint surface is intentionally small:

```bash
python .aaop/tools/journey.py show idea-to-production
python .aaop/tools/journey.py start idea-to-production --goal "..." --route <current-route>
python .aaop/tools/journey.py status idea-to-production --json
python .aaop/tools/journey.py checkpoint idea-to-production ...
```

It records continuity under `.aaop/runtime/journeys/`, which the AAOP installer already preserves across upgrades.

The checkpoint tool does **not**:

- select the Route;
- execute tasks;
- decide evidence authority;
- install providers;
- deploy;
- replace repository/project truth.

It enforces only a few cross-session invariants that are otherwise easy to lose:

- original long-horizon goal survives conversation changes;
- established Route changes require a reason and evidence;
- blockers remain visible;
- Journey completion requires direct target verification;
- old checkpoint versions are surfaced for reconciliation after Journey definition changes.

## 7. What “fully online” means

For this pipeline, “application complete and online” does **not** mean “the repository has code and CI passed.”

The current release is complete only when:

1. a real user-visible application slice exists;
2. it is deployed to the intended target;
3. the target revision/state is directly verified from the target environment;
4. the intended target acceptance path is proven where practical;
5. rollback/recovery status is known;
6. material residual risks are visible;
7. the next product decision can be based on real evidence.

If item 3 cannot be proven, the correct status is **blocked/not-complete**, with the exact unblock recorded.

## 8. One product, three internal layers

```text
Layer A — Protocol / Control Plane
AAOP intake, Routes, evidence, policy, capability matching, reroute

Layer B — Delivery Journey
idea-to-production continuity + conditional gates + checkpoint

Layer C — Capability Providers
host-native tools first; then Skills/MCP/specialists/runtimes only when justified
(agent-bundles is one optional specialist source)
```

This avoids two opposite failures:

- a rigid monolithic autopilot that forces every project through the same workflow;
- a loose collection of Skills/Agents/MCP servers that makes the novice assemble the system manually.

## 9. Regression gates

The Journey has a dedicated semantic validator and CI workflow because ordinary JSON/Skill structural checks cannot catch cross-route contradictions.

The regression gate verifies at least:

- Journey definition/schema/checkpoint files exist in source and installed packages;
- intake does not force `idea-to-build`;
- first-slice is explicitly conditional for existing implementations;
- Route changes from an established Route require evidence;
- blocked deployment cannot be marked complete;
- completion requires direct target verification;
- generic local Agent files do not falsely detect agent-bundles.

## 10. Migration rule

Going forward:

- new protocol decisions land in AAOP;
- new end-to-end delivery behavior lands in the AAOP Journey/Route system;
- cross-session Journey continuity lands in the lightweight `.aaop/runtime/journeys/` checkpoint contract;
- reusable external specialist sourcing remains in agent-bundles;
- creating-forward remains archived lineage;
- solo-dev-autopilot is a migration/reference source until its remaining unique assets are either absorbed, referenced, or explicitly retired.

Do not introduce a fifth orchestration repository.
