// Pure, side-effect-free core of the AAOP GitHub Mission Adapter.
// This is the importable contract/state logic. transport (gh/git I/O) lives in
// mission-watcher.mjs; nothing here touches the network, argv, or the filesystem.
//
// The field list below is machine-read from .aaop/schemas/github-mission-task-contract.schema.json
// (AAOP-owned canonical); a parity test asserts the two cannot drift.

export const REQUIRED_FIELDS = [
  "EXECUTOR", "GOAL", "SCOPE", "NOT-IN-SCOPE",
  "DONE-WHEN", "EVIDENCE", "FINAL VERIFICATION", "GATE",
];

export const AUTONOMOUS_EXTRA = ["STOP-WHEN", "RETURN-WHEN"];

export const DEFAULT_GATES = ["COMMANDER", "FOUNDER"];

export function gatesFromEnv(raw) {
  const list = (raw || "").split(",").map((s) => s.trim().toUpperCase()).filter(Boolean);
  return list.length ? list : DEFAULT_GATES;
}

export function taskIdFor(issueNumber, body) {
  return `mission-${issueNumber}-${createHash("sha1").update(body || "").digest("hex").slice(0, 12)}`;
}

import { createHash } from "node:crypto";

// TASK CONTRACT structure validation (never interprets the contract, only its shape).
export function validateContract(body, validGates = DEFAULT_GATES) {
  const field = (name) => {
    const m = (body || "").match(new RegExp(`^${name}:\\s*(.+)$`, "mi"));
    return m ? m[1].trim() : null;
  };
  const missing = REQUIRED_FIELDS.filter((f) => !field(f));
  const taskType = (field("TASK_TYPE") || "surgical").toLowerCase();
  if (taskType === "autonomous") {
    for (const f of AUTONOMOUS_EXTRA) if (!field(f)) missing.push(`${f}（autonomous 必填）`);
  }
  const gate = (field("GATE") || "").toUpperCase();
  if (field("GATE") && !validGates.includes(gate)) {
    missing.push(`GATE 非法值 "${gate}"（仅允许 ${validGates.join("/")}）`);
  }
  return { field, missing, taskType, gate };
}

export function matchField(body, key) {
  return (body.match(new RegExp(`${key}=([^\\s]+)`)) || [])[1] || null;
}

// timeline comments → ordered events (the single source of truth).
export function parseEvents(issue) {
  const events = [];
  for (const c of issue.comments || []) {
    const body = c.body || "";
    const at = c.createdAt;
    if (/^\s*\[CLAIM\]/.test(body)) {
      events.push({ type: "CLAIM", at, task_id: matchField(body, "task_id"), worker: matchField(body, "worker"), nonce: matchField(body, "claim_nonce") || "" });
    } else if (/^\s*\[EVIDENCE\]/.test(body)) {
      events.push({ type: "EVIDENCE", at, task_id: matchField(body, "task_id"), worker: matchField(body, "worker") });
    } else if (/^\s*\[RETURN\]/.test(body)) {
      events.push({ type: "RETURN", at, task_id: matchField(body, "task_id") });
    } else if (body.includes("[REVIEW: CHANGES_REQUIRED]")) {
      events.push({ type: "REVIEW_CHANGES", at });
    } else if (body.includes("[REVIEW: READY_TO_ADVANCE]")) {
      events.push({ type: "REVIEW_READY", at });
    }
  }
  return events.sort((a, b) => (a.at < b.at ? -1 : a.at > b.at ? 1 : 0));
}

export function deriveMissionState(issue, tid) {
  const ev = parseEvents(issue);
  const claims = ev.filter((e) => e.type === "CLAIM" && e.task_id === tid)
    .sort((a, b) => (a.at < b.at ? -1 : a.at > b.at ? 1 : a.nonce < b.nonce ? -1 : 1));
  const evidence = ev.filter((e) => e.type === "EVIDENCE" && e.task_id === tid);
  const winner = claims[0] || null; // earliest valid CLAIM = unique winner
  const lastEv = evidence[evidence.length - 1] || null;
  const afterLastEvidence = (e) => !lastEv || e.at > lastEv.at;
  const ready = ev.some((e) => e.type === "REVIEW_READY" && afterLastEvidence(e));
  const changes = ev.some((e) => e.type === "REVIEW_CHANGES" && afterLastEvidence(e));
  const returned = ev.some((e) => e.type === "RETURN" && e.task_id === tid && afterLastEvidence(e));
  const state = ready ? "READY_TO_ADVANCE"
    : returned ? "RETURNED"
    : changes ? "CHANGES_REQUIRED"
    : lastEv ? "EVIDENCE_SUBMITTED"
    : winner ? "CLAIMED"
    : "UNCLAIMED";
  return { state, winner, evidenceCount: evidence.length };
}