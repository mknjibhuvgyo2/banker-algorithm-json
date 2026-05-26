# 银行家算法 JSON 场景诊断系统

## 基本信息

| 项目 | 内容 |
|---|---|
| 学生姓名 | 武凯旋 |
| 学号 | 20231205788 |
| 课程 | 操作系统 |
| 实现方向 | JSON 场景诊断版 |

## 一、项目说明

本项目使用 Python 编写银行家算法模拟程序，通过 JSON 文件描述系统资源状态。程序读取进程列表、资源类型、最大需求矩阵、已分配矩阵和可用资源向量后，自动计算 Need 矩阵，并完成安全性检测。

与普通命令行输入方式相比，本版本将测试数据放在 JSON 文件中，便于保存不同实验案例，也方便后续扩展为批量测试工具。

## 二、主要功能

1. 从 `data/example_state.json` 读取系统状态。
2. 根据 Max 和 Allocation 计算 Need。
3. 使用银行家算法判断系统是否安全。
4. 安全状态下输出安全序列。
5. 不安全状态下输出 blocked 进程和诊断摘要。
6. 将检测过程整理为 `rounds` 字段，方便写入报告或交给 AI 解释。

## 三、目录结构

```text
项目/
├─ data/
│  └─ example_state.json
├─ src/
│  └─ json_case_advisor/
│     ├─ run_case.py
│     ├─ state_loader.py
│     ├─ safety_checker.py
│     └─ deadlock_advisor.py
├─ PROMPTS.md
├─ TEST_PLAN.md
└─ 报告数据填写参考.md
```

## 四、运行步骤

进入项目目录：

```powershell
cd "E:\0526代写\武凯旋20231205788\项目"
```

运行默认 JSON 案例：

```powershell
python ".\src\json_case_advisor\run_case.py"
```

保存输出结果：

```powershell
python ".\src\json_case_advisor\run_case.py" --out ".\result.json"
```

## 五、运行结果摘要

默认案例检测结果为安全，安全序列为：

```text
P1 -> P3 -> P0 -> P2
```

程序输出中包含 `need`、`rounds`、`sequence` 和 `diagnosis` 字段。其中 `rounds` 记录每一轮选择的进程、执行前 Work 向量和释放资源，适合用于报告中的算法过程分析。

## 六、AI 交互设计

项目提供 `PROMPTS.md` 文件，用于将 JSON 输出结果转换为自然语言讲解。AI 助教主要承担两个任务：解释安全性检测过程，以及在不安全状态下分析资源不足原因并给出处理建议。
