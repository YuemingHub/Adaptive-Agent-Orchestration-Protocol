---
name: provider-selection
description: Select the smallest sufficient external standard, runtime, discovery service, or workspace only after a concrete capability gap is proven. Use when AAOP must decide whether to stay host-native or add Agent Skills, MCP, ARD, A2A, Deep Agents, Microsoft Agent Framework, CAMEL, AutoAgent, AgentSpace, or another provider.
---

# Provider Selection

Use this Skill after project discovery and capability matching reveal a real gap.

## Principle

Do not ask which framework is globally best. Select the provider that closes the current gap with the smallest justified operational surface.

A provider is never permanently “safe”, “unsafe”, “approved”, or “rejected” merely because an AAOP Recipe contains a prior review. Provider status, implementation, deployment context, and mitigations can change.

## Step 1 — Prove the gap

Record:

- required capability;
- evidence the current host/project cannot satisfy it adequately;
- whether the gap is one-off or recurring;
- required reliability/durability/governance level.

If no gap is proven, select **no additional provider**.

## Step 2 — Prefer progressive enhancement

Check in order:

1. current host native capability;
2. current project scripts/libraries;
3. an existing Agent Skill;
4. an existing connected MCP/tool;
5. one new Skill or MCP;
6. ARD/A2A discovery/interoperability when provider identity is unknown or cross-system communication is needed;
7. one specialized runtime when runtime properties are the actual gap;
8. an organizational workspace only when governance/persistence is the actual gap.

Read `../../registries/providers.json` and `../../../docs/PROGRESSIVE_ADOPTION.md` when available.

## Step 3 — Separate discovery from installation

Discovery may use:

- current host catalogs;
- ARD-compatible discovery services;
- Official MCP Registry;
- A2A Agent Cards;
- first-party provider documentation.

A discovered candidate is not automatically trusted or installed.

Before external installation or connection evaluate:

- provenance and publisher;
- maintenance/activity;
- permissions and write scope;
- credentials/secrets;
- data egress;
- infrastructure burden;
- cost;
- lock-in and uninstall path;
- overlap with existing providers.

Apply `../../policies/mcp-and-tools.md` and `../../policies/autonomy.md`.

## Step 4 — Select by symptom

Use these as heuristics, not hard-coded routing:

- Missing repeatable procedure → **Agent Skill**.
- Missing external service access → **native tool or MCP**.
- Unknown resource/provider across catalogs → **ARD-compatible discovery**.
- Independent opaque agents must communicate → **A2A**.
- Long-horizon harness/context isolation/persistent execution is the gap → consider **Deep Agents** or another dedicated runtime.
- Typed production workflows/hosting are the gap → consider **Microsoft Agent Framework**.
- Dynamic workforce composition is the gap → consider **CAMEL Workforce**.
- Automatic creation/testing of new tools, agents, workflows is itself the desired capability → consider **AutoAgent**.
- Persistent multi-human/multi-agent governance, approvals, audit, scheduling and runtime routing are the gap → consider **AgentSpace** or another mature control plane.

## Step 5 — Resolve the integration recipe

If `.aaop/recipes/<provider-id>.json` exists, use it as the normalized integration contract.

A recipe centralizes:

- selection/avoid conditions;
- detection hints;
- smallest known upstream installation path;
- credentials and permissions;
- optional scoped `adoption_review` debt;
- verification;
- rollback;
- `source_of_truth` and `last_verified`.

Before executing any external installation, re-check the recipe's `source_of_truth` when network access is available. Upstream installation instructions override stale recipe commands.

### Adoption review rule

If the recipe contains `adoption_review`, treat it as **remembered review debt**, not a verdict.

Before consequential adoption of a surface that falls within the recorded `scope`:

1. read `reviewed_at`, `reason`, `current_observations`, `sources`, and `required_checks`;
2. re-check the current upstream source/release/issue/advisory state when accessible;
3. determine whether the intended provider mode/surface actually uses the reviewed mechanism;
4. evaluate the real deployment context, permissions, data exposure, network reachability, and mitigations relevant to the recorded concern;
5. update the decision based on current evidence, not the stale observation alone.

Interpret `decision_effect` as:

- `informational` — include the review in the decision but it does not require a special adoption gate by itself;
- `reverify-before-adoption` — re-check the scoped concern before enabling the relevant surface;
- `conditional-adoption-only` — use the relevant surface only when the recorded/current conditions or mitigations can be explicitly satisfied.

If the concern has been fixed upstream or is irrelevant to the selected surface/context, it should not block adoption. Update or retire the stale review when maintaining the Recipe.

If the concern remains materially relevant and cannot be mitigated within the user's authorization/risk boundary, prefer:

- a narrower surface of the same provider;
- an isolated deployment;
- another provider that closes the same gap with lower operational exposure;
- or no new provider yet.

Do not bypass or suppress a relevant adoption review merely to keep an earlier provider choice.

If no recipe exists, create an **ephemeral integration plan** from first-party documentation instead of guessing. Promote it to a reusable recipe only after it is validated and likely to recur.

The recipe browser is available at:

```bash
python .aaop/tools/recipe.py list
python .aaop/tools/recipe.py show <provider-id>
```

These commands never install providers.

## Step 6 — Produce a minimal integration plan

Return or materialize:

```yaml
capability_gap: <what is missing>
current_level: <0-5>
selected_providers: [<provider-id>]
why_now: <evidence-backed reason>
why_not_simpler: <why lower layers are insufficient>
adoption_review: <none | rechecked current finding/condition>
permissions_required: []
credentials_required: []
infrastructure_required: []
expected_benefit: <measurable improvement>
verification: <how to prove the integration helped>
rollback: <how to remove/disable it>
```

Do not propose a bundle of unrelated technologies.

## Step 7 — Verify after integration

After adding a provider, verify the original capability gap is actually closed.

When an adoption review applies, also verify that the actual installed/enabled surface matches the assumptions or mitigations used in the adoption decision.

If the capability gap is not closed, diagnose before adding another provider. Multiple failed additions are evidence the problem may be misunderstood rather than under-tooled.

## Completion criterion

Provider selection is complete when either:

- no external addition is needed; or
- exactly the justified provider set is selected, the current upstream integration path is known, any applicable adoption review has been rechecked against the intended surface/context, permission/cost implications are explicit, and verification/rollback are defined.
