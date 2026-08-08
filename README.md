# Adaptive Agent Orchestration Protocol (AAOP)

AAOP is a host-agnostic **developer intake, routing, evidence, decision, policy, and integration layer** for AI-assisted software work.

The intended experience is simple:

> Open a project, say what you want in ordinary language, and let AAOP determine the smallest justified engineering path using the capabilities already available.

AAOP is **not** another agent runtime, package manager, workflow engine, or multi-agent framework.

## Use AAOP now

### 1. Open a terminal in your project

Then run one command.

**macOS / Linux**

```bash
curl -fsSL https://raw.githubusercontent.com/YuemingHub/Adaptive-Agent-Orchestration-Protocol/main/scripts/bootstrap.py | python3 - --target .
```

**Windows PowerShell**

```powershell
curl.exe -fsSL https://raw.githubusercontent.com/YuemingHub/Adaptive-Agent-Orchestration-Protocol/main/scripts/bootstrap.py | py - --target .
```

If your Windows Python command is `python`, replace `py` with `python`.

The bootstrap downloads the official AAOP repository archive into a temporary directory, delegates all project mutation to the canonical state-preserving installer, then runs a readiness check. It installs no third-party provider and asks for no secret.

If you prefer to inspect the bootstrap before running it:

```bash
curl -fsSL https://raw.githubusercontent.com/YuemingHub/Adaptive-Agent-Orchestration-Protocol/main/scripts/bootstrap.py -o aaop-bootstrap.py
python3 aaop-bootstrap.py --target .
```

For reproducible installation, pin `--ref` to a specific commit or tag instead of `main`.

### 2. Confirm that the project is ready

```bash
python .aaop/tools/aaop.py ready .
```

A usable installation prints:

```text
AAOP READY
  version: ...
  project: ...
  health: healthy
  ...
```

The same command also gives you a starter prompt.

### 3. Open the project in Codex, Claude Code, Cursor, or another host that reads project instructions

Then speak normally. For example:

```text
Understand this project and its current rules, determine the highest-value current executable step toward my goal, and continue autonomously. Reuse what already exists, preserve project intent, make ordinary engineering decisions yourself, verify the result, and ask only for genuinely missing authorization, credentials, or material product decisions.
```

Or give AAOP a concrete task:

```text
Login returns 500. Fix it and verify the regression.
```

```text
This repository is messy. Understand the current state and continue the most important existing work without rewriting things for appearance.
```

```text
Review this PR and tell me whether it is safe to merge. Do not change code unless I ask.
```

```text
Add family invitations while preserving the existing product rules and tests.
```

## What happens internally

```text
Natural-language request
        ↓
Developer Intake
        ↓
One primary Route
        ↓
Minimum sufficient project evidence
        ↓
Desired outcome vs current evidence
        ↓
Proven execution delta?
  yes → smallest coherent change
  no  → verified no-op / correct blocker
        ↓
Use existing capability first
        ↓
Only a real capability gap may justify a Provider
        ↓
Execute → revalidate write baseline → verify → reroute if evidence changes
```

Current primary routes:

| Situation | Route |
| --- | --- |
| idea / no trustworthy implementation | `idea-to-build` |
| messy or contradictory repository | `repo-recovery` |
| error / regression / failure | `bug-fix` |
| new or changed behavior | `feature-change` |
| explanation / review / adoption decision | `understand-review` |
| deploy / release / migration / incident | `release-operations` |

You do **not** choose the route, Agent count, Skill, MCP server, runtime, or workflow mode yourself.

## One user command surface

After installation, the main human-facing command is:

```bash
python .aaop/tools/aaop.py <command>
```

Useful commands:

```bash
# Am I ready to use AAOP here?
python .aaop/tools/aaop.py ready .

# Is the local AAOP installation healthy?
python .aaop/tools/aaop.py status .

# What project/tool/provider evidence is present?
python .aaop/tools/aaop.py doctor .

# Print the starter prompt
python .aaop/tools/aaop.py prompt

# Print installed AAOP version
python .aaop/tools/aaop.py version
```

Lower-level tools such as `health.py`, `doctor.py`, `route.py`, `recipe.py`, and `instructions.py` remain available for orchestration and debugging, but a normal user should not need to memorize them.

## Upgrade

Run the same bootstrap command again.

A recognizable AAOP installation is upgraded through the existing state-preserving installer. Bootstrap requires actual AAOP ownership evidence before it will claim an existing `.aaop/` directory: a managed install manifest is sufficient; for legacy no-manifest installs, the Orchestrator must contain a recognizable AAOP identity. A generic `.aaop` directory name or standalone `VERSION` file is **not** ownership evidence.

Upgrade preserves:

- `.aaop/runtime/`;
- project-owned files under `.aaop/`;
- non-AAOP text in `AGENTS.md` / `CLAUDE.md`;
- locally modified managed files as backups before canonical replacement;
- malformed bootstrap markers fail before package mutation.

## Remove AAOP

Use the same bootstrap surface with `--uninstall`.

**macOS / Linux**

```bash
curl -fsSL https://raw.githubusercontent.com/YuemingHub/Adaptive-Agent-Orchestration-Protocol/main/scripts/bootstrap.py | python3 - --target . --uninstall
```

**Windows PowerShell**

```powershell
curl.exe -fsSL https://raw.githubusercontent.com/YuemingHub/Adaptive-Agent-Orchestration-Protocol/main/scripts/bootstrap.py | py - --target . --uninstall
```

Removal is manifest-scoped: AAOP removes only what it can prove it owns, preserves runtime/project-owned files, preserves project rules outside AAOP markers, and does not uninstall third-party providers.

## Safety and autonomy boundary

AAOP aims for high autonomy without pretending all actions are equivalent.

- read/analyze/test/reversible project work: normally autonomous;
- ordinary engineering decisions within the stated goal: autonomous where project rules allow;
- credentials, new external accounts, costs, production writes, destructive changes, consequential publication, or materially expanded permissions: require the appropriate authorization;
- stale write/merge preconditions: re-read and reconcile instead of forcing over concurrent work;
- no proven current delta: do not manufacture a diff merely to look productive.

## What AAOP deliberately does not build

AAOP reuses mature upstream layers instead of recreating them. It does not try to become:

- a general agent runtime;
- a generic workflow engine;
- a global MCP/Skill/Agent registry;
- a package manager for third-party agent systems;
- a competing Skill/MCP/A2A protocol;
- an organizational control plane;
- a system that installs more tooling whenever work is blocked.

Integration Recipes can reference mature providers such as Agent Skills, MCP, ARD, Spec Kit, Playwright, mini-SWE-agent, OpenHands, Deep Agents, Microsoft Agent Framework, CAMEL, AutoAgent, and AgentSpace, but only a proven capability gap should justify adoption.

## Project principles that matter in practice

1. Situation before machinery.
2. Read accessible evidence before asking the user.
3. Respect project-specific instructions and source authority.
4. Read only enough evidence to change the current decision.
5. Cross-repository relevance does not automatically create cross-repository work scope.
6. Prove a real execution delta before mutation.
7. Accept a verified no-op when nothing should change.
8. Revalidate the target baseline immediately before consequential writes.
9. Reuse current capabilities before adding providers.
10. Classify blockers before calling them capability gaps.
11. Preserve project/runtime state across install, upgrade, and removal.
12. Verify the outcome, not merely that code was written.

## Repository map

```text
AGENTS.md / CLAUDE.md              host-native bootstrap
.aaop/
├── VERSION                        package release identity
├── VERSIONING.md                  package vs component revision contract
├── ORCHESTRATOR.md                canonical orchestration protocol
├── policies/                      autonomy / tool / integration boundaries
├── routes/                        Route Capability Packs
├── recipes/                       lazy provider integration knowledge
├── schemas/                       machine-readable contracts
├── skills/                        reusable orchestration procedures
└── tools/
    ├── aaop.py                    human-facing command surface
    ├── health.py
    ├── doctor.py
    ├── instructions.py
    ├── route.py
    └── recipe.py

scripts/
├── bootstrap.py                   zero-clone install / upgrade / removal
├── install.py                     canonical state-preserving package lifecycle
├── validate.py
└── validate_pressure.py

tests/pressure/                    real-project orchestration regressions
docs/                              detailed design and research
```

## Deeper documentation

- [`docs/QUICKSTART.md`](docs/QUICKSTART.md) — practical use and lifecycle details
- [`docs/DEVELOPER_ENTRYPOINT.md`](docs/DEVELOPER_ENTRYPOINT.md) — natural-language intake and routing
- [`docs/ROUTE_CAPABILITY_PACKS.md`](docs/ROUTE_CAPABILITY_PACKS.md) — route execution model
- [`docs/REAL_PROJECT_PRESSURE_TESTS.md`](docs/REAL_PROJECT_PRESSURE_TESTS.md) — real-project regression discipline
- [`docs/PROGRESSIVE_ADOPTION.md`](docs/PROGRESSIVE_ADOPTION.md) — capability/provider escalation
- [`docs/ECOSYSTEM_MAP.md`](docs/ECOSYSTEM_MAP.md) — what AAOP reuses rather than rebuilds
- [`docs/HOST_BOOTSTRAP_CONFORMANCE.md`](docs/HOST_BOOTSTRAP_CONFORMANCE.md) — Codex / Claude Code / Cursor entry behavior
- [`docs/INSTRUCTION_TOPOLOGY.md`](docs/INSTRUCTION_TOPOLOGY.md) — scoped project rule discovery

## Status

**v0.20.1 — usable baseline with ownership-safe bootstrap.**

v0.20 closes the human entry loop: zero-clone bootstrap, safe repeat-upgrade/removal through the same surface, one installed user CLI, readiness feedback, and a copyable natural-language starting point. v0.20.1 tightens bootstrap ownership proof so an existing unrelated `.aaop/` directory cannot be auto-claimed merely because it contains a generic version-like file.

AAOP still does not ship a standalone agent runtime or third-party package manager — intentionally.

## License

Apache-2.0. See `LICENSE`.
