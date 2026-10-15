# 1.0.0 — 2026-10-01

Initial reviewed candidate. Installation requires approval of the current version/hash.

## 2026-10-01 — WorkBuddy 迁移（版本号仍为 1.0.0）

- 从 `~/.codex/skills/3d-print-design` 原样迁移到 `~/.workbuddy/skills/3d-print-design`，9 个文件，审计 SHA256 通过。
- `scripts/lifecycle.py` 的 `install` 目标白名单新增 `~/.workbuddy/skills`，使 plan/install 升级流程在 WorkBuddy 下可用（原仅 `.codex/skills`、`.agents/skills`）。
- 未改动 SKILL.md 的设计约束、manifest 的安全声明（require_human_approval / recursive_deletion / network_downloads 保持原值）。
