# Host Bootstrap Conformance

AAOP should activate from the instruction-discovery surfaces that coding hosts already support. It should not require the developer to remember “read `.aaop` first,” and it should not create duplicate persistent context merely to support multiple hosts.

Host behavior is external and can change independently of AAOP. The facts below were last verified on **2026-08-08** and must be rechecked against first-party documentation when a host changes materially.

## Common strategy

```text
                 root AGENTS.md
               common AAOP bridge
                /             \
             Codex           Cursor
                               +
                        thin CLAUDE.md bridge
                               |
                          Claude Code

Both bridges
    ↓
.aaop/ORCHESTRATOR.md
    ↓
developer-intake → route-execution → current Route Pack
```

Rules:

1. Keep `.aaop/ORCHESTRATOR.md` canonical.
2. Keep root `AGENTS.md` as the common cross-host table of contents.
3. Keep root `CLAUDE.md` as a thin Claude-specific bridge, not a second copy of common AAOP rules.
4. Do not generate `.cursor/rules` merely to repeat `AGENTS.md`.
5. Preserve all project-owned text outside AAOP marker blocks.
6. Host-specific discovery/scoping facts belong in `adapters/`, not in the host-neutral Orchestrator.

## Codex

Verified first-party behavior:

- Codex supports repository `AGENTS.md` / `AGENTS.override.md` instruction discovery.
- Project instructions can be aggregated from the project root toward the current working directory; more-specific instruction files can refine root guidance.

AAOP mapping:

```text
root AGENTS.md
→ .aaop/ORCHESTRATOR.md
→ developer-intake
→ route-execution + one current route pack
```

No Codex-specific AAOP plugin is required.

Sources:

- https://openai.com/index/unrolling-the-codex-agent-loop/
- https://openai.com/index/introducing-codex/

## Claude Code

Verified first-party behavior:

- Claude Code automatically loads project `CLAUDE.md` memory/instructions.
- Claude Code can discover more-specific `CLAUDE.md` files when work enters nested subtrees.
- `CLAUDE.md` supports `@path` imports, but AAOP does not require an import chain for baseline startup.

AAOP mapping:

```text
root CLAUDE.md (thin bridge)
→ .aaop/ORCHESTRATOR.md
→ developer-intake
→ route-execution + one current route pack
```

The bridge stays small because the canonical policy is already under `.aaop/`.

Source:

- https://docs.anthropic.com/en/docs/claude-code/memory

## Cursor

Verified first-party behavior:

- Cursor supports root `AGENTS.md` as simple project instructions.
- Cursor CLI reads root `AGENTS.md` and root `CLAUDE.md` alongside `.cursor/rules`.

AAOP consequence:

> If AAOP copies the same full bootstrap into both root files, Cursor CLI receives duplicated persistent context.

AAOP mapping:

```text
AGENTS.md = common full bridge
CLAUDE.md = small Claude-specific bridge only
.cursor/rules = none by default
```

Project-specific Cursor rules remain valid when the project needs Cursor-native scoping, but they should point to canonical sources rather than clone the entire AAOP protocol.

Sources:

- https://docs.cursor.com/context/rules-for-ai
- https://docs.cursor.com/en/cli/using

## What conformance can and cannot prove

Static AAOP CI can prove:

- required bootstrap markers exist;
- common and Claude bridges point to the canonical AAOP startup files;
- the Claude bridge stays materially smaller than the common bridge;
- adapters identify the current first-party source of truth and verification date;
- baseline installation does not create `.cursor/rules` duplication.

Static CI cannot prove that a proprietary host actually loaded the files at runtime. Runtime host behavior must be rechecked against first-party documentation and, when practical, with a real host smoke test before claiming conformance after major host changes.

This distinction prevents AAOP from treating an adapter assumption as a permanent platform fact.
