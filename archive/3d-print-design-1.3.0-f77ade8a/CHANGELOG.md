## 1.3.0 pending human approval

Physical fragile-snap feedback; load path separation, root/slot transitions, print direction and test-first repair. No repaired-model claim.

### 1.3.0+workbuddy.1 — 2026-10-07（WorkBuddy 平台适配）

- 从 `C:\Users\18168\.codex\skills\3d-print-design` 1.3.0 升级安装（前装版本 1.0.0，已备份为 `3d-print-design.bak-1.0.0-20261007`）。
- 平台适配：`scripts/lifecycle.py` 的 install 目标白名单追加 `~/.workbuddy/skills`（上游仅含 `.codex/skills`、`.agents/skills`），否则在 WorkBuddy 下无法走 plan/install 升级流程。每次从上游升级后需重新打此补丁。
- 新增文件（相对 1.0.0）：`references/efficient-production.md`、`references/assembly-and-support.md`、`references/fragile-snap-feedback.md`、`references/optimization-evidence.md`、`scripts/run_pipeline.py`、`scripts/batch_move.ps1`。
- 安装时排除上游 `scripts/__pycache__`。

## 1.2.0 pending human approval

Local mating-core exclusions, complete trial coverage, final G-code bore support audit; count nonprinting modifiers separately; preserve stage cache and consent gating.

# 1.1.0 制作效率升级（待人工批准）

- 保留1.0.1候选的免胶C口、颈杆出口、侧叉支架和布尔融合检查。
- 增加验证优先、接口先行、最终渲染后置与低清预览流程。
- 增加带输入/依赖/输出哈希的阶段运行器、旧输出逐文件保留、日志、计时和失败阻断。
- 修正维护脚本prepare未同步SKILL metadata版本、audit未核对版本的问题。
- 真实生产STL不变，9项运行器行为测试通过；完整新设计端到端提速尚未实测。
