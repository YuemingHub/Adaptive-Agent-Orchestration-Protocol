# LoopX Integration: Reuse the Long-Running Execution Layer

Verified against `huangruiteng/loopx` on 2026-08-11.

## Decision

AAOP should **not** build a parallel Execution Ledger, todo engine, quota engine, heartbeat scheduler, or handoff runtime merely to make long-running development more autonomous.

When a real project proves that host-native AAOP execution cannot reliably continue across many turns/sessions, AAOP may select **LoopX** as an optional long-running execution-control provider.

This is progressive adoption, not a new default dependency.

## Why this fits

LoopX already provides the exact family of mechanisms AAOP #40 was considering implementing locally:

- durable objective/todo/evidence state between turns;
- todo claim and peer handoff;
- user/operator gates;
- `quota should-run` compute/continuation decisions;
- quiet/wait/throttled/paused states that avoid useless model calls;
- scheduler/heartbeat hints and monitor waits;
- restartable execution without transcript replay;
- validated writeback before quota accounting;
- local-first public/private state boundaries.

AAOP already owns a different layer:

- Human-Agent Working Contract;
- aligned intent and decision ownership;
- developer Situation and current Route;
- Route Capability Packs and Pressure Guards;
- capability/provider selection;
- autonomy and exact-write-target policy;
- Task Pod responsibility/acceptance;
- long-horizon Journey and release-cycle continuity;
- final release/target verification.

The integration works only if these two ownership layers remain separate.

## Authority map

```text
Human intent / product truth
        ↓
AAOP Working Contract
        ↓
AAOP current Route + Journey + authorization
        ↓
AAOP bounded outcome / Task Pod acceptance
        ↓
[only when a proven long-running execution-control gap exists]
        ↓
LoopX bounded execution goal/frontier
  todo · claim · gate · evidence · quota · scheduler · handoff
        ↓
Codex / Claude Code / Cursor / custom runner
        ↓
real repo / tests / CI / runtime evidence
        ↓
LoopX validated writeback
        ↓
AAOP acceptance / reroute / Journey checkpoint
```

### AAOP remains authoritative for

- what the user is trying to make true;
- whether a question is human-owned, agent-owned, or joint;
- which Route owns the current engineering problem;
- whether a Provider is justified;
- repository/branch/environment write authorization;
- production, publication, credential, billing, destructive, and other protected effects;
- whether the bounded outcome is accepted;
- whether the current release cycle is complete.

### LoopX may own, for the selected bounded execution surface

- which durable todo is currently runnable;
- claim/handoff state for that bounded work;
- whether the next automatic turn should run, wait, ask, repair, or stay quiet;
- compact execution evidence/writeback state;
- scheduler/heartbeat hinting and monitor waiting;
- bounded run history and quota accounting.

### LoopX must not become

- a second AAOP Working Contract;
- the source of product/domain truth;
- a competing Route/Journey state machine;
- an authorization bypass;
- an automatic production controller;
- a reason to install the full LoopX capability catalog when only the CLI control contract is needed.

## Selection rule

Use host-native AAOP first.

Select LoopX only when current evidence proves at least one recurring gap such as:

1. execution must survive many sessions and host-native continuation loses the bounded frontier;
2. unchanged failures/polls cause repeated model calls or blind retries;
3. todo ownership/handoff between bounded agent contexts is not durable enough;
4. external waits/monitors require a real scheduler/wake contract rather than chat memory;
5. a custom runner needs provider-neutral `should-run → execute one bounded slice → validate → write back → schedule next wake` semantics.

Do not select LoopX for a small task merely because it is installed.

## Integration surface

Prefer LoopX's documented **direct CLI/custom-runner contract** first.

The minimum conceptual tick is:

```text
LoopX should-run decision
→ AAOP/host executes one bounded authorized action
→ independent repository/runtime validation
→ LoopX todo/evidence writeback
→ refresh state / account validated turn
→ host applies scheduler hint
→ next wake starts from fresh state
```

Do not make the experimental LoopX Turn adapter a production AAOP dependency until it is separately qualified.

## State duplication rule

Do not mirror LoopX todo/quota/run-history fields into a new `.aaop` Execution Ledger.

AAOP should persist only AAOP-owned continuity facts, such as Working Contract and Journey state, plus compact references to accepted execution evidence when useful.

If a real pilot exposes an AAOP-specific fact that cannot be represented safely by existing AAOP state plus LoopX, add the smallest missing AAOP field **after** proving that gap. Do not create a generic second execution database.

## First pilot acceptance

Before recommending LoopX as a normal AAOP escalation, prove this on one disposable or non-production real development task:

1. **Install identity** — select the intentionally reviewed LoopX stable/exact revision; `loopx doctor` proves the installed source/version.
2. **Non-destructive connect** — connecting the project does not replace AAOP/project-owned instructions or tracked authority files.
3. **Authority separation** — the AAOP Working Contract/Journey remain the source for intent, decisions, Route, and release truth; LoopX receives only a bounded derived execution outcome.
4. **Real delivery** — one actual repository change is executed through the bounded loop and independently validated by project-native checks.
5. **No-progress behavior** — an unchanged failure/wait cannot keep consuming model turns indefinitely; the loop reaches a durable wait/gate/blocker/quiet state.
6. **Restart** — a fresh host/session reconstructs the same bounded frontier from durable state plus current repository evidence without transcript replay.
7. **Human gate** — a genuine user-owned/authorization question is surfaced concretely, while unrelated safe work may proceed only when its authority is independent.
8. **Handoff** — a bounded responsibility can pass to another agent context without making that specialist an AAOP Journey/Working Contract owner.
9. **Privacy** — live LoopX controller/runtime state remains ignored/local; tracked artifacts contain no raw transcript, credential, private path, or private evidence.
10. **Rollback** — stop scheduling, inspect the uninstall/archive dry-run, remove/archive only LoopX-owned selected state, and resume host-native AAOP from authoritative AAOP state.

## Current upstream adoption notes

At the 2026-08-11 review point:

- LoopX is MIT licensed and requires Python 3.11+;
- package metadata declares no runtime Python dependencies;
- `main` reports package `0.4.4` while `stable` reports `0.4.3`;
- upstream recommends the stable no-clone install/update channel for normal users;
- direct CLI/custom-runner integration is the compatibility baseline;
- LoopX Turn is documented as experimental;
- upstream explicitly separates public schemas/contracts from project-local private goal/run state;
- upstream states that dangerous permissions, publishing, production writes, and final ownership remain human-controlled.

These are time-scoped observations, not permanent trust. Re-check upstream before consequential adoption.

## Consequence for AAOP #40

The proposed generic AAOP **Execution Ledger is no longer the default next implementation**.

The new order is:

```text
AAOP v1 host-native continuous-execution pressure test
→ if host-native is sufficient: add nothing
→ if long-running execution control is the proven gap: pilot LoopX
→ if LoopX closes it: keep LoopX as optional Provider and retire duplicated old-repo machinery
→ only if the pilot exposes an AAOP-specific missing fact: add the smallest AAOP-local state primitive
```

This keeps AAOP small and makes "integrate, do not reimplement" real rather than aspirational.
