---
name: project-discovery
description: Build a grounded environment and project profile before planning or editing. Use for new repositories, unfamiliar projects, broad requests, architecture work, or any task where hidden project constraints could change the solution.
license: Apache-2.0
metadata:
  aaop-version: "0.15.0"
---

# Project Discovery

## Goal

Create the minimum accurate model of the environment and project needed to make the next decision safely. Do not read everything by default, do not flatten every discovered artifact into equally trustworthy truth, and do not mistake a repository's reference graph for a mandatory reading list.

## Inputs

- user request and current conversation context;
- workspace/repository access;
- host capabilities;
- project instruction files and host-specific scoped rules;
- relevant connected sources if the project depends on them.

## Workflow

1. **Define the decision horizon.** State internally what this discovery must make possible now: select/confirm the route, reconstruct the current baseline, locate one target path, frame a review decision, or establish a risk/authorization boundary. Do not expand discovery merely because more repository knowledge exists.
2. **Resolve instruction scope.** Read the host/repository instructions that govern the files or systems likely to be touched. If the repository is unfamiliar, a monorepo, contains nested instruction files/rules, or the current working scope is unclear, use `.aaop/tools/instructions.py . --json` when available to inventory Codex/Claude/Cursor instruction topology before assuming the root bootstrap is the whole effective rule set. The topology is read-only evidence: do not auto-edit nested rules or infer semantic conflict resolution from filenames alone.
3. **Honor explicit entrypoints.** If project instructions or accepted/current status documents declare a first-read order, current-state file, source registry, product contract, or excluded historical sources, use that declared navigation before broad search. Project-declared source roles override generic discovery habits.
4. **Inventory the environment only as needed.** If `.aaop/tools/doctor.py` exists, run it read-only (optionally with the current `--route`) when environment/provider evidence can change the next decision. The inventory is evidence, not a recommendation or a mandatory ritual for every small task.
5. **Identify host capability.** Note available read/write/search/shell/browser/Skill/MCP/subagent features and permission boundaries that may not be visible to filesystem tools.
6. **Find candidate sources of truth.** Start from the smallest authoritative entrypoint set that can answer the decision horizon: for example repository instructions + current status + product/architecture source, or README + handoff + manifest in a small project.
7. **Traverse evidence by question, not by graph size.** Treat `related`, `depends_on`, link lists, indexes, registries, ADR/RFC references, historical release lists, and directory inventories as navigation. Follow a reference only when it can resolve a material unknown, contradiction, route choice, implementation target, acceptance condition, or risk boundary. Do not recursively read every referenced artifact merely because it is linked from an authoritative document.
8. **Classify material evidence by authority and freshness.** For claims that can change the route or implementation, record at least:
   - source/reference;
   - what claim/topic it supports;
   - role such as `current-fact`, `governance`, `reference`, `draft/proposed`, `historical`, or `unknown` when the project makes that distinction;
   - version/branch/commit/date or other freshness signal when available;
   - whether a newer or more authoritative source contradicts it.
   Project-declared terminology takes precedence over these generic labels.
9. **Find project intent.** Prefer explicitly authoritative product/architecture/governance sources over inferring intent from existing code alone. A merged file can still be Draft; a detailed file can still be historical.
10. **Map only the relevant implementation surface.** Inspect manifests, entrypoints, module boundaries, data models, API surfaces, tests, CI and deployment configuration that can affect the current decision or target path. Use doctor/project indexes as pointers, not proof of behavior.
11. **Check runtime evidence** when static inspection cannot answer a material question. Prefer a focused test/command over speculation.
12. **Record contradictions without erasing them.** Distinguish current intent from legacy implementation, generated files, experiments, stale docs, old PRs, unverified issue comments, and host-specific instruction layers. If authority/freshness/scope do not justify a winner, keep the conflict or unknown explicit.
13. **Stop when sufficient.** Discovery is complete when additional reading is unlikely to change the immediate route, current baseline, instruction scope, implementation target, acceptance evidence, capability plan, or risk model. State the unresolved material unknowns instead of chasing every link until none remain.

## Bounded evidence traversal

Good discovery is not proportional to repository size.

Prefer:

```text
current request
→ governing instructions
→ declared current/canonical entrypoints
→ one material unknown
→ one supporting reference if needed
→ current path/tests/runtime evidence
→ stop
```

Avoid:

```text
README
→ every linked document
→ every `related` / `depends_on` item
→ every historical release note
→ every directory
→ context exhaustion before a decision
```

Three common shapes:

- **Explicitly governed long-running project:** follow the declared first-read/current-source order and respect explicit exclusions before searching history.
- **Governance/reference-heavy repository:** read the current/canonical state and source-role registry first; reference graphs are navigation edges, not coverage obligations.
- **Small project/handoff:** if README, handoff/current-status, manifest, and the relevant implementation path already establish the next move, do not manufacture a large project profile or exhaustive inventory.

A deeper traversal is justified when a concrete question remains unresolved, not because the repository exposes more links.

## Instruction-topology boundary

Host instruction systems differ and evolve independently:

- Codex can aggregate project `AGENTS.md` / `AGENTS.override.md` along the root-to-current-working-directory path.
- Claude Code can read `CLAUDE.md` / deprecated `CLAUDE.local.md` along the cwd ancestry and discover nested `CLAUDE.md` when work enters a subtree.
- Cursor supports scoped `.cursor/rules/*.mdc`, including nested `.cursor/rules`; root `AGENTS.md` is currently a global simple project instruction surface, and Cursor CLI also reads root `CLAUDE.md`.

`instructions.py` inventories these documented filesystem surfaces. It does **not**:

- resolve Codex user-level `$CODEX_HOME` instructions or custom fallback filenames;
- resolve Claude user-level `~/.claude/CLAUDE.md` or recursively evaluate `@imports`;
- decide which Cursor MDC rules are active for every future file reference;
- decide which conflicting instruction is semantically correct;
- migrate deprecated files;
- mutate any rule merely because another host also reads it.

When an effective host prompt/precedence question is material, inspect the actual host/session/config rather than treating topology inventory as runtime proof.

## Evidence authority rules

- `main` / `production` / merged status does not by itself mean a document is accepted policy or current operational fact.
- newest timestamp does not automatically beat an explicitly designated current-fact or governance source.
- a canonical/current document's links and dependency metadata do not make every referenced artifact mandatory reading.
- explicit project first-read orders and historical-source exclusions should narrow discovery unless the current task specifically requires the excluded evidence.
- open/draft PRs and old branches are evidence of intent/history, not current implementation authority.
- issue comments and prior AI conclusions are hypotheses/reference unless independently supported.
- deployed/runtime facts require target-environment evidence; repository state is not a substitute.
- host-specific instruction filenames prove possible scope, not semantic correctness or runtime activation.
- preserve original contradictory evidence. Do not rewrite a source merely to make the project appear internally consistent.

## Output

Produce or hold a Project Profile containing only what is material to the current decision:

- project type;
- intended outcome;
- lifecycle stage;
- architecture / major modules when relevant;
- technology stack when relevant;
- current implementation baseline;
- current state relevant to the request;
- governing constraints;
- material instruction topology/scope when it affects the task;
- testing and deployment model when relevant;
- known risks;
- unresolved material questions/conflicts;
- evidence sources inspected, with material authority/freshness notes;
- material existing capabilities/providers already available.

When useful:

- serialize instruction topology to `.aaop/runtime/instruction-topology.json` against `.aaop/schemas/instruction-topology.schema.json`;
- serialize environment evidence to `.aaop/runtime/environment-inventory.json` against `.aaop/schemas/environment-inventory.schema.json`;
- serialize the synthesized project model to `.aaop/runtime/project-profile.json` against `.aaop/schemas/project-profile.schema.json`.

Do not create these artifacts merely to prove discovery happened.

## Quality checks

- Can you name the current decision horizon and why each inspected source could change it?
- Did you start from declared current/canonical/first-read sources when the project provided them?
- Did you avoid recursively traversing links, `related`, `depends_on`, indexes, and historical records without a material question?
- Presence of a package/config/CLI does not prove it should be used for the current route.
- No important project claim should rely solely on filenames when file contents/runtime evidence are available.
- Do not treat current implementation as product intent without corroboration.
- Do not treat historical/draft evidence as current fact merely because it is concrete or detailed.
- Do not treat discovery of a nested instruction file as proof that it overrides every other host/project rule.
- Do not ask the user for information already available in repository or connected context.
- Do not spend context inventorying unrelated modules or instruction surfaces when scope is already clear.
- Do not recommend installing a provider before checking whether the capability is already present.
- Stop before discovery becomes the work product unless the user explicitly asked for a repository audit/map.
