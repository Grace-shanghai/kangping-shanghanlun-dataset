import subprocess,re
out=subprocess.run([r"C:\Users\Admin\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\python\python.exe","verify.py","all"],capture_output=True,text=True,encoding="utf-8")
t=out.stdout
print("异常页",len(re.findall(r"✗ 问题",t)),"｜整页未量",len(re.findall(r"整页起笔差未量",t)),"｜无顶格",len(re.findall(r"无起笔差 0",t)),"｜越界",len(re.findall(r"起笔差=\S+（应为",t)))
for m in re.finditer(r"第 (\d+) 页：.*?\n(?:.*?\n)*?   ✗ 问题：\n(.*?)(?=\n第 |\Z)",t):
    if "整页" in m.group(2): print("  整页未量：p"+m.group(1))
