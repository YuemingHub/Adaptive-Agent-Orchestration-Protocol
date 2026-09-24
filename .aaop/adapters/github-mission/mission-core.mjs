// Pure, side-effect-free core of the AAOP GitHub Mission Adapter.
// This is the importable contract/state logic. transport (gh/git I/O) lives in
// mission-watcher.mjs; nothing here touches the network, argv, or the filesystem
// (except reading the canonical contract schema once, below).
//
// SINGLE CONTRACT AUTHORITY: the Markdown TASK CONTRACT is the human input format;
// it is parsed to a normalized object, then validated against
// .aaop/schemas/github-mission-task-contract.schema.json. The schema decides:
//   - required fields        (schema.required)
//   - task_type enum         (schema.properties.task_type.enum)
//   - gate enum              (schema.properties.gate.enum)
//   - autonomous => stop_when + return_when   (schema.if / schema.then)
// There is NO second copy of these rules in JS. The FIELD_MAP below is a FORMAT
// mapping only (human Markdown key -> schema field name), not a semantic truth.

import { readFileSync } from "node:fs";
import { createHash } from "node:crypto";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const SCHEMA_PATH = join(dirname(fileURLToPath(import.meta.url)), "..", "..", "schemas", "github-mission-task-contract.schema.json");
export const SCHEMA = JSON.parse(readFileSync(SCHEMA_PATH, "utf8"));

// Markdown (human) key -> schema field name. Format mapping only.
const FIELD_MAP = {
  "TASK_ID": "task_id",
  "TASK_TYPE": "task_type",
  "EXECUTOR": "executor",
  "GOAL": "goal",
  "SCOPE": "scope",
  "NOT-IN-SCOPE": "not_in_scope",
  "DONE-WHEN": "done_when",
  "EVIDENCE": "evidence",
  "FINAL VERIFICATION": "final_verification",
  "GATE": "gate",
  "STOP-WHEN": "stop_when",
  "RETURN-WHEN": "return_when",
};
const REVERSE_MAP = Object.fromEntries(Object.entries(FIELD_MAP).map(([md, sc]) => [sc, md]));

const esc = (s) => s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");

// MARKDOWN -> normalized object (schema field names). Human format preserved upstream.
export function parseContract(markdown) {
  const body = markdown || "";
  const obj = {};
  for (const [mdKey, schemaKey] of Object.entries(FIELD_MAP)) {
    const m = body.match(new RegExp(`^${esc(mdKey)}:\\s*(.+)$`, "mi"));
    if (m) obj[schemaKey] = m[1].trim();
  }
  return obj;
}

export function gateEnum(schema = SCHEMA) {
  return (schema.properties?.gate?.enum || []).map(String);
}

// Validate a normalized object against the schema (the schema is the authority).
export function validateContract(markdown, { schema = SCHEMA } = {}) {
  const obj = parseContract(markdown);
  const missing = [];
  const gateValues = gateEnum(schema).map(String);

  for (const key of schema.required || []) {
    if (!obj[key]) missing.push(REVERSE_MAP[key] ?? key);
  }

  for (const [key, prop] of Object.entries(schema.properties || {})) {
    if (Array.isArray(prop.enum) && obj[key] != null) {
      const ok = prop.enum.some((e) => String(e).toLowerCase() === String(obj[key]).toLowerCase());
      if (!ok) {
        if (key === "gate") {
          missing.push(`GATE 非法值 "${obj[key]}"（仅允许 ${gateValues.join("/")}）`);
        } else {
          missing.push(`${REVERSE_MAP[key] ?? key} 非法值 "${obj[key]}"`);
        }
      }
    }
  }

  if (schema.if && schema.then) {
    const condKey = Object.keys(schema.if.properties || {})[0];
    const condVal = schema.if.properties?.[condKey]?.const;
    if (condKey && condVal != null && String(obj[condKey] ?? "").toLowerCase() === String(condVal).toLowerCase()) {
      for (const k of schema.then.required || []) {
        if (!obj[k]) missing.push(`${REVERSE_MAP[k] ?? k}（${condVal} 必填）`);
      }
    }
  }

  return {
    obj,
    missing,
    taskType: String(obj.task_type || "surgical").toLowerCase(),
    gate: String(obj.gate || "").toUpperCase(),
  };
}

// TRANSPORT IDENTITY (issue-derived), distinct from the contract's `task_id`.
// This is what timeline events ([CLAIM] / [EVIDENCE] / [RETURN]) match on, posted
// under the `task_id=` key for reference-watcher compatibility. It is NOT the
// contract's TASK_ID (which is a schema-required human field on the contract body).
export function transportIdFor(issueNumber, body) {
  return `mission-${issueNumber}-${createHash("sha1").update(body || "").digest("hex").slice(0, 12)}`;
}

export function matchField(body, key) {
  return (body.match(new RegExp(`${esc(key)}=([^\\s]+)`)) || [])[1] || null;
}

// timeline comments -> ordered events (the single source of truth).
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