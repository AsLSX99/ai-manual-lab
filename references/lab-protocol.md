# 实验室协议：四步循环、出题原则、capture 执行

> 每节的执行手册。核心思想：**读是输入，预测是输出，实测是裁判**——手册的终点是"能预测手册没展示过的情况"，这是手册 README 的原话标准。

## 一节的完整循环

```
带 outcomes 读正文与 listing → ② 合书预测（2-3 道变体场景题）
  → ③ 实测验证（capture --check 或录制 listing 对照）
  → ④ 机制复述 + 记账（--predictions 带命中数）
```

## 出题原则（变体场景题怎么出）

1. **改参数不改机制**：动一个 flag、一个输入、一个负载档位——答案必须能从这节讲的机制推出来，不能靠猜
2. **答案有唯一方向**：能分对错，"看情况"的题要给出具体条件后收敛成唯一方向
3. **必须可验证**：每题标注验证方式——`capture --check` 的哪个事实、`capture/out/` 的哪个文件、或手册哪条 listing
4. **三档配比**：每节 2-3 题里至少 1 题"手册完全没展示过"（毕业要求的三个例子就从这类攒）
5. **先理由后结论**：用户必须先说推理链再给结论——猜对但说不出理由按错记

### 出题示例（sglang-101 第 3.2 节 mem-fraction-static）

- 手册展示过：两次启动快照不同 → 池大小不同（27.81GB→24.25GB / 38.29GB→33.39GB，都是 87.2%）
- **变体题**：同一台机器，浏览器多开 8 个标签页后立刻启动服务，池会怎么变？为什么这对笔记本是陷阱？
- 验证：`capture/out/` 的 startup 行 + 机制（快照比例规则假设机器归服务独占）

## 实测验证的三种方式（按优先级）

| 方式 | 何时用 | 怎么判 |
|---|---|---|
| `capture/run.py --check` | 环境满足手册 requirements | 比对不随时间变的事实（生成文本/token 数/缓存区间/压测总量），全对 = 验证通过 |
| `capture/run.py --only <case>` | 只想验证单个配置 | 对照该 case 的 out 文件 |
| 录制 listing 对照 | 环境不满足（skip） | 用手册自带 `capture/out/` 指认事实，报告标注 **"环境未验"** |

### skip 处理（如实，不糊弄）

1. `--check` 打印 `skipped` + 原因、exit 0 → **记 skip，不算验证通过**
2. 原因写进 prediction-log（缺 Apple silicon？版本不对？缺镜像？）
3. 升级路径写进 lab-plan：装环境 / 换机器 / 借 CI——但**别让整个手册停摆**，先用录制 listing 继续
4. 毕业标准里"capture 至少成功一次"没达成 → mastery-report 如实写"环境未验 + 替代验证方式"

## capture kit 执行规则

- 命令从 `manual.json` 的 `capture.run` / `capture.check` 取（`lab.py capture <id>` 直接打印），**在手册目录下执行**，超时按 `timeoutSeconds`（sglang 是 1800 秒）
- sglang 全量 run 起 4 个服务器约 20-25 分钟——告知用户时间预算，先 `--only small-pool` 试水
- kit 离线无密钥：不需要也不许往环境里塞任何 API key
- 产物写 `capture/out/`（run）或临时目录（check）——**不改手册自带的 out/ 录制文件**，那是基准

## 机制复述与记账

过关前用户说 2-3 句：这节的机制是什么、输入怎么走、输出在哪看。然后：

```bash
python scripts/lab.py log sglang-101 --section 3.2 --result pass --predictions 2/3
```

- `--predictions 2/3`：2 题对 3 题——命中率进毕业统计（目标 ≥70%）
- 连续两节命中率 <50% → 降速：当天不预测，回该 part 开头重读，明天再进循环

## 会话节奏

- 开场：`lab.py status` 报节次进度、最近命中率、待验证的 skip
- 中场：读 20-30 分钟 → 预测 → 实测（长 run 提前告知时长）
- 收尾：记账 + prediction-log 归档 + 预告下节
- 中断保护：进度在 `manual-progress.json`，capture run 可随时续（--only 分批）

## 时间异常处理

| 情况 | 处置 |
|---|---|
| 节太长读不完 | 按 section 切半，今天只到预测题，实测下次 |
| 预测全错 | 不是失败是发现——实测后当场修正，记进 prediction-log 的"修正"栏 |
| capture 环境跑不了 | 走 skip 三步（记原因/标注未验/录制对照），计划里排环境升级 |
| 手册版本升级（上游改 pin） | 比对新旧 pin，已过的节抽查 2 节，报告标版本迁移记录 |
