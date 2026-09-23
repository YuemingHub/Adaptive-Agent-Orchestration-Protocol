// Parity test for the AAOP GitHub Mission Adapter.
//
// Two layers, both against REAL code (no test-side re-implementation of the logic):
//   1. UNIT — imports `../mission-core.mjs` (the actual pure core the adapter ships).
//   2. SUBPROCESS PARITY — runs the actual AAOP adapter AND the actual Family-Space-Workspace
//      reference watcher (source read from FSW_REFERENCE) against the SAME contract and SAME
//      timeline fixtures, served by a fake `gh`. Asserts both derive the same task_id and the
//      same decision state per fixture.
//
// No network, no model, no real gh. The FSW watcher is executed from a byte-for-byte copy of
// its source relocated into an FSW-shaped temp layout (the real FSW repo is never written).
import test from "node:test";
import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { mkdtempSync, mkdirSync, writeFileSync, readFileSync, chmodSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

import {
  taskIdFor, validateContract, parseEvents, deriveMissionState,
} from "../mission-core.mjs";

const HERE = dirname(fileURLToPath(import.meta.url));
const ADAPTER = join(HERE, "..", "mission-watcher.mjs");
const FSW_REFERENCE = process.env.FSW_REFERENCE || "";
const FSW_WATCHER = FSW_REFERENCE ? join(FSW_REFERENCE, "tools", "mission-watcher.mjs") : "";

// The same contract body drives both watchers (mirrors fixtures/task-contract.example.md).
const CONTRACT = `TASK_TYPE: autonomous
TASK_ID: aaop-github-mission-parity
EXECUTOR: local-worker-1
GOAL: parity
SCOPE: read-only
NOT-IN-SCOPE: nothing real
DONE-WHEN: both watchers agree
EVIDENCE: timeline
FINAL VERIFICATION: timeline review
GATE: COMMANDER
STOP-WHEN: evidence v1 written
RETURN-WHEN: arbitration broken`;

const ISSUE = { number: 5, title: "parity mission", state: "OPEN", body: CONTRACT };
const TID = taskIdFor(5, CONTRACT);

// ---------------------------------------------------------------------------
// 1. UNIT — real mission-core.mjs (imported, not copied)
// ---------------------------------------------------------------------------
test("unit: illegal GATE rejected by the real validator", () => {
  const { missing } = validateContract(CONTRACT.replace("GATE: COMMANDER", "GATE: SENATE"));
  assert.ok(missing.some((m) => /GATE 非法值/.test(m)));
});

test("unit: autonomous requires STOP-WHEN and RETURN-WHEN", () => {
  const body = CONTRACT.replace(/STOP-WHEN: .*\n?/, "").replace(/RETURN-WHEN: .*\n?/, "");
  const { missing } = validateContract(body);
  assert.ok(missing.includes("STOP-WHEN（autonomous 必填）"), "STOP-WHEN flagged missing");
  assert.ok(missing.includes("RETURN-WHEN（autonomous 必填）"), "RETURN-WHEN flagged missing");
});

test("unit: surgical task may omit STOP-WHEN/RETURN-WHEN", () => {
  const body = CONTRACT.replace("TASK_TYPE: autonomous", "TASK_TYPE: surgical")
    .replace(/STOP-WHEN: .*\n?/, "").replace(/RETURN-WHEN: .*\n?/, "");
  assert.deepEqual(validateContract(body).missing, []);
});

test("unit: earliest valid CLAIM is the unique winner (nonce tie-break)", () => {
  const issue = { comments: [
    { body: `[CLAIM] task_id=${TID} worker=w2 claim_nonce=aaaa at=t1`, createdAt: "00:00:02" },
    { body: `[CLAIM] task_id=${TID} worker=w1 claim_nonce=zzzz at=t1`, createdAt: "00:00:01" },
  ]};
  const ms = deriveMissionState(issue, TID);
  assert.equal(ms.state, "CLAIMED");
  assert.equal(ms.winner.worker, "w1", "earliest-at wins");
});

test("unit: append-only evidence + CHANGES_REQUIRED recovery + READY/RETURN terminal", () => {
  const base = [
    { body: `[CLAIM] task_id=${TID} worker=w1 claim_nonce=n1`, createdAt: "00:00:01" },
    { body: `[EVIDENCE] task_id=${TID} worker=w1`, createdAt: "00:00:02" },
  ];
  assert.equal(deriveMissionState({ comments: [...base, { body: "[REVIEW: CHANGES_REQUIRED]", createdAt: "00:00:03" }] }, TID).state, "CHANGES_REQUIRED");
  assert.equal(deriveMissionState({ comments: [...base, { body: "[REVIEW: READY_TO_ADVANCE]", createdAt: "00:00:03" }] }, TID).state, "READY_TO_ADVANCE");
  assert.equal(deriveMissionState({ comments: [...base, { body: `[RETURN] task_id=${TID} at=x`, createdAt: "00:00:03" }] }, TID).state, "RETURNED");
  assert.equal(deriveMissionState({ comments: [...base, { body: `[EVIDENCE] task_id=${TID} worker=w1`, createdAt: "00:00:04" }] }, TID).evidenceCount, 2);
});

// ---------------------------------------------------------------------------
// 2. SUBPROCESS PARITY — runs both real watchers via a fake gh
// ---------------------------------------------------------------------------

function writeFakeGh(binDir) {
  const p = join(binDir, "gh");
  writeFileSync(p, `#!/usr/bin/env node
const fs = require("fs");
const p = process.env.FAKE_GH_STATE;
const s = JSON.parse(fs.readFileSync(p, "utf8"));
const a = process.argv.slice(2);
if (a[0] === "issue" && a[1] === "view") {
  const it = s.issue;
  process.stdout.write(JSON.stringify({ number: it.number, title: it.title, body: it.body, state: it.state, comments: it.comments, updatedAt: new Date().toISOString() }));
} else if (a[0] === "issue" && a[1] === "comment") {
  const bi = a.indexOf("--body");
  s.issue.comments.push({ body: bi >= 0 ? a[bi + 1] : "", createdAt: new Date().toISOString() });
  fs.writeFileSync(p, JSON.stringify(s, null, 2));
} else { process.stderr.write("unexpected gh call " + JSON.stringify(a)); process.exit(2); }
`);
  chmodSync(p, 0o755);
}

function fswShapedCopy(tmp) {
  // relocate the REAL FSW watcher source into an FSW-shaped layout so its hardcoded
  // ../state/WORKSPACE_STATE.json resolves to our fixture, never the real FSW repo.
  const tools = join(tmp, "fsw-layout", "tools");
  const state = join(tmp, "fsw-layout", "state");
  mkdirSync(tools, { recursive: true });
  mkdirSync(state, { recursive: true });
  writeFileSync(join(tools, "mission-watcher.mjs"), readFileSync(FSW_WATCHER, "utf8"));
  writeFileSync(join(state, "WORKSPACE_STATE.json"), JSON.stringify({ active_mission: { issue_number: 5 } }));
  return join(tools, "mission-watcher.mjs");
}

function runWatcher(watcherPath, binDir, issuePath, stateFile) {
  const args = ["check", "--once", "--repo", "FixtureOwner/FixtureRepo", "--worker", "local-worker-1"];
  if (stateFile) args.push("--state-file", stateFile);
  return spawnSync(process.execPath, [watcherPath, ...args], {
    encoding: "utf8",
    env: { ...process.env, PATH: binDir + ":" + process.env.PATH, FAKE_GH_STATE: issuePath },
  });
}

function freshWorkspace() {
  const tmp = mkdtempSync(join(tmpdir(), "aaop-parity-"));
  const binDir = join(tmp, "bin"); mkdirSync(binDir);
  writeFakeGh(binDir);
  const issuePath = join(tmp, "issue.json");
  const writeFixture = (comments, body) => writeFileSync(issuePath, JSON.stringify({ issue: { number: 5, title: "parity mission", state: "OPEN", body: body || CONTRACT, comments } }, null, 2));
  writeFixture([]);
  const aaopState = join(tmp, "aaop-state.json");
  writeFileSync(aaopState, JSON.stringify({ active_mission: { issue_number: 5 } }));
  const fswWatcher = fswShapedCopy(tmp);
  const postedClaims = () => JSON.parse(readFileSync(issuePath, "utf8")).issue.comments.filter((c) => /^\[CLAIM\]/.test(c.body));
  const claimedTaskIds = () => postedClaims().map((c) => (c.body.match(/task_id=(\S+)/) || [])[1]).filter(Boolean);
  return { tmp, binDir, issuePath, writeFixture, aaopState, fswWatcher, postedClaims, claimedTaskIds };
}

const fixtures = [
  { name: "UNCLAIMED", comments: [], decision: /won claim/ },
  { name: "CLAIMED_BY_OTHER", comments: [{ body: `[CLAIM] task_id=${TID} worker=w2 claim_nonce=n2 at=t`, createdAt: "00:00:01" }], decision: /已被其他 Primary Executor 接单（winner=w2）/ },
  { name: "CHANGES_REQUIRED", comments: [
    { body: `[CLAIM] task_id=${TID} worker=local-worker-1 claim_nonce=n1 at=t`, createdAt: "00:00:01" },
    { body: `[EVIDENCE] task_id=${TID} worker=local-worker-1`, createdAt: "00:00:02" },
    { body: `[REVIEW: CHANGES_REQUIRED]`, createdAt: "00:00:03" },
  ], decision: /CHANGES_REQUIRED\] 恢复/ },
  { name: "EVIDENCE_SUBMITTED", comments: [
    { body: `[CLAIM] task_id=${TID} worker=local-worker-1 claim_nonce=n1 at=t`, createdAt: "00:00:01" },
    { body: `[EVIDENCE] task_id=${TID} worker=local-worker-1`, createdAt: "00:00:02" },
  ], decision: /等待 .*Review/ },
  { name: "READY_TO_ADVANCE", comments: [
    { body: `[CLAIM] task_id=${TID} worker=local-worker-1 claim_nonce=n1 at=t`, createdAt: "00:00:01" },
    { body: `[EVIDENCE] task_id=${TID} worker=local-worker-1`, createdAt: "00:00:02" },
    { body: `[REVIEW: READY_TO_ADVANCE]`, createdAt: "00:00:03" },
  ], decision: /不再执行/ },
  { name: "RETURNED", comments: [
    { body: `[CLAIM] task_id=${TID} worker=local-worker-1 claim_nonce=n1 at=t`, createdAt: "00:00:01" },
    { body: `[EVIDENCE] task_id=${TID} worker=local-worker-1`, createdAt: "00:00:02" },
    { body: `[RETURN] task_id=${TID} at=x`, createdAt: "00:00:03" },
  ], decision: /\[RETURN\] 停止/ },
];

const INVALID_CONTRACT = CONTRACT.replace("GATE: COMMANDER", "GATE: SENATE");
const EXTRA_FIXTURES = [
  { name: "INVALID_GATE", body: INVALID_CONTRACT, comments: [], decision: /TASK CONTRACT 不合法.*GATE 非法值/ },
  { name: "TWO_CLAIMS", comments: [
    { body: `[CLAIM] task_id=${TID} worker=w1 claim_nonce=n1 at=t`, createdAt: "00:00:01" },
    { body: `[CLAIM] task_id=${TID} worker=w2 claim_nonce=n2 at=t`, createdAt: "00:00:02" },
  ], decision: /已被其他 Primary Executor 接单（winner=w1）/ },
];

for (const fx of [...fixtures, ...EXTRA_FIXTURES]) {
  test(`subprocess parity: ${fx.name} — AAOP adapter ≡ FSW reference`, (t) => {
    if (!FSW_WATCHER) { t.skip("FSW_REFERENCE not set — point it at a Family-Space-Workspace clone"); return; }
    const ws = freshWorkspace();
    try {
      // AAOP adapter (fresh fixture)
      ws.writeFixture(fx.comments, fx.body);
      const aaop = runWatcher(ADAPTER, ws.binDir, ws.issuePath, ws.aaopState);
      const aaopTids = ws.claimedTaskIds();

      // FSW reference (fresh fixture)
      ws.writeFixture(fx.comments, fx.body);
      const fsw = runWatcher(ws.fswWatcher, ws.binDir, ws.issuePath, null);
      const fswTids = ws.claimedTaskIds();

      assert.equal(aaop.status, 0, `AAOP exited ${aaop.status}: ${aaop.stderr}`);
      assert.equal(fsw.status, 0, `FSW exited ${fsw.status}: ${fsw.stderr}`);
      assert.match(aaop.stdout, fx.decision, `AAOP ${fx.name} decision mismatch`);
      assert.match(fsw.stdout, fx.decision, `FSW ${fx.name} decision mismatch`);

      if (fx.name === "UNCLAIMED") {
        assert.deepEqual(aaopTids, [TID], "AAOP derived the canonical sha1 task_id");
        assert.deepEqual(fswTids, [TID], "FSW derived the canonical sha1 task_id");
      }
    } finally {
      rmSync(ws.tmp, { recursive: true, force: true });
    }
  });
}