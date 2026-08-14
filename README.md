# Adaptive Agent Orchestration Protocol (AAOP)

AAOP is a host-agnostic **developer intake, human-agent working contract, routing, evidence, decision, policy, and integration layer** for AI-assisted software work.

The intended experience is simple:

> Open a project, speak in ordinary language, let AAOP understand the project/idea and resolve what it can itself, confirm your collaboration style once, then let the Agent carry the engineering process through verified delivery.

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
  working contract: ...
  ...
```

The same command also gives you a starter prompt.

For an installation whose bootstrap provenance is `official-ref@stable`, a non-trivial takeover also checks whether that internally healthy package is still the current deliberately promoted stable control plane:

```bash
python .aaop/tools/source_freshness.py --json
```

`current` means the local package release identity matches official `stable`. `stale` means reuse the canonical stable bootstrap above, which preserves AAOP runtime/project-owned state, then rerun project compatibility evidence before trusting takeover/no-op/completion semantics. Network/source failure is `unknown`, not proof of either freshness or staleness. Exact/pinned/local sources are preserved rather than silently moved to `stable`.

### 3. Open the project in Codex, Claude Code, Cursor, or another host that reads project instructions

Then speak normally. A recommended first sentence is:

```text
Take responsibility for this project from the current evidence. First understand the project and reconcile AAOP continuity state. If my autonomous/collaborative working mode is not already established, ask me that one question once. Resolve everything the repository or your engineering judgment can resolve without asking me, ask only for genuinely human-owned product/domain decisions or authorization, then continue through implementation and verification without making me schedule the engineering process.
```

Once the Working Contract is established, a later session can be as short as:

```text
Continue.
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
I have an idea for an app. Help me think it through, ask only what I truly need to decide, then turn it into a real verified release.
```

AAOP first establishes/reuses the **Human-Agent Working Contract**: autonomous vs collaborative mode, aligned outcome, success evidence, and decision ownership. It then keeps one current Route at a time. A broad idea-to-production goal uses the end-to-end Delivery Journey only to preserve continuity across Route transitions; it does not create a seventh Route or a second workflow engine.

On a later session, the user may simply say `continue`, `keep going`, or `what next?`. Existing Working Contract + Journey checkpoints are continuity evidence. Developer intake reconciles them against current project/runtime/target facts rather than restarting discovery from the short new message or blindly trusting stale saved state.

## What happens internally

```text
Natural-language request
        ↓
Developer Intake + project evidence
        ↓
Human-Agent Working Contract
  evidence-resolvable → Agent inspects
  expert-decidable    → Agent/CTO decides
  human-owned         → ask only this
        ↓
Alignment Gate
        ↓
One primary Route
        ↓
Minimum sufficient project evidence
        ↓
Desired outcome vs current evidence
        ↓
Proven execution delta?
  yes → smallest coherent change
  no  → scope-level verified no-op / correct blocker
        ↓
Reconcile current project frontier before project-level no-op/pause
        ↓
One Agent by default
  justified specialization → bounded Task Pod (1–5, one accountable owner)
        ↓
Use existing capability first
        ↓
Only a real capability gap may justify a Provider
        ↓
Resolve explicit write target
        ↓
Execute conditionally → verify destination + outcome
        ↓
Handoff to next bounded Pod when responsibility materially changes
        ↓
Reroute if evidence changes
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

You do **not** choose the route, Agent count, Skill, MCP server, runtime, framework, database, or workflow engine yourself.

For a multi-route product goal, `.aaop/skills/end-to-end-delivery/SKILL.md` coordinates these existing Routes. A lightweight checkpoint under `.aaop/runtime/journeys/` preserves long-horizon continuity. `.aaop/runtime/working-contract.json` separately preserves the human/agent collaboration and alignment contract. Current repository/runtime/target evidence remains authoritative over both.

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
python .aaop/tools/source_freshness.py --json
```

Lower-level tools such as `health.py`, `doctor.py`, `source_freshness.py`, `route.py`, `recipe.py`, `journey.py`, `working_contract.py`, and `instructions.py` remain available for orchestration and debugging, but a normal user should not need to memorize them.

## Human-Agent Working Contract

The Working Contract prevents both under-autonomy and over-autonomy.

- **Autonomous delivery** — after alignment, ordinary reversible engineering continues without repeatedly asking the human to approve steps.
- **Collaborative delivery** — implementation still belongs to the Agent, but material product/architecture tradeoffs are surfaced at meaningful checkpoints.
- AAOP never silently chooses the mode when no established preference exists.
- Project evidence answers evidence-resolvable questions; the Agent/CTO answers expert-decidable engineering questions; only human-owned product/domain/authorization questions interrupt the user.
- Sustained execution is gated until goal, actor, situation, observable outcome and success evidence are explicit and no human-owned open question remains.
- Contract mutations use revision/CAS + OS locking so stale sessions do not overwrite newer decisions.

See [`docs/HUMAN_AGENT_WORKING_CONTRACT.md`](docs/HUMAN_AGENT_WORKING_CONTRACT.md).

## Task Pods

AAOP is not “multi-agent by default.” It starts with one capable Agent.

When specialization, context isolation, safe parallelism, independent review, or permission boundaries materially help, AAOP may create a temporary Task Pod:

- 1–5 members maximum;
- exactly one accountable owner;
- members exist for bounded responsibilities, not honorary titles;
- objective acceptance criteria;
- independent review for consequential work when practical;
- standardized handoff before a materially different next Pod takes over.

External role libraries such as `agency-agents-zh` are optional specialist sources. External orchestrators such as `agency-orchestrator` are optional delegated execution providers only when the host lacks a justified multi-role primitive. Neither becomes a second AAOP control plane.

## Upgrade

Run the current `stable` bootstrap command again. It upgrades only when the `stable` channel has been deliberately advanced to a new fully gated release candidate; ordinary commits to `main` do not change the production install path.

Starting with v1.1, a stable semantic package promotion must use a new package release identity. A `stable-managed` installation can therefore compare its local `.aaop/VERSION` with official stable through `source_freshness.py`; local `health` / `ready` alone are not freshness proof.

If a consumer is intentionally pinned to an exact commit, keep using that exact command for reproducibility. To upgrade it, choose the newly validated commit deliberately rather than silently replacing the pin.

A recognizable AAOP installation is upgraded through the existing state-preserving installer. Bootstrap requires actual AAOP ownership evidence before it will claim an existing `.aaop/` directory: a managed install manifest is sufficient; for legacy no-manifest installs, the Orchestrator must contain a recognizable AAOP identity. A generic `.aaop` directory name or standalone `VERSION` file is **not** ownership evidence.

Upgrade preserves:

- `.aaop/runtime/`, including Journey and Working Contract continuity;
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
- `stable` — production channel. Advance it only to a candidate that has already passed the full AAOP release gate and production-readiness checks relevant to that release, with a package VERSION that identifies that stable semantic release.
- exact commit — immutable revision pin for consumers that require repeatable source identity.

A green `main` commit does not automatically move `stable`. Promotion is a separate release decision so downstream repositories are not silently upgraded by ordinary AAOP development. Do not fast-forward `stable` across materially changed managed AAOP semantics while reusing the previous package VERSION.

## Safety and autonomy boundary

AAOP aims for high autonomy without pretending all actions are equivalent.

- collaboration mode determines how often material decisions are surfaced, not whether safety policy applies;
- evidence-resolvable questions are inspected rather than asked;
- ordinary technical/engineering decisions inside established constraints are Agent-owned;
- human-owned product/domain/business choices are asked only when evidence cannot resolve them;
- read/analyze/test/reversible project work: normally autonomous;
- credentials, new external accounts, costs, production writes, destructive changes, consequential publication, or materially expanded permissions: require the appropriate authorization;
- remote write destination: resolve explicitly when branch/ref/environment/destination omission would silently select a target;
- stale write/merge/Working Contract/Journey preconditions: re-read and reconcile instead of forcing over concurrent work;
- no proven current delta: do not manufacture a diff merely to look productive;
- a green/local no-mutation scope is not project completion while current authoritative work topology or unmet acceptance evidence still supplies a meaningful authorized frontier.

A repository API's default branch is metadata, not the default engineering write destination. When a project requires a working branch + PR, remote file/ref mutations must explicitly target that branch; a syntactically optional `branch`/`ref` field must not be omitted if omission writes to `main`, `production`, or another implicit destination. Verify after the write that the intended target changed and the protected/default target did not change unexpectedly.

A PR's current `mergeable` flag is also not proof of semantic independence from other active work. If the repository declares a predecessor/order, or concurrent PRs overlap an authority-critical surface, merge approval is conditional on that sequence. After the predecessor changes the base, rebuild/rebase the remaining delta, rerun affected validation, and review the new head rather than carrying forward an approval made against the old base.

For end-to-end delivery, a safely blocked release is not complete. Direct target-environment evidence is required to complete the current release cycle, and evidence from an earlier completed release cannot prove a later one.

A blocked Journey resumed by a terse `continue` request first re-checks the recorded unblock condition. Unchanged credentials, authorization, network, or external-dependency blockers are not permission to retry blindly or install workaround machinery.

Journey and Working Contract writes follow the same stale-write principle as consequential project writes: the coordinator reads the latest revision, reconciles current evidence, and writes only against that revision. Their tools serialize local mutation and reject stale revisions instead of allowing last-writer-wins state loss.

## What AAOP deliberately does not build

AAOP reuses mature upstream layers instead of recreating them. It does not try to become:

- a general agent runtime;
- a generic workflow engine;
- a global agent/MCP/Skill registry;
- a package manager for third-party agent systems;
- a competing Skill/MCP/A2A protocol;
- an organizational control plane;
- a system that installs more tooling whenever work is blocked.

Integration Recipes can reference mature providers such as Agent Skills, MCP, ARD, Spec Kit, Playwright, mini-SWE-agent, OpenHands, Deep Agents, Microsoft Agent Framework, CAMEL, AutoAgent, AgentSpace, plus optional current specialist/delegated sources such as `agency-agents-zh` and `agency-orchestrator`, but only a proven capability or responsibility gap should justify adoption. `agent-bundles` remains retired compatibility lineage only and is not a current provider for new specialist composition.

## Project principles that matter in practice

1. Situation before machinery.
2. Establish/reconcile the Human-Agent Working Contract before sustained execution.
3. Read accessible evidence before asking the user.
4. Resolve evidence-resolvable questions; let Agent/CTO decide expert-decidable engineering choices; ask only human-owned decisions.
5. Respect project-specific instructions and source authority.
6. Read only enough evidence to change the current decision.
7. Cross-repository relevance does not automatically create cross-repository work scope.
8. Prove a real execution delta before mutation.
9. Accept a scope-level verified no-op when nothing in that selected scope should change; reconcile the project frontier before promoting it to a project pause/completion claim.
10. Resolve the explicit destination before a consequential remote mutation; do not let an optional API field silently choose the write target.
11. Revalidate the target baseline immediately before consequential writes.
12. Treat PR merge approval as scoped to its reviewed base/head and declared predecessor order; textual mergeability is not semantic independence.
13. Reuse current capabilities before adding providers.
14. Classify blockers before calling them capability gaps.
15. Default to one Agent; Task Pods are bounded to 1–5 members with one accountable owner.
16. Role libraries and delegated orchestrators never become a second Working Contract/Journey control plane.
17. Preserve project/runtime state across install, upgrade, and removal.
18. Verify the outcome, not merely that code was written.
19. Preserve long-horizon Journey continuity without letting stale checkpoints override current evidence.
20. Scope production verification to the current release cycle.
21. Resume an existing Journey from Working Contract + checkpoint + current evidence before inferring a new goal from a terse continuation message.
22. Reject stale Journey/Working Contract writes rather than allowing parallel or old coordinator state to overwrite newer evidence.
23. Treat consumer adapters, pinned protocol/provider revisions, generated bridges, and cached observations as execution dependencies: verify their freshness when material, but never let them override project truth or auto-upgrade without a proven local delta.
24. Treat `stable` promotion as a release action with a new package release identity for materially changed managed semantics, not a synonym for whatever happens to be on `main`.
25. Reconcile material current PR/candidate/branch/handoff/predecessor-successor topology before claiming the delegated project has no executable frontier.

## Repository map

```text
AGENTS.md / CLAUDE.md              host-native bootstrap
.aaop/
├── VERSION                        package release identity
├── PRODUCTION_RELEASE.json        machine-readable production gate
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
    ├── source_freshness.py        stable-managed release identity check
    ├── doctor.py
    ├── instructions.py
    ├── journey.py                 revisioned Journey checkpoint continuity
    ├── working_contract.py        revisioned Human-Agent collaboration/alignment continuity
    ├── route.py
    └── recipe.py

scripts/
├── bootstrap.py                   zero-clone install / upgrade / removal
├── install.py                     canonical state-preserving package lifecycle
├── validate.py
├── validate_journey.py            cross-route Journey semantic regressions
├── validate_working_contract.py   Human-Agent/Task Pod interaction regressions
└── validate_pressure.py

tests/pressure/                    real-project orchestration regressions
docs/                              detailed design and research
```

## Deeper documentation

- [`docs/QUICKSTART.md`](docs/QUICKSTART.md) — practical use and lifecycle details
- [`docs/HUMAN_AGENT_WORKING_CONTRACT.md`](docs/HUMAN_AGENT_WORKING_CONTRACT.md) — collaboration modes, decision ownership, Task Pods and handoff
- [`docs/DEVELOPER_ENTRYPOINT.md`](docs/DEVELOPER_ENTRYPOINT.md) — natural-language intake and routing
- [`docs/UNIFIED_IDEA_TO_PRODUCTION_PIPELINE.md`](docs/UNIFIED_IDEA_TO_PRODUCTION_PIPELINE.md) — end-to-end Journey consolidation and failure invariants
- [`docs/ROUTE_CAPABILITY_PACKS.md`](docs/ROUTE_CAPABILITY_PACKS.md) — route execution model
- [`docs/REAL_PROJECT_PRESSURE_TESTS.md`](docs/REAL_PROJECT_PRESSURE_TESTS.md) — real-project regression discipline
- [`docs/PROGRESSIVE_ADOPTION.md`](docs/PROGRESSIVE_ADOPTION.md) — capability/provider escalation
- [`docs/ECOSYSTEM_MAP.md`](docs/ECOSYSTEM_MAP.md) — what AAOP reuses rather than rebuilds
- [`docs/HOST_BOOTSTRAP_CONFORMANCE.md`](docs/HOST_BOOTSTRAP_CONFORMANCE.md) — Codex / Claude Code / Cursor entry behavior
- [`docs/INSTRUCTION_TOPOLOGY.md`](docs/INSTRUCTION_TOPOLOGY.md) — scoped project rule discovery
- [`docs/PRODUCTION_RELEASE.md`](docs/PRODUCTION_RELEASE.md) — production candidate/promotion/rollback contract

## Status

**v1.2.0 — production release line governed by the AAOP production release contract.**

A source-tree or pull-request copy is not production merely because it carries the v1.2.0 package identity. A commit becomes an AAOP production release only after the final candidate passes every required workflow, a real downstream consumer validates the exact candidate tree from the current stable release, the candidate is merged without material tree drift, and `stable` is fast-forwarded to that validated merged commit.

v1.2 keeps the v1 Human-Agent Working Contract and v1.1 release/freshness semantics, while hardening project-frontier completion truth, exact evidence-target fidelity, verification-harness integrity, capability composition/transfer closure, pressure-backed project-completion benchmarking, and the boundary between AAOP's generic provider contracts and optional execution chassis such as DeepSeek Harness.

Accumulated production hardening also includes stable-vs-edge bootstrap separation and exact-ref pinning; bounded archive extraction; transactional install/upgrade/uninstall with interrupted-operation recovery; fail-closed manifest and Journey schema handling; Journey CAS/OS locking and last-good recovery; CPython 3.11–3.14 support across Linux/Windows/macOS; install provenance with managed-byte fingerprinting; immutable reviewed GitHub Action pins; and exact-candidate downstream consumer validation.

See [`docs/PRODUCTION_RELEASE.md`](docs/PRODUCTION_RELEASE.md) for promotion/rollback and [`.aaop/PRODUCTION_RELEASE.json`](.aaop/PRODUCTION_RELEASE.json) for required gate topology.

AAOP still does not ship a standalone agent runtime, third-party package manager, generic workflow engine, or repository merge-queue service — intentionally.

## License

Apache-2.0. See `LICENSE`.
