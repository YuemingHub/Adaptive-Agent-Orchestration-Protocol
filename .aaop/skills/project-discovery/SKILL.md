---
name: project-discovery
description: Build a grounded environment and project profile before planning or editing. Use for new repositories, unfamiliar projects, broad requests, architecture work, or any task where hidden project constraints could change the solution.
license: Apache-2.0
metadata:
  aaop-version: "0.7.0"
---

# Project Discovery

## Goal

Create the minimum accurate model of the environment and project needed to make the next decision safely. Do not read everything by default, and do not flatten every discovered artifact into equally trustworthy truth.

## Inputs

- user request and current conversation context;
- workspace/repository access;
- host capabilities;
- project instruction files;
- relevant connected sources if the project depends on them.

## Workflow

1. **Resolve instruction scope.** Read host and repository instruction files that govern the files or systems likely to be touched.
2. **Inventory the environment.** If `.aaop/tools/doctor.py` exists, run it read-only (optionally with the current `--route`) and use its project/toolchain/provider evidence instead of guessing what is installed. The inventory is evidence, not a recommendation.
3. **Identify host capability.** Note available read/write/search/shell/browser/Skill/MCP/subagent features and permission boundaries that may not be visible to the filesystem doctor.
4. **Find candidate sources of truth.** Inspect README/product docs, architecture/ADRs, status files, issues/PRs, release/runbook material, tests/CI, runtime evidence, and scoped instructions relevant to the decision.
5. **Classify material evidence by authority and freshness.** For claims that can change the route or implementation, record at least:
   - source/reference;
   - what claim/topic it supports;
   - role such as `current-fact`, `governance`, `reference`, `draft/proposed`, `historical`, or `unknown` when the project makes that distinction;
   - version/branch/commit/date or other freshness signal when available;
   - whether a newer or more authoritative source contradicts it.
   Project-declared terminology takes precedence over these generic labels.
6. **Find project intent.** Prefer explicitly authoritative product/architecture/governance sources over inferring intent from existing code alone. A merged file can still be Draft; a detailed file can still be historical.
7. **Map implementation.** Inspect manifests, entrypoints, module boundaries, data models, API surfaces, tests, CI and deployment configuration relevant to the request. Use doctor project signals as pointers, not proof of behavior.
8. **Check runtime evidence** when static inspection cannot answer a material question. Prefer a focused test/command over speculation.
9. **Record contradictions without erasing them.** Distinguish current intent from legacy implementation, generated files, experiments, stale docs, old PRs, and unverified issue comments. If authority/freshness do not justify a winner, keep the conflict or unknown explicit.
10. **Stop when sufficient.** Discovery is complete when more reading is unlikely to change the immediate route, current baseline, capability plan, or risk model.

## Evidence authority rules

- `main` / `production` / merged status does not by itself mean a document is accepted policy or current operational fact.
- newest timestamp does not automatically beat an explicitly designated current-fact or governance source.
- open/draft PRs and old branches are evidence of intent/history, not current implementation authority.
- issue comments and prior AI conclusions are hypotheses/reference unless independently supported.
- deployed/runtime facts require target-environment evidence; repository state is not a substitute.
- preserve original contradictory evidence. Do not rewrite a source merely to make the project appear internally consistent.

## Output

Produce or hold a Project Profile containing:

- project type;
- intended outcome;
- lifecycle stage;
- architecture / major modules;
- technology stack;
- current implementation baseline;
- current state relevant to the request;
- governing constraints;
- testing and deployment model;
- known risks;
- unresolved material questions/conflicts;
- evidence sources inspected, with material authority/freshness notes;
- material existing capabilities/providers already available.

When useful:

- serialize environment evidence to `.aaop/runtime/environment-inventory.json` against `.aaop/schemas/environment-inventory.schema.json`;
- serialize the synthesized project model to `.aaop/runtime/project-profile.json` against `.aaop/schemas/project-profile.schema.json`.

## Quality checks

- Presence of a package/config/CLI does not prove it should be used for the current route.
- No important project claim should rely solely on filenames when file contents/runtime evidence are available.
- Do not treat current implementation as product intent without corroboration.
- Do not treat historical/draft evidence as current fact merely because it is concrete or detailed.
- Do not ask the user for information already available in repository or connected context.
- Do not spend context inventorying unrelated modules.
- Do not recommend installing a provider before checking whether the capability is already present.
