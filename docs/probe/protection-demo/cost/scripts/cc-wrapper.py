#!/usr/bin/env python3
"""Apply xollvm only while compiling libavcodec C translation units."""
from pathlib import Path
import hashlib,json,os,subprocess,sys,time

base=Path(__file__).resolve().parents[1]
variant=sys.argv[1];args=sys.argv[2:]
root=base.parents[3]
tool=json.loads((root/'docs/probe/protection-demo/obfuscation/toolchain.json').read_text())
cross=root/'.local-tools/sysroot/usr'
cmd=[tool['clang'],'--target=arm-linux-gnueabihf','--sysroot='+str(cross.parent),'--gcc-toolchain='+str(cross),
     '-isystem',str(cross/'arm-linux-gnueabihf/include'),'-L'+str(cross/'arm-linux-gnueabihf/lib')]
sources=[(i,Path(a).resolve()) for i,a in enumerate(args) if a.endswith('.c') and Path(a).is_file()]
codec=next(((i,p) for i,p in sources if 'libavcodec' in p.parts and '-c' in args),None)
record=None
if codec:
    i,source=codec;key=source.name+'-'+hashlib.sha256(str(source).encode()).hexdigest()[:10]
    eventdir=base/'private'/variant/'events';eventdir.mkdir(parents=True,exist_ok=True)
    record={'variant':variant,'source':str(source),'command_arguments':args,'started':time.time(),'obfuscation_requested':variant!='baseline'}
    if variant=='full':
        generated=base/'private'/variant/'generated'/source.name;generated.parent.mkdir(parents=True,exist_ok=True)
        prefix=(base/'scripts/full-annotation.h').read_text()
        generated.write_text(prefix+'\n#line 1 '+json.dumps(str(source))+'\n'+source.read_text()+'\n#pragma clang attribute pop\n')
        args[i]=str(generated);cmd+=['-iquote',str(source.parent)]
    if variant!='baseline':
        reports=base/'compiler-reports'/variant;reports.mkdir(parents=True,exist_ok=True)
        cmd+=['-mllvm','-enable-obfuscation','-mllvm','-obf-seed=1','-mllvm','-obf-deterministic',
              '-mllvm','-obf-verify','-mllvm','-obf-ir-budget-max=12000',
              '-mllvm','-obf-report-json='+str(reports/(key+'.json'))]
cmd+=args
try:
    p=subprocess.run(cmd,timeout=180 if codec and variant!='baseline' else 300)
    code=p.returncode
except subprocess.TimeoutExpired as e:
    print(str(e),file=sys.stderr);code=124
    if record:record['timeout_error']=str(e)
if record:
    record.update(ended=time.time(),exit=code,actual_command=cmd)
    (eventdir/(key+'.json')).write_text(json.dumps(record,indent=2)+'\n')
raise SystemExit(code)
