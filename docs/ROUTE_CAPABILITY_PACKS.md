# Route Capability Packs

AAOP v0.5 introduces **Route Capability Packs** as the bridge between natural-language developer intake and mature ecosystem capabilities.

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
4. when the current environment is insufficient;
5. which mature providers are plausible candidates for that specific gap;
6. what evidence means the route should change.

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
        ↓
What capabilities are needed now?
        ↓
Do we already have them?
   yes /            \ no
      ↓              ↓
   use them      prove the gap
                     ↓
                Provider + Recipe
                     ↓
                 upstream tool
                     ↓
                   verify
```

## Current packs

| Route | Normal engineering emphasis | Typical optional escalation |
| --- | --- | --- |
| `idea-to-build` | outcome → behavior contract → first real slice | Spec Kit for durable intent; Playwright for browser acceptance; dedicated runtime only when necessary |
| `repo-recovery` | preserve/inventory → reconstruct truth → stabilize one path | Spec Kit for durable brownfield intent; Deep Agents/OpenHands for long execution; reroute bounded defect to bug-fix |
| `bug-fix` | failure evidence → root cause → narrow fix/regression | mini-SWE-agent for bounded issue solving; Playwright for browser evidence; Spec Kit when bug traceability matters |
| `feature-change` | behavior contract → impact discovery → implementation/acceptance | Spec Kit for structured feature lifecycle; Playwright for UI acceptance; dedicated runtime for genuinely large autonomous work |
| `understand-review` | decision frame → evidence inspection → findings/action | structured review provider only when it adds evidence/independence; no mutation by default |
| `release-operations` | environment truth → preflight/rollback → controlled execution/observe | Playwright smoke checks; dedicated workflow runtime/control plane only when operations itself needs one |

## The provider candidate rule

A provider listed in a pack is a **candidate**.

It does not mean:

- install it;
- prefer it over the current IDE;
- load all of its extensions;
- treat its community catalog as trusted;
- migrate the project to that framework.

The candidate becomes relevant only when the pack's escalation condition is true **and** the named capability gap remains unresolved after checking the current host, repository, Skills, scripts, tests, and connected tools.

## Mature providers integrated in v0.5

### GitHub Spec Kit

AAOP does not reproduce Spec Kit's Spec → Plan → Tasks → Implement workflow, extension/catalog system, or bundles.

AAOP may select Spec Kit when durable intent/specification artifacts genuinely reduce drift. Existing projects can use Spec Kit's evolving-spec patterns. The current upstream project also includes an opt-in Agentic Bug Fix workflow and a community extension ecosystem.

Community extensions remain a separate trust surface: their source and permissions must be reviewed before use.

### Playwright

Playwright is modeled as a **tool family**, not simply an MCP server.

Choose by need:

- Playwright Test — repeatable E2E/regression evidence;
- Playwright CLI + Skills — agent-driven browser work where concise command interaction is preferable;
- Playwright MCP — persistent/introspective browser-agent loops where continuous page state matters.

AAOP should not install all surfaces by default.

### mini-SWE-agent

Use only when the issue is bounded, reproducible, and testable and a dedicated minimal SWE-agent loop is actually useful.

It is not a substitute for:

- understanding an ambiguous product request;
- recovering a contradictory repository;
- deciding what users actually want.

### OpenHands

OpenHands is treated as an optional software-engineering runtime/tooling ecosystem.

Use it when a dedicated autonomous coding environment, reusable Software Agent SDK, or isolated workspace is the real missing capability. Do not add it merely because the task contains code.

## Runtime use

After AAOP is installed into a project:

```bash
python .aaop/tools/route.py list
python .aaop/tools/route.py show bug-fix
python .aaop/tools/route.py show feature-change --json
```

These commands only inspect metadata. They do not run a route or install providers.

## Route correction

Route packs include `reroute_signals` because real software work changes shape.

Examples:

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

```text
"Add invitations"
        ↓
feature-change
        ↓
implementation complete; staging deployment now blocks acceptance
        ↓
release-operations
```

Changing route is not failure. It is evidence correcting the model of the work.

## Design test

A good Route Capability Pack should pass this question:

> If every named external provider disappeared tomorrow, would the pack still describe a sound engineering approach using ordinary host/repository capabilities?

If the answer is no, the pack is too coupled to a framework.

That constraint keeps AAOP useful as the ecosystem changes.
