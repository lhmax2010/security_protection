#!/usr/bin/env python3
import subprocess,json,hashlib,os
from pathlib import Path
root=Path.cwd();b=root/'docs/probe/samples/bin';d=root/'docs/probe/evidence';sysroot=root/'.local-tools/sysroot/usr/arm-linux-gnueabihf'
commands={
 'target_c_gcc_armv7l':['qemu-arm','-L',str(sysroot),str(b/'target_c_gcc_armv7l')],
 'target_c_llvm_armv7l':['qemu-arm','-L',str(sysroot),str(b/'target_c_llvm_armv7l')],
 'target_rust_armv7l':['qemu-arm','-L',str(sysroot),str(b/'target_rust_armv7l')],
 'target_py.pyc':['python3',str(b/'target_py.pyc')],
 'target_js.js':['node',str(b/'target_js.js')],
 'target_dotnet.dll':['dotnet',str(b/'dotnet-out/target_dotnet.dll')],
}
all_rows=[]
for name,cmd in commands.items():
 rows=[]
 for argument in [None,'0','1','65535','4294967295']:
  argv=cmd+([] if argument is None else [argument]);p=subprocess.run(argv,capture_output=True,text=True,timeout=30)
  row={'argv':argv,'input':argument,'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
  rows.append(row);all_rows.append((name,row))
 (d/name/'runtime-smoke.json').write_text(json.dumps({'artifact_sha256':hashlib.sha256((b/name).read_bytes()).hexdigest(),'executed_artifact_sha256':hashlib.sha256(Path(cmd[-1]).read_bytes()).hexdigest(),'cases':rows},indent=2)+'\n')
failures=[]
for argument in [None,'0','1','65535','4294967295']:
 group=[(name,row) for name,row in all_rows if row['input']==argument]
 if any(row['exit_code']!=0 for _,row in group) or len({row['stdout'] for _,row in group})!=1:failures.append({'input':argument,'rows':group})
summary={'tested_inputs':[None,'0','1','65535','4294967295'],'case_count':len(all_rows),'all_six_artifacts_equal_stdout_and_zero_exit':not failures,'failures':failures,'limitation':'This corroborates baseline equivalence for these five inputs only; does not establish all-input equivalence of source or decompiled pseudocode.'}
(d/'runtime-smoke-summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary));raise SystemExit(bool(failures))
