#!/usr/bin/env python3
import subprocess,sys,time,json,pathlib
path=pathlib.Path(sys.argv[1]);path.parent.mkdir(parents=True,exist_ok=True)
cmd=sys.argv[2:]; t=time.monotonic()
with path.open('w') as f:
 p=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT)
meta={'argv':cmd,'exit_code':p.returncode,'elapsed_seconds':round(time.monotonic()-t,3)}
path.with_name(path.name+'.meta.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
print(str(path),meta['exit_code']);sys.exit(p.returncode)
