#!/usr/bin/env python3
from pathlib import Path
import subprocess,os,json,time
root=Path(__file__).resolve().parents[1];log=root/'sdb-connect.txt'
if log.exists():raise SystemExit('Do not overwrite prior SDB evidence')
env=os.environ.copy();env.update(HOME=str(root/'local-runtime'),TMPDIR=str(root/'local-runtime/tmp'))
records=[]
with log.open('w') as f:
 for target in ['192.168.108.26','192.168.108.26:26101']:
  cmd=['sdb','connect',target];f.write('COMMAND: '+' '.join(cmd)+'\n');f.flush();t=time.monotonic()
  try:
   p=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,env=env,text=True,timeout=25);code=p.returncode;output=p.stdout
  except subprocess.TimeoutExpired as e:
   code=124;output=(e.stdout or b'').decode() if isinstance(e.stdout,bytes) else e.stdout or '';output+='\nLOCAL_TIMEOUT: SDB command did not finish in 25 seconds\n'
  f.write(output+f'\nEXIT_CODE: {code}\n');f.flush();records.append({'argv':cmd,'exit_code':code,'elapsed_seconds':round(time.monotonic()-t,3)})
  cmd=['sdb','devices'];f.write('\nCOMMAND: sdb devices\n');f.flush()
  try:p=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,env=env,text=True,timeout=15);devices=p.stdout;devcode=p.returncode
  except subprocess.TimeoutExpired as e:devices='LOCAL_TIMEOUT: sdb devices exceeded 15 seconds\n';devcode=124
  f.write(devices+f'\nEXIT_CODE: {devcode}\n');f.flush();records.append({'argv':cmd,'exit_code':devcode})
  serial=next((l.split()[0] for l in devices.splitlines() if len(l.split())>=2 and l.split()[0].startswith('192.168.108.26:') and l.split()[1] in ['device','online']),None)
  if serial:
   (root/'sdb-target.json').write_text(json.dumps({'serial':serial,'port':int(serial.rsplit(':',1)[1]),'connection_argument':target},indent=2)+'\n');break
 else:serial=None
(root/'sdb-connect.txt.meta.json').write_text(json.dumps({'attempts':records,'online_serial':serial},indent=2)+'\n')
print(log.read_text());raise SystemExit(0 if serial else 1)
