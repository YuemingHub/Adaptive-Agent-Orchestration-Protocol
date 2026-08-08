# AAOP Version Identity

AAOP has one installable package release identity:

```text
.aaop/VERSION
```

That value is authoritative for:

- installer output;
- `.aaop/.install-manifest.json` `aaop_version`;
- installation-health package/manifest comparison;
- release/status statements for the installable AAOP package.

Do **not** infer the package release from another file.

## Component revisions are different

Individual AAOP components can change at different times. Their own revision markers, when present, describe that component only.

Examples:

- `ORCHESTRATOR.md` uses `Protocol-Revision:` for the normative orchestration document;
- normative policy documents use `Policy-Revision:` when they carry an explicit revision marker;
- Route Capability Pack `version` fields are route-pack revisions;
- Recipe `last_verified` is upstream integration-evidence freshness, not an AAOP release number;
- schema `$id` / schema content evolves independently unless explicitly tied to a package release.

Component revisions are **not** compatibility claims and are **not** fallback package versions.

Within `.aaop` Markdown component headers, a bare `Version:` label is intentionally forbidden because it is ambiguous with the package release identity. Use a component-specific label such as `Protocol-Revision:` or `Policy-Revision:` instead.

Git history is normally sufficient for Skills and other text components; do not add `aaop-version` metadata to a Skill merely to record when it last changed.

## Fail closed on missing release identity

A source package without a readable, non-empty `.aaop/VERSION` is incomplete.

The installer must stop before copying AAOP-managed package files. It must not guess a release number from `ORCHESTRATOR.md`, policies, Route Packs, Skills, README status text, tags, branch names, or Git history.

For installed packages, `health.py` compares the tracked manifest against the managed `VERSION` file and reports missing/drifted managed state rather than inventing a release identity.

## Release bump rule

Bump `.aaop/VERSION` when publishing a new AAOP package release.

Do not mechanically rewrite every Route, Skill, Recipe, policy, or protocol component to the package release number unless that component actually changed and its own revision convention requires a bump.
