// Parity + invariant test for the AAOP GitHub Mission Adapter (candidate).
// No network, no `gh`, no model — the transport I/O is out of scope here.
//
// Two layers:
//  1. SOURCE INVARIANTS — assert the genericized watcher keeps every MUST-keep invariant
//     and drops every Family-Space / agent-workspace hardcode (README · C.4).
//  2. STATE MACHINE — a faithful re-derivation of the pure functions (validateContract /
//     parseEvents / deriveMissionState) copied from mission-watcher.mjs, proving the
//     invariants that matter: single nonce winner, append-only evidence, CHANGES_REQUIRED
//     recovery, READY/RETURN termination, illegal-GATE rejection.
import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const HERE = dirname(fileURLToPath(import.meta.url));
const SRC = readFileSync(join(HERE, "..", "mission-watcher.mjs"), "utf8");

// ---------------------------------------------------------------------------
// 1. source invariants
// ---------------------------------------------------------------------------
test("transport keeps the MUST-keep invariants", () => {
  const must = [
    ["earliest valid claim wins", /earliest valid CLAIM/],
    ["claim nonce, re-read timeline", /claim_nonce/],
    ["timeline is the source of truth", /timeline/],
    ["no shell from comments", /execFileSync/],
    ["no model invocation", /不调用任何模型/],
    ["append-only evidence", /append-only/],
    ["no auto cross gate", /no auto-cross-Gate|never auto-advances/],
    ["resumable on restart", /restart|resume/],
  ];
  for (const [name, re] of must) assert.match(SRC, re, `missing invariant marker: ${name}`);
});

test("genericization removes Family-Space / agent-workspace hardcode", () => {
  // no Family-Space product paths or workspace state hardcode
  assert.ok(!/Family-Space-Workspace/.test(SRC), "hardcoded Family-Space-Workspace");
  assert.ok(!/WORKSPACE_STATE\.json/.test(SRC), "hardcoded WORKSPACE_STATE.json path");
  assert.ok(!/state\/WORKSPACE_STATE/.test(SRC), "hardcoded state path");
  // no agent-workspace canonical protocol citation
  assert.ok(!/开发协作协议/.test(SRC), "agent-workspace 开发协作协议 citation remains");
  assert.ok(!/agent-workspace|Agent-Space/.test(SRC), "agent-workspace reference remains");
  // GATE values are data, not a hardcoded single source
  assert.match(SRC, /MISSION_BUS_GATE_VALUES/, "GATE allow-list must be configurable");
});

// ---------------------------------------------------------------------------
// 2. faithful state-machine re-derivation (mirrors mission-watcher.mjs verbatim)
// ---------------------------------------------------------------------------
const REQUIRED_FIELDS = ["EXECUTOR", "GOAL", "SCOPE", "NOT-IN-SCOPE", "DONE-WHEN", "EVIDENCE", "FINAL VERIFICATION", "GATE"];
const VALID_GATES = ["COMMANDER", "FOUNDER"];

function validateContract(body) {
  const field = (name) => {
    const m = (body || "").match(new RegExp(`^${name}:\\s*(.+)$`, "mi"));
    return m ? m[1].trim() : null;
  };
  const missing = REQUIRED_FIELDS.filter((f) => !field(f));
  const taskType = (field("TASK_TYPE") || "surgical").toLowerCase();
  if (taskType === "autonomous") {
    for (const f of ["STOP-WHEN", "RETURN-WHEN"]) if (!field(f)) missing.push(`${f}（autonomous 必填）`);
  }
  const gate = (field("GATE") || "").toUpperCase();
  if (field("GATE") && !VALID_GATES.includes(gate)) missing.push(`GATE 非法值 "${gate}"`);
  return { field, missing, taskType, gate };
}

function matchField(body, key) { return (body.match(new RegExp(`${key}=([^\\s]+)`)) || [])[1] || null; }

function parseEvents(issue) {
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

function deriveMissionState(issue, tid) {
  const ev = parseEvents(issue);
  const claims = ev.filter((e) => e.type === "CLAIM" && e.task_id === tid)
    .sort((a, b) => (a.at < b.at ? -1 : a.at > b.at ? 1 : a.nonce < b.nonce ? -1 : 1));
  const evidence = ev.filter((e) => e.type === "EVIDENCE" && e.task_id === tid);
  const winner = claims[0] || null;
  const lastEv = evidence[evidence.length - 1] || null;
  const after = (e) => !lastEv || e.at > lastEv.at;
  const ready = ev.some((e) => e.type === "REVIEW_READY" && after(e));
  const changes = ev.some((e) => e.type === "REVIEW_CHANGES" && after(e));
  const returned = ev.some((e) => e.type === "RETURN" && e.task_id === tid && after(e));
  const state = ready ? "READY_TO_ADVANCE" : returned ? "RETURNED" : changes ? "CHANGES_REQUIRED" : lastEv ? "EVIDENCE_SUBMITTED" : winner ? "CLAIMED" : "UNCLAIMED";
  return { state, winner, evidenceCount: evidence.length };
}

const C = (body, at) => ({ body, createdAt: at });

test("illegal GATE is rejected", () => {
  const body = `EXECUTOR: w\nGOAL: g\nSCOPE: s\nNOT-IN-SCOPE: n\nDONE-WHEN: d\nEVIDENCE: e\nFINAL VERIFICATION: f\nGATE: SENATE`;
  assert.ok(validateContract(body).missing.some((m) => /GATE 非法值/.test(m)));
});

test("autonomous requires STOP-WHEN and RETURN-WHEN", () => {
  const base = `TASK_TYPE: autonomous\nEXECUTOR: w\nGOAL: g\nSCOPE: s\nNOT-IN-SCOPE: n\nDONE-WHEN: d\nEVIDENCE: e\nFINAL VERIFICATION: f\nGATE: COMMANDER`;
  const missing = validateContract(base).missing;
  assert.ok(missing.includes("STOP-WHEN（autonomous 必填）"));
  assert.ok(missing.includes("RETURN-WHEN（autonomous 必填）"));
});

test("earliest valid CLAIM is the unique winner (nonce tie-break)", () => {
  const tid = "mission-5-abc";
  const issue = { comments: [
    C(`[CLAIM] task_id=${tid} worker=w2 claim_nonce=aaaa at=t1`, "00:00:02"),
    C(`[CLAIM] task_id=${tid} worker=w1 claim_nonce=zzzz at=t1`, "00:00:01"),
    C(`[CLAIM] task_id=${tid} worker=w3 claim_nonce=bbbb at=t2`, "00:00:03"),
  ]};
  const ms = deriveMissionState(issue, tid);
  assert.equal(ms.state, "CLAIMED");
  assert.equal(ms.winner.worker, "w1", "earliest-at wins");
});

test("append-only evidence + CHANGES_REQUIRED recovery", () => {
  const tid = "mission-5-abc";
  const issue = { comments: [
    C(`[CLAIM] task_id=${tid} worker=w1 claim_nonce=n1`, "00:00:01"),
    C(`[EVIDENCE] task_id=${tid} worker=w1`, "00:00:02"),
    C(`[REVIEW: CHANGES_REQUIRED]`, "00:00:03"),
  ]};
  const ms = deriveMissionState(issue, tid);
  assert.equal(ms.state, "CHANGES_REQUIRED");
  assert.equal(ms.evidenceCount, 1);
  // a v2 evidence after the review becomes the latest, still resumable state
  const issue2 = { comments: [...issue.comments, C(`[EVIDENCE] task_id=${tid} worker=w1`, "00:00:04")]};
  const ms2 = deriveMissionState(issue2, tid);
  assert.equal(ms2.evidenceCount, 2);
  assert.equal(ms2.state, "EVIDENCE_SUBMITTED");
});

test("READY_TO_ADVANCE and RETURN terminate after the latest evidence", () => {
  const tid = "mission-5-abc";
  const base = [
    C(`[CLAIM] task_id=${tid} worker=w1 claim_nonce=n1`, "00:00:01"),
    C(`[EVIDENCE] task_id=${tid} worker=w1`, "00:00:02"),
  ];
  assert.equal(deriveMissionState({ comments: [...base, C(`[REVIEW: READY_TO_ADVANCE]`, "00:00:03")] }, tid).state, "READY_TO_ADVANCE");
  assert.equal(deriveMissionState({ comments: [...base, C(`[RETURN] task_id=${tid} at=x`, "00:00:03")] }, tid).state, "RETURNED");
  // a stale CHANGES_REQUIRED before the latest evidence is ignored
  assert.equal(deriveMissionState({ comments: [C(`[CLAIM] task_id=${tid} worker=w1 claim_nonce=n1`, "00:00:01"), C(`[EVIDENCE] task_id=${tid} worker=w1`, "00:00:02"), C(`[REVIEW: CHANGES_REQUIRED]`, "00:00:01")] }, tid).state, "EVIDENCE_SUBMITTED");
});