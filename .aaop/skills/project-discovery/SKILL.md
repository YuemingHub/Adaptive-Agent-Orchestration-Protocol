---
name: project-discovery
description: Build a grounded environment and project profile before planning or editing. Use for new repositories, unfamiliar projects, broad requests, architecture work, or any task where hidden project constraints could change the solution.
license: Apache-2.0
metadata:
  aaop-version: "0.1.0"
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
2. **Identify host capability.** Note available read/write/search/shell/browser/Skill/MCP/subagent features and permission boundaries.
3. **Find project intent.** Prefer README, product/architecture docs, ADRs, roadmap, issue/PR context, and explicit domain principles over inferring intent from existing code alone.
4. **Map implementation.** Inspect manifests, entrypoints, module boundaries, data models, API surfaces, tests, CI and deployment configuration relevant to the request.
5. **Check runtime evidence** when static inspection cannot answer a material question. Prefer a focused test/command over speculation.
6. **Record contradictions.** Distinguish intended architecture from legacy implementation, generated files, experiments, or stale docs.
7. **Stop when sufficient.** Discovery is complete when more reading is unlikely to change the immediate capability plan or risk model.

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
- evidence sources inspected.

When useful, serialize to `.aaop/runtime/project-profile.json` using `.aaop/schemas/project-profile.schema.json`.

## Quality checks

- No important claim should rely solely on filenames when file contents are available.
- Do not treat current implementation as product intent without corroboration.
- Do not ask the user for information already available in the repository or connected context.
- Do not spend context inventorying unrelated modules.
