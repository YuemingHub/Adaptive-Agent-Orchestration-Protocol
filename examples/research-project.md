# Example: Research / Strategy Task

## User outcome

> Research whether our product should adopt a new interoperability standard. Compare the real benefits, migration cost, maturity, and risks, then make a recommendation backed by current primary sources.

## Discovery result

Assume:

- no implementation is requested yet;
- the repository already contains architecture principles and a legacy internal format;
- web access is available;
- no special external account is required.

## Capability plan

```text
project-discovery        → repository reading
research                 → web/native research provider
standards-analysis       → main reasoning context
migration-impact         → architecture/code inspection
independent-challenge    → reviewer context
verification             → source cross-check + claim/evidence audit
```

## Team decision

Two contexts are enough:

1. **Research Lead** — gather primary sources, map current system and prepare recommendation.
2. **Challenge Reviewer** — test the recommendation against counterarguments, migration cost and unsupported claims.

Do not create engineering implementation agents because implementation is outside the requested outcome.

## Tool resolution

Current web/repository tools satisfy all capabilities. No MCP installation is justified.

## Execution graph

```text
Project principles ─┐
Current format ─────┼→ Gap/impact model → Recommendation → Challenge review → Final decision memo
Primary sources ────┘
```

## Completion evidence

- current primary sources support all time-sensitive claims;
- current project constraints are explicitly mapped to the recommendation;
- migration cost/compatibility risks are addressed;
- reviewer identifies no unaddressed decisive counterargument;
- final recommendation distinguishes facts, assumptions and judgment.
