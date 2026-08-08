# Real-Project Pressure Tests

AAOP should evolve from failures observed in real developer work, not from a desire to make the protocol look complete.

`tests/pressure/` contains sanitized replay contracts derived from real repositories/issues. They are not benchmark claims and do not execute third-party projects. Their purpose is to preserve the engineering lesson that changed an AAOP route.

## Why this exists

A generic orchestration protocol can look correct while still making bad developer decisions:

- treating an old issue as though it describes current head;
- merging a deeply stale PR because its intent is still useful;
- choosing the newest document as truth when the project has an explicit authority hierarchy;
- treating a blocked network/authorization path as a reason to install more tooling;
- declaring production facts from Git/CI evidence that never reached the target environment.

These failures are more important than adding another provider to the catalog.

## Pressure-case contract

Each JSON case records:

- provenance and privacy class;
- a realistic minimal developer request;
- expected AAOP route;
- known facts available at intake;
- first engineering moves that should follow;
- facts/constraints that must be preserved;
- dangerous behaviors that must not occur;
- one or more `required_guard_ids` that must exist on the selected Route Capability Pack;
- the lesson learned.

The schema is `.aaop/schemas/pressure-case.schema.json`.

Run:

```bash
python scripts/validate_pressure.py
```

The validator ensures every case is structurally valid and that every `required_guard_id` still exists on the expected route. Removing a guard therefore breaks CI until the real-project regression is intentionally re-evaluated.

## Privacy rule

Private project content must not be copied into this public repository merely because it was useful during testing.

Use one of two modes:

1. **Public source** — public repository/issue may be named and referenced.
2. **Anonymized real-project** — preserve the engineering shape only. Do not publish repository names, URLs, credentials, hosts, user data, private business details, or sensitive logs.

Pressure cases should contain the minimum evidence necessary to preserve the orchestration lesson.

## Initial v0.7 cases

### Repository authority recovery

Derived from the public MingOS coordination model.

Lesson: repository recovery requires **source authority + freshness**, not just a file inventory. A merged file may still be Draft; an old branch may be historical; conflicting sources must remain explicit until authority/evidence resolves them.

Guards:

- `source-authority-freshness`
- `preserve-conflicting-evidence`

### Stale bug report

Derived from public AutoAgent issue #33.

Lesson: a detailed traceback is still tied to a reported version/environment. Before editing current code, reconcile the report with current head. Issue comments and workarounds are hypotheses, not root cause.

Guards:

- `reported-baseline-freshness`
- `discussion-is-hypothesis`

### Stale PR feature salvage

Anonymized real-project case.

Lesson: when a historical PR is far behind current baseline, preserve **behavior, invariants, tests, and rationale**, not old commits/architecture. Compare behavior-by-behavior and rebuild only what is still missing.

Guards:

- `stale-artifact-salvage`
- `behavior-over-commits`

### Environment-blocked release verification

Anonymized real-project case.

Lesson: network policy, authorization, credential, external dependency, and product decision blockers are not automatically technical capability gaps. A correct agent sometimes stops, preserves unknown state, and names the minimal unblock instead of installing a workaround.

Guards:

- `blocker-not-capability-gap`
- `preserve-unknown-operational-state`

## Adding future cases

Add a new pressure case when a real task reveals a repeatable orchestration error or a dangerous near-miss.

Do not add cases merely to cover every route numerically.

A useful new case should answer:

1. What did a real developer ask?
2. What evidence was actually available?
3. What tempting wrong action existed?
4. What rule would have prevented it?
5. Is that rule route-specific or general?
6. Can the lesson be preserved without publishing private project content?

If the lesson only says “use provider X,” it probably belongs in a Recipe or provider-selection test instead of a pressure guard.
