import subprocess,sys,re,io
out=subprocess.run([r"C:\Users\Admin\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\python\python.exe","verify.py","all"],capture_output=True,text=True,encoding="utf-8")
t=out.stdout
pages=re.findall(r"第 (\d+) 页：(\d+) 列，(\d+) 字",t)
bad=len(re.findall(r"✗ 问题",t))
skip=len(re.findall(r"未录入",t))
jump=len(re.findall(r"列号跳号",t))
notop=len(re.findall(r"无起笔差 0",t))
lv=len(re.findall(r"起笔差=\S+（应为",t))
print("体检：页",len(pages),"｜异常页",bad,"｜跳号",jump,"｜无顶格",notop,"｜级越界",lv)
print(t.strip().split("\n")[-1])
