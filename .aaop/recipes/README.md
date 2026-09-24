# AAOP Integration Recipes

Integration Recipes are **glue metadata**, not vendored dependencies and not an AAOP package manager.

The default answer to a capability question is **no new provider**: the current host, the repository, and existing standards come first (see `docs/ECOSYSTEM_MAP.md` and the provider-selection Skill). A recipe is written only when a surface has **real adoption evidence** (a proven pilot in a real consumer project) or documents a **format lineage AAOP itself depends on**. Conditional provider knowledge that has not been adopted stays as escalation vocabulary inside the Route Capability Packs and `registries/providers.json`; it does not get a recipe.

A recipe tells the orchestrator, in one predictable shape:

- when an upstream provider is justified;
- how to detect whether it is already present;
- the smallest known upstream installation path;
- credentials/permissions that may be required;
- optional, time-stamped provider-adoption review debt that must be rechecked for a relevant surface/context;
- how to verify the original capability gap is closed;
- how to remove or disable the integration.

## Current recipes

- `loopx.json` — long-running execution-control provider; qualified in a real consumer pilot (`docs/LOOPX_PILOT_EVIDENCE.md`).
- `agent-skills.json` — the Agent Skills file format (`https://agentskills.io`), which AAOP's own canonical Skills follow; `install.mode` is `none`.

## Detection contract

`.aaop/tools/doctor.py` consumes recipe `detect` hints so provider recognition stays with the integration knowledge rather than becoming a second hard-coded catalog.

Supported baseline hints:

- `commands` — executable names resolved on `PATH`;
- `python_packages` — Python distribution or top-level import package names visible to the active interpreter;
- `node_packages` — dependencies declared in the target project's root `package.json`;
- `files` — project-root-relative file/directory glob patterns.

Detection hints must be **provider-specific**. Do not use generic signals such as `package.json`, `pyproject.toml`, or `requirements.txt` by themselves: their presence says nothing about a particular provider and creates false positives.

A detection result means only **"evidence this provider is already present."** It does not mean:

- the current route needs it;
- it is configured correctly;
- it has sufficient permissions;
- it is safe/trusted;
- AAOP should activate or keep it.

The Route Capability Pack and provider-selection policy still decide relevance.

## Adoption review contract

A Recipe may optionally contain `adoption_review` when a real review has uncovered a **specific, reusable adoption concern that is easy to forget and important enough to re-check later**.

This field is intentionally not a vulnerability database, allowlist, denylist, certification, or permanent security label.

It records:

- `reviewed_at` — when the observation was last checked;
- `scope` — which provider mode/surface/context the observation applies to;
- `reason` — why future adoption needs a deliberate re-check;
- `decision_effect` — informational, reverify-before-adoption, or conditional-adoption-only;
- `current_observations` — what was actually observed at that date;
- `sources` — evidence locations to revisit;
- `required_checks` — what must be re-evaluated against current upstream and the actual deployment context;
- optional notes explaining uncertainty or retirement conditions.

### What it does not mean

A recorded concern does **not** mean:

```text
provider is globally unsafe
provider is permanently banned
issue report is maintainer-confirmed fact
all provider surfaces share the same risk
old observations override current upstream source
```

The orchestrator must re-check the concern before consequential adoption when the intended surface falls within its scope.

If upstream has fixed the mechanism, the intended mode does not use it, or the actual environment makes the concern irrelevant, the old observation should not block adoption. Update or retire the Recipe review instead of carrying stale fear indefinitely.

If the concern remains relevant and cannot be mitigated within the user's authorization/risk boundary, prefer a narrower provider surface, isolated deployment, another provider, or no new provider yet.

This is best thought of as **remembered review debt**: AAOP remembers what deserves another look, not what conclusion must be reached forever.

## Safety rule

Before executing an install command, re-check `source_of_truth` when network access is available. Recipes carry `last_verified` because external projects change faster than the AAOP protocol.

If `adoption_review` applies, also re-check its sources and conditions before enabling the relevant provider surface.

A recipe MUST NOT silently install anything merely because it exists or because the Doctor detects it.

## Contract

Recipes are resolver hints, not security endorsements. Consequential adoption still requires current provenance, permission, data exposure, cost, maintenance, operational context, and rollback review.
