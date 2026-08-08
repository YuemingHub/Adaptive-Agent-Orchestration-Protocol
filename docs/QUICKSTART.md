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
- an install manifest tracks hashes of AAOP-managed files;
- if a managed file was locally modified, it is backed up under `.aaop/runtime/upgrade-backups/` before the canonical version replaces it;
- if a future AAOP release starts managing a path that already belongs to the project, that colliding file is backed up before AAOP claims the path;
- malformed/duplicated bootstrap markers fail preflight before package mutation;
- target-only project files are never removed merely because an AAOP release does not know about them.

`--force` remains as a compatibility alias for `--upgrade`; it no longer means destructive replacement of the whole `.aaop` directory.

Legacy installations created before install manifests existed can also be upgraded. Their runtime and target-only files are preserved, but because old hashes are unavailable, the installer cannot distinguish local edits to legacy AAOP-managed paths before refreshing those current paths.

## 3. Give the outcome, not the team design

Prefer:

> Make the signup flow production-ready, including validation and regression checks. Preserve the current product principles. Handle ordinary engineering decisions yourself; ask only if you need a new credential or a material product decision.

Instead of:

> Create a PM agent, frontend agent, backend agent and QA agent, then use Playwright MCP.

AAOP is supposed to derive the required capabilities and provider mix from the project.

## 4. What the agent should do

For a meaningful task, expect this internal sequence:

1. inspect environment and project evidence;
2. resolve intended outcome and acceptance evidence;
3. derive required capabilities;
4. match existing Skills/tools/MCP/scripts;
5. resolve only real capability gaps;
6. decide whether one agent or multiple owners are justified;
7. execute dependency-aware work;
8. verify independently;
9. replan if evidence fails;
10. deliver results and remaining risks.

The agent does not need to show every runtime artifact to the user. The schemas exist to improve rigor and interoperability.

## 5. If an MCP/provider is needed

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

## 6. Validate AAOP

From the AAOP repository:

```bash
python scripts/validate.py
python scripts/validate_pressure.py
```

This verifies required protocol files, JSON syntax/schema markers, Skill presence, route/Recipe contracts, and real-project pressure guards without third-party Python packages.

## 7. Native host integration

See:

- `adapters/codex.md`
- `adapters/claude-code.md`
- `adapters/cursor.md`
- `adapters/generic.md`

Host adapters may evolve more quickly than the core protocol. Keep host-specific paths and permission knobs out of `.aaop/ORCHESTRATOR.md` unless they become genuinely portable concepts.
