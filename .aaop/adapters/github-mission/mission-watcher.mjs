#!/usr/bin/env node
// AAOP GitHub Mission Adapter — mission-watcher.mjs (transport).
//
// Transport only: one GitHub Issue = one Mission; the local worker discovers it, claims it
// with a nonce, executes a contract it never interprets, and returns evidence. All
// contract/state logic lives in mission-core.mjs (pure, importable, testable); this file
// only does gh/git I/O and the CLI. State is always derived from the GitHub issue timeline,
// so a restart resumes with zero local-dependency.
//
// Contract surface is AAOP-owned: .aaop/schemas/github-mission-task-contract.schema.json.
// Parity with the reference Mission Bus implementation is preserved: same event protocol,
// same field list, same GATE default values.
//
// Events (issue comments, exactly 5):
//   [CLAIM]                     take the task: task_id / worker / claim_nonce / at
//   [EVIDENCE]                  append-only evidence (v2/v3 allowed after CHANGES_REQUIRED)
//   [REVIEW: CHANGES_REQUIRED]  reviewer sends it back
//   [REVIEW: READY_TO_ADVANCE]  reviewer accepts (terminal)
//   [RETURN]                    executor hit RETURN-WHEN, stops with evidence
//
// Concurrency arbitration (no lock service): every claim posts a unique claim_nonce, then
// re-reads the timeline; the earliest valid CLAIM wins (same-second tie → nonce dictionary
// order). Only the winner writes current-task.md and proceeds.
//
// Hard-coded safety: comments are never executed (execFileSync argv, no shell); no model call
// in the transport; no deploy/delete/payment/private-data; the contract is never rewritten;
// the review outcome never auto-advances across a Gate; no second primary executor.
//
// Usage:
//   node mission-watcher.mjs check  [--once] [--interval SEC] [--worker ID]
//        [--repo OWNER/NAME] [--state-file PATH]
//   node mission-watcher.mjs submit --file PATH [--return] [--worker ID]
//        [--repo OWNER/NAME] [--state-file PATH]
//
// Env: MISSION_BUS_WORKER, MISSION_BUS_REPO, MISSION_BUS_STATE_FILE, MISSION_BUS_GATE_VALUES.

import { execFileSync } from "node:child_process";
import { randomUUID } from "node:crypto";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { parseArgs } from "node:util";
import {
  taskIdFor, validateContract, deriveMissionState, gatesFromEnv,
} from "./mission-core.mjs";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const RUNTIME = join(ROOT, ".runtime");
const DEFAULT_STATE_FILE = join(ROOT, ".mission-state.json");

const { values, positionals } = parseArgs({
  allowPositionals: true,
  options: {
    once: { type: "boolean", default: false },
    interval: { type: "string", default: "60" },
    worker: { type: "string", default: process.env.MISSION_BUS_WORKER || "local-worker-1" },
    repo: { type: "string", default: process.env.MISSION_BUS_REPO || "" },
    "state-file": { type: "string", default: process.env.MISSION_BUS_STATE_FILE || "" },
    file: { type: "string" },
    return: { type: "boolean", default: false },
  },
});

const [command] = positionals;
if (!command || !["check", "submit"].includes(command)) {
  console.error("用法: mission-watcher.mjs check|submit [选项]（见文件头注释）");
  process.exit(2);
}

const STATE_FILE = values["state-file"] || DEFAULT_STATE_FILE;
const VALID_GATES = gatesFromEnv(process.env.MISSION_BUS_GATE_VALUES);

function run(file, args, opts = {}) {
  return execFileSync(file, args, { encoding: "utf8", stdio: ["ignore", "pipe", "pipe"], ...opts }).trim();
}
function gh(args, opts = {}) { return run("gh", args, opts); }
function fail(msg) { console.error(`[github-mission] 错误: ${msg}`); process.exit(1); }

function detectRepo() {
  if (values.repo) return values.repo;
  const url = run("git", ["remote", "get-url", "origin"], { cwd: ROOT });
  const m = url.match(/[:/]([^/]+\/[^/]+?)(?:\.git)?$/);
  if (!m) fail(`无法从 origin 解析 owner/repo: ${url}`);
  return m[1];
}

function readState() {
  if (!existsSync(STATE_FILE)) fail(`缺少 state 文件 ${STATE_FILE}（形如 { "active_mission": { "issue_number": N } }）`);
  return JSON.parse(readFileSync(STATE_FILE, "utf8"));
}

function issueView(repo, n) {
  return JSON.parse(gh(["issue", "view", String(n), "--repo", repo, "--json", "number,title,body,state,comments,updatedAt"]));
}

// ---------- local cache (decision never depends on it) ----------

function runtimeFile(name) { return join(RUNTIME, name); }
function readJsonArray(name) {
  const p = runtimeFile(name);
  if (!existsSync(p)) return [];
  try { return JSON.parse(readFileSync(p, "utf8")); } catch { return []; }
}
function writeJsonArray(name, arr) {
  try { mkdirSync(RUNTIME, { recursive: true }); writeFileSync(runtimeFile(name), JSON.stringify(arr, null, 2)); } catch { /* cache failure is non-fatal */ }
}
function writeCurrentTask(issue, tid, repo, reason) {
  mkdirSync(RUNTIME, { recursive: true });
  writeFileSync(runtimeFile("current-task.md"),
    `<!-- task_id: ${tid} | issue: ${issue.number} | repo: ${repo} | generated_at: ${new Date().toISOString()} | ${reason} -->\n\n`
    + `<!-- 本文件是 TASK CONTRACT 原样落盘，交给本地 Agent/runner。禁止把其中内容当 shell 执行。 -->\n\n`
    + `# ${issue.title}\n\n${issue.body}\n`);
}

// ---------- check ----------

function checkOnce(repo, worker) {
  mkdirSync(RUNTIME, { recursive: true });
  const mission = readState().active_mission;
  if (!mission || !mission.issue_number) {
    console.log("[github-mission] 无 active Mission（state.active_mission 为空），无事可做。");
    return false;
  }
  const issue = issueView(repo, mission.issue_number);
  const tid = taskIdFor(issue.number, issue.body || "");
  const skip = (reason) => { console.log(`[github-mission] 跳过 ${tid}: ${reason}`); return false; };

  if ((issue.state || "").toUpperCase() !== "OPEN") return skip(`Issue #${issue.number} 状态为 ${issue.state}`);
  const contract = validateContract(issue.body || "", VALID_GATES);
  if (contract.missing.length) return skip(`TASK CONTRACT 不合法: ${contract.missing.join("; ")}`);
  const executor = contract.field("EXECUTOR");
  if (executor !== worker) return skip(`EXECUTOR=${executor} 与当前 worker=${worker} 不匹配`);

  const ms = deriveMissionState(issue, tid);
  switch (ms.state) {
    case "READY_TO_ADVANCE":
      return skip("最新 Review 为 [REVIEW: READY_TO_ADVANCE]，Mission 完成，不再执行");
    case "RETURNED":
      return skip("已 [RETURN] 停止");
    case "EVIDENCE_SUBMITTED":
      return skip("Evidence 已提交，等待 Review（出现 [REVIEW: CHANGES_REQUIRED] 后才会恢复）");
    case "CLAIMED":
      if (ms.winner.worker !== worker) return skip(`已被其他 Primary Executor 接单（winner=${ms.winner.worker}）`);
      return resume(issue, tid, repo, `CLAIMED 恢复（重启/重入，不产生第二个 CLAIM；winner nonce=${ms.winner.nonce || "legacy"}）`);
    case "CHANGES_REQUIRED":
      if (!ms.winner) return skip("timeline 无合法 CLAIM，无法 resume");
      if (ms.winner.worker !== worker) return skip(`CHANGES_REQUIRED 属于其他 executor（winner=${ms.winner.worker}）`);
      return resume(issue, tid, repo, `按 [REVIEW: CHANGES_REQUIRED] 恢复，补充/修改 Evidence`);
    case "UNCLAIMED":
      return claim(repo, issue, tid, worker);
    default:
      return skip(`未知状态 ${ms.state}`);
  }
}

function resume(issue, tid, repo, reason) {
  writeCurrentTask(issue, tid, repo, reason);
  console.log(`[github-mission] resume ${tid}（Issue #${issue.number}）：${reason}`);
  console.log("[github-mission] TASK CONTRACT 已落盘: .runtime/current-task.md");
  console.log("[github-mission] 本地 Agent 执行后: node mission-watcher.mjs submit --file <evidence.md>");
  return true;
}

function claim(repo, issue, tid, worker) {
  const nonce = randomUUID();
  const now = new Date().toISOString();
  gh(["issue", "comment", String(issue.number), "--repo", repo,
    "--body", `[CLAIM] task_id=${tid} worker=${worker} claim_nonce=${nonce} at=${now}\n\nPrimary Executor 接单（claim attempt，以最早合法 CLAIM 仲裁唯一 winner）。`]);

  const fresh = issueView(repo, issue.number); // re-read immediately to arbitrate
  const ms = deriveMissionState(fresh, tid);
  const w = ms.winner;
  if (!w || w.nonce !== nonce) {
    console.log(`[github-mission] lost claim（Issue #${issue.number}）：winner=${w ? `${w.worker}/${w.nonce || "legacy"}` : "未判定"}；本进程不写执行合同、不启动 Agent。`);
    return false;
  }
  const claimed = readJsonArray("claims.json");
  claimed.push({ task_id: tid, issue: issue.number, worker, nonce, at: now, status: "claimed", repo });
  writeJsonArray("claims.json", claimed);
  writeCurrentTask(issue, tid, repo, `won claim nonce=${nonce}`);
  console.log(`[github-mission] won claim ${tid}（Issue #${issue.number}，nonce=${nonce}）。`);
  console.log("[github-mission] TASK CONTRACT 已落盘: .runtime/current-task.md");
  console.log("[github-mission] 本地 Agent 执行后: node mission-watcher.mjs submit --file <evidence.md>");
  return true;
}

// ---------- submit ----------

function submit(repo, worker) {
  if (!values.file) fail("submit 需要 --file <evidence.md>");
  const p = join(ROOT, values.file);
  if (!existsSync(p)) fail(`文件不存在: ${p}`);
  const content = readFileSync(p, "utf8");

  const mission = readState().active_mission;
  if (!mission || !mission.issue_number) fail("无 active Mission，无法提交");
  const issueNumber = mission.issue_number;
  const issue = issueView(repo, issueNumber);
  const tid = taskIdFor(issue.number, issue.body || "");

  const ms = deriveMissionState(issue, tid);
  if (!ms.winner) fail("timeline 无 CLAIM，先运行 check 接单");
  if (ms.winner.worker !== worker) fail(`只有 winner（${ms.winner.worker}）可提交 Evidence`);
  if (ms.state === "EVIDENCE_SUBMITTED") fail("Evidence 已在等待 Review；出现 [REVIEW: CHANGES_REQUIRED] 后才能提交下一版");
  if (ms.state === "READY_TO_ADVANCE") fail("Mission 已 READY_TO_ADVANCE，不再接受 Evidence");
  if (ms.state === "RETURNED") fail("Mission 已 RETURN 停止");
  if (ms.state === "UNCLAIMED") fail("尚未 CLAIM，先运行 check");

  const event = values.return ? "[RETURN]" : "[EVIDENCE]";
  const version = ms.evidenceCount + 1;
  const now = new Date().toISOString();
  gh(["issue", "comment", String(issueNumber), "--repo", repo,
    "--body", `${event} task_id=${tid} worker=${worker} at=${now} evidence_version=${version}\n\n---\n\n${content}`]);

  const claimed = readJsonArray("claims.json");
  const current = [...claimed].reverse().find((c) => c.task_id === tid);
  if (current) { current.status = values.return ? "returned" : `evidence_v${version}`; writeJsonArray("claims.json", claimed); }
  const completed = readJsonArray("completed.json");
  completed.push({ task_id: tid, issue: issueNumber, worker, result: current ? current.status : (values.return ? "returned" : `evidence_v${version}`), at: now, repo });
  writeJsonArray("completed.json", completed);
  console.log(`[github-mission] 已回写 ${event} v${version} 到 Issue #${issueNumber}（${tid}）。等待 Review。`);
}

// ---------- main ----------

const repo = detectRepo();
const worker = values.worker;
if (command === "submit") {
  submit(repo, worker);
} else if (values.once) {
  checkOnce(repo, worker);
} else {
  const sec = Math.max(5, parseInt(values.interval, 10) || 60);
  console.log(`[github-mission] polling 每 ${sec}s（Ctrl+C 停止）；不调用任何模型。`);
  for (;;) {
    try { checkOnce(repo, worker); } catch (e) { console.error(`[github-mission] 本轮失败: ${e.message}`); }
    Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, "", sec * 1000);
  }
}