# DeepSeek Harness Integration

Verified against `deepseek-ai/deepseek-harness` on 2026-08-14.

Reviewed snapshot:

- commit: `47f943859bef60e4160492346772ded9b24f765a`
- CLI package: `@deepseek-ai/dsh@0.1.0-rc.5`
- license: MIT
- upstream maturity: developer preview

This document records an adoption decision for AAOP and the first Ming Workbench development slice. It is a dated review, not permanent trust.

## Decision

AAOP should treat DeepSeek Harness as a **host/runtime provider**, not absorb its runtime mechanisms and not compete with them.

For Ming Workbench, DeepSeek Harness is the preferred execution chassis for the first development profile because it already provides the capabilities we would otherwise duplicate:

- replaceable model adapters;
- guarded tool registry/execution;
- filesystem/shell/terminal/sandbox/LSP seams;
- MCP client bridging;
- Skill loading;
- durable Session event logs and retrieval;
- Agent Presets;
- Codex, Claude Code and in-process subagent providers;
- dynamic workflows;
- background jobs;
- human approvals/questions and permission presets;
- plugin-composable Web UI.

AAOP remains the software-development control protocol above that chassis.

## Why this changes the implementation plan

Before this review, AAOP ecosystem work still had a risk of slowly re-implementing runtime mechanisms around host execution: subagent routing, workflow execution, background work, tool composition, UI, session evidence and provider hosting.

Harness closes enough of that surface that the preferred architecture becomes:

```text
Human intent / product truth
        ↓
Workbench product layer
        ↓
AAOP software-development Domain Pack
  Working Contract · Route · authorization · acceptance
        ↓
DeepSeek Harness execution chassis
  Agent · Tools · Skills · MCP · Presets · Subagents · Workflow · Jobs
        ↓
Codex / Claude Code / native tools / external MCP
        ↓
real repository / tests / runtime / deployment evidence
        ↓
AAOP acceptance / reroute / release decision
```

When a proven cross-session durable-execution gap remains:

```text
AAOP bounded authorized outcome
        ↓
Harness host
        ↓
LoopX bounded durable execution provider
        ↓
current project/runtime evidence
        ↓
AAOP acceptance
```

LoopX remains optional and narrow. Harness adoption is not a reason to duplicate a second scheduler/ledger inside AAOP.

## Do not fork the product core

DeepSeek Harness explicitly expects compatibility-breaking changes during developer preview. A broad fork would create immediate upstream merge debt.

The preferred integration order is:

1. pin/review an upstream package or exact commit;
2. compose with Profiles/Bundles/patch overlays;
3. add out-of-tree plugins against documented capability seams;
4. add Workbench UI modules through supported client extension surfaces;
5. upstream narrowly useful changes when appropriate;
6. fork internals only for a proven blocker that cannot be solved at an extension seam.

Branding, Workbench domain objects and product navigation are not sufficient reasons to fork the runtime core.

## First vertical slice: Dev Workbench

The first consumer should not attempt to implement the whole Workbench.

### Product goal

A user can open one development Space, describe an ordinary software goal, and see it progress through one evidence-bearing Work Unit without choosing Agent/runtime machinery.

### Minimum Workbench objects

```text
Space
  └─ Work Unit
       ├─ outcome
       ├─ state
       ├─ current owner
       ├─ gate
       ├─ acceptance evidence
       ├─ artifacts/assets
       └─ next frontier
```

These are product-level Workbench objects. They are not replacements for AAOP Route/Journey state or Harness Session events.

### First supported Domain Pack

`development`:

- control protocol: AAOP;
- default host: DeepSeek Harness;
- coding providers: current Harness-native/integrated providers such as Codex or Claude Code when justified;
- external tools: Harness native tools or MCP only after capability selection;
- durable execution: LoopX only after a proven continuity gap.

### First end-to-end proof

Use the Workbench to make one real, bounded change in an existing repository and prove:

1. ordinary-language intake reaches AAOP;
2. AAOP selects/reconciles one Route;
3. Harness executes with one Agent by default;
4. a subagent/Workflow is added only if justified;
5. tool writes respect exact target authorization;
6. tests/runtime evidence are read back independently;
7. the Work Unit presents outcome, evidence and residual risk;
8. a fresh session can inspect the resulting evidence without relying on a fabricated summary.

A dashboard with no real repository delivery does not satisfy this proof.

## Compatibility seam

Because Harness is rapidly changing, Workbench code should isolate upstream-specific bindings behind a small compatibility package.

Conceptual structure:

```text
workbench-core/
  Space
  WorkUnit
  Gate
  Evidence
  Asset
  Outcome

domain-packs/
  development-aaop/
hosts/
  harness-compat/
    version-detection
    capability-map
    session-adapter
    preset-adapter
    subagent-adapter
    workflow-adapter
    permission-adapter
```

Only `harness-compat` should know detailed upstream package/config names where practical.

When upstream breaks compatibility, update and test this seam before changing Workbench domain logic.

## Permission profiles

One Workbench installation may expose different profiles, but they must not share one unconstrained permission posture.

Initial policy direction:

| Profile | Default posture |
| --- | --- |
| Development | broad reversible local/repository execution; protected remote/production effects gated |
| Creator | content/file/research tools; publication remains explicit external effect |
| Research | read-heavy; bounded file outputs; external writes minimal |
| Family Service | strict least privilege; sensitive-data boundaries; runtime self-modification disabled; publication/external effects gated |
| Production Operations | explicit environment/write target and consequential-effect authorization |

Harness permission presets are an implementation surface for these restrictions, not the source of the policy itself.

## Self-modification and dynamic workflows

Harness can expose powerful runtime self-modification and model-authored workflow capabilities.

Treat them as profile-dependent capabilities:

- acceptable in a constrained development/research environment when useful;
- not enabled merely because the package ships them;
- disabled or tightly constrained for sensitive service profiles;
- never treated as a security boundary by prompt convention alone.

Dynamic Workflow worker isolation is execution isolation, not a complete security boundary.

## Session and evidence model

Harness Session events should be used for execution provenance, replay and model-visible input reconstruction.

Workbench Evidence should reference, not copy, the minimum useful execution facts and independently verified target state.

Preferred evidence flow:

```text
Harness execution/session events
        +
current repository/runtime/deployment readback
        ↓
AAOP verification decision
        ↓
Workbench Evidence record
```

Do not turn raw transcripts into the Workbench's universal memory model.

## Open-source direction

The open-source project should not present itself as another Agent framework.

Its differentiated layer is:

> turn a person's ordinary intent into a bounded, observable Work Unit; let domain control policy choose capabilities; use existing runtimes to execute; return evidence rather than machinery.

The reusable public surface should center on **Domain Packs**, not a replacement plugin protocol.

A Domain Pack may compose existing Harness primitives:

```text
procedures / Skills
+ Agent Presets
+ workflows
+ tools / MCP
+ permission policy
+ evidence rules
+ Workbench UI surfaces
```

Example future Packs can target software building, content creation, research, consulting or other knowledge work without extending AAOP beyond software development.

## Immediate implementation order

1. land the AAOP Harness adapter and provider review;
2. create the standalone Ming Workbench repository/distribution;
3. pin the reviewed Harness version behind `harness-compat`;
4. implement only `Space` + `Work Unit` + `Evidence` + `Gate` first;
5. ship the `development-aaop` Domain Pack;
6. execute one real Family Space/AAOP development task through it;
7. measure where native Harness continuity actually fails before adding LoopX;
8. only then add Creator/Research/Service Packs;
9. extract user-private configuration from reusable open-source Pack contracts;
10. publish examples and contribution contracts after the first internal workflow is repeatedly useful.

## Upgrade rule

Never upgrade Harness because upstream is merely newer.

Before changing the pinned/reviewed version:

1. resolve the current upstream release/commit identity;
2. read breaking changes relevant to used seams;
3. run compatibility tests for Workbench host bindings;
4. run at least one real Dev Workbench delivery regression;
5. verify permission behavior and evidence integrity;
6. then deliberately promote the new pin.

This keeps acceleration compatible with reproducibility rather than trading speed for uncontrolled runtime drift.