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

Lesson: early mentions of Agent, MCP, RAG, vector DB, graph orchestration, memory, or similar concepts may be exploration vocabulary. Classify them as hard constraint, preference, or hypothesis before architecture. If an essential user-owned product fact is still missing, ask one concrete question rather than handing the user a requirements form.

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

The repository explicitly separates principle/governance, shared protocol/kernel, and family-product responsibilities. Its coordination record is Proposed navigation, not a replacement for each repository's current fact sources. The downstream Foundation dependency record is also Proposed and requires an upstream refresh only when a new release/protocol/cross-repository claim makes the recorded baseline material.

Lesson: repository maps define ownership and dependency edges. They do not automatically create a multi-repository task. Use the local dependency/coordination record while it is current and sufficient; cross to the claim owner only when material evidence is missing/stale, read the smallest authoritative source/revision, then return to the active repository.

Guards:

- `source-authority-freshness`
- `bounded-evidence-traversal`
- `cross-repository-scope-boundary`

### External repository evidence is not an active work target — `repo-recovery`

Public source: `YuemingHub/mingos-foundation` source registry.

The source registry distinguishes canonical Foundation governance from scope-limited product/implementation evidence and explicitly prevents external product repositories from becoming automatic active work targets.

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

At capture time, the shared protocol/kernel repository had recently merged its coordination refresh. The current coordination order says the family product should continue generating real/product evidence, and only cross-scenario patterns that repeatedly generalize should rise into MingOS protocol candidates.

Lesson: “continue autonomously” is execution authorization, not evidence that a new local protocol/schema/document change must exist. If current evidence shows meaningful next work is conditional on evidence that has not arrived yet, a verified no-local-mutation result is more correct than manufacturing a diff.

Guards:

- `bounded-evidence-traversal`
- `cross-repository-scope-boundary`
- `prove-delta-before-mutation`

### Concrete local delta → leave analysis and execute — `repo-recovery`

Public source: `YuemingHub/ymai-website` (`HANDOFF.md`, `data/site.ts`) plus the current accepted Foundation repository identity.

The handoff says the site should preserve its current product language and progressively integrate real capabilities rather than be broadly rewritten. At capture time, its centralized site configuration still defaulted the Foundation link to historical `YuemingHub/Ming-Foundation`, while the current accepted repository identity is `YuemingHub/mingos-foundation`.

Lesson: the no-op rule must not become analysis paralysis. Once recovery proves a current local delta inside the requested action class, AAOP should make the smallest coherent change or reroute to the owning implementation route and continue through verification.

Guards:

- `source-authority-freshness`
- `bounded-evidence-traversal`
- `prove-delta-before-mutation`

### General rule earned by v0.17

Before a material mutation, classify the difference between the desired/route outcome and current evidence:

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

The rule cuts both ways:

- **no proven delta** → do not mutate merely to demonstrate progress;
- **proven local authorized delta** → do not remain in analysis merely to avoid risk.

Repository-specific planning, testing, review, and release gates still apply after a delta is proven.

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
