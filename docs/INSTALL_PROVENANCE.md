# AAOP Install Provenance

AAOP keeps three different questions separate:

1. **Ownership** — which package files may AAOP manage/remove?
2. **Health** — do current managed files and bootstrap blocks still match the installed ownership baseline?
3. **Provenance** — what bootstrap source label was recorded for these managed bytes, and do the bytes still match that record?

These are deliberately different authorities.

## Ownership authority

Only:

```text
.aaop/.install-manifest.json
```

may describe AAOP-managed package ownership.

Install/upgrade/uninstall validates that manifest before mutation. Provenance is never consulted to decide which project/package path AAOP may modify or delete.

## Provenance storage

Bootstrap install/upgrade records:

```text
.aaop/runtime/install-provenance.json
```

The record contains:

- AAOP package version;
- source kind (`official-ref` or `local-archive`);
- source ref for official GitHub archive installs;
- ownership-manifest schema version;
- managed-file count;
- deterministic SHA-256 fingerprint of the **actual installed managed-file bytes**;
- a diagnostic-only authority statement.

Local archive filesystem paths are intentionally not persisted.

The runtime location is intentional: provenance survives a normal package upgrade/removal as historical diagnostic evidence but is outside the set of package files AAOP claims as canonical source.

## User commands

```bash
python .aaop/tools/aaop.py provenance
python .aaop/tools/aaop.py provenance --json
```

`aaop.py ready` also includes:

- `provenance_state`;
- `provenance_source`;
- `package_fingerprint`.

## States

### `verified`

The recorded package fingerprint equals the fingerprint recomputed from the current managed AAOP files.

This means the currently observed managed bytes match the recorded bootstrap event. It does **not** prove that the source repository/ref itself was trustworthy.

### `missing`

No bootstrap provenance record exists.

This is valid for direct/legacy installer usage. AAOP must not invent an upstream source from the package version, directory name, Git history, or current `stable` pointer.

### `mismatch`

Current managed bytes no longer match the recorded fingerprint.

Review installation health/drift before relying on the source label.

### `invalid`

The provenance JSON/schema is malformed or unsupported.

Treat the source identity as unknown. Do not copy paths/claims from the damaged record into the ownership manifest.

### `unverifiable`

The ownership/managed-file surface cannot currently be fingerprinted, for example because a managed file is missing.

Health/recovery takes priority.

## Stable vs exact refs

A record such as:

```text
source.kind = official-ref
source.ref = stable
```

means the install was performed from the `stable` ref **at that time**. `stable` is intentionally movable, so the durable byte identity is the package fingerprint, not the word `stable`.

For immutable source-ref identity, install with the same exact commit SHA in both the bootstrap URL and `--ref`; provenance then records that exact ref plus the resulting package fingerprint.

## Recovery semantics

`--recover-interrupted` restores a previous lifecycle generation. The bootstrap used to execute recovery is therefore **not** recorded as a new package source.

The recovered package retains its prior runtime provenance. After recovery, run health/readiness/provenance again and reconcile current state before another lifecycle mutation.

## Uninstall semantics

Uninstall reads ownership only from `.install-manifest.json`. It ignores provenance fields entirely.

Runtime provenance may remain after AAOP package removal as historical evidence. It grants no authority to later tools.

## Security boundary

Install provenance is not:

- a signature;
- an attestation service;
- a cryptographic trust root;
- permission to mutate files;
- proof that a movable Git ref still points at the same commit;
- proof that a downloaded upstream source was benign.

Its purpose is narrower: prevent silent source ambiguity and make consumer drift/debugging explainable without merging source labels into file-ownership authority.
