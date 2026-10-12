#!/usr/bin/env python3
import json,subprocess,shlex,re,os
from pathlib import Path
r=Path(__file__).resolve().parents[1];samples=json.loads((r/'samples.json').read_text());serial=json.loads((r/'sdb-target.json').read_text())['serial'];identities=[]
env=os.environ.copy();env.update(HOME=str(r/'local-runtime'),TMPDIR=str(r/'local-runtime/tmp'))
with (r/'sample-resolution-batched.txt').open('w') as log:
 for s in samples:
  command='readlink -f '+shlex.quote(s['path'])+'; stat -Lc '+shlex.quote('device=%d inode=%i bytes=%s mode=%a type=%F')+' '+shlex.quote(s['path'])
  log.write('SAMPLE '+s['id']+' '+s['path']+'\nCOMMAND: '+command+'\n');log.flush()
  p=subprocess.run(['sdb','-s',serial,'shell',command],env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=15)
  log.write(p.stdout+'\nEXIT_CODE: '+str(p.returncode)+'\n');log.flush();assert p.returncode==0,p.stdout
  lines=p.stdout.splitlines();resolved=next(l for l in lines if l.startswith('/') and ' ' not in l)
  stat=next(l for l in lines if re.fullmatch(r'device=\d+ inode=\d+ bytes=\d+ mode=\d+ type=regular file',l))
  s['resolved_path']=resolved;s['file_stat']=stat;identities.append(re.search(r'device=\d+ inode=\d+',stat)[0])
assert len(set(identities))==28
(r/'samples.json').write_text(json.dumps(samples,ensure_ascii=False,indent=2)+'\n')
lines=['代表性定向样本：28份（12系统可执行、16平台共享库）；非随机全平台抽样。','同一device+inode不重复计数，原路径均在/usr/bin或/usr/lib。','id\t路径\t类别\t选择理由\t真实路径']+['\t'.join([s['id'],s['path'],s['kind'],s['reason'],s['resolved_path']]) for s in samples]
(r/'sample-list.txt').write_text('\n'.join(lines)+'\n')
print('28 paths resolved; no duplicate device/inode')
