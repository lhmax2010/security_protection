#!/usr/bin/env python3
from pathlib import Path
import json
import shlex
import subprocess
import time

base=Path('docs/probe/protection-demo/cost')
records=[]
def call(args,timeout=30):
    start=time.monotonic()
    try:
        p=subprocess.run(args,capture_output=True,text=True,timeout=timeout)
        r={'command':shlex.join(args),'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
    except subprocess.TimeoutExpired as e:
        r={'command':shlex.join(args),'exit':124,'stdout':(e.stdout or b'').decode() if isinstance(e.stdout,bytes) else e.stdout or '', 'stderr':(e.stderr or b'').decode() if isinstance(e.stderr,bytes) else e.stderr or '', 'error':'subprocess.TimeoutExpired: '+str(e)}
    r['elapsed_seconds']=time.monotonic()-start;records.append(r)
    (base/'board-connect.json').write_text(json.dumps(records,indent=2)+'\n')
    (base/'board-connect.txt').write_text('\n'.join('$ '+r['command']+'\n'+r['stdout']+r['stderr']+'\n'+r.get('error','')+f'\nexit={r["exit"]}\n' for r in records))
    return r

connected=False
for target in ['192.168.108.26','192.168.108.26:26101']:
    r=call(['sdb','connect',target])
    text=(r['stdout']+r['stderr']).lower()
    if r['exit']==0 and ('connected to' in text or 'already connected' in text):connected=True;break
if not connected:
    print((base/'board-connect.txt').read_text())
    raise SystemExit('BOARD_CONNECTION_FAILED; stop experiment as requested')
devices=call(['sdb','devices'])
rows=[line.split() for line in devices['stdout'].splitlines()]
serial=next((row[0] for row in rows if len(row)>=2 and '192.168.108.26' in row[0] and row[1]=='device'),None)
assert serial,devices
root=call(['sdb','-s',serial,'root','on'])
assert root['exit']==0,root
script='id; uname -a; cat /etc/tizen-release; cat /proc/version; tr "\\000" "\\n" < /proc/device-tree/model; cat /proc/cpuinfo | head -n 18; df -k /opt; cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor; command -v date; date +%s.%N; command -v sha256sum; command -v timeout'
identity=call(['sdb','-s',serial,'shell','sh -c '+shlex.quote(script)])
(base/'board-identity.txt').write_text('$ '+identity['command']+'\n'+identity['stdout']+identity['stderr']+f'\nexit={identity["exit"]}\n')
assert identity['exit']==0 and 'Raspberry Pi 4 Model B' in identity['stdout'] and 'armv7l' in identity['stdout'] and 'uid=0' in identity['stdout'],identity
(base/'board-target.json').write_text(json.dumps({'serial':serial,'verified_open_board':'Raspberry Pi 4 Model B','architecture':'armv7l','target_directory':'/opt/protection-cost-20261013'},indent=2)+'\n')
print('Verified root connection:',serial,'Raspberry Pi4 / ARMv7 / Tizen; see board-identity.txt.')
