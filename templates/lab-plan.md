# 实验计划（lab-plan.md）

> 选手册模式产出。与 `manual-progress.json`（机器记账）互为表里。

---

## 手册与钉版

- **手册 id**：[如 sglang-101] · **标题**：[title]（edition [YYYY.MM]）
- **pin**：subject [X] · version [Y] · commit [Z 前 12 位] · verified [YYYY-MM-DD]（源：`manual.json`）
- **我的环境版本**：[与 pin 一致 / 差异：……]（差异已声明）
- **学它干什么**：[部署运维 / 面试深挖 / 排障 / 兴趣]
- **每天**：[X] 节（每节约 45-60 分钟含实测）
- **建档日期**：[YYYY-MM-DD]

## capture 环境检查（建档时跑一次）

| 检查项 | 结果 |
|---|---|
| 手册 requirements（如 Apple silicon + 指定版本） | [满足 / 缺：……] |
| `capture/run.py --check` 试跑 | [通过 / skipped：原因 / 未跑] |
| 替代验证方式（skip 时） | [用 capture/out/ 录制 listing 对照] |

## 分部与节次表（从 `lab.py info` 抄）

| Part | 标题 | 节 | 计划 | 实际 |
|---|---|---|---|---|
| 1 | | | [日期] | |
| … | | | | |

## 毕业标准（写死）

1. [ ] 必读节全部 pass（reference 节按需）
2. [ ] 累计预测命中率 ≥70%（`lab.py status` 查）
3. [ ] capture `--check` 成功一次（或 skip 如实注明 + 录制对照完成）
4. [ ] mastery-report 出稿：outcomes 自评 + 预测三例（面试素材）

## 规则（写死）

1. 先预测后验证，没预测的节不算过
2. 实测与手册对不上 → 先查 pin 版本
3. skip 不算验证通过，报告标"环境未验"
4. 每个数字标来源（capture/out/<file> 或 pin）
5. 连续两节命中率 <50% → 降速回读
6. 一次会话一节

## 当前状态

- **进行中**：[Part X · 节 Y]
- **预测命中率**：[累计 __/__]
- **待办 skip**：[原因与升级路径]

## 变更记录

| 日期 | 变更 | 原因 |
|---|---|---|
| [建档日] | 选定 [手册]，pin [verified 日期] | 选手册 |
