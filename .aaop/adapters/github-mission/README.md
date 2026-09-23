# AAOP GitHub Mission Adapter (candidate)

> Status: **candidate**. Reference implementation today is
> `Family-Space-Workspace/tools/mission-watcher.mjs`. This adapter is its genericized form:
> same event protocol and invariants, with Family-Space paths/state and the
> agent-workspace-canonical dependency removed. FSW's original stays in place until a parity
> fixture proves this adapter is a drop-in.

## Files

- `mission-watcher.mjs` — the transport CLI (gh/git I/O only).
- `mission-core.mjs` — pure, importable contract/state logic. It parses the Markdown TASK CONTRACT to
  a normalized object and validates it against `.aaop/schemas/github-mission-task-contract.schema.json`,
  which is the **single contract authority** for required fields / `task_type` enum / `gate` enum /
  `autonomous ⇒ stop_when+return_when` (no parallel hardcoded rules). It also owns `transportIdFor()`.
- `fixtures/task-contract.example.md` — a shared contract fixture.
- `test/parity.test.mjs` — unit (imports `mission-core.mjs`) + subprocess parity against the
  Family-Space-Workspace reference watcher (via `FSW_REFERENCE`).

## Contract authority & identity

- **One authority.** The Markdown TASK CONTRACT is the human input format; it is parsed to a
  normalized object and validated against the AAOP-owned JSON schema. The schema decides required
  fields, the `task_type` enum, the `gate` enum, and the `autonomous ⇒ stop_when+return_when`
  conditional. There is no second copy of these rules in JS.
- **Two identities, not one.** The contract's `TASK_ID` (a human field on the body, schema-required)
  is **not** the transport identity. `transportIdFor(issueNumber, body)` derives
  `mission-<n>-<sha1(body)>` for timeline matching; timeline events use that transport id under the
  `task_id=` key (reference-watcher compatibility), and it is never confused with the contract `TASK_ID`.

## What it is

A single-file, zero-third-party-dependency Node transport that turns **one GitHub Issue = one
Mission** into a *resumable* execution handoff to a local worker. AAOP already owns the
*contract semantics* (`working-contract` / `task-handoff`) plus, for the GitHub-issue mission
form specifically, `.aaop/schemas/github-mission-task-contract.schema.json`; this adapter owns only the
**transport**: how the issue timeline becomes the source of truth, how exactly one worker
wins the task, and how evidence/review/recovery flow.

```
Commander opens a Mission Issue (canonical TASK CONTRACT in the body)
        ↓
local worker:  mission-watcher.mjs check --once
        ↓   discovers issue from mission state
        ↓   validates the TASK CONTRACT structure + GATE
        ↓   participates in [CLAIM] nonce arbitration (single winner)
        ↓   writes the contract verbatim to current-task.md (never executed)
local agent reads current-task.md and does the work
        ↓
local worker:  mission-watcher.mjs submit --file evidence.md   (append-only)
        ↓
Commander:     [REVIEW: CHANGES_REQUIRED]  → winner resumes and re-submits
               [REVIEW: READY_TO_ADVANCE]  → mission terminates
               [RETURN]                    → executor stopped with evidence
```

## Invariants (must hold; enforced, not aspirational)

1. **GitHub Issue timeline = resumable transport truth.** State is *derived* from comments,
   never from a local cache. A worker killed/restarted resumes purely from the timeline.
2. **nonce 唯一 claim.** Every `[CLAIM]` carries a `claim_nonce`; after posting, the worker
   re-reads the timeline and only the **earliest valid CLAIM** wins (tie-break: nonce
   lexicographic). Losers never write the contract or start an agent.
3. **no shell execution from comments.** All `gh`/`git` calls go through `execFileSync` with an
   argument array; comment text is never interpolated into a shell.
4. **no model invocation in transport.** The watcher never calls an LLM/API.
5. **no auto-cross-Gate.** The watcher never advances/merges/deploys after a review; it only
   stops or resumes an executor.
6. **append-only Evidence.** `[EVIDENCE] v1, v2, v3` are new comments; earlier versions are
   never edited. `CHANGES_REQUIRED` only ever follows the latest evidence.
7. **crash/restart recovery.** `.runtime/` is cache only; every decision is recomputed from the
   timeline on the next run.

## Safety boundary (hard-coded, no switch)

- never deploys production, deletes assets, handles payments, or reads private user data;
- never modifies the TASK CONTRACT (only writes it verbatim);
- never creates a second primary executor (nonce arbitration guarantees one winner);
- never executes review outcomes (no auto-advance across a Gate).

## De-Familization vs the reference implementation

- **State source**: `--state-file <path>` (default `./.mission-state.json`), read as
  `{ "active_mission": { "issue_number": <n> } }`. No hardcoded `../state/WORKSPACE_STATE.json`.
- **Contract ownership**: the TASK CONTRACT is AAOP-owned — machine-readable in
  `.aaop/schemas/github-mission-task-contract.schema.json` (`executor`/`goal`/`scope`/`not_in_scope`/
  `done_when`/`evidence`/`final_verification`/`gate` + `task_type`-conditional `stop_when`/
  `return_when`). `mission-core.mjs` mirrors that schema's fields; the adapter validates against
  the AAOP-owned contract, not against a free-floating field list and not against `agent-workspace`.
- **GATE values**: allow-list configurable via `MISSION_BUS_GATE_VALUES` (default
  `COMMANDER,FOUNDER` to preserve parity with the original Mission Bus). In AAOP terms these
  are the two advance-authority classes; see `decision_ownership` in the migration matrix.
- **Wording**: no "Family-Space" / "Commander" / "Agent-Space" hardcoded strings (Commander kept
  only as the default GATE *value*, not as a hardcoded dependency).

## Parity strategy (do not delete FSW first)

1. `test/state-machine.test.mjs` exercises the pure state derivation
   (`validateContract`, `parseEvents`, `deriveMissionState`) against fixtures — no network,
   no `gh`, no model.
2. `fixtures/task-contract.example.md` is a single contract usable as `current-task.md` input by
   **both** this adapter and `Family-Space-Workspace/tools/mission-watcher.mjs`.
3. Only after the parity fixture passes against both implementations should FSW's original be
   retired and repointed here.

## Known limitation (v1, non-blocking)

All comment authors share one GitHub principal; v1 cannot machine-separate Commander from
Local Worker authorship. Because v1 never auto-advances after review, this is currently benign.
It must be re-examined before remote/parallel executors, auto-merge, or auto-next-task.