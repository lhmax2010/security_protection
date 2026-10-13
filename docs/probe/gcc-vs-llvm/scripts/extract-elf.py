#!/usr/bin/env python3
"""Read RPM cpio payload; materialize only selected regular ELF, never links."""
import json,os,subprocess,re,hashlib
from pathlib import Path
r=Path(__file__).resolve().parents[1];private=r/'private';rows=[];logs=[]
env=os.environ.copy();env.update(HOME=str(r/'local-runtime'),TMPDIR=str(r/'local-runtime/tmp'))
for package in json.loads((private/'packages.json').read_text()):
 if package['curl_exit']!=0:continue
 archive=private/'download'/package['filename'];cpio=private/'extract'/(package['package']+'.cpio')
 with cpio.open('wb') as f:
  q=subprocess.run(['rpm2cpio',str(archive)],stdout=f,stderr=subprocess.PIPE,env=env)
 logs.append({'package':package['filename'],'rpm2cpio_exit':q.returncode,'stderr':q.stderr.decode()})
 if q.returncode:continue
 data=cpio.read_bytes();pos=0;entries=[];hardlinks={}
 while pos<len(data):
  head=data[pos:pos+110];assert head[:6] in [b'070701',b'070702'],(package['filename'],pos,head[:6])
  fields=[int(head[6+i*8:14+i*8],16) for i in range(13)];ino,mode,uid,gid,nlink,mtime,size,devmaj,devmin,rdevmaj,rdevmin,namesize,check=fields
  name=data[pos+110:pos+110+namesize-1].decode();pos=(pos+110+namesize+3)&~3
  content=data[pos:pos+size];assert len(content)==size
  pos=(pos+size+3)&~3
  if name=='TRAILER!!!':break
  if mode&0o170000!=0o100000:continue
  key=(ino,devmaj,devmin)
  if size:hardlinks[key]=content
  entries.append((name,content,key))
 for sample_id,pattern,kind,reason in package['selectors']:
  matches=[]
  for name,content,key in entries:
   content=content or hardlinks.get(key,b'')
   if re.fullmatch(pattern,Path(name).name) and content.startswith(b'\x7fELF'):matches.append((name,content))
  if len(matches)!=1:
   logs.append({'sample':sample_id,'error':'Expected exactly one selected regular ELF','matches':[m[0] for m in matches]});continue
  name,content=matches[0];target=private/'extract'/(sample_id+'.elf');target.write_bytes(content)
  rows.append({'id':sample_id,'kind':kind,'package':package['filename'],'repo':package['repo'],'url':package['url'],'rpm_query':package['rpm_query'].strip(),'archive_path':name,'local_path':str(target.relative_to(r)),'bytes':len(content),'sha256':hashlib.sha256(content).hexdigest(),'reason':reason})
(private/'samples.json').write_text(json.dumps(rows,indent=2)+'\n')
(r/'extraction-status.json').write_text(json.dumps({'method':'rpm2cpio plus in-memory newc reader; only selected regular ELF copied under private; no symlinks materialized or installed','samples':rows,'operations':logs},indent=2)+'\n')
print('Selected ELF:',len(rows))
if len(rows)!=16:raise SystemExit('Missing ELF selections; see real extraction-status errors')
