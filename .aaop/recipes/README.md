# AAOP Integration Recipes

Integration Recipes are **glue metadata**, not vendored dependencies and not an AAOP package manager.

A recipe tells the orchestrator, in one predictable shape:

- when an upstream provider is justified;
- how to detect whether it is already present;
- the smallest known upstream installation path;
- credentials/permissions that may be required;
- how to verify the original capability gap is closed;
- how to remove or disable the integration.

## Detection contract

`.aaop/tools/doctor.py` consumes recipe `detect` hints so provider recognition stays with the integration knowledge rather than becoming a second hard-coded catalog.

Supported baseline hints:

- `commands` — executable names resolved on `PATH`;
- `python_packages` — Python distribution or top-level import package names visible to the active interpreter;
- `node_packages` — dependencies declared in the target project's root `package.json`;
- `files` — project-root-relative file/directory glob patterns.

Detection hints must be **provider-specific**. Do not use generic signals such as `package.json`, `pyproject.toml`, or `requirements.txt` by themselves: their presence says nothing about a particular provider and creates false positives.

A detection result means only **“evidence this provider is already present.”** It does not mean:

- the current route needs it;
- it is configured correctly;
- it has sufficient permissions;
- it is safe/trusted;
- AAOP should activate or keep it.

The Route Capability Pack and provider-selection policy still decide relevance.

## Safety rule

Before executing an install command, re-check `source_of_truth` when network access is available. Recipes carry `last_verified` because external projects change faster than the AAOP protocol.

A recipe MUST NOT silently install anything merely because it exists or because the Doctor detects it.

## Developer experience

```text
User states outcome
  ↓
Developer Intake selects current route
  ↓
Doctor inventories what already exists
  ↓
Route Capability Pack requires capability X
  ↓
Can current environment satisfy X?
  ├─ yes → reuse it
  └─ no  → prove the gap
             ↓
          Provider selected
             ↓
          Recipe gives one integration path
             ↓
          Ask only for genuinely required credential/high-risk permission
             ↓
          Upstream package manager/host performs installation
             ↓
          AAOP verifies the original gap closed
```

This removes the need for developers to manually hunt across repositories while avoiding an all-in-one distribution and avoiding repeated installation of capabilities they already have.

## Contract

Recipes should conform to `../schemas/integration-recipe.schema.json`.

They are resolver hints, not security endorsements. Consequential adoption still requires provenance, permission, data exposure, cost, maintenance, and rollback review.
