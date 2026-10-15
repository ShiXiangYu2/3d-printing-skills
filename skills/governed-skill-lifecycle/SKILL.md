---
name: governed-skill-lifecycle
description: 为创建、训练、安装、升级和优化技能提供来源哈希、只读检查、候选差异和人工批准后自动备份安装校验；不静默覆盖已装技能。
metadata:
  version: "1.0.0"
---

# 技能自动维护与人工批准

用户要求每个今后训练或安装的技能具有自动升级检查、自动优化候选和人工同意后自动安装完成能力。创建新技能时，把本包 scripts/lifecycle.py 和 scripts/atomic_move.ps1 复制到候选技能 scripts，包含 VERSION、manifest.json、sources、require_human_approval=true，以及 [维护规范](references/maintenance-policy.md)，并记录复制源哈希。

每次使用执行只读来源检查。每次训练或维护时，根据真实使用问题实际调整候选并验证。来源不可用时如实报告，不猜测上游版本。官方远程来源需要浏览只读验证，本地脚本不假装已经查过远程。

在 artifacts 中自动准备候选、展示差异和验证结果，生成绑定候选内容及当前目标内容的 plan。首次安装、升级、覆盖、激活均须得到用户对当前候选明确同意。不得自行传入审批哈希；它是技术校验值，不是人类授权证据。

用户同意后自动执行备份、同卷暂存、安装、内容校验和回执，失败保留现场并恢复备份。候选或目标变动使计划失效，重新展示并重新请求批准。没有人类同意时保持候选待审，不注册绕过门禁的后台任务。

只在本次请求涉及的技能范围内维护；现有其他技能逐个准备补齐候选，不能静默全量改造。目标支持 Codex ~/.codex/skills 与 WorkBuddy ~/.agents/skills，其他运行时需明确适配目标校验。

具体命令与限制见 [维护规范](references/maintenance-policy.md)。
