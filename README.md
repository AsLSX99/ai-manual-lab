# ai-manual-lab

> 开源**系统手册实验室**（SKILL）——驱动 [AI Engineering from Scratch](https://github.com/rohitg00/ai-engineering-from-scratch) 的 `manuals/` 六本版本钉死的系统手册：**SGLang 0.5.22、vLLM 0.31.0、A2A 1.0.1、Docker 沙箱、MILES、逆向工程（rea-agents + Ghidra）**。按"读一节 → 合书预测 → 跑离线 capture kit 实测 → 验证"循环，把一个系统学到**能预测手册没展示过的情况**。

手册的标准（原仓库原话）：*"A manual stays with one system until a reader can predict what it will do in a case the manual never showed."*——这个 Skill 就是把这句话变成可执行的训练协议。

## 六件套定位

| Skill | 管什么 | 交付物 |
|---|---|---|
| 学习型（上课） | 输入：理解 | 考核通过的课时 |
| 特训型（练题） | 输出：手搓代码 | 毕业的练习题 |
| 面试型（被考） | 检验：定级 | 模拟面试报告 |
| 作品集型（做项目） | 产出：真东西 | 过完成测试的项目 |
| 认证型（备考） | 拿凭证：考试 | 模考趋势 + 考前一页纸 |
| **本 Skill（吃系统）** | **深度：运维直觉** | **精通报告 + 预测战报** |

手册 `related` 链的课交给学习型；毕业报告的"预测三例"是面试型 debugging/system-design 轮的硬素材（"我压测过 SGLang 的 KV 池"）。六件独立安装，互不依赖。

## 仓库结构

```
ai-manual-lab/
├── SKILL.md                        # 主文档：选手册 + 每节四步循环 + 6 条铁律
├── README.md
├── LICENSE
├── references/
│   ├── manual-map.md               # 六本手册钉版/受众/结构/环境要求/按目标选书
│   └── lab-protocol.md             # 出题原则、capture 三种验证方式、skip 处理
├── templates/
│   ├── lab-plan.md                 # 实验计划（pin/环境检查/节次表/毕业标准）
│   ├── prediction-log.md           # 每节预测记录（预测/理由/实测/修正）
│   └── mastery-report.md           # 精通报告（outcomes 自评 + 预测三例）
└── scripts/
    └── lab.py                      # manuals/info/capture/refs/log/next/status（零依赖）
```

## 手册长什么样

每本一个目录（`manuals/<id>/`），四条硬规则：

1. **一个主题、一个版本、一个日期**——`manual.json` 的 `pin` 钉死 subject/version/commit/release date/**verified 日期**
2. **每条 listing 来自真实运行**——`capture/` 采集套件**离线跑、不要网络不要密钥**，正文里的记录是从 `capture/out/` 剪出来的，不凭记忆写
3. **每个论断可溯源**——分级来源表，每节结尾列它依据的文件
4. **颜色与箭头语法全书统一**——图例在 front matter 教一次

以 sglang-101 为例：七部 27 节（Start → 请求路径 → KV Cache → 每次前向 → 测量 → 集群 → 生产）+ 参考区（flags / metrics / 事故索引 / 术语 / 来源）。

## 核心机制：四步循环（每节 45-60 分钟）

1. **读**——带着该节 outcomes 读正文和 listing，数字让用户自己读出来
2. **合书预测**（灵魂）——你出 2-3 道**变体场景题**：改一个 flag/输入/负载，问系统会怎样；至少 1 题是手册完全没展示过的；用户**先说推理链再给结论**，猜对说不出理由按错记
3. **实测验证**——`capture/run.py --check` 比对不随时间变的事实（生成文本/token 数/缓存区间/压测总量）；环境不满足 → `skipped` 如实记，**不算通过**，改用录制 listing 对照并在报告标"环境未验"
4. **复述记账**——机制 2-3 句 + `lab.py log --section 3.2 --predictions 2/3`

**毕业四标准**：必读节全 pass / 预测命中率 ≥70% / capture check 至少成功一次（或 skip 如实注明）/ 精通报告出稿（outcomes 逐条自评 + **三个"手册没展示的场景"预测实例**——面试素材）。

## 如何使用

**① 作为 Agent 技能安装**：本目录克隆/复制到你的 AI Agent 识别技能的目录，目录名保持 `ai-manual-lab`，`SKILL.md` 直接位于其内；课程仓库克隆到任意位置（脚本自动向上找）。

**② 直接当开场指令**：`SKILL.md` 全文发给 Agent，再说"带我吃透 SGLang"。

**③ 只用查询脚本**：
```bash
python scripts/lab.py manuals                 # 六本手册钉版一览
python scripts/lab.py info sglang-101         # pin + outcomes + 分部
python scripts/lab.py capture sglang-101      # run/check 命令（去手册目录执行）
python scripts/lab.py refs sglang-101         # 参考区（flags/metrics/事故索引）
python scripts/lab.py log sglang-101 --section 3.2 --result pass --predictions 2/3 --capture passed
python scripts/lab.py next sglang-101
python scripts/lab.py status
```

## 环境准备

| 依赖 | 用途 | 获取方式 |
|---|---|---|
| **AI Agent**（Claude Code / Codex / 其他支持 SKILL.md 的宿主） | 执行实验室协议 | 你现有的工具链 |
| **课程仓库** | 手册、capture kit、录制 listing | `git clone --depth 1 https://github.com/rohitg00/ai-engineering-from-scratch.git` |
| **手册对应 runtime**（按所选手册） | 跑 capture 实测 | 见 `references/manual-map.md`（如 sglang 需 Apple silicon + SGLang 0.5.22） |
| **Python ≥ 3.9** | 跑记账脚本 | 无第三方依赖 |

没有对应环境也能学：capture kit 的 `--check` 会打印 `skipped` + 原因退出 0，用手册自带 `capture/out/` 录制 listing 完成对照，报告如实标"环境未验"，环境升级路径写进计划。

## 快速开始

1. 克隆课程仓库（任意位置）
2. 安装本 Skill（或把 `SKILL.md` 发给你的 Agent）
3. 说 **"带我吃透 [系统]"** → `manuals` 选书 + 钉版声明 + capture 环境检查 → 拿到 `lab-plan.md`
4. 每天一节：读 → 合书预测 → 实测 → 记账
5. 毕业：`mastery-report.md`（outcomes 自评 + 预测三例）

## 设计原则

1. **预测先行**——读完就过是幻觉，能预测变体才算懂
2. **版本先查**——实测对不上，第一反应查 pin，这是运维肌肉记忆
3. **skip 如实**——环境未验就标未验，录制对照是替代不是冒充
4. **数字有来源**——每个数标 `capture/out/<file>` 或 pin verified 日期
5. **离线无密钥**——capture kit 设计如此，实验室不碰任何 key
6. **状态落盘**——进度双文件，换会话能接

## 常见问题

**Q：和课程仓库自带的 skills 什么关系？**
互补。本 Skill 是独立实现的实验室协议与记账工具，不依赖其内部状态格式，可单独用、可裁剪。

**Q：手册和 capture kit 会更新吗？**
会——本仓库不复制任何手册，以课程仓库 `manuals/` 为准，上游 `git pull` 即同步；`manual-map.md` 是速查索引，权威以 `manual.json` 的 `pin` 为准。上游改 pin 时按协议做版本迁移抽查。

**Q：没有 Apple silicon 怎么学 sglang-101？**
正常走读与预测，capture 记 skip，用 `capture/out/` 录制 listing 对照完成验证并标"环境未验"；想补实测就按 lab-plan 的升级路径排期（换机/借 CI）。

**Q：预测题是谁出？**
你出——Agent 按 `lab-protocol.md` 的出题原则出变体场景题，改参数不改机制、答案可验证、至少一题手册没展示过。

**Q：进度文件要提交 git 吗？**
建议提交（复盘资产）；想私有加进 `.gitignore`。

## 致谢

- 六本手册、capture kit、录制 listing 与全部课件：[rohitg00/ai-engineering-from-scratch](https://github.com/rohitg00/ai-engineering-from-scratch)（MIT）
- 本仓库只提供实验室协议与记账工具，手册内容版权归原作者所有

## License

[MIT](./LICENSE)
