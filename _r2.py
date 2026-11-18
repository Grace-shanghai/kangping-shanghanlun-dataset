import io
p="verify.py"; s=io.open(p,encoding="utf-8").read()
s=s.replace('if rows and all(x["lv"] not in (0,) for x in rows) and not any(x["lv"]==3 for x in rows):',
'''allnull = all(x["lv"] is None for x in rows)
    if allnull:
        issues.append("整页起笔差未量（%d 列）" % len(rows))
    elif rows and all(x["lv"] not in (0,) for x in rows) and not any(x["lv"]==3 for x in rows):''')
io.open(p,"w",encoding="utf-8").write(s); print("规则已改：级全空→报“整页未量”，不再报无顶格")
