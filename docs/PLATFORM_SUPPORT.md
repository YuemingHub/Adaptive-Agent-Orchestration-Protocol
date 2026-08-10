# AAOP Production Platform Support

This document defines the runtime environments AAOP treats as **production-supported**, not merely environments where some source may happen to execute.

## Supported runtime

AAOP v0.25.0 production support:

| Surface | Supported |
| --- | --- |
| Python implementation | CPython |
| Python versions | 3.11, 3.12, 3.13, 3.14 |
| Linux | supported |
| Windows | supported |
| macOS | supported |
| Third-party Python dependencies | none required by AAOP core/bootstrap |

The user-facing bootstrap refuses Python versions outside 3.11–3.14 **before archive download and before project mutation**.

## Why Python 3.10 is not in the production contract

Python 3.10 is still in upstream security support at the time this contract was introduced, but its scheduled end of life is October 2026. AAOP is establishing a durable production baseline now rather than promising a runtime that is about to leave upstream support.

Authoritative upstream lifecycle reference:

- Python Developer's Guide — Status of Python versions: <https://devguide.python.org/versions/>

This is a support-policy decision, not a claim that every AAOP source file necessarily fails to parse or execute on Python 3.10.

## What the CI proves

`validate-platform-support` exercises both ends of the supported minor-version range on all three operating-system families:

```text
Ubuntu   × CPython 3.11
Ubuntu   × CPython 3.14
Windows  × CPython 3.11
Windows  × CPython 3.14
macOS    × CPython 3.11
macOS    × CPython 3.14
```

Each supported cell executes:

1. AAOP source/schema/pressure validation;
2. transactional install/upgrade/uninstall fault regressions;
3. Journey schema/recovery regressions;
4. real bootstrap install;
5. `AAOP READY` / health validation;
6. repeat bootstrap upgrade;
7. bootstrap uninstall.

Existing AAOP workflows also exercise Python 3.12 on Linux and Windows, including Windows Journey locking/CAS.

A separate Python 3.10 CI job proves the bootstrap refuses the unsupported runtime before it can read the requested archive or create `.aaop` / `.aaop-install-transaction` in the target project.

## What this does not promise

Production support does not mean:

- every Python distribution, embedded runtime, or alternative interpreter is covered;
- every future Python minor is automatically supported;
- every filesystem/network environment is equivalent;
- AAOP can compensate for OS/account permissions it does not have;
- a successful AAOP runtime test proves a downstream application's own dependencies support the same Python/OS matrix.

A consumer project may have a narrower runtime contract. AAOP must preserve that project-specific contract instead of upgrading or changing its application runtime merely because AAOP itself supports a wider range.

## Adding a new Python or OS target

Do not expand this table from assumption. A new target becomes production-supported only after:

1. the bootstrap can identify it safely;
2. the lifecycle/Journey regression set executes on that target;
3. failures are either fixed or explicitly classified as unsupported behavior;
4. the platform-support workflow is updated so future regressions stay visible;
5. the stable release containing the expanded support is promoted only after the full release gate passes.
