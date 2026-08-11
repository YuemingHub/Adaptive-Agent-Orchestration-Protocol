#!/usr/bin/env python3
"""Validate the source-repository contract for promoting real consumer pressure into AAOP."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "docs" / "REAL_PROJECT_PRESSURE_PROMOTION.md"
PRESSURE_ROOT = ROOT / "tests" / "pressure"
BANNED_CORE_TOKENS = ("Family Space", "aaop-family", "chat-first")
CLASSIFICATIONS = (
    "consumer-only",
    "existing-AAOP-coverage",
    "candidate-generic-gap",
    "promoted-invariant",
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    require(POLICY.is_file(), "missing real-project pressure promotion contract")
    text = POLICY.read_text(encoding="utf-8")
    lower = text.lower()

    for classification in CLASSIFICATIONS:
        require(classification.lower() in lower, f"promotion contract missing classification: {classification}")

    for phrase in (
        "pressure source",
        "no existing mechanism already closes it",
        "smallest reusable invariant",
        "consumer authority stays local",
        "regression exists",
        "compatibility is proven",
        "many consumer findings should **not** change aaop",
        "duplicate policy",
        "exact candidate",
    ):
        require(phrase.lower() in lower, f"promotion contract missing invariant: {phrase}")

    pressure_cases = sorted(PRESSURE_ROOT.glob("*.json"))
    require(pressure_cases, "pressure promotion requires at least one pressure case")
    anonymized_count = 0
    for path in pressure_cases:
        payload = json.loads(path.read_text(encoding="utf-8"))
        require(isinstance(payload, dict), f"{path}: expected JSON object")
        provenance = payload.get("provenance")
        require(isinstance(provenance, dict), f"{path}: missing provenance")
        if provenance.get("privacy") == "anonymized":
            anonymized_count += 1
            require(not provenance.get("repository"), f"{path}: anonymized pressure leaked repository")
            require(not provenance.get("reference"), f"{path}: anonymized pressure leaked reference")
        require(isinstance(payload.get("lessons"), list) and payload["lessons"], f"{path}: pressure case needs reusable lessons")
        require(isinstance(payload.get("must_not"), list) and payload["must_not"], f"{path}: pressure case needs anti-overfit boundaries")

    require(anonymized_count >= 1, "pressure suite should prove private real-project findings can be retained anonymously")

    # The source evolution contract may discuss consumers generically, but must not encode
    # the current private consumer's product-specific adapter/test vocabulary.
    for token in BANNED_CORE_TOKENS:
        require(token.lower() not in lower, f"promotion contract leaked consumer-specific token: {token}")

    print(
        "PASS pressure promotion: real consumer findings are classified before Core changes; "
        "existing mechanisms are reused, consumer authority stays local, and promoted invariants "
        "require safe pressure evidence plus exact-candidate compatibility proof"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
