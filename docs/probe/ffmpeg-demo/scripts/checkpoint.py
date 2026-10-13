#!/usr/bin/env python3
import subprocess,sys
from pathlib import Path
message,*paths=sys.argv[1:]
for path in paths:
 p=Path(path)
 if not (str(p).startswith('docs/probe/ffmpeg-demo/') or str(p)=='docs/probe/STATE.md'): raise SystemExit('Path outside task: '+path)
subprocess.run(['git','add','--',*paths],check=True)
files=subprocess.check_output(['git','diff','--cached','--name-only','--diff-filter=ACMR']).decode().splitlines()
for name in files:
 p=Path(name)
 if '/private/' in name or '/local-runtime/' in name: raise SystemExit('Private file staged: '+name)
 if not (name.startswith('docs/probe/ffmpeg-demo/') or name=='docs/probe/STATE.md'):raise SystemExit('Unrelated staged file: '+name)
 data=p.read_bytes()
 if data.startswith(b'\x7fELF') and not name.startswith('docs/probe/ffmpeg-demo/upstream-artifacts/'):raise SystemExit('Non-upstream ELF staged: '+name)
subprocess.run(['git','diff','--cached','--stat'],check=True)
subprocess.run(['git','commit','-m',message],check=True)
subprocess.run(['git','push'],check=True)
