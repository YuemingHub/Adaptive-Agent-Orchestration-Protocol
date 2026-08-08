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
- continuing to inventory a small handoff repository after current state and the next target are already clear;
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

The public issue reports an unauthenticated command-execution TCP path. At capture time, current `docker_env.py` still maps the communication port to the host, while current `tcp_server.py` binds `0.0.0.0` and executes received command text through `shell=True` inside the container. Those source facts matter, but the review still must distinguish them from deployment-specific reachability, firewall configuration, workspace sensitivity, and the issue author's broader impact interpretation.

Lesson: a review exists to support a decision. Verify material external claims against current source when practical, contextualize risk to the intended usage, keep unknowns explicit, and remain read-only unless implementation is requested.

Guards:

- `decision-frame-before-review`
- `current-source-before-conclusion`
- `risk-is-contextual`
- `review-is-read-only-by-default`

## v0.15 bounded-discovery pressure batch

This batch used three real repository shapes to test whether AAOP v0.14 knew **when to stop reading**, not only what instruction files existed.

### Governance reference graph — `repo-recovery`

Public source: `YuemingHub/mingos-foundation`.

The repository has explicit current/canonical state and source-role records, but those authoritative documents link to a very large governance graph through `related`, `depends_on`, registries, RFCs, ADRs, and historical records.

Lesson: an authoritative index is a navigation anchor, not a recursive coverage obligation. Start from the current/canonical entrypoints and follow a reference only when it can resolve a material question affecting the route, baseline, target, acceptance evidence, or risk boundary.

Guards:

- `source-authority-freshness`
- `bounded-evidence-traversal`

### Small handoff repository — `repo-recovery`

Public source: `YuemingHub/ymai-website`.

The README and handoff already describe the prototype boundary, missing real capabilities, recommended integration order, and first real end-to-end Definition of Done.

Lesson: small repositories need less discovery, not the same ceremony compressed into fewer files. Once current state and one next target are defensible, stop; inspect implementation details only when the next engineering step needs them.

Guard:

- `bounded-evidence-traversal`

### Explicit read order beats historical scan — `repo-recovery`

Anonymized real-project source.

The repository has a long history, release/server documents, and a production-named branch, but the root instructions explicitly declare a short first-read order and exclude historical deployment/release records from ordinary current work.

Lesson: project-declared first-read and historical-exclusion rules are discovery controls. Follow them before broad scanning; branch names and old deployment artifacts do not override an explicit current-state source.

Guards:

- `source-authority-freshness`
- `bounded-evidence-traversal`

### General rule earned by this batch

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

## Adding future cases

Add a new pressure case when a real task reveals a repeatable orchestration error or dangerous near-miss.

A useful new case should answer:

1. What did a real developer ask?
2. What evidence was actually available?
3. What tempting wrong action existed?
4. What rule would have prevented it?
5. Is that rule route-specific or general?
6. Can the lesson be preserved without publishing private project content?

Do not invent cases simply to increase counts. The all-route coverage gate now prevents accidental loss of an already-earned baseline; it does not justify synthetic examples.

If the lesson only says “use provider X,” it probably belongs in a Recipe or provider-selection test instead of a pressure guard.
