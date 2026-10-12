#!/usr/bin/env python3
import os,subprocess,json,time,shlex,argparse,hashlib,base64
from pathlib import Path
root=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--script',required=True);p.add_argument('--output',required=True);p.add_argument('--timeout',type=int,default=60);p.add_argument('--stdin',action='store_true');a=p.parse_args()
script=Path(a.script).resolve();out=Path(a.output).resolve()
if not all(x.is_relative_to(root) for x in [script,out]):raise SystemExit('All paths must remain in board-survey')
if out.exists():raise SystemExit('Do not overwrite '+str(out))
serial=json.loads((root/'sdb-target.json').read_text())['serial'];text=script.read_text()
env=os.environ.copy();env.update(HOME=str(root/'local-runtime'),TMPDIR=str(root/'local-runtime/tmp'))
cmd=['sdb','-s',serial,'shell'] if a.stdin else ['sdb','-s',serial,'shell','sh -c '+shlex.quote(text)]
encoded=base64.b64encode(text.encode()).decode();chunks=[encoded[i:i+96] for i in range(0,len(encoded),96)]
stream='unset HISTFILE; HISTSIZE=0; set +o history; set +o emacs; set +o vi; PS1=; PS2=;\n'
stream+="printf '%s' "+chr(92)+'\n'
for chunk in chunks[:-1]:stream+=' '+shlex.quote(chunk)+' '+chr(92)+'\n'
stream+=' '+shlex.quote(chunks[-1])+' | base64 -d | sh\nexit\n'
start=time.monotonic();out.parent.mkdir(parents=True,exist_ok=True)
with out.open('wb') as f:
 try:result=subprocess.run(cmd,input=stream.encode() if a.stdin else None,stdout=f,stderr=subprocess.STDOUT,env=env,timeout=a.timeout);code=result.returncode
 except subprocess.TimeoutExpired:code=124;f.write(b'\nLOCAL_TIMEOUT: sdb shell deadline exceeded\n')
meta={'serial':serial,'script':str(script.relative_to(root)),'script_sha256':hashlib.sha256(text.encode()).hexdigest(),'sdb_exit_code':code,'elapsed_seconds':round(time.monotonic()-start,3),'transport':'SDB stdin: base64 of authored shell source decoded into noninteractive sh pipe; no board file created; history/readline disabled' if a.stdin else 'sdb shell sh -c, no script file copied to board','remote_script_readonly_except_explicit_network_persistence':True}
out.with_name(out.name+'.meta.json').write_text(json.dumps(meta,indent=2)+'\n');print(json.dumps({'output':str(out),'sdb_exit_code':code}));raise SystemExit(code)
