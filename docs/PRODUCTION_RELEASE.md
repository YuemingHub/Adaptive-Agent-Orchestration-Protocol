# AAOP Production Release Contract

AAOP does not become production-ready because a version number changes or because one pull request is green. Production eligibility is the conjunction of package, lifecycle, continuity, platform, supply-chain, and downstream-consumer evidence.

## Production release line

AAOP v1.0 establishes the first production release line.

The user-facing production channel is:

```text
stable
```

`main` remains the development/edge branch. A commit landing on `main` never promotes itself to production automatically.

## Release candidate gate

A candidate is eligible for production promotion only when all of the following are true on the final candidate tree:

1. `.aaop/VERSION` matches `.aaop/PRODUCTION_RELEASE.json`;
2. README Status identifies the same production release line;
3. `idea-to-production` Journey has canonical, non-experimental status;
4. every workflow listed in `.aaop/PRODUCTION_RELEASE.json` exists;
5. all required workflows pass on the final candidate head;
6. external GitHub Actions are pinned to reviewed immutable commit SHAs;
7. long-lived validation workflows retain read-only repository contents permission;
8. transactional lifecycle fault injection passes;
9. Journey CAS/lock/schema/recovery regressions pass;
10. platform support matrix passes across the declared Python/OS surfaces;
11. install provenance regressions pass without expanding ownership authority;
12. a real downstream consumer validates the **exact candidate tree** while preserving that consumer's own project authority and continuity rules;
13. if the PR base/head changes after any material review evidence, affected validation is rerun before merge.

The machine-readable static portion of this contract is validated by:

```text
validate-production-release
```

The final merge/promotion controller must additionally verify current GitHub workflow conclusions and downstream-consumer evidence; a repository file cannot truthfully certify a future GitHub run by itself.

## Downstream consumer validation

The consumer check is not “can Python import AAOP?” It must exercise a real project boundary.

At minimum:

- use a real AAOP consumer repository with its own project instructions/authority surfaces;
- validate the exact release-candidate commit/ref, not whatever `stable` happens to point to before promotion;
- install or upgrade without overwriting consumer-owned project rules;
- run `aaop.py ready` and health/provenance checks;
- preserve existing `.aaop/runtime` continuity when upgrading an existing consumer;
- verify that project-specific authority/current-state files still outrank AAOP history/checkpoints;
- run the consumer's own relevant validation when its CI/runtime is available;
- if consumer executable validation is externally blocked, do not count static inspection as the downstream production gate.

A failure found downstream returns to the AAOP release candidate as a real compatibility defect. Do not waive it merely because AAOP's own workflows are green.

## Stable promotion

Promotion is deliberately separate from merge:

```text
candidate PR head
  ↓ all AAOP gates green + downstream exact-candidate validation
merge to main
  ↓ verify merged tree preserves candidate tree / no base drift
stable fast-forward → merged validated commit
```

Rules:

- `stable` is moved only after the candidate is merged;
- promotion is a non-force fast-forward;
- never make ordinary `main` pushes auto-advance `stable`;
- re-read the merged commit before promotion;
- if the merged tree differs materially from the consumer-validated candidate, revalidate before moving `stable`.

## Rollback / bad production release

`stable` is a monotonic production channel. Do not silently force-move it backward to an old commit as routine rollback.

If a production defect is discovered:

1. classify the defect and affected release;
2. prepare a minimal repair or explicit revert **as a new forward commit**;
3. run the same relevant AAOP gates plus downstream compatibility evidence;
4. merge the repair;
5. fast-forward `stable` to the repaired/reverted tree.

Consumers pinned to an exact commit remain pinned until they deliberately change that pin. Consumers following `stable` receive the next promoted repair when they next upgrade.

Emergency repository-owner intervention may require a different control-plane action, but it must be recorded explicitly as an emergency exception rather than becoming the normal release mechanism.

## Required production evidence classes

### Package lifecycle

- bounded bootstrap download/extraction;
- explicit stable/edge/exact-ref semantics;
- transactional install/upgrade/uninstall;
- interrupted lifecycle detection and explicit recovery;
- manifest path/schema fail-closed behavior.

### Journey continuity

- one current Route under a long-horizon Journey;
- cross-session continuation;
- revision CAS + OS locking;
- completed release-cycle isolation;
- future checkpoint schema fail-closed behavior;
- explicit last-good recovery with damaged-state preservation.

### Platform

See `docs/PLATFORM_SUPPORT.md`.

### Provenance

See `docs/INSTALL_PROVENANCE.md`.

### CI supply chain

See `docs/CI_SUPPLY_CHAIN.md`.

## Why v1.0 does not freeze all future design

Production-ready means the current contracts are safe and operationally supportable for their declared surfaces. It does not mean AAOP will never evolve.

Future changes may add routes, providers, schemas, or release capabilities, but they must preserve versioning/upgrade boundaries. A future schema must not be silently downgrade-managed by an older tool; a new provider must not become a default dependency merely because it exists; a new release gate must be added explicitly to the machine-readable production contract.

## Production declaration

A v1.0 source tree may describe the production release contract before it is promoted. The authoritative runtime distribution statement is:

> **A commit is an AAOP production release only when the `stable` channel points to that fully gated commit after the required downstream consumer validation.**

The README Status and package version describe the release line; `stable` + release evidence determine actual production promotion.
