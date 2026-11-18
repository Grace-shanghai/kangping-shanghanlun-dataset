import subprocess,re
out=subprocess.run([r"C:\Users\Admin\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\python\python.exe","verify.py","all"],capture_output=True,text=True,encoding="utf-8")
t=out.stdout
print("异常页",len(re.findall(r"✗ 问题",t)),"｜跳号",len(re.findall(r"列号跳号",t)),"｜无顶格",len(re.findall(r"无起笔差 0",t)),"｜越界",len(re.findall(r"起笔差=\S+（应为",t)))
print(t.strip().split("\n")[-1])
