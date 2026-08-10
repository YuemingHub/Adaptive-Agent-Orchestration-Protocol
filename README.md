# Adaptive Agent Orchestration Protocol (AAOP)

AAOP is a host-agnostic **developer intake, routing, evidence, decision, policy, and integration layer** for AI-assisted software work.

The intended experience is simple:

> Open a project, say what you want in ordinary language, and let AAOP determine the smallest justified engineering path using the capabilities already available.

AAOP is **not** another agent runtime, package manager, workflow engine, or multi-agent framework.

## Use AAOP now

### 1. Open a terminal in your project

For normal/production use, install from the deliberately promoted `stable` channel rather than the fast-moving `main` development branch.

**macOS / Linux**

```bash
curl -fsSL https://raw.githubusercontent.com/YuemingHub/Adaptive-Agent-Orchestration-Protocol/stable/scripts/bootstrap.py | python3 - --target .
```

**Windows PowerShell**

```powershell
curl.exe -fsSL https://raw.githubusercontent.com/YuemingHub/Adaptive-Agent-Orchestration-Protocol/stable/scripts/bootstrap.py | py - --target .
```

If your Windows Python command is `python`, replace `py` with `python`.

The stable bootstrap downloads the AAOP archive from the same deliberately promoted channel into a temporary directory, validates compressed and expanded archive resource limits plus path safety, delegates all project mutation to the canonical state-preserving installer, then runs a readiness check. It installs no third-party provider and asks for no secret.

If you prefer to inspect the stable bootstrap before running it:

```bash
curl -fsSL https://raw.githubusercontent.com/YuemingHub/Adaptive-Agent-Orchestration-Protocol/stable/scripts/bootstrap.py -o aaop-bootstrap.py
python3 aaop-bootstrap.py --target .
```

### Exact-revision installation

`stable` is a release channel: it changes only when a candidate has passed the release gates, but it is intentionally movable. When the exact source revision must be reproducible, resolve and use one commit SHA for **both** the bootstrap script and package archive:

```bash
AAOP_REF=<validated-commit-sha>
curl -fsSL "https://raw.githubusercontent.com/YuemingHub/Adaptive-Agent-Orchestration-Protocol/${AAOP_REF}/scripts/bootstrap.py" | python3 - --target . --ref "${AAOP_REF}"
```

PowerShell:

```powershell
$AAOP_REF = '<validated-commit-sha>'
curl.exe -fsSL "https://raw.githubusercontent.com/YuemingHub/Adaptive-Agent-Orchestration-Protocol/$AAOP_REF/scripts/bootstrap.py" | py - --target . --ref $AAOP_REF
```

Using the same commit for both steps prevents a bootstrap from one revision from silently installing a package from another.

### Development / edge channel

`main` is the development channel. Opt into it explicitly only when testing unreleased AAOP changes:

```bash
curl -fsSL https://raw.githubusercontent.com/YuemingHub/Adaptive-Agent-Orchestration-Protocol/main/scripts/bootstrap.py | python3 - --target . --ref main
```

Do not use `main` merely because it is newer. A consumer should upgrade because a concrete compatibility, safety, or capability delta justifies the change.

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

For a broad novice goal, ordinary language is enough too:

```text
I have an idea for an app. Help me turn it into a real verified release and keep going across the necessary development stages.
```

AAOP keeps one current Route at a time. A broad idea-to-production goal uses the end-to-end Delivery Journey only to preserve continuity across Route transitions; it does not create a seventh Route or a second workflow engine.

On a later session, the user may simply say `continue`, `keep going`, or `what next?`. If an existing Journey checkpoint is present, developer intake treats it as continuity evidence, reconciles it against current project/runtime/target facts, and resumes the long-horizon goal rather than restarting discovery from the short new message.

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
Resolve explicit write target
        ↓
Execute conditionally → verify destination + outcome → reroute if evidence changes
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

For a multi-route product goal, `.aaop/skills/end-to-end-delivery/SKILL.md` coordinates these existing Routes. A lightweight checkpoint under `.aaop/runtime/journeys/` preserves continuity across sessions while current repository/runtime/target evidence remains authoritative.

## One user command surface

After installation, the main human-facing command is:

```bash
python .aaop/tools/aaop.py <command>
```

Useful commands:

```bash
python .aaop/tools/aaop.py ready .
python .aaop/tools/aaop.py status .
python .aaop/tools/aaop.py doctor .
python .aaop/tools/aaop.py prompt
python .aaop/tools/aaop.py version
```

Lower-level tools such as `health.py`, `doctor.py`, `route.py`, `recipe.py`, `journey.py`, and `instructions.py` remain available for orchestration and debugging, but a normal user should not need to memorize them.

## Upgrade

Run the current `stable` bootstrap command again. It upgrades only when the `stable` channel has been deliberately advanced to a new fully gated release candidate; ordinary commits to `main` do not change the production install path.

If a consumer is intentionally pinned to an exact commit, keep using that exact command for reproducibility. To upgrade it, choose the newly validated commit deliberately rather than silently replacing the pin.

A recognizable AAOP installation is upgraded through the existing state-preserving installer. Bootstrap requires actual AAOP ownership evidence before it will claim an existing `.aaop/` directory: a managed install manifest is sufficient; for legacy no-manifest installs, the Orchestrator must contain a recognizable AAOP identity. A generic `.aaop` directory name or standalone `VERSION` file is **not** ownership evidence.

Upgrade preserves:

- `.aaop/runtime/`, including Journey checkpoints;
- project-owned files under `.aaop/`;
- non-AAOP text in `AGENTS.md` / `CLAUDE.md`;
- locally modified managed files as backups before canonical replacement;
- malformed bootstrap markers fail before package mutation.

Legacy Journey checkpoints created by v0.21.0/v0.21.1 are preserved. Their first v0.21.2+ mutation treats the missing revision as revision `0` and requires an explicit latest-state write precondition before migrating the checkpoint.

A project-local AAOP/provider pin is not automatically wrong merely because upstream moved. It becomes a recovery concern only when the consumer relies on behavior that the pinned revision does not provide, or when stale adapter/profile evidence is being promoted into current execution truth. Upgrade only after proving that local compatibility/safety delta; then verify the consumer repository rather than assuming an upstream green build proves downstream compatibility.

## Remove AAOP

Use the stable bootstrap surface with `--uninstall`.

**macOS / Linux**

```bash
curl -fsSL https://raw.githubusercontent.com/YuemingHub/Adaptive-Agent-Orchestration-Protocol/stable/scripts/bootstrap.py | python3 - --target . --uninstall
```

**Windows PowerShell**

```powershell
curl.exe -fsSL https://raw.githubusercontent.com/YuemingHub/Adaptive-Agent-Orchestration-Protocol/stable/scripts/bootstrap.py | py - --target . --uninstall
```

Removal is manifest-scoped: AAOP removes only what it can prove it owns, preserves runtime/project-owned files, preserves project rules outside AAOP markers, and does not uninstall third-party providers.

## Release channels

- `main` — development/edge. It may advance whenever reviewed development work lands.
- `stable` — production channel. Advance it only to a candidate that has already passed the full AAOP release gate and production-readiness checks relevant to that release.
- exact commit — immutable revision pin for consumers that require repeatable source identity.

A green `main` commit does not automatically move `stable`. Promotion is a separate release decision so downstream repositories are not silently upgraded by ordinary AAOP development.

## Safety and autonomy boundary

AAOP aims for high autonomy without pretending all actions are equivalent.

- read/analyze/test/reversible project work: normally autonomous;
- ordinary engineering decisions within the stated goal: autonomous where project rules allow;
- credentials, new external accounts, costs, production writes, destructive changes, consequential publication, or materially expanded permissions: require the appropriate authorization;
- remote write destination: resolve explicitly when branch/ref/environment/destination omission would silently select a target;
- stale write/merge preconditions: re-read and reconcile instead of forcing over concurrent work;
- no proven current delta: do not manufacture a diff merely to look productive.

A repository API's default branch is metadata, not the default engineering write destination. When a project requires a working branch + PR, remote file/ref mutations must explicitly target that branch; a syntactically optional `branch`/`ref` field must not be omitted if omission writes to `main`, `production`, or another implicit destination. Verify after the write that the intended target changed and the protected/default target did not change unexpectedly.

A PR's current `mergeable` flag is also not proof of semantic independence from other active work. If the repository declares a predecessor/order, or concurrent PRs overlap an authority-critical surface, merge approval is conditional on that sequence. After the predecessor changes the base, rebuild/rebase the remaining delta, rerun affected validation, and review the new head rather than carrying forward an approval made against the old base.

For end-to-end delivery, a safely blocked release is not complete. Direct target-environment evidence is required to complete the current release cycle, and evidence from an earlier completed release cannot prove a later one.

A blocked Journey resumed by a terse `continue` request first re-checks the recorded unblock condition. Unchanged credentials, authorization, network, or external-dependency blockers are not permission to retry blindly or install workaround machinery.

Journey checkpoint writes follow the same stale-write principle as consequential project writes: the coordinator reads the latest checkpoint revision, reconciles current evidence, and writes only against that revision. `journey.py` serializes local mutation and rejects a stale revision instead of allowing last-writer-wins state loss.

## What AAOP deliberately does not build

AAOP reuses mature upstream layers instead of recreating them. It does not try to become:

- a general agent runtime;
- a generic workflow engine;
- a global agent/MCP/Skill registry;
- a package manager for third-party agent systems;
- a competing Skill/MCP/A2A protocol;
- an organizational control plane;
- a system that installs more tooling whenever work is blocked.

Integration Recipes can reference mature providers such as Agent Skills, MCP, ARD, Spec Kit, Playwright, mini-SWE-agent, OpenHands, Deep Agents, Microsoft Agent Framework, CAMEL, AutoAgent, AgentSpace, and optional specialist sources such as agent-bundles, but only a proven capability or responsibility gap should justify adoption.

## Project principles that matter in practice

1. Situation before machinery.
2. Read accessible evidence before asking the user.
3. Respect project-specific instructions and source authority.
4. Read only enough evidence to change the current decision.
5. Cross-repository relevance does not automatically create cross-repository work scope.
6. Prove a real execution delta before mutation.
7. Accept a verified no-op when nothing should change.
8. Resolve the explicit destination before a consequential remote mutation; do not let an optional API field silently choose the write target.
9. Revalidate the target baseline immediately before consequential writes.
10. Treat PR merge approval as scoped to its reviewed base/head and declared predecessor order; textual mergeability is not semantic independence.
11. Reuse current capabilities before adding providers.
12. Classify blockers before calling them capability gaps.
13. Preserve project/runtime state across install, upgrade, and removal.
14. Verify the outcome, not merely that code was written.
15. Preserve long-horizon Journey continuity without letting stale checkpoints override current evidence.
16. Scope production verification to the current release cycle.
17. Resume an existing Journey from checkpoint + current evidence before inferring a new goal from a terse continuation message.
18. Reject stale Journey checkpoint writes rather than allowing parallel or old coordinator state to overwrite newer evidence.
19. Treat consumer adapters, pinned protocol/provider revisions, generated bridges, and cached observations as execution dependencies: verify their freshness when material, but never let them override project truth or auto-upgrade without a proven local delta.
20. Treat `stable` promotion as a release action, not a synonym for whatever happens to be on `main`.

## Repository map

```text
AGENTS.md / CLAUDE.md              host-native bootstrap
.aaop/
├── VERSION                        package release identity
├── VERSIONING.md                  package vs component revision contract
├── ORCHESTRATOR.md                canonical orchestration protocol
├── journeys/                      multi-route continuity definitions
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
    ├── journey.py                 revisioned Journey checkpoint continuity
    ├── route.py
    └── recipe.py

scripts/
├── bootstrap.py                   zero-clone install / upgrade / removal
├── install.py                     canonical state-preserving package lifecycle
├── validate.py
├── validate_journey.py            cross-route Journey semantic regressions
└── validate_pressure.py

tests/pressure/                    real-project orchestration regressions
docs/                              detailed design and research
```

## Deeper documentation

- [`docs/QUICKSTART.md`](docs/QUICKSTART.md) — practical use and lifecycle details
- [`docs/DEVELOPER_ENTRYPOINT.md`](docs/DEVELOPER_ENTRYPOINT.md) — natural-language intake and routing
- [`docs/UNIFIED_IDEA_TO_PRODUCTION_PIPELINE.md`](docs/UNIFIED_IDEA_TO_PRODUCTION_PIPELINE.md) — end-to-end Journey consolidation and failure invariants
- [`docs/ROUTE_CAPABILITY_PACKS.md`](docs/ROUTE_CAPABILITY_PACKS.md) — route execution model
- [`docs/REAL_PROJECT_PRESSURE_TESTS.md`](docs/REAL_PROJECT_PRESSURE_TESTS.md) — real-project regression discipline
- [`docs/PROGRESSIVE_ADOPTION.md`](docs/PROGRESSIVE_ADOPTION.md) — capability/provider escalation
- [`docs/ECOSYSTEM_MAP.md`](docs/ECOSYSTEM_MAP.md) — what AAOP reuses rather than rebuilds
- [`docs/HOST_BOOTSTRAP_CONFORMANCE.md`](docs/HOST_BOOTSTRAP_CONFORMANCE.md) — Codex / Claude Code / Cursor entry behavior
- [`docs/INSTRUCTION_TOPOLOGY.md`](docs/INSTRUCTION_TOPOLOGY.md) — scoped project rule discovery

## Status

**v0.22.0 — production bootstrap channel and bounded archive extraction.**

v0.22.0 separates ordinary development from production bootstrap behavior. `stable` is now the default package ref and recommended user-facing bootstrap channel; `main` is explicit edge/development opt-in. Exact-commit bootstrap/package pinning remains available for immutable revision reproducibility. Bootstrap also rejects dangerous archive paths plus excessive member count, per-member expanded size, total expanded size, and encrypted members before extraction, so a small compressed archive cannot consume unbounded disk during install.

v0.21.5 hardens multi-PR convergence: GitHub textual mergeability no longer counts as proof that active PRs are semantically independent. `understand-review` now treats repository-declared predecessor order, shared authority/configuration surfaces, and base/head relationships as merge evidence. A dependent PR built before its required predecessor is only conditionally mergeable; once the predecessor lands, the dependent delta must be rebuilt/rebased from the new base, affected validation rerun, and the new head reviewed.

v0.21.4 requires explicit remote write destinations before conditional mutation. v0.21.3 hardens consumer integration freshness. v0.21.2 adds revisioned Journey checkpoint CAS + OS locking, including Windows coverage. v0.21.1 hardens terse cross-session continuation. v0.21 introduced the resumable idea-to-production Delivery Journey on top of the six existing Routes.

AAOP still does not ship a standalone agent runtime, third-party package manager, generic workflow engine, or repository merge-queue service — intentionally.

## License

Apache-2.0. See `LICENSE`.
