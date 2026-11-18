import io
p="verify.py"; s=io.open(p,encoding="utf-8").read()
s=s.replace('if x["lv"] not in (0, 1, 2, None):','if x["lv"] not in (0, 1, 2, 3, None):')
s=s.replace('issues.append("列%s 起笔差=%s（应为 0/1/2）" % (x["col"], x["lv"]))','issues.append("列%s 起笔差=%s（应为 0/1/2/3 或空）" % (x["col"], x["lv"]))')
s=s.replace('if rows and all(x["lv"] not in (0,) for x in rows):','if rows and all(x["lv"] not in (0,) for x in rows) and not any(x["lv"]==3 for x in rows):')
s=s.replace('    1 起笔差是否在 0/1/2 之内','    1 起笔差是否在 0/1/2/3 之内（3＝篇题层；空＝未量）')
io.open(p,"w",encoding="utf-8").write(s); print("规则已更新")
