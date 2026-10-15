# Optimization evidence

# 本次实际问题与改进依据

1. 带挡边轴与侧支架仅共面接触，首次布尔结果为多个连通体；通过真实交叠后布尔融合，11件单连通且封闭。
2. C夹下方的中央立柱和钻头颈杆可能占据夹环环壁；改为侧叉支架并将钻头端C口对准颈杆，通过全部55对静态实体检查。
3. 车身边缘与保险杠有54.86立方毫米穿插；保留保险杠并缩短车身底板/前装甲，通过复查后重新切片。
4. C口装配方向应明确：夹环从开口侧靠近关节销，不能沿轴线越过挡边；本次10项进入方向各9个位置做外部障碍抽样。配合对排除刚体相交，不宣称形变已验证。
5. 主盘和试打盘实际导出通过现有verify_3mf；单部件组的部件extruder省略时正确继承父组，无需强行要求重复字段。

证据：本目录 build.py、audit_trial.py、assembly_audit.json.tmp、trial-topology.json.tmp、delivery.json。实体卡扣未验证。


Agent must make evidence-backed changes, test behavior, and set validated_candidate before planning.
