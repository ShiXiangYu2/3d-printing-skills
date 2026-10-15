# Blender / Bambu 已实施流程

## 来源与可重现文件

2026-10-01 本地实施：铁甲搬运者免胶 v3 和 A1 mini v4。归档正式文件在 D:\AI3D建模\铁甲搬运者\A1mini-免胶-v4；构建/检查脚本保留在 C:\Users\18168\.agents\artifacts\mecha-forklift-a1mini-v4。源码及官方本地配置的 SHA256 在 manifest.sources。

使用本机 Blender 5.2.2 LTS、Bambu Studio 2.8.2.61。运行前发现实际安装位置与版本，不假设路径永久不变。

## 模型和接口

13 件：底盘、整体车身、一体内饰、门架、货叉、4 轮、2 轴、2 帽。删去只能粘贴的装饰。卡柱开槽提供弹性，母槽配锁腔；轴端倒钩与帽内锁腔保持固定、轮孔留滚动间隙。

缩小到 62.5% 后重新加粗 2.4 mm 轮轴、调整 2.8 mm 轮孔、轴帽与轮毂，相关弹性臂约 0.8 mm。不是普适参数；丝绸 PLA 等材料必须重新试打。11 个试打件来自真实接口裁切和完整轮轴帽，数字验证仍不保证整机装配路径或实物强度。

Blender：Boolean EXACT 做实体连接/减料；BMesh 检查 nonmanifold_edges=0、connected_components=1、正体积；世界坐标 STL 导出；装配对象包围盒相交时用 Boolean INTERSECT 检查体积。允许正确设计的动态干涉时要分析装配形变，不把静态零交集当作卡扣强度证明。

## 配置和导入

从安装目录 resources/profiles/BBL 加载机型、工艺、耗材 JSON，递归合并 inherits 和 include（包含 G-code 模板），不能保留 A1 G-code 只换成 180 mm 盘。

通用 core 3MF 保存部件 mesh 与三个 component 组对象；Metadata/model_settings.config 设置父组与部件对应的 extruder。颜色组对象各自只用一种耗材。避免照抄自编错误 production-extension 结构，曾造成空盘或崩溃。

本例槽 1 黑、2 金、3 银；连续组顺序黑→银→金，对应 M620 S0A → S2A → S1A。A1 mini 原厂盘 180×180、杆高 25、最大避让半径 73。数值仅用于这个机型当前官方配置，不适用于其他机器。

## CLI 与原生工程

使用 Python subprocess.run 参数列表、creationflags=0x08000000 启动本机 CLI 并等其结束，不要把 Start-Process 启动成功当作切片完成。

```text
bambu-studio.exe --load-settings machine.json;process.json --load-filaments black.json;gold.json;silver.json --curr-bed-type "Textured PEI Plate" --arrange 0 --slice 0 --debug 2 --outputdir OUTPUT_DIR --export-3mf output.tmp.3mf input.3mf
```

参数以列表传递；不要复制这行到 shell 后任由分号分割。`--arrange 0` 保留已验证摆盘。指定 --outputdir 时 --export-3mf 用文件名，绝对路径曾导致导出 -13。

检查进程退出码、result.json return_code、实际输出 3MF、slice_info.config、project_settings.config 与 G-code。普通窗口启动没有终端回执，必须读结果文件。副作用大的动作串行执行，避免覆盖同目录 result.json。

工程切片后设置自定义 print_settings_id、inherits_group 与 different_settings_to_system，保证 GUI 打开仍保留 0.16 mm、支撑与 by object。三耗材时这些数组通常为工艺、三耗材、打印机共 5 项；按真实配置核对，不通过修补配置来伪造已切片参数。

## 结果证据

A1 mini v4：13 件、3 色组、2 次换色，G-code 3 个组各自连续完成；装配约 76.88×45.25×50.94 mm；主盘 9332 秒/33.87 g，试打盘 2204 秒/5.11 g。20 对静态相交候选实体交集为 0。physical_fit_verified=false。

延时摄影警告 not_support_traditional_timelapse / not_generate_timelapse 可解释；碰撞、越界、空盘和其他未解决错误不可忽略。用户改摆盘、拆组、机型或打印顺序后必须重新验证。
