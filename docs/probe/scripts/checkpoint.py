#!/usr/bin/env python3
from pathlib import Path
import subprocess,sys
message,note,*paths=sys.argv[1:]
p=Path('docs/probe/STATE.md')
s=p.read_text()
if '## 子步骤提交日志' not in s:s+='\n## 子步骤提交日志\n'
s+='\n- '+note+'\n';p.write_text(s)
subprocess.run(['git','add','docs/probe/STATE.md',*paths],check=True)
subprocess.run(['git','commit','-m',message],check=True)
subprocess.run(['git','push'],check=True)
