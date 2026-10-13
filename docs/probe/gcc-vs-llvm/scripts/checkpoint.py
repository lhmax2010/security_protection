#!/usr/bin/env python3
from pathlib import Path
import subprocess,sys,re
message,*paths=sys.argv[1:]
root='docs/probe/gcc-vs-llvm/'
for name in paths:assert name.startswith(root) or name=='docs/probe/STATE.md',name
subprocess.run(['git','add','--',*paths],check=True)
files=subprocess.check_output(['git','diff','--cached','--name-only','--diff-filter=ACMR']).decode().splitlines()
for name in files:
 assert name.startswith(root) or name=='docs/probe/STATE.md',name
 p=Path(name);data=p.read_bytes()
 assert '/private/' not in name and '/local-runtime/' not in name,name
 assert p.suffix not in ['.rpm','.so','.cpio'] and not data.startswith((b'\x7fELF',b'\xed\xab\xee\xdb')),name
 assert b'\x00' not in data,name
 if name.startswith(root+'raw/'):
  text=data.decode();assert not re.search(r'^\s*\d+:\s+[0-9a-f]+\s+\d+\s+(?:FUNC|OBJECT|IFUNC|NOTYPE)',text,re.M), 'Full dynsym listing forbidden: '+name
  assert not re.search(r'^(DYNAMIC_SYMBOL|EXPORT)\t',text,re.M), 'Full Lua symbol listing forbidden: '+name
subprocess.run(['git','diff','--cached','--stat'],check=True)
subprocess.run(['git','commit','-m',message],check=True)
subprocess.run(['git','push'],check=True)
