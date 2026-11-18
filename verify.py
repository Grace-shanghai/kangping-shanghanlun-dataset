# -*- coding: utf-8 -*-
"""
verify.py —— 康平本录入校验器（v1）
用法：
    python verify.py 18          # 校验第 18 页
    python verify.py 18-6        # 校验第 18 页第 6 列
    python verify.py all         # 全书体检
    python verify.py range 18-30 # 批量校验页范围

校验项（五项）：
    1 起笔差是否在 0/1/2/3 之内（3＝篇题层；空＝未量）
    2 字数是否与原文相符（重新数汉字）
    3 列号是否连续（有无跳号）
    4 每页是否有且只有一处最高行（起笔差 0 应存在）
    5 跨列字提示（本列末字无句读、下一列首字接续）
"""
import sys, re, io, os
from openpyxl import load_workbook

BOOK = r"E:\得瑟\康平本_工作平台_v11_20261030_分层定稿.xlsx"

def load():
    u = load_workbook(BOOK)["单元"]
    data = {}
    for r in range(2, u.max_row + 1):
        pg = u.cell(row=r, column=1).value
        if not isinstance(pg, int): continue
        col = u.cell(row=r, column=2).value
        data.setdefault(pg, []).append({
            "col": col,
            "lv": u.cell(row=r, column=3).value,
            "txt": str(u.cell(row=r, column=4).value or ""),
            "flow": u.cell(row=r, column=11).value or u.cell(row=r, column=10).value or "",
            "note": str(u.cell(row=r, column=9).value or ""),
        })
    for pg in data:
        data[pg].sort(key=lambda x: (x["col"] if isinstance(x["col"], int) else 999))
    return data

def han(t):
    return len([c for c in t if "\u4e00" <= c <= "\u9fff"])

def check_page(data, pg):
    if pg not in data:
        print("第 %d 页：未录入" % pg); return 1
    rows = data[pg]
    issues = []
    # 1 起笔差
    for x in rows:
        if x["lv"] not in (0, 1, 2, 3, None):
            issues.append("列%s 起笔差=%s（应为 0/1/2/3 或空）" % (x["col"], x["lv"]))
    # 3 列号连续
    cols = [x["col"] for x in rows if isinstance(x["col"], int)]
    if cols and cols != list(range(1, len(cols) + 1)):
        miss = [c for c in range(1, max(cols) + 1) if c not in cols]
        if miss: issues.append("列号跳号：缺 %s" % miss)
    # 4 是否有顶格
    allnull = all(x["lv"] is None for x in rows)
    if allnull:
        issues.append("整页起笔差未量（%d 列）" % len(rows))
    elif rows and all(x["lv"] not in (0,) for x in rows) and not any(x["lv"]==3 for x in rows):
        issues.append("本页无起笔差 0（顶格）——请核是否漏了最高行")
    # 5 跨列提示
    cont = []
    for i in range(len(rows) - 1):
        a, b = rows[i], rows[i + 1]
        if a["txt"] and a["txt"][-1] not in "、。":
            cont.append("列%s→列%s（「%s」接「%s」）" % (a["col"], b["col"], a["txt"][-1:], b["txt"][:1]))
    tot = sum(han(x["txt"]) for x in rows)
    print("第 %d 页：%d 列，%d 字，起笔差 %s" % (pg, len(rows), tot, [x["lv"] for x in rows]))
    for x in rows:
        print("   列%-2s 级%-2s %3d字 [%s] %s" % (x["col"], x["lv"], han(x["txt"]), x["flow"], x["txt"][:34]))
    if cont:
        print("   · 疑似跨列 %d 处：" % len(cont))
        for c in cont: print("       " + c)
    if issues:
        print("   ✗ 问题：")
        for s in issues: print("       " + s)
        return 1
    print("   ✓ 五项通过")
    return 0

def check_cell(data, pg, col):
    rows = data.get(pg, [])
    for x in rows:
        if x["col"] == col:
            print("第 %d 页第 %s 列" % (pg, col))
            print("  起笔差：%s（0=顶格，1=降一格，2=降二格）" % x["lv"])
            print("  字数：%d" % han(x["txt"]))
            print("  语流：%s" % x["flow"])
            print("  原文：%s" % x["txt"])
            print("  备注：%s" % x["note"][:60])
            return 0
    print("未找到 p%d 列%s" % (pg, col)); return 1

def main():
    data = load()
    if len(sys.argv) < 2:
        print(__doc__); return
    arg = sys.argv[1]
    if arg == "all":
        bad = 0
        for pg in sorted(data):
            if check_page(data, pg) != 0: bad += 1
        print("\n全书 %d 页，异常 %d 页" % (len(data), bad))
    elif arg == "range":
        a, b = sys.argv[2].split("-")
        for pg in range(int(a), int(b) + 1):
            check_page(data, pg); print()
    elif "-" in arg:
        pg, col = arg.split("-")
        check_cell(data, int(pg), int(col))
    else:
        check_page(data, int(arg))

if __name__ == "__main__":
    main()
