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

- copies the canonical `.aaop/` package;
- creates or appends an AAOP bootstrap block in `AGENTS.md`;
- creates or appends an AAOP bootstrap block in `CLAUDE.md`;
- does not replace unrelated existing project rules;
- does not copy or request secrets.

If the target already contains `.aaop/`, the installer refuses to overwrite it. Review the change first, then deliberately update with:

```bash
python scripts/install.py /path/to/your-project --force
```

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

## 5. If an MCP is needed

AAOP should not ask “Which MCP do you want?” by default.

It should first check whether the required capability already exists. If not, it should recommend the lowest-risk sufficient provider and tell you exactly:

- why it is needed;
- where it comes from;
- what to install/connect;
- minimum permission required;
- whether credentials or cost are involved;
- what data/action access it gains.

You provide the authorization that only you can provide; the orchestrator does the rest.

## 6. Validate AAOP

From the AAOP repository:

```bash
python scripts/validate.py
```

This verifies required protocol files, JSON syntax/schema markers, Skill presence, and core Agent Skills naming/metadata constraints without third-party Python packages.

## 7. Native host integration

See:

- `adapters/codex.md`
- `adapters/claude-code.md`
- `adapters/cursor.md`
- `adapters/generic.md`

Host adapters may evolve more quickly than the core protocol. Keep host-specific paths and permission knobs out of `.aaop/ORCHESTRATOR.md` unless they become genuinely portable concepts.
