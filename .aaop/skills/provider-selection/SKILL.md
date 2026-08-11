---
name: provider-selection
description: Select the smallest sufficient external standard, runtime, execution control plane, discovery service, or workspace only after a concrete capability gap is proven. Use when AAOP must decide whether to stay host-native or add Agent Skills, MCP, LoopX, Deep Agents, a delegated multi-agent runtime, or another provider.
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

For work expected to span many turns, sessions, agents, or external waits, explicitly ask whether the missing capability is **execution continuity/control** rather than implementation ability. A useful local capability label is `execution-continuity`:

- preserve one bounded executable frontier across sessions;
- know when another model turn should run versus wait/gate/quiet;
- keep todo ownership, evidence and handoff durable;
- resume from state plus current project evidence rather than transcript memory.

Do **not** declare `execution-continuity` missing merely because a task is large. First prove the current host/Journey/Working Contract cannot continue it reliably enough.

If no gap is proven, select **no additional provider**.

## Step 2 — Prefer progressive enhancement

Check in order:

1. current host native capability;
2. current project scripts/libraries;
3. an existing Agent Skill;
4. an existing connected MCP/tool;
5. one new Skill or MCP;
6. ARD/A2A discovery/interoperability when provider identity is unknown or cross-system communication is needed;
7. one specialized runtime or execution-control provider when runtime/control properties are the actual gap;
8. an organizational workspace only when shared governance is the actual gap.

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
- Existing host can perform the engineering work, but durable cross-turn/session todo/evidence/gate/quota/wake/handoff control is the missing property → consider **LoopX** or another execution-control provider.
- The agent runtime itself is inadequate for long-horizon reasoning/execution, context isolation, persistence, filesystem/Skills/MCP-heavy work → consider **Deep Agents** or another dedicated agent runtime.
- A justified AAOP Task Pod specifically needs bounded multi-role DAG/resume execution that the current host cannot supply → consider **agency-orchestrator** or another delegated multi-agent runtime; AAOP remains the Pod/Journey/Working Contract authority.
- Typed production workflows/hosting are the gap → consider **Microsoft Agent Framework**.
- Dynamic workforce composition is the gap → consider **CAMEL Workforce**.
- Automatic creation/testing of new tools, agents, workflows is itself the desired capability → consider **AutoAgent**.
- Persistent multi-human/multi-agent governance, approvals, audit, scheduling and runtime routing are the gap → consider **AgentSpace** or another mature organizational workspace.

### Do not collapse these three gaps

`LoopX`, `Deep Agents`, and a delegated multi-agent runtime solve different primary problems:

| Proven gap | Preferred provider family | AAOP boundary |
| --- | --- | --- |
| The current agent can do the work, but the loop cannot reliably decide/resume/hand off across turns | LoopX-style execution control plane | AAOP keeps intent, Route/Journey, authorization and acceptance; provider governs bounded execution continuity |
| The current agent runtime itself lacks the long-horizon execution/context/persistence mechanics needed to do the work | Deep Agents-style agent runtime | AAOP delegates the bounded Route/Pod execution but keeps product/authorization/release authority |
| A justified Task Pod needs explicit multi-role DAG/resume execution | agency-orchestrator-style delegated Pod runtime | AAOP defines the Pod outcome, members, gates, acceptance and handoff; provider executes the bounded Pod |

Do not install two of these merely because the task is long. Choose the smallest provider whose **primary mechanism** matches the proven gap. If one provider fails to close the gap, diagnose the mismatch before stacking another control plane/runtime on top.

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
selected_surface: <smallest provider surface actually needed>
authority_owner: <which AAOP/project state remains authoritative>
why_now: <evidence-backed reason>
why_not_simpler: <why lower layers are insufficient>
why_not_adjacent_provider: <why a runtime/control-plane/workspace alternative is the wrong primary mechanism>
adoption_review: <none | rechecked current finding/condition>
permissions_required: []
credentials_required: []
infrastructure_required: []
expected_benefit: <measurable improvement>
verification: <how to prove the integration helped>
rollback: <how to remove/disable it>
```

Do not propose a bundle of unrelated technologies.

For a provider that stores execution/control state, explicitly state which facts remain authoritative in AAOP/project state and which facts the provider may own. Never allow two systems to become silent competing sources of truth for the same decision class.

## Step 7 — Verify after integration

After adding a provider, verify the original capability gap is actually closed.

When an adoption review applies, also verify that the actual installed/enabled surface matches the assumptions or mitigations used in the adoption decision.

For execution-control/runtime providers, verification must include at least one behavior that the host previously could not prove reliably: restart/resume, no-progress quieting, durable handoff, independent validation/writeback, or another gap-specific property. “Installed successfully” is not gap closure.

If the capability gap is not closed, diagnose before adding another provider. Multiple failed additions are evidence the problem may be misunderstood rather than under-tooled.

## Completion criterion

Provider selection is complete when either:

- no external addition is needed; or
- exactly the justified provider set is selected, the current upstream integration path is known, the authority seam is explicit, any applicable adoption review has been rechecked against the intended surface/context, permission/cost implications are explicit, and the original gap has a concrete verification/rollback plan.
