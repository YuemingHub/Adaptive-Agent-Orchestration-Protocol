# AAOP CI Supply-Chain Contract

AAOP's production gate is only as stable as the code that executes that gate. A workflow that says `actions/checkout@v6` or `actions/setup-python@v6` is still delegating execution to a movable ref.

AAOP therefore treats third-party GitHub Action revisions as production dependencies.

## Current reviewed pins

The permanent validator registry currently approves:

```text
actions/checkout@d23441a48e516b6c34aea4fa41551a30e30af803  # v6 at review time
actions/setup-python@ece7cb06caefa5fff74198d8649806c4678c61a1  # v6 at review time
```

These are not chosen merely because they were the newest revisions. They are the exact Action commits that were already exercised by the full AAOP production gate set immediately before the repository was pinned.

## Permanent rule

Every external `uses:` target in `.github/workflows/*.yml` / `*.yaml` must:

1. use a full lowercase 40-hex commit SHA;
2. appear in the reviewed registry in `scripts/validate_ci_supply_chain.py`;
3. match the exact approved SHA for that Action;
4. run under workflows whose repository contents permission remains read-only.

Local actions referenced through `./...` are not external supply-chain dependencies and are not subject to the external registry.

The permanent workflow:

```text
validate-ci-supply-chain
```

fails if a mutable tag/branch is reintroduced, an unreviewed external Action appears, an approved Action silently moves to a different SHA, or a long-lived workflow requests `contents: write`.

## Updating an Action

An Action update is a deliberate dependency review, not routine string replacement.

Required sequence:

1. inspect the upstream Action change/release and identify the exact candidate commit SHA;
2. update the reviewed registry and all workflow references in one isolated PR;
3. keep the human-readable major/release comment next to the SHA for maintainability;
4. run the **entire** AAOP production gate set with the candidate Action revision, including platform, lifecycle, Journey recovery, provenance, and supply-chain validation;
5. do not merge if only the supply-chain validator is green while another AAOP gate regresses;
6. only after merge and the broader release gate may a new AAOP stable candidate be promoted.

## Permission boundary

Normal AAOP validation workflows use:

```yaml
permissions:
  contents: read
```

AAOP does not keep a standing GitHub Actions workflow with repository write permission merely to make dependency maintenance convenient.

The one-time migration that originally converted the repository from movable `@v6` tags to reviewed SHAs used a branch-scoped temporary write workflow. GitHub correctly refused that workflow's App token from updating workflow refs without the separate workflows permission. The migration was completed through separately authorized Git Data assembly, and all temporary workflow-write machinery was removed before the candidate became merge-eligible.

That history is useful evidence for the permanent rule: **do not widen runtime/CI permissions to bypass a supply-chain control-plane blocker.**

## What pinning proves—and does not prove

A commit SHA pin prevents a workflow from silently executing a different upstream revision because a tag/branch moved.

It does not by itself prove:

- the pinned upstream code is benign;
- GitHub-hosted runner images never change;
- the Action's own transitive downloads are immutable;
- AAOP's source repository is a cryptographic trust root;
- a green CI run proves downstream application behavior.

AAOP therefore combines immutable Action refs with its own platform/lifecycle/Journey/provenance gates and downstream consumer validation rather than treating SHA pinning as complete supply-chain security.
