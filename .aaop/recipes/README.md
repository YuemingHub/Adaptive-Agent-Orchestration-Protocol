# AAOP Integration Recipes

Integration recipes are **glue metadata**, not vendored dependencies and not an AAOP package manager.

A recipe tells the orchestrator, in one predictable shape:

- when an upstream provider is justified;
- how to detect whether it is already present;
- the smallest known upstream installation path;
- credentials/permissions that may be required;
- how to verify the original capability gap is closed;
- how to remove or disable the integration.

## Safety rule

Before executing an install command, re-check `source_of_truth` when network access is available. Recipes carry `last_verified`, because external projects change faster than the AAOP protocol.

A recipe MUST NOT silently install anything merely because it exists.

## Developer experience

The intended flow is:

```text
User states outcome
  ↓
AAOP proves a capability gap
  ↓
Provider is selected
  ↓
Recipe gives the agent one integration path
  ↓
Agent asks only for any genuinely required credential/high-risk permission
  ↓
Upstream package manager/installer performs installation
  ↓
AAOP runs recipe verification
  ↓
Keep the provider only if the gap is closed
```

This removes the need for the developer to manually hunt across multiple repositories while still avoiding an all-in-one distribution.

## Contract

Recipes should conform to `../schemas/integration-recipe.schema.json`.

They are resolver hints, not security endorsements. Consequential adoption still requires provenance, permission, data exposure, cost, maintenance, and rollback review.
