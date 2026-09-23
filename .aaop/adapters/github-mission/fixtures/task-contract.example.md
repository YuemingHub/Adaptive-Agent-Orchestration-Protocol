# TASK CONTRACT

TASK_TYPE: autonomous
TASK_ID: aaop-github-mission-parity-20260923
EXECUTOR: local-worker-1

GOAL:
证明同一份 TASK CONTRACT 可以被 AAOP GitHub Mission Adapter 与 Family-Space-Workspace 的
原 Mission Bus watcher 用同一套事件协议等价消费 —— 二者产出的 current-task.md 与
非交互状态推导（CLAIM winner / EVIDENCE 版本 / REVIEW 恢复）逐项一致。

SCOPE:
- 只读；不修改任何仓库文件；不 deploy、不删除资产、不处理付款；
- 只验证 transport：check 接单、nonce 仲裁、submit 回写 evidence。

NOT-IN-SCOPE:
- 任何真实家庭/公司数据；
- 任何模型调用；
- 任何 Review 后的自动推进（不越 Gate）。

DONE-WHEN:
同一 Issue 上可见 [CLAIM]（带 claim_nonce）、[EVIDENCE] v1，且两个 watcher 对
非交互状态推导得到相同的 winner 与 evidence_count。

EVIDENCE:
- watcher 的 check 输出（won/lost claim 与 nonce）；
- Issue timeline 中的 [CLAIM] / [EVIDENCE] 评论；
- 两实现各一份 current-task.md（应逐字节同义）。

FINAL VERIFICATION:
只凭 Issue timeline 即可复核 winner 唯一性与 evidence 版本单调递增；无需询问本地 Agent。

GATE: COMMANDER

STOP-WHEN:
[EVIDENCE] v1 已回写且两实现状态推导一致即停。

RETURN-WHEN:
- 仲裁实现缺陷导致无法判定唯一 winner；
- 两实现对同一 timeline 推导出不同的 winner 或 evidence_count 且无法归因于实现差异。