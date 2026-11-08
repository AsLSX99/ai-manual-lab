# 预测记录（prediction-log.md）

> 每节一节（重要场次必写：手册没展示过的场景、预测错的、skip 的）。这是 mastery-report"预测三例"的原料库。

---

## [YYYY-MM-DD] · [手册 id] · 节 [X.Y · 标题] · 预测 [对 n / 共 m]

**验证方式**：[capture --check 通过 / --only <case> / 录制 listing 对照（环境未验）]

### 预测 1（手册展示过的变体）

- **场景**：[改了什么参数/输入/负载]
- **我的预测 + 理由**：[先推理链后结论]
- **实测**：[listing 指认 / check 事实]
- **判定**：[✓ / ✗ → 修正认知：……]

### 预测 2（手册没展示过的场景 ★）

- **场景**：
- **我的预测 + 理由**：
- **实测**：
- **判定**：[✓ / ✗ → 修正：]

### 机制复述（过关前 2-3 句）

[这节机制：输入怎么走、在哪变换、输出哪看]

### 来源标注

- 数字来自：[capture/out/<file> · pin verified <日期>]

### 记账

```
python scripts/lab.py log <id> --section X.Y --result pass --predictions n/m
```

---
