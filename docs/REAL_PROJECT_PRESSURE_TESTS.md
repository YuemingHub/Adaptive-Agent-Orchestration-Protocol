# Real-Project Pressure Tests

AAOP should evolve from failures and near-misses observed in real developer work, not from a desire to make the protocol look complete.

`tests/pressure/` contains sanitized replay contracts derived from real repositories/issues. They are not benchmark claims and do not execute third-party projects. Their purpose is to preserve the engineering lesson that changed an AAOP route.

## Why this exists

A generic orchestration protocol can look correct while still making bad developer decisions:

- turning a broad idea into a giant architecture before learning whether the first workflow is useful;
- accepting trendy solution vocabulary as immutable product requirements;
- treating an old issue as though it describes current head;
- merging a deeply stale PR because its intent is still useful;
- choosing the newest document as truth when the project has an explicit authority hierarchy;
- recursively reading every link/reference in a governance-heavy repository until context is exhausted;
- treating every referenced repository as a mandatory read or active work target;
- continuing to inventory a small handoff repository after current state and the next target are already clear;
- creating a cosmetic or unrelated diff because the user said “continue” even though no current local delta is proven;
- using “verified no-op” as an excuse to stay in analysis after a concrete local delta is already visible;
- replaying stale whole-file content after a conditional write says the target moved;
- merging/deploying from review or CI evidence that belongs to an older head/revision;
- copying a security issue's headline directly into a present-tense adoption verdict;
- turning a read-only review into unrequested fixes;
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

The validator ensures every case is structurally valid and every `required_guard_id` still exists on the expected route. From v0.8 onward it also requires at least one real pressure case for every AAOP route. Coverage became a gate only after real cases existed for all six routes; it was not created to invent synthetic cases for numerical completeness.

Removing a guard therefore breaks CI until the corresponding real-project regression is intentionally re-evaluated.

## Privacy rule

Private project content must not be copied into this public repository merely because it was useful during testing.

Use one of two modes:

1. **Public source** — public repository/issue may be named and referenced.
2. **Anonymized real-project** — preserve the engineering shape only. Do not publish repository names, URLs, credentials, hosts, user data, private business details, or sensitive logs.

Pressure cases should contain the minimum evidence necessary to preserve the orchestration lesson.

## v0.7 baseline cases

### Repository authority recovery — `repo-recovery`

Derived from the public MingOS coordination model.

Lesson: repository recovery requires **source authority + freshness**, not just a file inventory. A merged file may still be Draft; an old branch may be historical; conflicting sources must remain explicit until authority/evidence resolves them.

Guards:

- `source-authority-freshness`
- `preserve-conflicting-evidence`

### Stale bug report — `bug-fix`

Derived from public AutoAgent issue #33.

Lesson: a detailed traceback is still tied to a reported version/environment. Before editing current code, reconcile the report with current head. Issue comments and workarounds are hypotheses, not root cause.

Guards:

- `reported-baseline-freshness`
- `discussion-is-hypothesis`

### Stale PR feature salvage — `feature-change`

Anonymized real-project case.

Lesson: when a historical PR is far behind current baseline, preserve **behavior, invariants, tests, and rationale**, not old commits/architecture. Compare behavior-by-behavior and rebuild only what is still missing.

Guards:

- `stale-artifact-salvage`
- `behavior-over-commits`

### Environment-blocked release verification — `release-operations`

Anonymized real-project case.

Lesson: network policy, authorization, credential, external dependency, and product decision blockers are not automatically technical capability gaps. A correct agent sometimes stops, preserves unknown state, and names the minimal unblock instead of installing a workaround.

Guards:

- `blocker-not-capability-gap`
- `preserve-unknown-operational-state`

## v0.8 pressure expansion

### Broad vision → first proof — `idea-to-build`

Anonymized real-project case.

Lesson: a large future vision should guide direction but must not become the first implementation scope. The first slice should test one material assumption with a real end-to-end result. Autonomy is a desired user experience; it is not proof that a multi-agent architecture is required.

Guards:

- `outcome-before-architecture`
- `first-slice-must-buy-learning`
- `user-does-not-own-stack-choice`

### Solution vocabulary is hypothesis — `idea-to-build`

Anonymized real-project case.

Lesson: early mentions of Agent, MCP, RAG, vector DB, graph orchestration, memory, or similar concepts may be exploration vocabulary. Classify them as hard constraint, preference, or hypothesis before architecture. If an essential user-owned fact still prevents a meaningful first slice, ask one concrete question rather than handing the user a requirements form.

Guards:

- `solution-vocabulary-is-hypothesis`
- `one-question-only-when-outcome-blocked`

### Provider adoption security review — `understand-review`

Derived from public AutoAgent issue #96 plus the current `main` implementation at capture time.

Lesson: a review exists to support a decision. Verify material external claims against current source when practical, contextualize risk to the intended usage, keep unknowns explicit, and remain read-only unless implementation is requested.

Guards:

- `decision-frame-before-review`
- `current-source-before-conclusion`
- `risk-is-contextual`
- `review-is-read-only-by-default`

## v0.15 bounded-discovery pressure batch

This batch used three real repository shapes to test whether AAOP knew **when to stop reading**, not only what instruction files existed.

### Governance reference graph — `repo-recovery`

Public source: `YuemingHub/mingos-foundation`.

Lesson: an authoritative index is a navigation anchor, not a recursive coverage obligation. Start from current/canonical entrypoints and follow a reference only when it can resolve a material question affecting the route, baseline, target, acceptance evidence, or risk boundary.

Guards:

- `source-authority-freshness`
- `bounded-evidence-traversal`

### Small handoff repository — `repo-recovery`

Public source: `YuemingHub/ymai-website`.

Lesson: small repositories need less discovery, not the same ceremony compressed into fewer files. Once current state and one next target are defensible, stop; inspect implementation details only when the next engineering step needs them.

Guard:

- `bounded-evidence-traversal`

### Explicit read order beats historical scan — `repo-recovery`

Anonymized real-project source.

Lesson: project-declared first-read and historical-exclusion rules are discovery controls. Follow them before broad scanning; branch names and old deployment artifacts do not override an explicit current-state source.

Guards:

- `source-authority-freshness`
- `bounded-evidence-traversal`

### General rule earned by v0.15

```text
current request
→ governing instructions
→ declared current/canonical entrypoints
→ material unknown
→ one supporting reference if needed
→ relevant implementation/test/runtime evidence
→ stop
```

Reference graphs, directory size, and document counts do not create a duty to read more. Deeper traversal must be justified by a concrete unresolved question.

## v0.16 cross-repository scope pressure batch

This batch tested a related but distinct failure: **repository relevance can silently turn into repository work scope**.

### Repository map is not execution scope — `repo-recovery`

Public source: `YuemingHub/MingOS` (`README.md`, `docs/CROSS_REPOSITORY_COORDINATION.md`, `docs/FOUNDATION_DEPENDENCY.md`).

Lesson: repository maps define ownership and dependency edges. They do not automatically create a multi-repository task. Use the local dependency/coordination record while it is current and sufficient; cross to the claim owner only when material evidence is missing/stale, read the smallest authoritative source/revision, then return to the active repository.

Guards:

- `source-authority-freshness`
- `bounded-evidence-traversal`
- `cross-repository-scope-boundary`

### External repository evidence is not an active work target — `repo-recovery`

Public source: `YuemingHub/mingos-foundation` source registry.

Lesson: being useful evidence and being a mutation target are different states. Cross-repository reads require a material evidence reason; cross-repository writes require separate requested scope plus the target repository's own instructions and merge/risk gates.

Guards:

- `source-authority-freshness`
- `bounded-evidence-traversal`
- `cross-repository-scope-boundary`

### General rule earned by v0.16

```text
local decision
→ active repository/work target
→ identify external claim owner
→ check local dependency/coordination record
→ if current + sufficient: stay local
→ if stale/materially insufficient: read minimal external current source
→ record exact source/revision/status
→ return to local decision
```

Evidence access does not authorize mutation. A product finding does not become shared protocol/governance merely because AAOP can access both repositories.

## v0.17 execution-delta pressure batch

This batch tests what should happen **after** recovery has reconstructed enough truth to act.

### No local delta → do not invent work — `repo-recovery`

Public source: `YuemingHub/MingOS` current cross-repository coordination state.

Lesson: “continue autonomously” is execution authorization, not evidence that a new local protocol/schema/document change must exist. If current evidence shows meaningful next work is conditional on evidence that has not arrived yet, a verified no-local-mutation result is more correct than manufacturing a diff.

Guards:

- `bounded-evidence-traversal`
- `cross-repository-scope-boundary`
- `prove-delta-before-mutation`

### Concrete local delta → leave analysis and execute — `repo-recovery`

Public source: `YuemingHub/ymai-website` (`HANDOFF.md`, `data/site.ts`) plus the current accepted Foundation repository identity.

Lesson: the no-op rule must not become analysis paralysis. Once recovery proves a current local delta inside the requested action class, AAOP should make the smallest coherent change or reroute to the owning implementation route and continue through verification.

Guards:

- `source-authority-freshness`
- `bounded-evidence-traversal`
- `prove-delta-before-mutation`

### General rule earned by v0.17

```text
local-delta
→ execute smallest coherent change and verify

verified-no-op
→ desired state already holds / no local mutation currently justified
→ record evidence; do not manufacture a diff

reroute
→ real delta exists but belongs to another route/repository/action class

blocked
→ delta may exist but legitimate execution lacks evidence, environment, authorization,
   credential, external dependency, or product decision
```

The rule cuts both ways: no proven delta means no progress-theater mutation; a proven local authorized delta means AAOP should not remain in analysis.

## v0.18 write-precondition pressure batch

This batch tests what happens when an execution delta was valid when discovered, but the target changes before the mutation lands.

### Stale file write → re-read and reconcile — `feature-change`

Anonymized real AAOP repository operation.

A bounded README/current-doc edit was computed from content version A. Before the update landed, another repository change moved the same file to version B. GitHub rejected the stale conditional update because the expected content SHA no longer matched.

Lesson: the 409/precondition failure is new baseline evidence. Re-read B, preserve concurrent work, recompute the intended delta against B, and retry conditionally only if that delta still exists. Replaying the stale whole-file content from A—or forcing it through—would turn autonomy into data loss.

Guard:

- `revalidate-write-precondition`

### Stale PR head → old review is revision-scoped — `feature-change`

Public source: `YuemingHub/MingOS` PR #16 (`docs: establish three-repository coordination contract`).

The historical PR explicitly recorded that its branch had baseline drift and required re-check before merge. It stayed Draft/closed unmerged; later coordination work rebuilt the still-valid intent against a current baseline rather than treating the stale commit graph as the deliverable.

Lesson: review and CI evidence belong to the exact head/revision they validated. If the PR head or base moves, do not merge from stale evidence. Reconcile current main, salvage behavior/invariants/rationale, re-prove the delta, and merge only the newly validated head.

Guards:

- `stale-artifact-salvage`
- `behavior-over-commits`
- `revalidate-write-precondition`

### General rule earned by v0.18

```text
read baseline A
→ prove execution delta
→ before consequential write require/revalidate A
→ still A? write + verify
→ target is now B?
    re-read B
    preserve concurrent state
    recompute the intended delta
    rerun the execution-delta gate
    re-check authorization/risk if the action changed
    retry conditionally from B only if still justified
```

Use the strongest available native precondition: content/blob SHA, expected branch/PR head, ref ancestry, ETag/`If-Match`, resource version/generation, row version, lease/lock token, or deployment revision.

A precondition failure is first a **baseline/concurrency problem**, not a capability gap. `force` is a separate higher-risk decision, not the default recovery path.

## Adding future cases

Add a new pressure case when a real task reveals a repeatable orchestration error or dangerous near-miss.

A useful new case should answer:

1. What did a real developer ask?
2. What evidence was actually available?
3. What tempting wrong action existed?
4. What rule would have prevented it?
5. Is that rule route-specific or general?
6. Can the lesson be preserved without publishing private project content?

Do not invent cases simply to increase counts. The all-route coverage gate prevents accidental loss of an already-earned baseline; it does not justify synthetic examples.

If the lesson only says “use provider X,” it probably belongs in a Recipe or provider-selection test instead of a pressure guard.
