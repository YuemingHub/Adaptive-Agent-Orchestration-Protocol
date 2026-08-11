# AAOP Quick Start

This guide is for a developer who wants to **use AAOP now**, not study the whole protocol first.

## 1. Install AAOP into the project you want to work on

Open a terminal in that project. Normal/production use follows the deliberately promoted `stable` channel, not the fast-moving `main` development branch.

### macOS / Linux

```bash
curl -fsSL https://raw.githubusercontent.com/YuemingHub/Adaptive-Agent-Orchestration-Protocol/stable/scripts/bootstrap.py | python3 - --target .
```

### Windows PowerShell

```powershell
curl.exe -fsSL https://raw.githubusercontent.com/YuemingHub/Adaptive-Agent-Orchestration-Protocol/stable/scripts/bootstrap.py | py - --target .
```

If your Python command is `python`, use it instead of `py` / `python3`.

The bootstrap:

- downloads the AAOP repository archive for the selected ref into a temporary directory;
- rejects unsafe paths, encrypted members, excessive archive member counts, excessive per-member expanded size, and excessive total expanded size before extraction;
- validates that the archive contains a recognizable AAOP source package;
- uses the canonical `scripts/install.py` for all target mutation;
- preserves unrelated project rules in `AGENTS.md` / `CLAUDE.md`;
- writes AAOP under `.aaop/` and records ownership in `.aaop/.install-manifest.json`;
- installs no third-party provider;
- requests no secret;
- runs a readiness check after installation.

### Inspect-first option

If you do not want to pipe a remote script directly into Python:

```bash
curl -fsSL https://raw.githubusercontent.com/YuemingHub/Adaptive-Agent-Orchestration-Protocol/stable/scripts/bootstrap.py -o aaop-bootstrap.py
python3 aaop-bootstrap.py --target .
```

Review the downloaded file before executing it.

### Pin an exact revision

`stable` is a deliberately promoted release channel and may move when a new candidate passes all release gates. For immutable revision reproducibility, use the same exact commit for both the bootstrap script and archive:

```bash
AAOP_REF=<validated-commit-sha>
curl -fsSL "https://raw.githubusercontent.com/YuemingHub/Adaptive-Agent-Orchestration-Protocol/${AAOP_REF}/scripts/bootstrap.py" | python3 - --target . --ref "${AAOP_REF}"
```

PowerShell:

```powershell
$AAOP_REF = '<validated-commit-sha>'
curl.exe -fsSL "https://raw.githubusercontent.com/YuemingHub/Adaptive-Agent-Orchestration-Protocol/$AAOP_REF/scripts/bootstrap.py" | py - --target . --ref $AAOP_REF
```

### Opt into development / edge

`main` is not the production default. Use it explicitly only when testing unreleased AAOP changes:

```bash
curl -fsSL https://raw.githubusercontent.com/YuemingHub/Adaptive-Agent-Orchestration-Protocol/main/scripts/bootstrap.py | python3 - --target . --ref main
```

## 2. Confirm AAOP is ready

```bash
python .aaop/tools/aaop.py ready .
```

A normal installed project should report:

```text
AAOP READY
  version: <installed version>
  project: <your project>
  health: healthy
  working contract: <uninitialized|present> mode=<...> alignment=<...> execution=<gated|allowed>
```

`AAOP READY` means the package is healthy enough to use. The Working Contract can still be `uninitialized` on first use; that is expected and is resolved through normal conversation, not by asking the user to edit JSON.

If it says `REVIEW REQUIRED`, follow the `Next:` line instead of blindly reinstalling.

## 3. Open the project in your normal AI coding host

AAOP is designed to enter through project instruction surfaces your host already understands.

Supported target shapes include:

- Codex → `AGENTS.md` and scoped project rules;
- Claude Code → `CLAUDE.md` plus project rules;
- Cursor → root project instructions and relevant scoped rules;
- other coding agents that can read project files/instructions → generic AAOP bootstrap path.

You do not need to choose Routes, Skills, Agents, MCP servers, runtimes, frameworks, databases, or orchestration topology.

## 4. Say what you want in ordinary language

Recommended first prompt:

```text
AAOP: take over this project.
```

This means: recover the current project and intent from evidence, choose the highest-value
safe next goal, implement and verify it, then keep selecting the next verified delta.
You do not need to know the project stage or give AAOP a roadmap. If the autonomous or
collaborative preference is not already established, AAOP asks that one question once;
an explicit takeover request is an autonomous preference. It returns only for an
irreducible product/domain decision, credentials or external-account access, new cost,
production authorization, or irreversible/high-impact action.

If this is a new idea:

```text
I have an idea: <describe it normally>. Help me think it through, research what can be researched, ask only what I truly need to decide, then turn the aligned idea into a verified product slice and keep going.
```

Concrete tasks are better when you have one:

```text
Login returns 500. Fix it and verify the regression.
```

```text
Add family invitations while preserving the existing product rules and tests.
```

```text
This repository is messy. Reconstruct the current state, identify the real next executable work, and continue without cosmetic rewrites.
```

```text
Review this change and tell me whether it is safe to merge. Stay read-only unless I ask for implementation.
```

### What happens the first time

If no Working Contract exists, the Agent should first inspect the project and initialize the known goal. If your collaboration preference is not already established from authoritative context, it asks one question:

```text
For this project, should I normally:
A. work autonomously after we align the goal, only returning for human-owned decisions/authorization/final acceptance; or
B. work collaboratively and surface material checkpoints as we go?
```

The answer is persisted project-locally. A later `continue` should not ask again unless the preference itself changes.

## 5. The one user CLI

Normal human-facing commands use:

```bash
python .aaop/tools/aaop.py <command>
```

### Readiness

```bash
python .aaop/tools/aaop.py ready .
```

### Installation health

```bash
python .aaop/tools/aaop.py status .
```

### Environment/project evidence

```bash
python .aaop/tools/aaop.py doctor .
```

For one known route:

```bash
python .aaop/tools/aaop.py doctor . --route feature-change
```

### Starter prompt

```bash
python .aaop/tools/aaop.py prompt
```

### Version

```bash
python .aaop/tools/aaop.py version
```

Lower-level tools remain available under `.aaop/tools/`, including `working_contract.py`, but ordinary use should not require memorizing them.

## 6. What the agent should do after your request

Internally, expect approximately this shape:

```text
your request
→ inspect current project/rules/continuity
→ establish/reconcile Human-Agent Working Contract
→ evidence-resolvable question? inspect it
→ expert-decidable engineering choice? Agent/CTO decides it
→ human-owned product/domain/authorization question? ask only that
→ confirm observable outcome + success evidence
→ Working Contract execution gate
→ select one primary route
→ prove whether a real execution delta exists
→ default to one Agent
→ create a 1–5 member Task Pod only when specialization/isolation/review/parallelism justifies it
→ reuse current capabilities
→ add a provider only for a real capability/responsibility gap
→ execute
→ revalidate the target before consequential write/merge
→ verify
→ hand off when a materially different Task Pod takes over
→ reroute/replan if evidence changes the problem
```

Important consequences:

- “continue” does not mean “manufacture a diff” or restart discovery;
- autonomous mode does not mean “guess human-owned product intent”;
- collaborative mode does not mean “ask before every file edit”;
- finding a fix does not authorize mutation during a read-only review;
- a referenced repository does not automatically become a mutation target;
- a stale write/Working Contract/Journey precondition means re-read/reconcile, not force overwrite;
- a network/credential/product-decision blocker is not automatically a capability gap;
- a detected provider is not automatically needed;
- more Agents are not automatically better: a Task Pod is capped at five members and must have one accountable owner.

## 7. Upgrade

Run the current **stable bootstrap command** again.

The `stable` branch moves only after a release candidate passes the required release gates; ordinary `main` commits therefore do not silently change the production install path. A consumer pinned to an exact commit remains pinned until that exact revision is deliberately changed.

The bootstrap recognizes an existing AAOP installation and delegates to safe `--upgrade` behavior.

Upgrade preserves:

- `.aaop/runtime/`, including Working Contract and Journey continuity;
- project-owned files under `.aaop/`;
- project text outside AAOP markers in `AGENTS.md` / `CLAUDE.md`;
- local managed-file edits as backups before canonical replacement;
- third-party providers and project dependencies.

Install, upgrade, and uninstall are journaled lifecycle mutations. AAOP snapshots the package ownership surface and project bootstrap files before promotion, uses atomic per-file replacement, and rolls back caught failures. Malformed/duplicated AAOP marker pairs and unsupported ownership metadata fail before destructive mutation.

### If install / upgrade / uninstall was interrupted

A process or machine can stop without giving AAOP a chance to roll back. To avoid treating a mixed package as healthy, AAOP leaves the project-root journal:

```text
.aaop-install-transaction/
```

While that journal exists:

- health reports `interrupted-install`;
- normal install / upgrade / uninstall refuses to continue;
- do **not** manually delete the journal or blindly reinstall over the package.

Recover with the same trusted release source you intend to use.

Stable channel, macOS / Linux:

```bash
curl -fsSL https://raw.githubusercontent.com/YuemingHub/Adaptive-Agent-Orchestration-Protocol/stable/scripts/bootstrap.py | python3 - --target . --recover-interrupted
```

Stable channel, Windows PowerShell:

```powershell
curl.exe -fsSL https://raw.githubusercontent.com/YuemingHub/Adaptive-Agent-Orchestration-Protocol/stable/scripts/bootstrap.py | py - --target . --recover-interrupted
```

For an exact-revision consumer, use that matching/newer trusted exact revision for both the bootstrap URL and `--ref`.

Recovery first preserves the interrupted current files, then restores the pre-transaction package / manifest / `AGENTS.md` / `CLAUDE.md` state. After recovery, run:

```bash
python .aaop/tools/aaop.py status .
python .aaop/tools/aaop.py ready .
```

Only retry the original lifecycle operation after health/readiness reflects the restored current state.

## 8. Remove AAOP

Use the stable bootstrap surface with `--uninstall`.

### macOS / Linux

```bash
curl -fsSL https://raw.githubusercontent.com/YuemingHub/Adaptive-Agent-Orchestration-Protocol/stable/scripts/bootstrap.py | python3 - --target . --uninstall
```

### Windows PowerShell

```powershell
curl.exe -fsSL https://raw.githubusercontent.com/YuemingHub/Adaptive-Agent-Orchestration-Protocol/stable/scripts/bootstrap.py | py - --target . --uninstall
```

Safe removal:

- removes only files listed as AAOP-owned in the install manifest;
- removes only marked AAOP blocks from `AGENTS.md` / `CLAUDE.md`;
- preserves text outside those markers;
- preserves `.aaop/runtime/`;
- preserves project-owned files under `.aaop/`;
- backs up modified managed files before removal;
- leaves external role libraries, MCP servers, OpenHands, Agency Orchestrator, and other providers untouched;
- refuses automatic uninstall when ownership cannot be established safely;
- rejects future manifest schemas or unsafe managed paths instead of downgrade-managing unknown ownership metadata.

## 9. Health semantics

`aaop.py status` / `health.py` answer:

> Does this local AAOP package still match the baseline installed or upgraded here?

Typical states include:

```text
healthy
upgrade-recommended
legacy-install
drifted
incomplete
interrupted-install
invalid-manifest
unsupported-manifest
source-tree
```

`interrupted-install` takes precedence over ordinary package health. Recover the journaled lifecycle mutation before relying on the package or attempting another mutation.

Health is best-effort accidental-drift detection. It is **not** a cryptographic trust root, a guarantee that your package is the latest upstream version, or permission to overwrite local changes.

## 10. If a provider is genuinely needed

AAOP should first determine whether the gap is a **technical capability** or a **specialist responsibility**, then check what is already present.

Only a real capability/responsibility gap justifies provider selection.

Examples:

- `agency-agents-zh` may provide one or a few bounded specialist role procedures for a justified Task Pod;
- `agency-orchestrator` may provide delegated DAG/resume execution when a justified Pod needs it and the current host cannot do it adequately;
- neither provider owns the Working Contract, Journey, authorization boundary, acceptance gate, or handoff.

When an external provider is actually needed, AAOP should surface what capability/responsibility is missing, why existing options are insufficient, the minimum provider surface, permissions/credentials/cost/data exposure, verification, and rollback path.

The user should not have to answer “Which MCP/runtime/Agent team do you want?” as the first step.

## 11. Developing AAOP itself

Inside the AAOP source repository:

```bash
python scripts/validate.py
python scripts/validate_pressure.py
python scripts/validate_install_transaction.py
python scripts/validate_working_contract.py
python .aaop/tools/aaop.py ready .
```

Source-tree readiness is valid but is different from a manifest-tracked installation.

The end-to-end usability gate additionally exercises bootstrap archive safety, injected lifecycle failures + rollback/recovery, install → READY → repeat upgrade → safe refusal of unrelated `.aaop` → manifest-scoped removal. The Human-Agent gate separately exercises collaboration-mode persistence, alignment blocking, stale-write rejection, Task Pod limits, and handoff boundaries.

## Release channels

- `main`: development/edge.
- `stable`: deliberately promoted production channel.
- exact commit: immutable consumer pin when exact source identity is required.

A green `main` commit does not automatically promote `stable`.

## More detail

- `docs/HUMAN_AGENT_WORKING_CONTRACT.md`
- `docs/DEVELOPER_ENTRYPOINT.md`
- `docs/ROUTE_CAPABILITY_PACKS.md`
- `docs/REAL_PROJECT_PRESSURE_TESTS.md`
- `docs/PROGRESSIVE_ADOPTION.md`
- `docs/HOST_BOOTSTRAP_CONFORMANCE.md`
- `docs/INSTRUCTION_TOPOLOGY.md`
- `docs/ECOSYSTEM_MAP.md`
- `docs/PRODUCTION_RELEASE.md`
