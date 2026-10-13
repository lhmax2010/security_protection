#!/usr/bin/env python3
"""Apply xollvm only while compiling libavcodec C translation units."""
from pathlib import Path
import hashlib,json,os,re,subprocess,sys,time

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
cmd+=args
try:
    if codec:
        # Annotate only real post-O2 definitions: no forced retention of unused
        # source/inline helpers or disabled-codec branches. Transformation is
        # still entirely the real xollvm sub/bcf/fla implementation.
        ir=base/'private'/variant/'ir';ir.mkdir(parents=True,exist_ok=True)
        before=ir/(key+'.ll');annotated=ir/(key+'.annotated.ll');after=ir/(key+'.obfuscated.ll')
        frontargs=[];j=0
        while j<len(args):
            if args[j]=='-o':j+=2;continue
            if args[j]=='-c':j+=1;continue
            frontargs.append(args[j]);j+=1
        front=cmd[:-len(args)]+frontargs+['-S','-emit-llvm','-o',str(before)]
        record['pipeline_commands']=[front]
        p=subprocess.run(front,timeout=180)
        if p.returncode:raise subprocess.CalledProcessError(p.returncode,front)
        text=before.read_text();assert '@llvm.global.annotations' not in text
        functions=re.findall(r'(?m)^define\b[^\n]*?@([^\s(]+)\(',text)
        record['post_O2_definitions']=functions[:]
        if variant=='baseline':
            functions=[]
        elif variant=='selective':
            selection=json.loads((base/'selected-functions.json').read_text())['functions']
            wanted={f for functions_in_file in selection.values() for f in functions_in_file}
            functions=[f for f in functions if f in wanted]
        annotation='obf: substitution(prob=50,loop=1), bcf(prob=30,loop=1,maxBlocks=200), flattening(minBlocks=3,maxBlocks=200)'
        entries=['{ ptr, ptr, ptr, i32, ptr } { ptr @'+f+', ptr @cost_obf_annotation, ptr null, i32 0, ptr null }' for f in functions]
        if entries:
            text+='\n@cost_obf_annotation = private unnamed_addr constant ['+str(len(annotation)+1)+' x i8] c"'+annotation+'\\00"\n'
            text+='@llvm.global.annotations = appending global ['+str(len(entries))+' x { ptr, ptr, ptr, i32, ptr }] ['+', '.join(entries)+'], section "llvm.metadata"\n'
        annotated.write_text(text);reports=base/'compiler-reports'/variant;reports.mkdir(parents=True,exist_ok=True)
        opt=[tool['opt'],'-passes=obfuscation','-obf-seed=1','-obf-deterministic','-obf-verify','-obf-ir-budget-max=12000',
             '-obf-report-json='+str(reports/(key+'.json')),'-S',str(annotated),'-o',str(after)]
        record['pipeline_commands'].append(opt);record['post_O2_definitions_annotated']=functions
        if variant=='baseline':
            after.write_text(text)
            record['pipeline_commands'].pop()
        else:
            p=subprocess.run(opt,timeout=180)
            if p.returncode:raise subprocess.CalledProcessError(p.returncode,opt)
        backend=cmd[:];backend[len(cmd)-len(args)+i]=str(after)
        backend+=['-Xclang','-disable-llvm-passes']
        record['pipeline_commands'].append(backend)
        p=subprocess.run(backend,timeout=180);code=p.returncode
    else:
        p=subprocess.run(cmd,timeout=180 if codec and variant!='baseline' else 300)
        code=p.returncode
except subprocess.CalledProcessError as e:
    code=e.returncode
    if record:record['pipeline_error']=str(e)
except subprocess.TimeoutExpired as e:
    print(str(e),file=sys.stderr);code=124
    if record:record['timeout_error']=str(e)
if record:
    record.update(ended=time.time(),exit=code,actual_command=cmd)
    (eventdir/(key+'.json')).write_text(json.dumps(record,indent=2)+'\n')
raise SystemExit(code)
