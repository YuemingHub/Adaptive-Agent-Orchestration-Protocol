# Routing Model

AAOP routes are not permanent project categories. They describe the **best next development path** for the current observable outcome.

## Route transitions

Common transitions:

```text
idea-to-build → feature-change
repo-recovery → bug-fix
repo-recovery → feature-change
feature-change → release-operations
bug-fix → release-operations
understand-review → feature-change
understand-review → bug-fix
```

A route may also correct itself when evidence disproves the original framing.

Example:

```text
User asks for “a retry feature”
        ↓
feature-change
        ↓ inspect existing code
existing retry path is present but broken
        ↓
bug-fix
```

The correction is success, not routing failure.

## Route selection invariant

Select the route that determines the correct **first irreversible engineering assumption**.

When two routes are plausible, prefer the one that:

1. preserves more existing information;
2. performs more reversible discovery first;
3. reduces the largest immediate uncertainty/blocker;
4. avoids creating redundant architecture;
5. reaches observable evidence sooner.

## Secondary intents

Do not lose user intent when choosing one primary route. Keep secondary intents queued, but do not execute them prematurely.

Example:

```yaml
primary_route: bug-fix
queued_secondary_intents:
  - repo-recovery
  - feature-change: coupons
```

Re-evaluate queued intents after the primary route reaches a stable checkpoint.

## Route completion is not project completion

Completing `repo-recovery` may only mean the project now has a trustworthy state map and a verified next target. It should then naturally transition to another route.

Completing `feature-change` may transition to `release-operations` if deployment was part of the user's original request.

AAOP should therefore optimize for **continuous state transition**, not one giant workflow selected at the beginning.