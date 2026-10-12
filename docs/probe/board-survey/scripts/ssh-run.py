#!/usr/bin/env python3
import argparse,os,pathlib,subprocess,json,time
root=pathlib.Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--user',required=True);p.add_argument('--script',required=True);p.add_argument('--output',required=True);args=p.parse_args()
script=pathlib.Path(args.script).resolve();output=pathlib.Path(args.output).resolve()
for path in [script,output]:
 if not path.is_relative_to(root):raise SystemExit('All survey paths must stay within docs/probe/board-survey')
if not args.user or any(c not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_.-' for c in args.user):raise SystemExit('Invalid SSH user')
output.parent.mkdir(parents=True,exist_ok=True)
if output.exists():raise SystemExit('Refusing to overwrite earlier evidence: '+str(output))
env=os.environ.copy();env.update(SSH_ASKPASS=str(root/'scripts/ssh-askpass.sh'),SSH_ASKPASS_REQUIRE='force')
command=['setsid','-w','ssh','-T','-p','22','-o','ConnectTimeout=10','-o','ConnectionAttempts=1','-o','NumberOfPasswordPrompts=1','-o','ServerAliveInterval=10','-o','ServerAliveCountMax=2','-o','ControlMaster=no','-o','ControlPath=none','-o','StrictHostKeyChecking=accept-new','-o','UpdateHostKeys=no','-o','UserKnownHostsFile='+str(root/'ssh/known_hosts'),args.user+'@192.168.108.26','sh -s']
start=time.monotonic()
with script.open('rb') as stdin,output.open('wb') as log:
 result=subprocess.run(command,stdin=stdin,stdout=log,stderr=subprocess.STDOUT,env=env)
metadata={'ssh_argv':command,'remote_script':str(script.relative_to(root)),'ssh_exit_code':result.returncode,'elapsed_seconds':round(time.monotonic()-start,3),'policy':'Remote script is streamed on stdin to sh -s; no remote files are created. Only textual stdout/stderr are retained. SSH credentials flow only through local askpass to OpenSSH.'}
output.with_name(output.name+'.meta.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'output':str(output),'ssh_exit_code':result.returncode},ensure_ascii=False))
raise SystemExit(result.returncode)
