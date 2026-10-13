#!/usr/bin/env python3
import subprocess,sys,json,hashlib
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
 if data.startswith(b'\x7fELF'):
  if not name.startswith('docs/probe/ffmpeg-demo/upstream-artifacts/'):raise SystemExit('Non-upstream ELF staged: '+name)
  manifest=json.loads(Path('docs/probe/ffmpeg-demo/upstream-artifacts/manifest.json').read_text())
  digest=hashlib.sha256(data).hexdigest()
  if manifest.get(p.name,{}).get('sha256')!=digest:raise SystemExit('Upstream provenance hash mismatch: '+name)
  board_digest=hashlib.sha256(Path('docs/probe/ffmpeg-demo/private/board-libavcodec.so').read_bytes()).hexdigest()
  if digest==board_digest:raise SystemExit('Board binary upload blocked')
subprocess.run(['git','diff','--cached','--stat'],check=True)
subprocess.run(['git','commit','-m',message],check=True)
subprocess.run(['git','push'],check=True)
