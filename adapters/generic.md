# Generic Host Adapter

Use this adapter for any AI IDE, coding agent, workflow engine, or LLM host that can read project files but has no dedicated AAOP adapter.

## Minimum host requirement

The host must be able to receive:

1. the user's task;
2. `AGENTS.md`;
3. `.aaop/ORCHESTRATOR.md`;
4. relevant project files.

Everything else is optional.

## Capability levels

### Level 0 — text-only LLM

- Load AAOP instructions manually.
- Simulate team ownership as explicit sequential roles.
- The user or another system performs real-world actions.

### Level 1 — single agent + filesystem/tools

- Execute the full AAOP cycle.
- Use canonical Skills by reading their `SKILL.md` when relevant.
- Represent separate owners as isolated sequential task contexts.

### Level 2 — task workers / background sessions

- Map independent AAOP owners to workers/sessions.
- Keep the lead agent as orchestrator.
- Return bounded outputs/evidence to the lead.

### Level 3 — native multi-agent / teams

- Create real workers only after capability planning.
- Use tool/permission boundaries per owner.
- Use direct peer coordination only when the execution graph benefits from it.

## Skill compatibility

AAOP canonical Skills follow the open Agent Skills structure. If the host has a native Skill installer, install/mirror `.aaop/skills/<name>/` into its documented project Skill location. Otherwise read the Skill directly on demand.

## Tool compatibility

Translate host tools into capability providers rather than changing the core protocol. For example:

```text
host filesystem search → project-discovery provider
browser automation      → browser-validation provider
GitHub connector        → repository-operations provider
database connector      → data-access provider
```

If the host cannot perform a required external action, continue all independent work and return the smallest concrete handoff required from the user or another system.
