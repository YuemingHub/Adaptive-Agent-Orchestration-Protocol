# Auxiliary Repository Consolidation and Retirement

Date: 2026-08-11

Canonical control plane: **AAOP** (`YuemingHub/Adaptive-Agent-Orchestration-Protocol`).

This document closes the consolidation decision tracked by AAOP issue #40. It distinguishes mechanisms that were absorbed, providers that remain optional, historical lineage that can be retired, and personal-machine configuration that intentionally stays outside AAOP.

## Decision summary

| Repository / source | Final AAOP status | Operational dependency? | Retirement decision |
| --- | --- | --- | --- |
| `YuemingHub/solo-dev-autopilot` | historical operational lineage | **No** | retire as a separate development control plane after consumers confirm no direct dependency |
| historical `creating-forward` | historical protocol lineage | **No** | retire as a separate protocol/runtime; do not install beside AAOP |
| `YuemingHub/agent-bundles` | retired compatibility alias | **No new dependency** | stop all new adoption; migrate legacy references to Task Pods + direct role providers; repository may be deleted once external consumers are checked |
| `YuemingHub/ai-dotfiles` | separate personal/global host configuration layer | intentionally outside AAOP | keep separate unless the user later replaces that machine-config system |
| `huangruiteng/loopx` | optional Level-4 execution-continuity Provider | only when a proven gap selects it | keep external; do not vendor or rebuild its todo/quota/scheduler layer in AAOP |
| `randyjin/agency-agents-zh` | optional specialist-role source | only when a bounded role gap selects it | direct current role source; minimum justified subset only |
| `jnMetaCode/agency-orchestrator` | optional delegated Task Pod runtime | only when a distinct DAG/resume gap selects it | direct runtime candidate; never a second AAOP Journey |

## What AAOP absorbed from solo-dev-autopilot

AAOP keeps the reusable engineering behavior, not the old fixed 21-Skill topology:

- inspect environment/project state before changing it;
- plan from the current delta rather than a speculative roadmap;
- prefer project-native validation;
- use the practical sequence `format -> lint -> typecheck -> build -> test -> runtime/acceptance` only where relevant;
- classify validation failures before retrying;
- stop unchanged blind retries;
- inspect diffs, debug residue, and sensitive data before consequential writes;
- distinguish release-candidate proof from direct production-target proof;
- treat environment/network/credential/authorization failures as blockers rather than reasons to widen permissions or install more agents;
- preserve branch/write-target correctness and current-baseline preconditions.

These behaviors now live in AAOP Routes, Pressure Guards, the End-to-End Journey, Working Contract, release-cycle rules, and validation gates. AAOP does **not** require the solo-dev-autopilot repository at runtime.

## What AAOP absorbed from creating-forward

The historical protocol contributed durable ideas:

- requirement/outcome baseline;
- context and evidence discipline;
- dependency-aware bounded tasks;
- `observe -> plan -> act -> verify -> checkpoint -> continue/repair/block` thinking;
- authorization boundaries;
- attempt/no-progress discipline;
- interruption recovery from persisted state instead of transcript memory.

AAOP represents these ideas through current Route/Journey/Working Contract/Task Pod/evidence mechanisms. The historical `.creating-forward/` workspace and a second Task Graph engine are not reintroduced.

The real LoopX pilot in issue #42 also showed that AAOP does not need to build a second generic Execution Ledger/todo/quota/scheduler database merely to preserve long-running execution continuity.

## agent-bundles retirement

`YuemingHub/agent-bundles` was useful as a cross-host installer for curated specialist role prompts. It did **not** create tool/API/runtime capability and it fetched another role catalog at runtime.

AAOP v1 now has the missing control semantics directly:

- Task Pod composition is owned by AAOP;
- every Pod has one accountable owner and bounded role responsibilities;
- consequential work may use an independent reviewer;
- current host/project roles are checked first;
- `agency-agents-zh` is a directly reviewed optional role source when a concrete role is missing;
- `agency-orchestrator` is separately selectable only when a justified Pod needs delegated DAG/resume execution.

Therefore agent-bundles no longer closes a unique capability gap.

### Compatibility policy

The Provider Registry and `agent-bundles.json` Recipe remain temporarily as a **retired compatibility alias/tombstone** so an older installed AAOP instruction does not fail open or clone the old repository by accident.

The tombstone:

- contains no new agent-bundles install/bootstrap command;
- redirects new role selection to current Task Pod policy and reviewed providers;
- explicitly forbids new adoption;
- allows legacy installations to be removed using their original ownership evidence.

This compatibility alias is not an operational dependency on the `agent-bundles` repository. A later major-version cleanup may delete the alias after supported legacy consumers no longer reference it.

## ai-dotfiles boundary

`ai-dotfiles` solves a different problem: personal/global host configuration, cross-host config ownership, copy-vs-symlink behavior, backup-before-overwrite, secret hygiene, and machine-level preferences.

AAOP is project/developer orchestration policy. Merging personal machine configuration into AAOP would mix ownership domains and create unnecessary authority over the user's host.

Generic lessons such as explicit ownership, backup before overwrite, and secret scanning may inform AAOP tooling, but the repository itself remains separate.

## LoopX result

AAOP issue #42 produced a passing real-consumer pilot and `docs/LOOPX_PILOT_EVIDENCE.md` records the evidence.

Result:

- LoopX closes the tested bounded Linux direct-CLI/custom-runner `execution-continuity` gap;
- LoopX remains optional and conditional;
- AAOP retains Working Contract, Route/Journey, authorization, acceptance, and release truth;
- full-root provider scanning does not expand AAOP authorization;
- human gates and terminal-no-followup are legitimate wait/stop states;
- no parallel AAOP Execution Ledger is justified by the evidence.

## Retirement gates

An old repository is safe for the user to delete only after both conditions hold:

1. **AAOP runtime independence** — current AAOP no longer requires that repository to execute supported routes/journeys/provider selection.
2. **External consumer check** — no remaining project, host config, automation, or human workflow still imports/clones/links the repository in a way the user intends to keep.

This PR establishes condition 1 for `solo-dev-autopilot`, historical `creating-forward`, and new adoption of `agent-bundles`.

The GitHub connector used by this work does not provide repository archive/delete operations. This document therefore records **safe-to-retire architecture**, not a false claim that the old GitHub repositories were physically deleted.

## Canonical rule going forward

Do not create another top-level development control plane beside AAOP.

For every proposed framework/repository/tool:

1. identify the exact capability gap on current evidence;
2. check host-native and project-native capability first;
3. distinguish role source, technical tool, execution runtime, execution-continuity control, and organizational governance;
4. select the smallest provider surface that closes the gap;
5. keep AAOP authority explicit;
6. verify real outcome delta and rollback;
7. retire redundant adapters/installers rather than preserving layers for historical symmetry.

The target state is **one AAOP control plane, many replaceable providers, no duplicate ownership**.
