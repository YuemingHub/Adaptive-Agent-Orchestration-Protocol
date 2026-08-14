# DeepSeek Harness Adapter

This adapter maps AAOP's control-plane contract onto DeepSeek Harness (`dsh`) without making Harness a second AAOP control plane.

## Status

Reviewed upstream snapshot:

- repository: `deepseek-ai/deepseek-harness`
- commit: `47f943859bef60e4160492346772ded9b24f765a`
- package: `@deepseek-ai/dsh@0.1.0-rc.5`
- review date: `2026-08-14`
- upstream status: developer preview; compatibility-breaking changes are explicitly expected

Treat this as a compatibility snapshot, not permanent trust. Re-check the current upstream release and package contracts before a consequential upgrade.

## Authority boundary

AAOP remains authoritative for:

- Human-Agent Working Contract;
- developer Situation and current Route;
- user-owned vs agent-owned decisions;
- capability-gap classification and provider selection;
- repository, branch, environment and external-effect authorization;
- Task Pod responsibility and acceptance criteria;
- evidence requirements and final acceptance;
- Journey and release-cycle continuity.

DeepSeek Harness may own the selected execution surface:

- model routing and model adapters;
- tool registration and guarded tool execution;
- filesystem, shell, terminal, sandbox and LSP providers;
- MCP tool bridging;
- Skills discovery/loading;
- session event logging and session retrieval;
- per-session Agent Presets;
- subagent creation/control;
- dynamic workflows;
- process-local background jobs;
- interactive approvals/questions and permission presets;
- Web UI execution/observability surfaces.

Harness MUST NOT become:

- the source of product/domain intent;
- a replacement Human-Agent Working Contract;
- a competing AAOP Route/Journey state machine;
- an authorization bypass;
- proof of delivery merely because an Agent, Workflow or Job reports completion.

## Capability mapping

| AAOP concept | Preferred Harness surface | Notes |
| --- | --- | --- |
| execution context | Harness Agent/session | One capable Agent remains the default |
| bounded Task Pod | parent Agent + bounded subagents | Use only when AAOP Task Pod criteria justify specialization/isolation |
| multi-step Pod execution | `workflow` capability | Workflow is an execution provider, not the source of AAOP acceptance |
| specialist coding worker | Codex / Claude Code subagent provider | Provider selection follows the actual bounded responsibility |
| reusable procedure | Harness Skill provider | Skill remains procedure, not tool authority |
| external tool/API | Harness MCP client / native tool | Prefer native capability before adding MCP |
| background in-process work | Harness Jobs | Do not confuse process-local jobs with durable cross-session execution |
| session evidence | durable Session events + project/runtime readback | Session logs are execution evidence; current repository/runtime truth still wins |
| human confirmation | Harness approval / user-question surfaces | AAOP decides when the question is human-owned; Harness carries the interaction |
| per-task capability profile | Agent Preset | Prefer presets over creating separate applications/runtimes |
| long-running durable continuation | LoopX only after a proven gap | Harness Jobs/Schedule do not by themselves prove cross-session durable execution |

## Selection rule

Use the current host natively first.

Select DeepSeek Harness when its unified plugin/runtime surface materially reduces duplicated execution machinery or provides one or more needed capabilities such as:

1. one process needs multiple differently composed Agent Presets;
2. the task benefits from a unified tool + Skill + MCP + subagent + workflow execution substrate;
3. Codex, Claude Code and in-process agents should coexist behind one subagent seam;
4. execution/session observability and replay need one durable event model;
5. the product needs an extensible Web UI around the same runtime;
6. a Workbench-like host needs replaceable capability providers without forking a privileged core.

Avoid selecting Harness when:

- the existing AI IDE already completes the bounded task reliably and Harness would only add another runtime;
- the real blocker is credentials, authorization, product truth, environment access, cost, network or deployment access;
- a tiny one-off task does not benefit from another host layer;
- the proposed adoption requires deep-forking rapidly changing Harness internals instead of using plugins/profiles/bundles/patches;
- durable cross-session continuation is the only missing capability and a narrower LoopX escalation closes that proven gap.

## AAOP startup mapping inside Harness

When Harness is the selected host, the Agent should still follow the ordinary AAOP startup contract from the repository:

1. read project `AGENTS.md` / AAOP bootstrap;
2. reconcile Working Contract and current project evidence;
3. select one Route;
4. load the Route Capability Pack progressively;
5. inspect Harness-native capability before selecting another provider;
6. bind bounded responsibilities to one Agent by default;
7. create a subagent or Workflow only when AAOP Task Pod/capability evidence justifies it;
8. execute inside current authorization;
9. independently read back repository/runtime/target evidence;
10. let AAOP accept, reroute, gate or escalate.

Harness configuration does not replace these steps.

## Task Pod binding

A Task Pod is a responsibility contract, not a Harness feature name.

Recommended mapping:

```text
AAOP accountable owner
        ↓
Harness parent Agent
        ↓
optional bounded members
  ├─ Codex subagent
  ├─ Claude Code subagent
  ├─ in-process subagent
  └─ Workflow-started child
        ↓
project/runtime evidence
        ↓
AAOP owner accepts or reroutes
```

Rules:

- keep the AAOP 1–5 member cap;
- preserve exactly one accountable owner;
- do not create role-shaped agents merely because Harness can;
- Workflow phases are progress/observability vocabulary, not AAOP Route stages;
- child completion is not final acceptance;
- a Workflow failure or cancellation must remain a real failure/cancellation rather than being rewritten as success.

## Permissions

Harness permission presets implement execution permissions. AAOP defines the higher-level authorization decision.

Therefore:

- AAOP may narrow what Harness is allowed to do;
- a permissive Harness preset MUST NOT widen AAOP authorization;
- production writes, publishing, destructive actions, credential use, billing/cost, or materially expanded permissions retain the relevant AAOP/human gate;
- for domain-sensitive profiles, disable unnecessary self-modification and high-risk dynamic execution surfaces rather than relying on prompt instructions alone.

## Evidence and session logs

Harness's append-only Session event model is useful evidence, but it is not the final source of project truth.

Use session records for:

- what the Agent/model/tool actually attempted;
- workflow/subagent lifecycle evidence;
- replay/inspection;
- bounded provenance of model-visible inputs.

Before AAOP accepts a result, re-read the authoritative target when practical:

- repository diff and current ref;
- tests and CI;
- browser/runtime behavior;
- deployed environment;
- API/database/schema state;
- other route-specific acceptance evidence.

A stale Session event, child report or Workflow result never outranks fresher authoritative evidence.

## LoopX escalation

Do not duplicate LoopX inside a Harness adapter.

Harness already supplies goals, workflows, subagents, jobs and session state. LoopX is justified only when current evidence proves a remaining execution-continuity gap such as:

- execution must survive many sessions/restarts and the bounded frontier is otherwise lost;
- unchanged waits/failures cause blind repeated model turns;
- durable todo claim/handoff is required across execution contexts;
- an external monitor/scheduler wake contract is required.

When selected, keep the existing AAOP → LoopX authority boundary from `docs/LOOPX_INTEGRATION.md`.

## Integration style

Prefer this order:

1. published `@deepseek-ai/dsh` package or reviewed source checkout;
2. Harness Profiles / Bundles / `cordis.patch.yml` overlays;
3. out-of-tree plugins depending on documented Service Definitions;
4. MCP/Skill/Agent Preset composition;
5. only then consider a narrowly justified upstream patch.

Do not maintain a broad long-lived fork of DeepSeek Harness merely to brand or compose the product.

## Workbench consequence

A Workbench distribution can use Harness as the execution chassis while adding its own product-level concepts above it, for example:

```text
Space
Work Unit
Gate
Evidence
Asset
Outcome
Domain Pack
```

Those are Workbench/product objects. They should not be forced into AAOP Route state or Harness Session state merely because both systems are available.

The first intended consumer is a development Workbench where AAOP is the software-development Domain Pack and Harness is the default execution substrate. Other domains can define separate Packs without extending AAOP into a universal life/work protocol.