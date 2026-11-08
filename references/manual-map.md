# 手册地图：六本手册的钉版与环境

> 选手册用。权威源是各手册的 `manuals/<id>/manual.json`（`pin` 字段钉死版本），本文件是速查版；引用任何版本号前用 `lab.py info <id>` 现场核对。

## 六本手册一览（edition 均为 2026.10）

| id | 主题 | 钉版（pin） | 受众一句话 |
|---|---|---|---|
| `sglang-101` | SGLang 服务引擎 | SGLang **0.5.22**（commit baa9bef，verified 2026-10-16） | 调过模型 API、想自己服务开源模型的工程师 |
| `vllm-101` | vLLM 服务引擎 | vLLM **0.31.0** | 同上，vLLM 路线 |
| `a2a-101` | A2A 协议 | A2A protocol **1.0.1** | 要做 agent 互操作的开发者 |
| `docker-sandboxes-101` | Docker 沙箱 | sbx **0.47.0** / docker-agent **1.149.0** | 要隔离执行 agent 代码的工程师 |
| `miles-101` | Miles | radixark/miles:latest，main of **2026-10-15** | 该系统生态的使用者 |
| `reverse-engineering-101` | 逆向工程 | rea-agents **6.7.0** + Ghidra **12.1.4** | 想读编译产物的工程师 |

## 每本手册的结构（以 sglang-101 为例，六本同构）

```
manuals/<id>/
├── manual.json        # 元数据：pin / outcomes / palette / parts / capture(run,check,timeout)
├── front.md           # "How to read this manual"——先读
├── sections/          # 正文章节：1-1 … 7-2 + 参考区 r-1…r-7
├── figures/           # 静态图（颜色与箭头语法全手册统一）
├── capture/           # capture kit：run.py / --check / --only + out/ 录制结果
└── research/          # 事实 brief 与来源
```

**分部法**（sglang-101 七部 27 节）：1 Start（3 节）→ 2 请求路径（5）→ 3 KV Cache（6）→ 4 每次前向（6）→ 5 测量服务（3）→ 6 单机到集群（4）→ 7 生产与训练（2）+ 参考区（flags/metrics/事故索引/术语/来源/图索引/制作说明）。

## 环境要求（capture kit 跑通的前提）

| 手册 | 关键要求 | 不满足时 |
|---|---|---|
| sglang-101 | **Apple silicon + macOS 14+**，SGLang 0.5.22（`srt_mps` extra），首跑需网络下 `mlx-community/Qwen3-0.6B-4bit` | `--check` 打印 `skipped` + 原因，exit 0 |
| vllm-101 | 按 front.md（capture 字段可能为空——以 `capture/README.md` 为准） | 同上 |
| a2a-101 | `python3 capture/run.py`（协议实现离线跑） | 同上 |
| docker-sandboxes-101 | Docker 环境 + sbx/docker-agent 指定版本 | 同上 |
| miles-101 | Docker 镜像 `radixark/miles:latest` | 同上 |
| reverse-engineering-101 | rea-agents 6.7.0 + Ghidra 12.1.4 | 同上 |

**通则**：capture kit 设计为**离线、无网络、无密钥**；`--check` 记到临时目录并比对**不随时间变的事实**（temperature 0 的生成文本与 token 数、缓存命中区间、压测成功数与 token 总量），计时类数据不比对。

## 按目标选手册

- **部署+压测+调参上手** → `sglang-101` 或 `vllm-101`（先 1-Start 三节十分钟起服务，再按需跳到 3-KV / 5-测量）
- **面试讲 serving 深度** → 同上两本任选，重点 2-请求路径、3-KV Cache、5-测量，毕业报告的"预测三例"就是素材
- **agent 基础设施** → `a2a-101`（协议）→ `docker-sandboxes-101`（隔离）
- **安全/逆向兴趣** → `reverse-engineering-101`

## 引用规范

- 笔记、报告里每个版本号/数字后面标来源：`manual.json pin (verified 2026-10-16)` 或 `capture/out/<file>`
- 用户环境与 pin 不一致 → 先声明差异再比较结果，差异本身写进 lab-plan 变更记录
