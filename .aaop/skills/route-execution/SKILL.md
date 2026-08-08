---
name: route-execution
description: Execute a selected AAOP developer route by loading its Route Capability Pack, matching required capabilities against the current environment, and escalating to mature providers only for proven gaps. Use after developer-intake selects idea-to-build, repo-recovery, bug-fix, feature-change, understand-review, or release-operations.
---

# Route Execution

Use this Skill after `developer-intake` has selected one primary route.

## Principle

A Route Capability Pack is an **engineering capability map**, not a workflow engine, package bundle, or script that must be followed mechanically.

The route pack answers:

- what must become true in this development situation;
- which engineering capabilities are normally required;
- what evidence should move the work forward;
- which mature providers may close specific gaps;
- when evidence means the route itself should change.

The developer should not operate the pack directly.

## Step 1 — Load exactly one current pack

Read `.aaop/routes/<route-id>.json`, where `<route-id>` is the current primary route.

Do not load all route packs unless comparison is genuinely needed.

## Step 2 — Inventory before matching

When `.aaop/tools/doctor.py` is available, prefer a read-only inventory before guessing what the environment contains:

```bash
python .aaop/tools/doctor.py . --route <route-id> --json
```

The doctor reads provider detection hints from Integration Recipes, so its `provider_detection` evidence is preferable to hard-coded assumptions about installed frameworks.

Treat the inventory as **presence evidence, not a recommendation**. A detected provider can still be irrelevant; a non-detected provider can still be unnecessary.

For the current stage, map each `required_capabilities` entry against:

1. current host-native ability;
2. repository scripts/libraries/tests;
3. already-installed Skills;
4. already-connected tools/MCP/apps;
5. detected existing providers/runtimes;
6. specialist/subagent capability already available.

If the capability is already available, use it.

A provider candidate in the route pack is **not** a default dependency.

## Step 3 — Work stage by stage, evidence first

For each stage:

- understand its `purpose`;
- collect the smallest useful `evidence`;
- perform the work using current capabilities;
- stop the stage when `exit_when` is satisfied.

Do not manufacture documents merely because a stage exists. Evidence may be code, a failing test, runtime behavior, a decision, a short spec, a browser trace, or a validated deployment state.

## Step 4 — Prove a gap before escalation

Use an escalation only when its `when` condition is actually present and the named `capability_gap` remains unresolved.

Then:

1. run provider selection;
2. inspect `.aaop/registries/providers.json`;
3. check environment inventory to avoid duplicating a provider already present;
4. load `.aaop/recipes/<provider-id>.json` when available;
5. re-check upstream source of truth before consequential installation;
6. choose the smallest provider surface that closes the gap;
7. apply autonomy/permission policy;
8. verify the original gap after integration.

If no provider is justified, keep using the current host.

## Step 5 — Prefer provider surfaces, not provider brands

When a provider exposes several surfaces, select only the one needed.

Examples:

- Playwright Test vs CLI+Skills vs MCP;
- OpenHands CLI vs SDK vs sandboxed/remote workspace;
- Spec Kit core flow vs one reviewed extension;
- one-time `uvx` evaluation vs persistent installation.

Do not install a provider's entire ecosystem to obtain one narrow capability.

## Step 6 — Treat community catalogs as discovery, not trust

Before adopting a community extension/plugin/bundle check source repository and publisher, maintenance, install scripts/hooks, filesystem/network/write permissions, credentials/data egress, and rollback/removal path.

Catalog presence alone is never sufficient authorization.

## Step 7 — Correct the route when evidence changes the situation

Evaluate `reroute_signals` after meaningful discoveries.

Examples:

- feature request is actually a regression → `bug-fix`;
- bug cannot be localized because the repository is contradictory → `repo-recovery`;
- feature implementation is complete and deployment becomes the blocker → `release-operations`;
- review becomes an explicit implementation request → `feature-change` or `bug-fix`.

Re-routing is progress, not failure. Keep queued secondary intents, but only one route should normally own the immediate outcome.

## Step 8 — Verify route completion

Use the pack's `verification` list as the final route-level evidence contract.

Also verify separately that any provider added during execution actually closed the capability gap that justified it.

Remove or disable unnecessary provider machinery when the task can return to a simpler layer.

## Completion criterion

Route execution is complete when:

- the current route's observable outcome is supported by evidence;
- required capabilities were satisfied with the smallest practical integration surface;
- existing environment capability was reused instead of duplicated;
- any escalation was justified, verified, and reversible;
- route corrections were applied when evidence required them;
- the user did not have to manage the orchestration machinery.
