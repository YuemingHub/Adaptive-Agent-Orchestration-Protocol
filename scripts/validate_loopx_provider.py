#!/usr/bin/env python3
"""Static and local-smoke regression guard for the optional AAOP <-> LoopX provider seam."""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROVIDERS = ROOT / ".aaop" / "registries" / "providers.json"
PROFILES = ROOT / ".aaop" / "registries" / "adoption-profiles.json"
RECIPE = ROOT / ".aaop" / "recipes" / "loopx.json"
PROVIDER_SELECTION = ROOT / ".aaop" / "skills" / "provider-selection" / "SKILL.md"
CAPABILITY_PLANNING = ROOT / ".aaop" / "skills" / "capability-planning" / "SKILL.md"
END_TO_END = ROOT / ".aaop" / "skills" / "end-to-end-delivery" / "SKILL.md"
INTEGRATION_DOC = ROOT / "docs" / "LOOPX_INTEGRATION.md"
PROGRESSIVE_DOC = ROOT / "docs" / "PROGRESSIVE_ADOPTION.md"
DOCTOR = ROOT / ".aaop" / "tools" / "doctor.py"
RECIPE_TOOL = ROOT / ".aaop" / "tools" / "recipe.py"
UPSTREAM_QUALIFIER = ROOT / "scripts" / "qualify_loopx_upstream.py"
FULL_SHA_RE = re.compile(r"^[0-9a-f]{40}$")
SEMVER_TAG_RE = re.compile(r"^v\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?$")
EXPECTED_UPSTREAM_SMOKES = (
    "examples/control_plane/quota-contract-smoke.py",
    "examples/control_plane/todo-cli-smoke.py",
    "examples/control_plane/todo-durability-fixture-smoke.py",
    "examples/blocker-push-runtime-smoke.py",
    "examples/project/project-uninstall-smoke.py",
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load(path: Path) -> dict[str, object]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(payload, dict), f"{path}: expected JSON object")
    return payload


def row_by_id(rows: object, item_id: str) -> dict[str, object]:
    require(isinstance(rows, list), f"expected list while resolving {item_id}")
    for row in rows:
        if isinstance(row, dict) and row.get("id") == item_id:
            return row
    raise AssertionError(f"missing row {item_id!r}")


def contains_text(value: object, needle: str) -> bool:
    if isinstance(value, str):
        return needle.lower() in value.lower()
    if isinstance(value, list):
        return any(contains_text(item, needle) for item in value)
    if isinstance(value, dict):
        return any(contains_text(item, needle) for item in value.values())
    return False


def run_json(args: list[str], *, env: dict[str, str] | None = None) -> dict[str, object]:
    completed = subprocess.run(
        args,
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )
    require(
        completed.returncode == 0,
        f"command failed ({completed.returncode}): {' '.join(args)}\nstdout:\n{completed.stdout}\nstderr:\n{completed.stderr}",
    )
    payload = json.loads(completed.stdout)
    require(isinstance(payload, dict), f"command must return JSON object: {' '.join(args)}")
    return payload


def validate_runtime_detection() -> None:
    require(DOCTOR.is_file(), "missing doctor.py for LoopX provider detection smoke")
    require(RECIPE_TOOL.is_file(), "missing recipe.py for LoopX recipe smoke")

    shown = run_json([sys.executable, str(RECIPE_TOOL), "show", "loopx"])
    require(shown.get("provider_id") == "loopx", "recipe CLI must expose LoopX recipe")
    install = shown.get("install")
    require(isinstance(install, dict) and install.get("mode") == "manual-choice", "recipe CLI must preserve explicit LoopX adoption")

    with tempfile.TemporaryDirectory(prefix="aaop-loopx-detect-") as tmp:
        root = Path(tmp)
        project = root / "project"
        fakebin = root / "fakebin"
        project.mkdir()
        fakebin.mkdir()
        executable = fakebin / "loopx"
        executable.write_text("#!/usr/bin/env sh\nexit 0\n", encoding="utf-8")
        executable.chmod(0o755)

        env = os.environ.copy()
        env["PATH"] = str(fakebin) + os.pathsep + env.get("PATH", "")
        doctor = run_json([sys.executable, str(DOCTOR), str(project), "--json"], env=env)
        detection = doctor.get("provider_detection")
        require(isinstance(detection, dict), "doctor must expose provider_detection")
        detected_loopx = detection.get("loopx")
        require(isinstance(detected_loopx, dict), "doctor must expose LoopX provider detection row")
        require(detected_loopx.get("detected") is True, "provider detection must recognize a LoopX executable on PATH")
        evidence = detected_loopx.get("evidence")
        require(isinstance(evidence, dict), "LoopX detection must expose structured evidence")
        commands = evidence.get("commands")
        require(isinstance(commands, dict) and "loopx" in commands, "LoopX detection must report executable command evidence")
        require(doctor.get("observed_surface_level", 0) >= 4, "detected LoopX must project its Level 4 observed surface")

        # Presence is evidence of availability only. Selection remains a policy decision.
        require(
            "recommended" not in json.dumps(detected_loopx, ensure_ascii=False).lower(),
            "doctor detection must not silently turn LoopX presence into an adoption recommendation",
        )
        require(
            "Presence is not a recommendation" in str(doctor.get("policy", "")),
            "doctor must preserve presence-versus-selection policy when LoopX is detected",
        )


def validate_upstream_qualifier_contract() -> None:
    require(UPSTREAM_QUALIFIER.is_file(), "missing exact-revision LoopX upstream qualification harness")
    completed = subprocess.run(
        [sys.executable, str(UPSTREAM_QUALIFIER), "--help"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    require(completed.returncode == 0, f"LoopX upstream qualifier --help failed: {completed.stderr}")
    require("--checkout" in completed.stdout, "LoopX upstream qualifier must require an explicit checkout")
    require("--no-execute" in completed.stdout, "LoopX upstream qualifier must support plan-only identity checks")
    require("--include-install-smoke" in completed.stdout, "LoopX install smoke must remain explicit/optional")

    text = UPSTREAM_QUALIFIER.read_text(encoding="utf-8")
    for smoke in EXPECTED_UPSTREAM_SMOKES:
        require(smoke in text, f"LoopX upstream qualifier missing reviewed upstream smoke {smoke}")
    require("fresh-clone-quickstart-smoke.py" in text, "LoopX qualifier must expose optional upstream install/quickstart smoke")
    require("reviewed_commit" in text, "LoopX qualifier must bind execution to Recipe-reviewed immutable revision")
    require("checkout_clean" in text, "LoopX qualifier must reject/identify dirty source before qualification")
    require(
        "does not prove AAOP selected LoopX correctly" in text,
        "LoopX upstream qualification must not impersonate real AAOP consumer-pilot evidence",
    )


def main() -> int:
    for path in (
        PROVIDERS,
        PROFILES,
        RECIPE,
        PROVIDER_SELECTION,
        CAPABILITY_PLANNING,
        END_TO_END,
        INTEGRATION_DOC,
        PROGRESSIVE_DOC,
        UPSTREAM_QUALIFIER,
    ):
        require(path.is_file(), f"missing LoopX integration surface: {path.relative_to(ROOT)}")

    providers = load(PROVIDERS)
    loopx = row_by_id(providers.get("providers"), "loopx")
    require(loopx.get("kind") == "long-running-execution-control-plane", "LoopX provider kind drifted")
    require(loopx.get("adoption_level") == 4, "LoopX must remain Level 4 optional escalation")
    require(contains_text(loopx.get("avoid_when"), "host-native"), "LoopX registry must preserve host-native-first avoidance")
    require(contains_text(loopx, "Working Contract"), "LoopX registry must preserve AAOP Working Contract authority")
    require(contains_text(loopx, "Journey"), "LoopX registry must preserve AAOP Journey authority")

    profiles = load(PROFILES)
    profile_rows = profiles.get("profiles")
    protocol_only = row_by_id(profile_rows, "protocol-only")
    require(protocol_only.get("default") is True, "protocol-only must remain the default adoption profile")
    require("loopx" not in protocol_only.get("requires", []), "LoopX must never become a protocol-only default requirement")
    specialized = row_by_id(profile_rows, "specialized-runtime")
    choices = specialized.get("choose_one_or_few")
    require(isinstance(choices, list) and "loopx" in choices, "LoopX must be discoverable in Level 4 provider choices")
    require("deepagents" in choices, "Level 4 must retain adjacent runtime alternative Deep Agents")
    require("agency-orchestrator" in choices, "Level 4 must retain delegated Task Pod runtime alternative")

    # No adoption profile may silently require LoopX. It stays evidence-selected and optional.
    require(isinstance(profile_rows, list), "adoption profiles must be a list")
    for profile in profile_rows:
        if not isinstance(profile, dict):
            continue
        require("loopx" not in profile.get("requires", []), f"profile {profile.get('id')} must not require LoopX")

    recipe = load(RECIPE)
    require(recipe.get("provider_id") == "loopx", "LoopX recipe provider id mismatch")

    reviewed = recipe.get("reviewed_upstream")
    require(isinstance(reviewed, dict), "LoopX recipe must retain a reviewed upstream identity snapshot")
    stable_tag = reviewed.get("stable_tag")
    stable_commit = reviewed.get("stable_commit")
    stable_package_version = reviewed.get("stable_package_version")
    require(isinstance(stable_tag, str) and SEMVER_TAG_RE.fullmatch(stable_tag), "LoopX reviewed stable tag must be explicit SemVer tag")
    require(isinstance(stable_commit, str) and FULL_SHA_RE.fullmatch(stable_commit), "LoopX reviewed stable commit must be a full immutable SHA")
    require(isinstance(stable_package_version, str) and stable_tag == f"v{stable_package_version}", "LoopX reviewed tag/package version must agree")
    require(contains_text(reviewed, "Re-check"), "LoopX reviewed upstream identity must remain time-scoped evidence")

    install = recipe.get("install")
    require(isinstance(install, dict) and install.get("mode") == "manual-choice", "LoopX adoption must remain explicit/manual-choice")
    review = recipe.get("adoption_review")
    require(isinstance(review, dict), "LoopX recipe must retain scoped adoption review")
    require(review.get("decision_effect") == "conditional-adoption-only", "LoopX adoption review must remain conditional")
    require(contains_text(recipe, stable_tag), "LoopX recipe must retain reviewed stable tag evidence")
    require(contains_text(recipe, stable_commit), "LoopX recipe must retain exact reviewed stable revision evidence")
    require(contains_text(recipe, "experimental") and contains_text(recipe, "Turn"), "LoopX Turn must remain separately qualified/experimental")
    require(contains_text(recipe, "Windows") or contains_text(recipe, "WSL"), "LoopX recipe must preserve Windows/WSL qualification boundary")
    require(contains_text(recipe, "feedback template") and contains_text(recipe, "not") and contains_text(recipe, "support"), "LoopX recipe must not mistake Windows/WSL feedback options for support evidence")
    require(contains_text(recipe, "quiet"), "LoopX recipe must preserve no-progress quiet/wait behavior")
    require(contains_text(recipe, "rollback"), "LoopX recipe must define rollback semantics")
    require(contains_text(recipe, "production") and contains_text(recipe, "authorization"), "LoopX must not bypass AAOP production/authorization gates")

    provider_selection = PROVIDER_SELECTION.read_text(encoding="utf-8")
    capability_planning = CAPABILITY_PLANNING.read_text(encoding="utf-8")
    end_to_end = END_TO_END.read_text(encoding="utf-8")
    integration_doc = INTEGRATION_DOC.read_text(encoding="utf-8")
    progressive_doc = PROGRESSIVE_DOC.read_text(encoding="utf-8")

    require("execution-continuity" in capability_planning, "capability planning must model execution-continuity explicitly")
    require("LoopX" in provider_selection, "provider selection must route execution-continuity toward LoopX-style providers")
    require("Deep Agents" in provider_selection, "provider selection must distinguish long-horizon agent runtime gaps")
    require("agency-orchestrator" in provider_selection, "provider selection must distinguish bounded Task Pod runtime gaps")
    require("Do not collapse these three gaps" in provider_selection, "provider-selection anti-collapse rule is missing")
    require("Execution-continuity escalation" in end_to_end, "end-to-end Journey must have an execution-continuity escalation seam")
    require("execution-continuity failure" in end_to_end, "Journey must distinguish execution-continuity failure from implementation/environment/human gates")
    require("provider-selection/SKILL.md" in end_to_end, "Journey must route proven continuity gaps through provider selection")
    require("recipes/loopx.json" in end_to_end, "Journey must load the LoopX recipe only after selection")
    require("Do not create a parallel `.aaop` Execution Ledger" in end_to_end, "Journey must forbid duplicate LoopX execution state")
    require("Provider stacking without distinct proven gaps" in end_to_end, "Journey must prevent provider-stacking anti-thrash")
    require("Authority map" in integration_doc, "LoopX integration must preserve an explicit authority map")
    require("State duplication rule" in integration_doc, "LoopX integration must forbid duplicate AAOP execution state")
    require("First pilot acceptance" in integration_doc, "LoopX integration must retain real-pilot acceptance criteria")
    require("LoopX-style provider" in progressive_doc, "progressive adoption must place LoopX by primary mechanism")
    require("Deep Agents-style provider" in progressive_doc, "progressive adoption must preserve runtime alternative")
    require("agency-orchestrator-style" in progressive_doc, "progressive adoption must preserve delegated Pod alternative")

    validate_runtime_detection()
    validate_upstream_qualifier_contract()

    print(
        "PASS LoopX provider seam: optional Level 4 escalation, immutable reviewed upstream identity, "
        "runtime detection without auto-adoption, reusable upstream-owned qualification harness, "
        "Journey escalation only for proven execution-continuity gaps, AAOP authority, adjacent-provider "
        "separation, anti-stacking, and rollback gates"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
