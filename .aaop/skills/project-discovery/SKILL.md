---
name: project-discovery
description: Build a grounded environment and project profile before planning or editing. Use for new repositories, unfamiliar projects, broad requests, architecture work, or any task where hidden project constraints could change the solution.
license: Apache-2.0
metadata:
  aaop-version: "0.6.0"
---

# Project Discovery

## Goal

Create the minimum accurate model of the environment and project needed to make the next decision safely. Do not read everything by default.

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
4. **Find project intent.** Prefer README, product/architecture docs, ADRs, roadmap, issue/PR context, and explicit domain principles over inferring intent from existing code alone.
5. **Map implementation.** Inspect manifests, entrypoints, module boundaries, data models, API surfaces, tests, CI and deployment configuration relevant to the request. Use doctor project signals as pointers, not proof of behavior.
6. **Check runtime evidence** when static inspection cannot answer a material question. Prefer a focused test/command over speculation.
7. **Record contradictions.** Distinguish intended architecture from legacy implementation, generated files, experiments, or stale docs.
8. **Stop when sufficient.** Discovery is complete when more reading is unlikely to change the immediate route, capability plan, or risk model.

## Output

Produce or hold a Project Profile containing:

- project type;
- intended outcome;
- lifecycle stage;
- architecture / major modules;
- technology stack;
- current state relevant to the request;
- governing constraints;
- testing and deployment model;
- known risks;
- unresolved material questions;
- evidence sources inspected;
- material existing capabilities/providers already available.

When useful:

- serialize environment evidence to `.aaop/runtime/environment-inventory.json` against `.aaop/schemas/environment-inventory.schema.json`;
- serialize the synthesized project model to `.aaop/runtime/project-profile.json` against `.aaop/schemas/project-profile.schema.json`.

## Quality checks

- Presence of a package/config/CLI does not prove it should be used for the current route.
- No important project claim should rely solely on filenames when file contents/runtime evidence are available.
- Do not treat current implementation as product intent without corroboration.
- Do not ask the user for information already available in repository or connected context.
- Do not spend context inventorying unrelated modules.
- Do not recommend installing a provider before checking whether the capability is already present.
