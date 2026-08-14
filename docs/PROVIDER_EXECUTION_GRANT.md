# Provider Execution Grant

## Purpose

AAOP needs one explicit machine-readable seam between **control-plane acceptance to execute** and a selected execution provider such as DeepSeek Harness, Codex, Claude Code, LoopX, or another bounded runtime.

The Provider Execution Grant is that seam.

It exists because neither of these should be overloaded:

- the Human-Agent Working Contract — long-lived collaboration/alignment authority;
- the Execution Plan — the engineering task graph and verification intent.

A provider needs a smaller projection that answers only:

> What exact bounded work may this provider execute now, under which authorization, and what evidence must come back?

Canonical schema:

```text
.aaop/schemas/provider-execution-grant.schema.json
```

## Authority flow

```text
Human intent / product truth
        ↓
AAOP Working Contract
        ↓
AAOP Developer Intake + current Route
        ↓
AAOP Execution Plan / Task Pod decision
        ↓
AAOP authorization check
        ↓
Provider Execution Grant
        ↓
selected provider executes only the grant
        ↓
repository/runtime evidence readback
        ↓
AAOP acceptance / reroute / blocker / handoff
```

A grant is downstream derived state. It never outranks fresher project evidence or the current Working Contract.

## What the grant contains

The schema carries only execution-relevant facts:

- selected provider;
- current AAOP Route;
- Working Contract revision used to issue the grant;
- one bounded goal and baseline;
- single-agent vs justified Task Pod mode;
- bounded executable tasks and their verification/failure paths;
- read-only vs write-authorized mutation boundary;
- exact repository/base/working ref when writes are authorized;
- allowed and protected effects;
- required acceptance evidence;
- references back to authoritative AAOP/project evidence.

`human_open_questions` is constrained to an empty array. If a genuinely human-owned question is unresolved, AAOP has not reached the state where it may issue an execution grant.

Consumer products may maintain their own correlation identifier outside this schema and place a stable evidence pointer in `references` when useful. Product-specific objects, IDs and state models do not become AAOP grant fields merely because one consumer needs correlation.

## Exact write target

A provider must never infer a write destination from repository defaults.

For a write-authorized grant:

```text
repository + base_ref + working_ref
```

are mandatory.

For a read-only grant, `write_target` must be `null`.

A permissive host configuration or syntactically optional branch/ref field cannot widen this grant.

## Single agent and Task Pods

`execution_mode` is explicit:

- `single-agent` — `task_pod` must be `null`;
- `task-pod` — `task_pod` is required, carries one accountable owner, and is capped at 1–5 members.

This prevents an execution provider from turning a single-agent decision into an unsolicited multi-agent team merely because the runtime supports delegation.

## Relationship to Execution Plan

The grant is a bounded projection of currently runnable work, not a second planning system.

The task vocabulary intentionally follows the useful subset of `execution-plan.schema.json`:

- id;
- owner;
- dependencies/inputs;
- action;
- expected output;
- verification;
- failure path.

Do not persist a second long-horizon plan inside the provider. If the current evidence changes enough to alter Route, authorization, responsibility or acceptance, return to AAOP and issue a fresh grant.

## Relationship to provider state

Harness Session events, LoopX writeback, Codex/Claude output, workflow completion, and other provider-local records are **execution evidence**.

They do not mutate the grant into success by themselves.

Before accepting delivery, the AAOP coordinator re-reads the current authoritative target where practical and verifies the required acceptance evidence.

## Consumer correlation boundary

A consumer may correlate a grant with its own product-level object, ticket, case, work item, or UI state. That mapping remains consumer-owned.

AAOP does not standardize those product objects in the Provider Execution Grant. Consumers should retain their own mapping and, when useful, put a stable pointer in `references`. The provider executes the AAOP grant and returns evidence; the consumer updates its own state only after the appropriate acceptance decision.
