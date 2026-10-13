#!/usr/bin/env python3
import re,json,subprocess,hashlib,os,concurrent.futures
from pathlib import Path
from urllib.parse import unquote,urljoin
r=Path(__file__).resolve().parents[1];private=r/'private'
repos={'base':'https://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Base/reference/repos/standard/packages/','unified':'https://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Unified/reference/repos/standard/packages/'}
choices=[('unified','libavcodec',[('libavcodec',r'libavcodec\.so\.\d+\.\d+\.\d+','shared-library','ffmpeg-demo/board counterpart')]),('base','glibc',[('libc_so_6',r'(?:libc-[0-9.]+\.so|libc\.so\.6)','shared-library','C runtime/provider')]),('base','libstdc++',[('libstdc++_so_6',r'libstdc\+\+\.so\.6\.\d+\.\d+','shared-library','C++ ABI runtime')]),('base','libopenssl3',[('libcrypto_so_3',r'libcrypto\.so\.3','shared-library','crypto ABI'),('libssl_so_3',r'libssl\.so\.3','shared-library','TLS ABI')]),('unified','dbus',[('dbus_daemon',r'dbus-daemon','executable','IPC daemon')]),('unified','dbus-libs',[('libdbus_1_so_3',r'libdbus-1\.so\.3\.\d+\.\d+','shared-library','IPC library')]),('unified','libglib',[('libglib_2_0_so_0',r'libglib-2\.0\.so\.0\.\d+\.\d+','shared-library','GLib platform ABI')]),('base','sqlite',[('sqlite3',r'sqlite3','executable','database CLI')]),('base','libsqlite',[('libsqlite3_so_0',r'libsqlite3\.so\.\d+\.\d+\.\d+','shared-library','database library')]),('base','bash',[('bash',r'bash','executable','shell')]),('unified','systemd',[('systemctl',r'systemctl','executable','service CLI')]),('base','rpm',[('rpm',r'rpm','executable','package manager')]),('base','findutils',[('find',r'find','executable','file utility')]),('unified','libdlog',[('libdlog_so_0',r'libdlog\.so\.0\.\d+\.\d+','shared-library','Tizen logging ABI')]),('unified','pkgmgr-info',[('libpkgmgr_info_so_0',r'libpkgmgr-info\.so\.0\.\d+\.\d+','shared-library','Tizen C++ implementation exposure')])]
plan=[]
for repo,pkg,selectors in choices:
 links=re.findall(r'href="([^"]+\.rpm)"',(private/(repo+'-armv7l.html')).read_text())
 candidates=[n for n in links if re.match('^'+re.escape(pkg)+r'-[0-9][^-]*-[^.]+.*\.armv7l\.rpm$',unquote(n))]
 assert len(candidates)==1,(repo,pkg,candidates)
 name=unquote(candidates[0]);plan.append({'repo':repo,'package':pkg,'filename':name,'url':urljoin(repos[repo]+'armv7l/',candidates[0]),'selectors':selectors})
(private/'plan.json').write_text(json.dumps(plan,indent=2)+'\n')
env=os.environ.copy();env.update(HOME=str(r/'local-runtime'),TMPDIR=str(r/'local-runtime/tmp'))
prior={p['filename']:p for p in json.loads((private/'packages.json').read_text())} if (private/'packages.json').exists() else {}
def fetch(p):
 target=private/'download'/p['filename'];log=private/'download'/(p['filename']+'.curl.txt');headers=target.with_suffix('.headers')
 if p['filename'] in prior and target.exists() and hashlib.sha256(target.read_bytes()).hexdigest()==prior[p['filename']].get('sha256'):
  old=prior[p['filename']];p.update({k:v for k,v in old.items() if k not in ['selectors','repo','package','filename','url']});p['download_reused']=True;return p
 with log.open('w') as f:
  proc=subprocess.run(['curl','-fL','--retry','1','--connect-timeout','20','--max-time','120','-D',str(headers),p['url'],'-o',str(target)],stdout=f,stderr=subprocess.STDOUT,env=env)
 p['curl_exit']=proc.returncode
 if proc.returncode==0:
  p['sha256']=hashlib.sha256(target.read_bytes()).hexdigest();p['size']=target.stat().st_size
  q=subprocess.run(['rpm','-qp','--qf','%{NAME}\t%{VERSION}\t%{RELEASE}\t%{ARCH}\t%{SOURCERPM}\n',str(target)],stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=env)
  p['rpm_query_exit']=q.returncode;p['rpm_query']=q.stdout.decode();p['rpm_query_stderr']=q.stderr.decode()
 print(p['filename'],p['curl_exit'],flush=True);return p
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:result=list(pool.map(fetch,plan))
(private/'packages.json').write_text(json.dumps(result,indent=2)+'\n')
lines=['Public Tizen reference ARMv7 RPM selection; snapshot URLs are mutable, observed hashes/time are recorded. Compiler classification pending, not assumed GCC.','15 common ELF counterparts + libavcodec, from 15 RPMs.','repo\tpackage NEVRA\tSource RPM\tbytes\tSHA256\tURL\tintended ELF IDs']
for p in result:
 query=p.get('rpm_query','FAILED').strip().split('\t');lines.append('\t'.join([p['repo'],' '.join(query[:4]),query[4] if len(query)>4 else 'Unknown',str(p.get('size','Unknown')),p.get('sha256','Unknown'),p['url'],','.join(s[0] for s in p['selectors'])]))
(r/'gcc-sample-list.txt').write_text('\n'.join(lines)+'\n')
network=[]
for repo in repos:
 for stem in [repo+'-index',repo+'-armv7l']:
  network.append('URL='+repos[repo]+('armv7l/' if stem.endswith('armv7l') else ''))
  network.append((private/(stem+'.headers')).read_text());network.append((private/(stem+'.curl.txt')).read_text())
for p in result:
 network.extend(['PACKAGE '+p['filename']+' CURL_EXIT '+str(p['curl_exit']),(private/'download'/(p['filename']+'.curl.txt')).read_text()])
(r/'network-downloads.txt').write_text('\n'.join(network)+'\n')
if any(p['curl_exit'] or p.get('rpm_query_exit',1) for p in result):raise SystemExit('Some real downloads/query operations failed; consult evidence.')
