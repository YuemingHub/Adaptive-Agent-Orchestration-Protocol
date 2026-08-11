# Pre-Mutation Reconciliation Policy

Status: normative cross-route policy for existing-project mutation.

## Purpose

AAOP must not execute quickly against an untrusted picture of the project.

Before the first material mutation of an **existing** project or deployed resource, establish that the baseline used to compute the change is trustworthy enough for that change. This is a cross-route invariant, not a project-specific onboarding flow, not a new workflow engine, and not a mandatory snapshot document.

The policy applies when `bug-fix`, `feature-change`, `repo-recovery`, or `release-operations` will mutate existing code, configuration, tests, documentation, data, deployment state, or another existing resource.

## Minimum reconciliation surface

Reconcile only the facts that can change the immediate route, delta, write target, acceptance evidence, or risk boundary:

1. **Active work target** — repository/resource plus current branch/ref/environment/destination when material.
2. **Requested outcome** — what observable state the current work is trying to make true.
3. **Current baseline** — implementation/runtime/deployment state relevant to the change.
4. **Evidence authority and freshness** — which sources own which claims and whether they are current, historical, draft/reference, or unknown.
5. **Material contradictions** — disagreements among code, tests, state/handoff documents, runtime evidence, adapters, CI, deployment records, specs, or historical artifacts.
6. **Acceptance baseline** — which tests/checks/reviews currently prove the desired behavior and which evidence becomes stale if its governing assumption changed.
7. **Unknowns** — facts that cannot be established from available evidence and therefore must remain unknown.

Do not inventory the whole repository merely to satisfy this policy. Stop when the immediate mutation decision is defensible.

## Evidence rules

- A test is evidence about an expected behavior; it is not automatically the highest authority for product identity, current deployment state, user state, policy, or another external fact.
- A failing test may prove a product defect, a test defect, a stale assertion, an environment mismatch, or an unresolved contract conflict. Classify before fixing.
- A state/status/handoff file may be authoritative for some claims and stale for others. Respect project-declared scope and freshness.
- Current code proves what is implemented, not necessarily what is intended.
- Runtime/target facts require runtime/target evidence when they materially affect the decision.
- Historical PRs, branches, comments, old names, cached adapters, generated bridges, and prior AI conclusions remain historical/reference evidence until reconciled.
- `unknown` is a first-class state. Do not silently convert unknown into `false`, absent, disabled, unused, non-production, or any other negative assertion.
- Newest timestamp, default branch, merged status, or most detailed document does not automatically win an authority conflict.

## Mutation gate

Before the first material mutation, classify the reconciled result:

- **trusted-current-delta** — enough current evidence agrees on the baseline and a real authorized delta exists; continue in the owning route.
- **stale-derived-evidence** — current authoritative evidence is sufficient, but a derived test/adapter/report/assertion still encodes an old assumption; update only the stale derived surface and re-establish affected evidence.
- **material-conflict** — sources disagree and authority/freshness do not justify a winner; preserve the conflict and use `repo-recovery` or a human-owned decision when required.
- **unknown-blocker** — a fact required to execute safely cannot currently be established; keep it unknown and block only the affected action.
- **verified-no-op** — the requested state already holds or no current mutation is justified.

Do not change current product behavior merely to satisfy stale derived evidence. Do not rewrite historical sources merely to make the repository look internally consistent.

## Relationship to route execution

This policy strengthens the existing AAOP execution-delta gate:

```text
request / continuation
  -> inspect current evidence
  -> reconcile material authority + freshness
  -> classify contradictions / unknowns / stale derived evidence
  -> prove current execution delta
  -> mutate the explicit authorized target
  -> revalidate write precondition
  -> verify on the new baseline
```

For a tiny, obvious edit in a trustworthy project, reconciliation may be a few reads and one current test. For a contradictory long-running project, it may require `repo-recovery`. The amount of process scales with uncertainty and risk, not repository size.

## Project independence

AAOP Core must not encode product names, organization names, domain actors, fixed status filenames, brand strings, deployment conventions, or project-specific state fields in this policy.

A project may declare its own authoritative sources, status vocabulary, adapters, and invariants. AAOP consumes those declarations as evidence; it does not replace them with a universal product schema.

Real consumer projects should feed anonymized/public pressure cases back into AAOP only when a failure pattern generalizes across projects.