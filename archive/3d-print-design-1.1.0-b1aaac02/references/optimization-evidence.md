# Optimization evidence

# 制作效率复盘依据

钻臂工程车实施中，多次整套运行build.py：车身出现5个连通体、连接臂13条非流形边、保险杠54.86mm³穿插。脚本内包含Cycles渲染，导致几何改动连带重渲染。首次直接调用Blender未获得Python异常回执，后增加日志才定位失败。最终拓扑/装配/切片均通过，实体配合未验证。

需增加：不渲染的几何阶段、接口小样先检查、验证优先于切片、依赖清单和输入输出哈希缓存、可靠的非零异常退出、每阶段耗时记录。复用几何原语时必须保留机型/喷嘴/材料/间隙/姿态参数，不将未试打卡扣升级为已验证标准件。

旧端到端耗时未被记录，不能给出总体提速百分比；对本次真实模型的新分阶段流程测量首次与缓存重放耗时，并做输入变化、输出篡改和失败阻断测试。


Agent must make evidence-backed changes, test behavior, and set validated_candidate before planning.
