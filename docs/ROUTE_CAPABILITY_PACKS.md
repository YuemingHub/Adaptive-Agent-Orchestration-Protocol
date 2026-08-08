# Route Capability Packs

AAOP uses **Route Capability Packs** as the bridge between natural-language developer intake and mature ecosystem capabilities.

A pack is deliberately small. It is **not**:

- a workflow engine;
- a role/team template;
- an installer bundle;
- a replacement for Spec Kit, OpenHands, Playwright, mini-SWE-agent, or another provider;
- a form that the developer fills out.

It is internal metadata that answers:

1. what engineering stages normally matter for this developer situation;
2. what capabilities those stages require;
3. what evidence should move the work forward;
4. which **pressure guards** must prevent known real-project failure modes;
5. when the current environment is insufficient;
6. which mature providers are plausible candidates for that specific gap;
7. what evidence means the route should change.

## Why this layer exists

Without Route Capability Packs, AAOP risks one of two failures:

- putting every development practice into one giant orchestrator prompt; or
- creating a separate AAOP implementation for bug fixing, feature work, repository recovery, review, release, and greenfield development.

Both would duplicate mature systems and become difficult to maintain.

The pack keeps AAOP thin:

```text
Natural-language request
        ↓
Developer Intake
        ↓
Current Route
        ↓
Route Capability Pack
  stages + evidence + pressure guards
        ↓
What capabilities are needed now?
        ↓
Do we already have them?
   yes /            \ no
      ↓              ↓
   use them      classify blocker
                     ↓
              genuine capability gap?
                no /          \ yes
                ↓              ↓
          preserve/resolve   Provider + Recipe
            real blocker          ↓
                              upstream tool
                                  ↓
                                verify
```

## Current packs

| Route | Normal engineering emphasis | Real-pressure emphasis | Typical optional escalation |
| --- | --- | --- | --- |
| `idea-to-build` | outcome → behavior contract → first real slice | technology vocabulary is hypothesis; first slice must buy learning; beginner does not choose stack | Spec Kit for demonstrated intent drift; Playwright for browser acceptance; dedicated runtime only when necessary |
| `repo-recovery` | preserve/inventory → reconstruct truth → stabilize one path | source authority/freshness; preserve unresolved conflicts | Spec Kit for durable brownfield intent; Deep Agents/OpenHands for long execution; reroute bounded defect to bug-fix |
| `bug-fix` | reported baseline → failure evidence → root cause → narrow fix/regression | stale tracebacks/source lines are historical; issue comments are hypotheses | mini-SWE-agent for bounded issue solving; Playwright for browser evidence; Spec Kit when bug traceability matters |
| `feature-change` | behavior contract → current baseline → impact discovery → implementation/acceptance | salvage behavior/invariants/tests from stale PRs, not obsolete commits | Spec Kit for structured feature lifecycle; Playwright for UI acceptance; dedicated runtime for genuinely large autonomous work |
| `understand-review` | decision frame → targeted current evidence → findings/action | external claims require current verification when practical; risk is contextual; read-only by default | structured review provider only when it adds needed evidence/independence |
| `release-operations` | environment truth → blocker/preflight/rollback → controlled execution/observe | environment/auth/credential/product blockers are not capability gaps; preserve unknown operational state | Playwright smoke checks; dedicated workflow runtime/control plane only when operations itself needs one |

## Pressure Guards

`pressure_guards` are not best-practice decoration. They are route invariants earned from real developer failures or near-misses.

Examples:

```text
idea-to-build
  outcome-before-architecture
  solution-vocabulary-is-hypothesis
  first-slice-must-buy-learning

understand-review
  decision-frame-before-review
  current-source-before-conclusion
  risk-is-contextual
  review-is-read-only-by-default
```

The AAOP source repository stores replay cases under `tests/pressure/`. Each case names the guard IDs it depends on. `scripts/validate_pressure.py` fails if those guards disappear or, from v0.8 onward, if any of the six routes loses all real pressure coverage.

This means route evolution is constrained by remembered real-world failure, not only by prompt wording.

## The provider candidate rule

A provider listed in a pack is a **candidate**.

It does not mean:

- install it;
- prefer it over the current IDE;
- load all of its extensions;
- treat its community catalog as trusted;
- migrate the project to that framework.

The candidate becomes relevant only when the pack's escalation condition is true **and** the named capability gap remains unresolved after checking the current host, repository, Skills, scripts, tests, and connected tools.

A blocker caused by missing evidence, environment/network policy, authorization, credentials, an external dependency, or an unresolved product decision is not converted into a provider search.

## Provider examples

### GitHub Spec Kit

AAOP does not reproduce Spec Kit's Spec → Plan → Tasks → Implement workflow, extension/catalog system, or bundles.

AAOP may select Spec Kit when durable intent/specification artifacts genuinely reduce demonstrated drift. A broad greenfield vision alone is not enough; first define a concrete outcome and first slice.

### Playwright

Playwright is modeled as a **tool family**, not simply an MCP server.

Choose by need:

- Playwright Test — repeatable E2E/regression evidence;
- Playwright CLI + Skills — agent-driven browser work where concise command interaction is preferable;
- Playwright MCP — persistent/introspective browser-agent loops where continuous page state matters.

AAOP should not install all surfaces by default.

### mini-SWE-agent

Use only when the issue is bounded, current-baseline reconciled, reproducible, and testable and a dedicated minimal SWE-agent loop is actually useful.

It is not a substitute for understanding an ambiguous product request or recovering a contradictory repository.

### OpenHands / Deep Agents

Treat these as optional execution runtimes/harnesses. Use them only when a concrete execution property is missing from the current host. A request for “more autonomy” or “many agents” is not itself a capability gap.

## Review/provider adoption nuance

When `understand-review` is evaluating whether to adopt a provider, the provider is the **subject of review**, not automatically a candidate to install.

The review should:

1. define the adoption context;
2. inspect current source/status material to the decision;
3. separate reported claims from verified mechanism and unknowns;
4. contextualize permissions/exposure/risk;
5. recommend adopt / reject / conditionally adopt / investigate further;
6. remain read-only until the user chooses implementation.

## Runtime use

After AAOP is installed into a project:

```bash
python .aaop/tools/route.py list
python .aaop/tools/route.py show idea-to-build
python .aaop/tools/route.py show understand-review --json
```

These commands only inspect metadata. They do not run a route or install providers.

## Route correction

Route packs include `reroute_signals` because real software work changes shape.

Examples:

```text
"Review this framework; integrate it if acceptable"
        ↓
understand-review
        ↓
conditional adoption decision made
        ↓
feature-change / integration
```

```text
"Add retry button"
        ↓
feature-change
        ↓
existing retry is discovered but broken
        ↓
bug-fix
```

```text
"Fix login"
        ↓
bug-fix
        ↓
repository is too contradictory to establish the failing path
        ↓
repo-recovery
```

Changing route is not failure. It is evidence correcting the model of the work.

## Design test

A good Route Capability Pack should pass two questions:

> If every named external provider disappeared tomorrow, would the pack still describe a sound engineering approach using ordinary host/repository capabilities?

> If the developer were a beginner, could the route still proceed without making them choose the internal machinery?

If either answer is no, the pack is too coupled to a framework or too dependent on user orchestration labor.
