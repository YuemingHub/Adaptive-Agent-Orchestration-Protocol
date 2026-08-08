# AAOP Quick Start

## 1. Use AAOP inside this repository

Open the repository in an AI host that reads project instructions and state an outcome, for example:

> Review this project and make the orchestration protocol actually usable across Codex, Claude Code and Cursor. Resolve ordinary implementation details autonomously and verify the result.

The host should read `AGENTS.md` / `CLAUDE.md`, then `.aaop/ORCHESTRATOR.md`, discover the project, derive capabilities, and choose the minimum sufficient execution structure.

## 2. Install AAOP into another project

From a clone of this repository:

```bash
python scripts/install.py /path/to/your-project
```

The installer:

- copies the canonical AAOP-managed files into `.aaop/`;
- creates or appends a marked AAOP bootstrap block in `AGENTS.md`;
- creates or appends a marked AAOP bootstrap block in `CLAUDE.md`;
- does not replace unrelated existing project rules;
- records a managed-file + bootstrap integrity baseline in `.aaop/.install-manifest.json`;
- installs no third-party provider;
- does not copy or request secrets.

### Upgrade an existing AAOP installation

If the target already contains `.aaop/`, use:

```bash
python scripts/install.py /path/to/your-project --upgrade
```

Safe upgrade rules:

- `.aaop/runtime/` is preserved;
- files inside `.aaop/` that were not installed/managed by AAOP are preserved;
- AAOP bootstrap text between `<!-- AAOP:BEGIN -->` / `<!-- AAOP:END -->` is updated in place while surrounding project rules remain untouched;
- an install manifest tracks hashes of AAOP-managed files and the canonical marked bootstrap blocks;
- if a managed file was locally modified, it is backed up under `.aaop/runtime/upgrade-backups/` before the canonical version replaces it;
- if a future AAOP release starts managing a path that already belongs to the project, that colliding file is backed up before AAOP claims the path;
- malformed/duplicated bootstrap markers fail preflight before package mutation;
- target-only project files are never removed merely because an AAOP release does not know about them.

`--force` remains as a compatibility alias for `--upgrade`; it no longer means destructive replacement of the whole `.aaop` directory.

Legacy installations created before install manifests existed can also be upgraded. Their runtime and target-only files are preserved, but because old hashes are unavailable, the installer cannot distinguish local edits to legacy AAOP-managed paths before refreshing those current paths.

### Safely remove AAOP

AAOP should also be easy to leave without making the developer understand which files are safe to delete.

For a manifest-tracked installation:

```bash
python scripts/install.py /path/to/your-project --uninstall
```

Safe removal rules:

- remove only files listed as AAOP-owned in `.aaop/.install-manifest.json`;
- remove only the marked AAOP blocks from `AGENTS.md` / `CLAUDE.md`;
- preserve all text outside those markers;
- preserve `.aaop/runtime/`;
- preserve project-owned files under `.aaop/` that are not in the manifest;
- back up locally modified AAOP-managed files under `.aaop/runtime/uninstall-backups/` before removing their canonical path;
- leave third-party providers, MCP configuration, project dependencies, and other ecosystem tools untouched;
- refuse malformed/duplicated bootstrap markers before deleting package files;
- refuse automatic uninstall when no install manifest exists, because ownership cannot be inferred safely.

For a legacy no-manifest installation, first run a trusted safe upgrade to establish explicit ownership, then uninstall:

```bash
python scripts/install.py /path/to/your-project --upgrade
python scripts/install.py /path/to/your-project --uninstall
```

If runtime history or project-owned `.aaop` files remain after uninstall, the `.aaop/` directory intentionally remains. If nothing project-owned remains, empty AAOP directories may disappear.

Safe removal does **not** uninstall Playwright, MCP servers, AutoAgent, Deep Agents, or any other provider. Those resources were not installed merely because AAOP referenced or selected them, and their lifecycle must follow their own provenance/ownership.

## 3. Check installation health before repairing it

An installed AAOP can be inspected without changing anything:

```bash
python .aaop/tools/health.py .
python .aaop/tools/health.py . --json
```

The health tool compares the current installation with its local install baseline and reports states such as:

```text
healthy
upgrade-recommended
legacy-install
drifted
incomplete
invalid-manifest
unsupported-manifest
```

It checks:

- package VERSION vs the tracked manifest version;
- missing/modified/unreadable AAOP-managed files;
- `AGENTS.md` / `CLAUDE.md` AAOP marker shape;
- whether the marked bootstrap block still matches what the installer wrote;
- whether the integrity manifest is an older compatible baseline.

Important boundary:

> **Health means “matches this installation baseline,” not “latest upstream” and not “cryptographically trusted.”**

The tool is for accidental/local drift caused by edits, partial copies, stale bootstrap blocks, or interrupted maintenance. A modified `health.py` itself could lie, so it is not an adversarial tamper-proof trust root.

Do not silently repair `drifted` or `incomplete` installations. Review the listed differences first. When canonical repair is intended, run `--upgrade` from a trusted AAOP source; locally modified managed files are backed up before replacement.

## 4. Give the outcome, not the team design

Prefer:

> Make the signup flow production-ready, including validation and regression checks. Preserve the current product principles. Handle ordinary engineering decisions yourself; ask only if you need a new credential or a material product decision.

Instead of:

> Create a PM agent, frontend agent, backend agent and QA agent, then use Playwright MCP.

AAOP is supposed to derive the required capabilities and provider mix from the project.

## 5. What the agent should do

For a meaningful task, expect this internal sequence:

1. when AAOP integrity is uncertain, inspect installation health before trusting or repairing local protocol files;
2. inspect environment and project evidence;
3. resolve intended outcome and acceptance evidence;
4. derive required capabilities;
5. match existing Skills/tools/MCP/scripts;
6. resolve only real capability gaps;
7. decide whether one agent or multiple owners are justified;
8. execute dependency-aware work;
9. verify independently;
10. replan if evidence fails;
11. deliver results and remaining risks.

The agent does not need to show every runtime artifact to the user. The schemas exist to improve rigor and interoperability.

## 6. If an MCP/provider is needed

AAOP should not ask “Which MCP do you want?” by default.

It should first check whether the required capability already exists. If not, it should recommend the lowest-risk sufficient provider and tell you exactly:

- why it is needed;
- where it comes from;
- what to install/connect;
- minimum permission required;
- whether credentials or cost are involved;
- what data/action access it gains;
- whether the selected Recipe carries a scoped adoption review that must be rechecked for this use.

You provide the authorization that only you can provide; the orchestrator does the rest.

## 7. Validate AAOP

From the AAOP repository:

```bash
python scripts/validate.py
python scripts/validate_pressure.py
python .aaop/tools/health.py .
```

The first two commands verify source package structure and real-project pressure regressions. In the AAOP source repository, `health.py` reports `source-tree` because source development is not an installed manifest-tracked package.

## 8. Native host integration

See:

- `adapters/codex.md`
- `adapters/claude-code.md`
- `adapters/cursor.md`
- `adapters/generic.md`

Host adapters may evolve more quickly than the core protocol. Keep host-specific paths and permission knobs out of `.aaop/ORCHESTRATOR.md` unless they become genuinely portable concepts.
