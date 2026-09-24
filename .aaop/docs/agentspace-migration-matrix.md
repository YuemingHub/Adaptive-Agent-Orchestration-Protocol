# Agent-Space → AAOP Semantic Migration Matrix

> Purpose: settle, once, whether Agent-Space's engineering protocol concepts already exist in
> AAOP v1.2, or are a genuine gap. The target architecture is fixed: **Agent-Space = WHO /
> WHERE / YueMing context / Agent entry; AAOP = HOW software development works.** So new
> *generic* engineering capability must not keep sedimenting into `agent-workspace`.
>
> Sources compared:
> - `agent-workspace/开发协作协议.md` (§2 One Task = One Primary Executor, §3 TASK CONTRACT, §7 STOP-WHEN/RETURN-WHEN, §1 roles)
> - `agent-workspace/contracts/development-loop/task-contract.schema.json` and `mission.schema.json` / `evidence.schema.json`
> - AAOP v1.2 `.aaop/schemas/working-contract.schema.json`, `task-handoff.schema.json`, `journey.schema.json`, `execution-plan.schema.json` and `.aaop/policies/*`, `.aaop/routes/*`
> - `Family-Space-Workspace/tools/mission-watcher.mjs` (the Mission Bus transport)

## Decision rule

> **2026-09-23 update (Wave 1B review)**: GATE, STOP-WHEN and RETURN-WHEN were previously only
> policy-level in AAOP; marking them `AAOP_HAS_EQUIVALENT` and retiring them would have left a
> task-level contract without a machine-readable home. That gap is closed by a new AAOP-owned
> schema — `.aaop/schemas/github-mission-task-contract.schema.json` (fields incl. `gate`,
> `stop_when`, `return_when`, with an `autonomous ⇒ stop_when+return_when` conditional). The
> Mission Adapter consumes THAT schema; it is no longer a free-floating field list and is not a
> second contract authority.


- **AAOP_ALREADY_HAS** — same concept with the same semantics and an active schema/policy. Agent-Space should **retire** it as the canonical source (pointer only).
- **AAOP_HAS_EQUIVALENT** — not field-identical, but the same semantic/capability exists. Agent-Space **retires** to a pointer, optionally adding a small field to an AAOP schema.
- **AAOP_GENUINE_GAP** — no AAOP equivalent. **Migrate** the minimal generic semantics into AAOP.
- **FAMILY_ONLY / CULTURE_ONLY** — not engineering protocol; stays in Agent-Space (roles/culture/context).
- **OBSOLETE** — superseded; do not migrate.

## Matrix

| Agent-Space concept | AAOP v1.2 equivalent | Verdict | Action |
|---|---|---|---|
| **TASK CONTRACT** (`EXECUTOR / GOAL / SCOPE / NOT-IN-SCOPE / DONE-WHEN / EVIDENCE / FINAL VERIFICATION / GATE`) | `working-contract.schema.json` §`alignment` (`goal`, `actor`, `situation`, `outcome`, `must`, `non_goals`, `constraints`, `success_evidence`) + `task-handoff.schema.json` (`accountable_owner`, `long_horizon_goal`, `delivered`, `evidence`, `next_outcome`) | AAOP_HAS_EQUIVALENT | Retire; pointer to AAOP `working-contract` + `task-handoff`. No new schema needed. |
| **GATE** (`COMMANDER \| FOUNDER`; human-authority escalation only) | `decision_ownership` (`human_owned` / `agent_owned` / `joint`) + `task_pod_policy.independent_review_when_consequential`; now machine-readable as `github-mission-task-contract.schema.json` §`gate` (enum `COMMANDER`/`FOUNDER`) | **AAOP_ALREADY_HAS** (now both policy *and* task-level) | Retire. The adapter validates `gate` against the AAOP-owned schema, not against a local constant. |
| **STOP-WHEN** (autonomous terminal criterion) | `autonomy.md` policy + `alignment.success_evidence` + route `Outcome` + `github-mission-task-contract.schema.json` §`stop_when` (required iff `task_type=autonomous`) | **AAOP_ALREADY_HAS** (policy *and* task-level) | Retire. The autonomous stop criterion now has a machine-readable AAOP contract field. |
| **RETURN-WHEN** (escalate-with-evidence) | `human_open_questions` + `blockers` + `risks` + `Decision Frame` + `github-mission-task-contract.schema.json` §`return_when` | **AAOP_ALREADY_HAS** (policy *and* task-level) | Retire. Escalation-with-evidence is now both a policy and a schema field. |
| **Evidence** | `task-handoff.evidence`, `alignment.success_evidence`, and the core-ontology term **Evidence Authority/Freshness** | AAOP_ALREADY_HAS | Retire. Explicitly keep the "current reality > README claim · source > summary" discipline AAOP already encodes. |
| **Verification / FINAL VERIFICATION** | `success_evidence` + `independent_review_when_consequential` + Route Capability Pack `verification` stage | AAOP_ALREADY_HAS | Retire. |
| **Primary Executor** (one task, one executor) | `task_pod_policy.default_single_agent: true` + `accountable_owner` | AAOP_ALREADY_HAS | Retire. |
| **Founder / Human authority** | `decision_ownership.human_owned` + `alignment.must` + `human_open_questions` + `autonomy.md` | AAOP_ALREADY_HAS | Retire the *engineering* half. The *YueMing-specific role culture* (Founder = Reality/Intent/Vision/Human Authority; Commander = engineering owner; `FOUNDER CONSTRAINT` vs `FOUNDER SUGGESTION`) is **CULTURE_ONLY** → stays in Agent-Space. |
| **Mission Bus transport** (GitHub Issue → watcher → `[CLAIM]` nonce arbitration → `[EVIDENCE]`/`[REVIEW]` → resume/return/ready, timeline-derived resumable state) | none — AAOP has schemas/policies for *what* a task/contract is, but no GitHub-Issue **transport** that turns an issue into a resumable mission with single-winner claim arbitration | **AAOP_GENUINE_GAP** | **Migrate** → `.aaop/adapters/github-mission/` (see below). |

## Which Agent-Space engineering semantics can retire

These may become pointer-only in Agent-Space (the canonical text moves to AAOP, Agent-Space keeps a one-line reference):

1. TASK CONTRACT field semantics → AAOP `working-contract` + `task-handoff`.
2. GATE / decision authority → AAOP `decision_ownership`.
3. STOP-WHEN / RETURN-WHEN semantics → AAOP `autonomy.md` + `success_evidence` / escalation fields.
4. Evidence & verification discipline → AAOP `evidence`/`success_evidence`/`Evidence Authority/Freshness`.
5. One-primary-executor → AAOP `task_pod_policy`.

What **stays** in Agent-Space (WHO/WHERE/context, not HOW): the role table (Founder/Commander/Local Reality Worker), the `FOUNDER INTENT/VISION/CONSTRAINT/SUGGESTION` translation discipline, the collaboration culture, and the product/repo map.

## What becomes the AAOP GitHub Mission Adapter

The only genuine engineering gap is the **transport**. Its full spec is
`.aaop/adapters/github-mission/README.md`; the reference implementation is
`Family-Space-Workspace/tools/mission-watcher.mjs` (kept in place for parity until the adapter
is proven). See that README for the invariant list and the parity-fixture strategy.