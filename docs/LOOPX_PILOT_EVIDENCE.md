# LoopX Provider Pilot Evidence

Date: 2026-08-11

Status: **passed for the bounded Linux direct-CLI/custom-runner `execution-continuity` use case**.

This document records the evidence behind AAOP issue #42 and does not make LoopX a default dependency.

## Exact candidate

- AAOP candidate: `0250ea7a9fe1a43a3f2e54bc8916cea6b2a744a5`
- LoopX tag: `v0.4.3`
- LoopX exact commit: `1a7cc56a4c0873be0dc2cb55a32394cb31f78b48`
- LoopX package version: `0.4.3`
- real consumer: `YuemingHub/mingos-foundation`
- isolated consumer branch: `agent/aaop-loopx-pilot-20260811`
- final consumer head: `d26d257cc193e2a9ec191b9308c2e22ee44e2209`
- successful Actions run: `31465474613`, job `93697384831`
- consumer experiment PR: `YuemingHub/mingos-foundation#18`, closed without merge

## Proven gap

Host-native AAOP already preserves Working Contract/Journey/blocker/next-action continuity. The missing property was narrower: a fresh execution process did not have a durable provider-neutral `run / gate / wait / quiet` decision plus bounded scheduler behavior.

The pilot therefore tested whether LoopX could close only that `execution-continuity` gap while AAOP retained intent, Route/Journey, authorization, acceptance, and production authority.

## Passing evidence

1. **Upstream identity and mechanisms** — the exact LoopX checkout was clean and AAOP's qualification harness passed five upstream-owned public smokes covering quota, todo lifecycle, todo durability, blocker behavior, and project uninstall.
2. **Non-destructive connect** — connect was previewed before execution. Foundation authority-file hashes remained unchanged and LoopX runtime/controller state stayed untracked.
3. **First-connect control** — `connected_without_run` selected an explicit `onboarding_connection_validation` todo. The runner claimed and completed that health frontier before product work rather than bypassing it.
4. **Validation integrity** — a deliberate validator exit `23` left the todo open and caused no quota spend. A later real repository marker plus `python scripts/validate_repository.py` readback allowed completion.
5. **Validated accounting** — the builder created and linked a real reviewer successor before completion. With a non-terminal frontier, the validated builder writeback appended exactly one spend.
6. **Terminal stop behavior** — an earlier pressure run completed a todo with `--no-follow-up` and no successor; LoopX entered terminal-no-followup and refused spend. AAOP treats this as correct anti-thrash behavior, not a reason to fabricate more work.
7. **Bounded handoff** — reviewer ownership was explicit and silent builder takeover was blocked.
8. **Human gate** — a real merge-authorization gate returned `should_run=false` on repeated probes, left durable state unchanged, exposed `scheduler_action=backoff_waiting_for_user`, and set `next_automatic_turn=null` with explicit unchanged-poll stop/backoff policy.
9. **Fresh-process recovery** — new CLI processes recovered the same status, todos, and human gate from durable state without transcript replay.
10. **Rollback** — uninstall/archive was previewed, then executed only for the selected goal. The active goal state was removed/archived and `python scripts/validate_repository.py` passed afterward.

## Compatibility boundaries discovered

### Public-boundary scan scope

A LoopX full-root public-boundary scan produced false positives on legitimate Foundation governance prose containing generic secret-related terms such as `credential`.

AAOP did **not** rewrite Foundation governance text and did **not** disable the security scanner. LoopX v0.4.3 officially supports repeatable `--scan-path` for `check` and `status`; the passing pilot kept provider reads inside the already-authorized bounded execution surface and preserved the broader incompatibility as evidence.

The rule is: provider scanning does not expand AAOP authorization.

### Multi-agent actor identity

Once builder and reviewer identities were registered, LoopX rejected `refresh-state` without explicit `--agent-id`. AAOP treats this as the correct boundary: multi-agent state-changing writeback must identify its actor rather than infer identity from text.

### Consumer-native governance validator

Foundation's existing `validate_id_reservations.py` binds unrelated substantive PR changes to a historical PR #12 review state. The experiment did not alter that governance system merely to turn a temporary pilot green. The independent repository metadata/reference validator remained the applicable native integrity check and passed before and after rollback.

## Qualification limits

This evidence does **not** qualify:

- native Windows or WSL installation/execution;
- every LoopX optional capability or the experimental LoopX Turn adapter;
- every repository's full-root public-boundary scan;
- a production host scheduler/session restart model;
- automatic production, publication, credential, billing, or destructive authority.

## Decision

Verdict: `closes-gap` for the bounded Linux direct-CLI/custom-runner execution-continuity case.

Consequences:

- LoopX remains optional and evidence-selected, not default;
- AAOP does not add a parallel Execution Ledger/todo/quota/scheduler database;
- user/operator gates and terminal-no-followup are legitimate stop/backoff states, not failures to be hidden by more model calls;
- provider reads/writes stay inside the AAOP-authorized bounded surface;
- the old `solo-dev-autopilot` / `creating-forward` execution machinery does not need to be rebuilt beside AAOP + optional LoopX.
