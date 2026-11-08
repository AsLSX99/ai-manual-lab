#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""手册实验室记账与查询（纯标准库，Python >= 3.9）。

用法：
  python lab.py manuals                          # 列出六本手册（钉版/状态/节数）
  python lab.py info <id>                        # pin + outcomes + 分部结构
  python lab.py capture <id>                     # 打印 run/check 命令与超时（在手册目录执行）
  python lab.py refs <id>                        # 参考区章节（flags/metrics/事故索引/术语）
  python lab.py log <id> --section 3.2 --result pass [--predictions 2/3]
  python lab.py next <id>                        # 建议下一节
  python lab.py status                           # 各手册节次进度与预测命中率

数据文件：./manual-progress.json
手册元数据源：课程仓库 manuals/<id>/manual.json
"""
import argparse
import json
import pathlib
import re
import sys
from datetime import datetime

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

DATA_FILE = pathlib.Path("manual-progress.json")


# ---------- 进度 ----------

def load():
    if DATA_FILE.exists():
        try:
            data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as e:
            sys.exit("进度文件损坏：%s（修复或删除 %s 后重试）" % (e, DATA_FILE))
        data.setdefault("manuals", {})
        data.setdefault("records", [])
        return data
    return {"manuals": {}, "records": []}


def save(data):
    DATA_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2),
                         encoding="utf-8")


# ---------- 定位与解析 ----------

def find_root():
    p = pathlib.Path.cwd().resolve()
    for _ in range(5):
        if (p / "manuals").is_dir():
            return p
        if p.parent == p:
            break
        p = p.parent
    return None


def manual_file(mid):
    root = find_root()
    if not root:
        sys.exit("未找到课程仓库的 manuals/ 目录（先 git clone）")
    f = root / "manuals" / mid / "manual.json"
    if not f.exists():
        sys.exit("找不到手册 %r（列表：python lab.py manuals）" % mid)
    return f


def read_meta(mid):
    try:
        return json.loads(manual_file(mid).read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        sys.exit("读取 manual.json 失败：%s" % e)


def all_sections(meta):
    """按 parts 顺序返回 [(part_number, section_id, title)]，section_id 如 3.2。"""
    out = []
    for part in meta.get("parts", []):
        num = part.get("number")
        for i, sec in enumerate(part.get("sections", []), 1):
            title = sec if isinstance(sec, str) else sec.get("title", str(sec))
            out.append((num, "%s.%d" % (num, i), title))
    return out


def parse_pred(text):
    m = re.match(r"^(\d+)/(\d+)$", text or "")
    if not m:
        return None
    return int(m.group(1)), int(m.group(2))


# ---------- 命令 ----------

def cmd_manuals(_args):
    root = find_root()
    if not root:
        sys.exit("未找到课程仓库的 manuals/ 目录")
    print("%-26s %-14s %-10s %-6s %s" % ("ID", "Subject", "Version", "状态", "标题"))
    print("-" * 100)
    for d in sorted((root / "manuals").iterdir()):
        mf = d / "manual.json"
        if not mf.exists():
            continue
        m = json.loads(mf.read_text(encoding="utf-8"))
        pin = m.get("pin", {})
        sections = all_sections(m)
        print("%-26s %-14s %-10s %-6s %s（%d 节）" % (
            m.get("id", d.name), str(pin.get("subject", "?"))[:14],
            str(pin.get("version", "?"))[:10], m.get("status", "?"),
            (m.get("title") or "")[:30], len(sections)))
    print("-" * 100)
    print("详情：python lab.py info <id> · 钉版引用必须带 verified 日期")


def cmd_info(args):
    m = read_meta(args.id)
    pin = m.get("pin", {})
    print("%s（edition %s · status %s）" % (
        m.get("title"), m.get("edition"), m.get("status")))
    print("subtitle：%s" % (m.get("subtitle") or ""))
    print("-" * 72)
    print("pin：subject %s · version %s" % (pin.get("subject"), pin.get("version")))
    print("     commit %s · date %s · verified %s" % (
        str(pin.get("commit", ""))[:12], pin.get("date"), pin.get("verified")))
    print("     source %s" % pin.get("source", ""))
    print("-" * 72)
    print("outcomes：")
    for i, o in enumerate(m.get("outcomes", []), 1):
        print("  %d. %s" % (i, o))
    print("-" * 72)
    print("分部结构：")
    for part in m.get("parts", []):
        secs = part.get("sections", [])
        print("  Part %s %s（%d 节）" % (
            part.get("number"), part.get("title"), len(secs)))
    ref = m.get("reference") or {}
    if ref:
        print("  参考区 %s（%d 节）" % (ref.get("title", "Reference"),
                                  len(ref.get("sections", []))))
    print("-" * 72)
    print("受众：%s" % (m.get("audience") or "")[:120])


def cmd_capture(args):
    m = read_meta(args.id)
    cap = m.get("capture") or {}
    root = find_root()
    workdir = root / "manuals" / args.id
    pin = m.get("pin", {})
    print("手册目录（在它下面执行）：%s" % workdir)
    print("pin：%s %s · verified %s" % (
        pin.get("subject"), pin.get("version"), pin.get("verified")))
    run = cap.get("run")
    check = cap.get("check")
    if run:
        print("录制：%s" % " ".join(run))
    if check:
        print("校验：%s（超时 %ss）" % (
            " ".join(check), cap.get("timeoutSeconds", 300)))
    if not run and not check:
        print("该手册 manual.json 无 capture 字段 → 看 manuals/%s/capture/README.md"
              % args.id)
    print("规则：离线无密钥；不改 capture/out/ 录制文件；skip 不算验证通过。")
    print("环境要求见 references/manual-map.md。")


def cmd_refs(args):
    m = read_meta(args.id)
    ref = m.get("reference") or {}
    secs = ref.get("sections", [])
    if not secs:
        sys.exit("该手册没有参考区")
    print("%s 参考区（%s）：" % (args.id, ref.get("title", "")))
    for i, sec in enumerate(secs, 1):
        title = sec if isinstance(sec, str) else sec.get("title", str(sec))
        print("  R.%d  %s" % (i, title))
    print("运维值班时按需查，不必顺序读。")


def cmd_log(args):
    if args.result not in ("pass", "fail"):
        sys.exit("--result 只能是 pass / fail")
    pred = parse_pred(args.predictions) if args.predictions else None
    if args.predictions and pred is None:
        sys.exit("--predictions 格式 n/m，如 2/3")
    data = load()
    mid = args.id
    entry = data["manuals"].setdefault(mid, {
        "sections": {}, "pred_correct": 0, "pred_total": 0,
        "capture_check": None, "started": datetime.now().isoformat(timespec="seconds"),
    })
    rec = {
        "ts": datetime.now().isoformat(timespec="seconds"),
        "id": mid,
        "section": args.section,
        "result": args.result,
        "predictions": args.predictions or "",
        "note": args.note or "",
    }
    data["records"].append(rec)
    entry["sections"][args.section] = args.result
    if pred:
        entry["pred_correct"] += pred[0]
        entry["pred_total"] += pred[1]
    if args.capture == "passed":
        entry["capture_check"] = "passed"
    elif args.capture == "skipped":
        entry["capture_check"] = entry.get("capture_check") or "skipped"

    done = sum(1 for v in entry["sections"].values() if v == "pass")
    line = "%s 节 %s → %s（已过 %d 节）" % (mid, args.section, args.result, done)
    if pred:
        line += " · 预测 %s（累计 %d/%d）" % (
            args.predictions, entry["pred_correct"], entry["pred_total"])
    if args.capture:
        line += " · capture %s" % args.capture
    print(line)
    if entry["pred_total"] >= 6:
        rate = entry["pred_correct"] / entry["pred_total"]
        if rate < 0.5:
            print("注意：累计命中率 %.0f%% < 50%% → 按协议降速回读" % (rate * 100))
    save(data)


def cmd_next(args):
    data = load()
    m = read_meta(args.id)
    entry = data["manuals"].get(args.id, {})
    passed = {k for k, v in entry.get("sections", {}).items() if v == "pass"}
    sections = all_sections(m)
    for _, sid, title in sections:
        if sid not in passed:
            print("%s 下一节：%s %s" % (args.id, sid, title))
            rate_note = ""
            if entry.get("pred_total"):
                rate = entry["pred_correct"] / entry["pred_total"]
                rate_note = " · 累计预测命中 %d/%d（%.0f%%）" % (
                    entry["pred_correct"], entry["pred_total"], rate * 100)
            print("进度：%d/%d 节%s" % (len(passed), len(sections), rate_note))
            return
    print("%s 全部节已过 → 检查毕业标准，出 mastery-report（预测命中率目标 ≥70%%）。"
          % args.id)


def cmd_status(_args):
    data = load()
    manuals, records = data["manuals"], data["records"]
    if not manuals:
        print("没有实验记录。先：python lab.py manuals")
        return
    print("记录 %d 条 · 手册 %d 本" % (len(records), len(manuals)))
    print("-" * 66)
    for mid in sorted(manuals):
        e = manuals[mid]
        try:
            m = read_meta(mid)
            total = len(all_sections(m))
        except SystemExit:
            total = "?"
        done = sum(1 for v in e["sections"].values() if v == "pass")
        line = "%-24s 节 %s/%s" % (mid[:24], done, total)
        if e.get("pred_total"):
            line += " · 预测 %d/%d（%.0f%%）" % (
                e["pred_correct"], e["pred_total"],
                100.0 * e["pred_correct"] / e["pred_total"])
        if e.get("capture_check"):
            line += " · capture %s" % e["capture_check"]
        fails = [k for k, v in e["sections"].items() if v == "fail"]
        if fails:
            line += " · fail:%s" % ",".join(fails)
        print(line)
    if records:
        print("-" * 66)
        last = records[-1]
        print("最近：%s · %s · 节 %s · %s" % (
            last["ts"][:16], last["id"], last["section"], last["result"]))


def main():
    ap = argparse.ArgumentParser(description="手册实验室记账与查询")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("manuals", help="列出手册")
    p.set_defaults(func=cmd_manuals)

    p = sub.add_parser("info", help="手册详情")
    p.add_argument("id")
    p.set_defaults(func=cmd_info)

    p = sub.add_parser("capture", help="打印 capture 命令")
    p.add_argument("id")
    p.set_defaults(func=cmd_capture)

    p = sub.add_parser("refs", help="参考区章节")
    p.add_argument("id")
    p.set_defaults(func=cmd_refs)

    p = sub.add_parser("log", help="记录节结果")
    p.add_argument("id")
    p.add_argument("--section", required=True)
    p.add_argument("--result", required=True, choices=["pass", "fail"])
    p.add_argument("--predictions", default="", help="n/m，如 2/3")
    p.add_argument("--capture", choices=["passed", "skipped", "recorded"],
                   default=None)
    p.add_argument("--note", default="")
    p.set_defaults(func=cmd_log)

    p = sub.add_parser("next", help="建议下一节")
    p.add_argument("id")
    p.set_defaults(func=cmd_next)

    p = sub.add_parser("status", help="总览")
    p.set_defaults(func=cmd_status)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
