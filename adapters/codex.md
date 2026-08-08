# Codex Adapter

Purpose: map AAOP concepts onto Codex without making Codex-specific behavior part of the core protocol.

Host behavior last verified: **2026-08-08**

Official sources:

- https://openai.com/index/unrolling-the-codex-agent-loop/
- https://openai.com/index/introducing-codex/

## Bootstrap

Codex natively aggregates repository instructions from `AGENTS.md` / `AGENTS.override.md` while walking from the project root toward the current working directory. More specific instruction files can therefore refine root guidance.

AAOP uses the root `AGENTS.md` marked block as the **common cross-host bootstrap**.

For a task:

1. honor the active Codex instruction scope and any more-specific project rules;
2. read `.aaop/ORCHESTRATOR.md` for non-trivial work;
3. start with `.aaop/skills/developer-intake/SKILL.md`;
4. after routing, load `.aaop/skills/route-execution/SKILL.md` and only the current route pack;
5. discover the actual tools/apps/skills exposed to the current Codex session before planning providers.

Do not turn root `AGENTS.md` into an encyclopedia. It should remain a compact table of contents into canonical AAOP/project sources.

## Skills

AAOP Skills follow the open Agent Skills format. Codex Skill installation/discovery can vary by product surface and workspace configuration, so this repository does not assume a single global installation path.

Two valid modes:

- **Direct protocol mode:** `AGENTS.md` explicitly references the canonical `.aaop/skills/.../SKILL.md` paths and the agent reads them when relevant.
- **Native Skill mode:** install/copy the canonical Skills into the Skill location supported by the current Codex surface. Keep `.aaop/skills/` canonical; do not fork their meaning silently.

If native Skill discovery and repository instructions disagree, follow the actual capabilities presented by the current host session rather than assuming a Skill is installed.

## Subagents / parallel work

Do not require a particular Codex multi-agent primitive. Apply AAOP host degradation:

- use available task/agent/worktree/background primitives when they provide isolation or safe parallelism;
- otherwise keep a single orchestrator and execute ownership contexts sequentially;
- preserve an independent review pass even if implemented by the same underlying model in a fresh review context.

## Tools and apps

Treat every connected Codex app/tool as a provider in the capability matrix. Discover current availability first. Do not tell the user to install MCP if Codex already exposes an equivalent first-party/native connector.

## Conformance boundary

AAOP depends only on Codex's documented project-instruction discovery surface, not on an AAOP-specific Codex plugin. If Codex changes instruction filenames/scoping, update this adapter and host-bootstrap conformance evidence; do not encode that change into the host-neutral Orchestrator unless it becomes portable across hosts.
