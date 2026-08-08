# Instruction Topology Inventory

AAOP installs a host-native root bootstrap, but real repositories can already contain additional scoped instruction layers. Those layers can materially change what a coding host sees for a given working directory or referenced file.

AAOP therefore treats **instruction topology as project evidence**, not as something the installer should normalize automatically.

Host behavior last verified: **2026-08-08**.

## Why this exists

A repository can contain combinations such as:

```text
AGENTS.md
backend/AGENTS.md
backend/AGENTS.override.md

CLAUDE.md
services/CLAUDE.md
legacy/CLAUDE.local.md

.cursor/rules/global.mdc
frontend/.cursor/rules/ui.mdc
.cursorrules
```

The root AAOP bootstrap may still be correct, but it is not necessarily the only instruction context that matters.

The wrong response would be to rewrite or delete these files merely to make AAOP look uniform. The correct first step is to **see the topology**.

## Read-only inventory

```bash
python .aaop/tools/instructions.py .
python .aaop/tools/instructions.py . --json
```

The tool reports documented filesystem instruction surfaces for:

- Codex;
- Claude Code;
- Cursor.

It also emits small observations such as:

- nested Codex instruction files exist;
- the same directory contains both `AGENTS.md` and `AGENTS.override.md`;
- nested Claude memory files exist;
- deprecated `CLAUDE.local.md` exists;
- nested Cursor `.cursor/rules/*.mdc` exist;
- deprecated root `.cursorrules` exists;
- AAOP root marker blocks are present.

These observations are review hints, not conflict verdicts.

## Codex model

Current first-party documentation says Codex aggregates project instructions from the Git/project root toward the current working directory, using `AGENTS.override.md`, `AGENTS.md`, and optionally configured fallback filenames. More-specific instructions appear later in the aggregated user instructions.

AAOP inventories repository-local:

- `AGENTS.md`;
- `AGENTS.override.md`.

It does **not** try to resolve:

- `$CODEX_HOME` user instructions;
- `project_doc_fallback_filenames` from arbitrary user config;
- the exact effective prompt for every possible future `cwd`.

Source:

- https://openai.com/index/unrolling-the-codex-agent-loop/

## Claude Code model

Current first-party documentation says Claude Code:

- reads `CLAUDE.md` / `CLAUDE.local.md` along the current working directory ancestry;
- can discover nested `CLAUDE.md` in child subtrees when files there are read;
- supports `@path` imports;
- documents `CLAUDE.local.md` as deprecated in favor of imports.

AAOP inventories repository-local:

- `CLAUDE.md`;
- `CLAUDE.local.md`.

It does **not** resolve:

- user-level `~/.claude/CLAUDE.md`;
- recursive `@imports`;
- which nested subtree the current task will actually enter.

Source:

- https://docs.anthropic.com/en/docs/claude-code/memory

## Cursor model

Current first-party documentation says Cursor:

- supports project rules in `.cursor/rules`;
- supports nested `.cursor/rules` directories scoped to nearby subtrees;
- supports root `AGENTS.md` as a simple global project instruction alternative;
- still supports root `.cursorrules`, but marks it deprecated;
- Cursor CLI also reads root `AGENTS.md` and root `CLAUDE.md` alongside `.cursor/rules`.

AAOP inventories:

- root `AGENTS.md`;
- root `CLAUDE.md` for Cursor CLI context;
- all repository `.cursor/rules/*.mdc` surfaces, including nested rule directories;
- root `.cursorrules`.

For `.mdc` files, AAOP reads only a few simple frontmatter hints (`description`, `globs`, `alwaysApply`) to help explain potential scope. It does not claim that every discovered rule is active for every task.

Sources:

- https://docs.cursor.com/context/rules-for-ai
- https://docs.cursor.com/en/cli/using

## Conflict boundary

Instruction topology is not a conflict resolver.

AAOP MUST NOT infer:

```text
nested file exists
→ nested file is correct

newer file exists
→ newer rule wins semantically

legacy file exists
→ delete/migrate it automatically

another host reads this file
→ rewrite it for cross-host uniformity
```

When instructions materially disagree:

1. determine which host/scope is actually relevant to the current task;
2. read the conflicting content;
3. apply explicit repository/host precedence rules where known;
4. preserve unresolved product/governance conflicts as evidence;
5. ask only when a genuine user-owned decision remains.

## Privacy and performance

The inventory stays inside the project root and skips common dependency/generated directories such as `.git`, `node_modules`, virtual environments, build output, and vendor directories.

Do not recursively inventory instruction topology for every tiny request. Use it when the repository is unfamiliar, scoped rules are visible, a monorepo has multiple instruction layers, or rule scope can materially change the work.

## Machine-readable output

When useful, save the JSON output to:

```text
.aaop/runtime/instruction-topology.json
```

against:

```text
.aaop/schemas/instruction-topology.schema.json
```

The runtime artifact is derived evidence and normally remains uncommitted.
