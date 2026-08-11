# LoopX Integration: Reuse the Long-Running Execution Layer

Verified against `huangruiteng/loopx` on 2026-08-11.

Reviewed stable identity at that point:

- tag: `v0.4.3`;
- exact commit: `1a7cc56a4c0873be0dc2cb55a32394cb31f78b48`;
- GitHub compare result: tag and commit are identical;
- stable package metadata: `0.4.3`;
- moving `main` package metadata observed: `0.4.4`.

This identity is a review snapshot, not permanent trust. Re-resolve the current stable/tag/commit identity before consequential adoption.

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
[only when a proven execution-continuity gap exists]
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

Select LoopX only when current evidence proves at least one recurring `execution-continuity` gap such as:

1. execution must survive many sessions and host-native continuation loses the bounded frontier;
2. unchanged failures/polls cause repeated model calls or blind retries;
3. todo ownership/handoff between bounded agent contexts is not durable enough;
4. external waits/monitors require a real scheduler/wake contract rather than chat memory;
5. a custom runner needs provider-neutral `should-run → execute one bounded slice → validate → write back → schedule next wake` semantics.

Do not select LoopX for a small task merely because it is installed.

Do not classify these neighboring problems as a LoopX gap:

- the implementation itself is wrong;
- the host cannot perform the actual long-horizon reasoning/tool execution;
- the Task Pod specifically needs multi-role DAG/resume execution;
- the project needs organization-level governance/audit;
- credentials, production authorization, network, cost, or another human gate is unresolved.

Those are different capability classes and may call for no provider, another provider, or a real blocker.

## Integration surface

Prefer LoopX's documented **direct CLI/custom-runner contract** first.

The minimum conceptual tick is:

```text
fresh LoopX should-run decision
→ AAOP/host executes one bounded authorized action
→ independent repository/runtime validation
→ LoopX todo/evidence writeback
→ refresh state / account validated turn
→ host applies scheduler hint
→ next wake starts from fresh state
```

Every wake starts from fresh LoopX/project evidence. Do not cache a previous `should-run` packet in the AAOP Journey or treat chat memory as the execution frontier.

Do not make the experimental LoopX Turn adapter a production AAOP dependency until it is separately qualified.

## State duplication rule

Do not mirror LoopX todo/quota/run-history fields into a new `.aaop` Execution Ledger.

AAOP should persist only AAOP-owned continuity facts, such as Working Contract and Journey state, plus compact references to **accepted** execution evidence when useful.

If a real pilot exposes an AAOP-specific fact that cannot be represented safely by existing AAOP state plus LoopX, add the smallest missing AAOP field **after** proving that gap. Do not create a generic second execution database.

## Pilot contract: what crosses the seam

A LoopX pilot should receive only the bounded execution facts needed for the current AAOP outcome.

### AAOP → LoopX

Pass or derive:

- one bounded observable execution outcome;
- current project/repository baseline reference needed for the bounded work;
- compact acceptance criteria/evidence expectations;
- current authorized write surface and protected-effect boundary;
- current accountable owner/agent lane when material;
- unresolved human gate only as a concrete gate, never as an answer fabricated by the Agent.

Do **not** copy the whole Working Contract, raw conversation, speculative roadmap, private user history, or all Journey history into LoopX merely for convenience.

### LoopX → AAOP

Return only what AAOP needs to decide acceptance/rerouting:

- bounded outcome status;
- compact evidence references/readback results;
- durable blocker/gate/wait classification;
- relevant handoff/completion receipt;
- residual execution risk;
- current repository/runtime evidence that materially changes the Route/Journey decision.

Do not import raw LoopX run history, transcripts, local paths, private controller state, or scheduler chatter into tracked AAOP state.

### Reconciliation rule

LoopX writeback is execution evidence, not current truth by itself. Before AAOP mutates its Journey checkpoint or accepts the bounded outcome, the AAOP coordinator re-reads the current project/runtime/target evidence and the latest Journey/Working Contract state.

Current authoritative evidence outranks a stale LoopX handoff or cached status.

## First pilot acceptance

Before recommending LoopX as a normal AAOP escalation, prove this on one disposable or non-production **real development task**:

1. **Install identity** — select the intentionally reviewed LoopX stable/tag/exact revision; `loopx doctor` and source identity evidence agree with the adoption decision.
2. **Non-destructive connect** — connecting the project does not replace AAOP/project-owned instructions or tracked authority files.
3. **Authority separation** — the AAOP Working Contract/Journey remain the source for intent, decisions, Route, and release truth; LoopX receives only a bounded derived execution outcome.
4. **Real delivery** — one actual repository change is executed through the bounded loop and independently validated by project-native checks.
5. **No-progress behavior** — an unchanged failure/wait cannot keep consuming model turns indefinitely; the loop reaches a durable wait/gate/blocker/quiet state.
6. **Restart** — a fresh host/session reconstructs the same bounded frontier from durable state plus current repository evidence without transcript replay.
7. **Human gate** — a genuine user-owned/authorization question is surfaced concretely, while unrelated safe work may proceed only when its authority is independent.
8. **Handoff** — a bounded responsibility can pass to another agent context without making that specialist an AAOP Journey/Working Contract owner.
9. **Validation integrity** — failed or missing real validation cannot be written back as completed delivery or quota-spent success.
10. **Privacy** — live LoopX controller/runtime state remains ignored/local; tracked artifacts contain no raw transcript, credential, private path, or private evidence.
11. **Rollback** — stop scheduling, inspect the uninstall/archive dry-run, remove/archive only LoopX-owned selected state, and resume host-native AAOP from authoritative AAOP state.
12. **Delta proof** — compare the result against the specific host-native failure that justified adoption; prove LoopX closed that gap rather than merely adding machinery.

A pilot that only proves installation, `doctor`, or one successful CLI command is insufficient.

## Pilot failure interpretation

If the pilot fails, do not immediately build the old AAOP Execution Ledger or install another runtime.

Classify the failure:

- **provider integration defect** — LoopX can represent the needed mechanism but our AAOP seam/adapter is wrong → repair the integration;
- **provider capability mismatch** — LoopX's primary mechanism does not close the proven gap → return to capability/provider selection;
- **upstream/platform blocker** — supported OS/runtime/install path is missing or unreliable → keep provider unadopted for that host and preserve the blocker;
- **AAOP-specific missing fact** — only after evidence proves that AAOP genuinely needs a continuity fact not safely owned by Working Contract/Journey/handoff/LoopX, add the smallest AAOP-local primitive;
- **misdiagnosed original problem** — the real blocker was implementation, environment, authorization, product truth, or another class → remove the unnecessary provider escalation.

Do not respond to a failed pilot by stacking LoopX + Deep Agents + agency-orchestrator unless each additional provider closes a separate proven capability gap.

## Current upstream adoption notes

At the 2026-08-11 review point:

- LoopX is MIT licensed and requires Python 3.11+;
- package metadata declares no runtime Python dependencies;
- tag `v0.4.3` is identical to exact commit `1a7cc56a4c0873be0dc2cb55a32394cb31f78b48`;
- stable/tag package metadata reports `0.4.3`, while moving `main` reports `0.4.4`;
- upstream recommends the stable no-clone install/update channel for normal users;
- direct CLI/custom-runner integration is the compatibility baseline;
- LoopX Turn is documented as experimental;
- upstream explicitly separates public schemas/contracts from project-local private goal/run state;
- upstream states that dangerous permissions, publishing, production writes, and final ownership remain human-controlled;
- the reviewed quick-start names macOS/Linux shell requirements;
- the upstream first-run feedback form offers Windows and WSL as reportable OS values, but this is **not** proof of a supported native Windows/WSL install contract.

These are time-scoped observations, not permanent trust. Re-check upstream before consequential adoption.

## Consequence for AAOP #40

The proposed generic AAOP **Execution Ledger is no longer the default next implementation**.

The new order is:

```text
AAOP v1 host-native continuous-execution pressure test
→ if host-native is sufficient: add nothing
→ if execution-continuity is the proven gap: pilot LoopX
→ if LoopX closes it: keep LoopX as optional Provider and retire duplicated old-repo machinery
→ only if the pilot exposes an AAOP-specific missing fact: add the smallest AAOP-local state primitive
```

This keeps AAOP small and makes "integrate, do not reimplement" real rather than aspirational.
