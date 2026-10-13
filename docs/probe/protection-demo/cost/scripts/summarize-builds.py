#!/usr/bin/env python3
from pathlib import Path
from collections import Counter
import hashlib,json,subprocess

root=Path.cwd();base=root/'docs/probe/protection-demo/cost'
status=json.loads((base/'build-status.json').read_text());rows=[];scope={}
for variant in ['baseline','selective','full']:
    reports=[]
    for p in sorted((base/'compiler-reports'/variant).glob('*.json')):
        reports += [dict(f,report_file=str(p.relative_to(base))) for f in json.loads(p.read_text())['functions'] if not f.get('declaration')]
    events=[json.loads(p.read_text()) for p in (base/'private'/variant/'events').glob('*.json')]
    actual=[];skip=Counter();perpass={}
    for f in reports:
        changed=any(p.get('changed') and p.get('status')=='ran' for p in f['passes'])
        for p in f['passes']:
            counts=perpass.setdefault(p['id'],Counter());counts[p['status']]+=1
            if p.get('changed'):counts['changed']+=1
            if p.get('skip_reason'):skip[p['id']+':'+p['skip_reason']]+=1
        actual.append({'function':f['name'],'report':f['report_file'],'any_pass_changed':changed,
            'insts':f['insts'],'passes':[{k:p[k] for k in ['id','status','changed','skip_reason','insts_before','insts_after'] if k in p} for p in f['passes']]})
    scope[variant]={'C_TUs_completed':sum(e['exit']==0 for e in events),'C_TU_failures':sum(e['exit']!=0 for e in events),
        'optimized_definition_count':sum(len(e.get('post_O2_definitions',[])) for e in events),
        'annotated_definition_count':sum(len(e.get('post_O2_definitions_annotated',[])) for e in events),
        'reported_functions':len(reports),'functions_any_pass_changed':sum(a['any_pass_changed'] for a in actual),
        'per_pass':perpass,'skip_reasons':skip,'functions':actual,
        'limit':'Per-function per-TU optimized IR definitions, not unique source functions or all production codecs; assembly and other libraries excluded.'}
    if status[variant]['status']!='complete':rows.append({'variant':variant,'measured':False,'status':status[variant]['status']});continue
    target=Path(status[variant]['shared_library']);elfout=base/'elf';elfout.mkdir(exist_ok=True)
    lua=base/'private'/(variant+'-metadata.lua')
    decoder=root/'docs/probe/board-survey/scripts/elf-metadata.lua'
    lua.write_text('TARGET_PATH='+json.dumps(str(target))+'\nTARGET_KIND="shared-library"\n'+decoder.read_text())
    p=subprocess.run(['python3',str(root/'docs/probe/board-survey/scripts/lua-host-run.py'),str(lua)],capture_output=True,text=True)
    (elfout/(variant+'-lua.txt')).write_text(p.stdout+p.stderr+f'\nexit={p.returncode}\n');assert p.returncode==0,p.stderr
    line=next(l.split('\t') for l in p.stdout.splitlines() if l.startswith('SECTION\t') and l.split('\t')[2]=='.text')
    textbytes=int(line[line.index('size')+1])
    ref=subprocess.run(['readelf','-SW',str(target)],capture_output=True,text=True)
    (elfout/(variant+'-readelf-sections.txt')).write_text(ref.stdout+ref.stderr);assert ref.returncode==0
    fields=next(l.split(']',1)[1].split() for l in ref.stdout.splitlines() if '] .text ' in l)
    assert textbytes==int(fields[4],16)
    binary=Path(status[variant]['ffmpeg_static'])
    rows.append({'variant':variant,'measured':True,'so_file_bytes':target.stat().st_size,'text_bytes':textbytes,
                 'so_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'ffmpeg_static_bytes':binary.stat().st_size,
                 'ffmpeg_static_sha256':hashlib.sha256(binary.read_bytes()).hexdigest(),'library_stripped':False})
baseline=next(r for r in rows if r['variant']=='baseline')
for r in rows:
    if r['measured']:
        for key in ['so_file_bytes','text_bytes']:r[key+'_growth_percent']=(r[key]/baseline[key]-1)*100
(base/'obfuscation-scope.json').write_text(json.dumps(scope,indent=2)+'\n')
(base/'size-comparison.json').write_text(json.dumps({'method':'Existing validated read-only Lua ELF decoder; .text size independently agrees with GNU readelf; identical unstripped release/PIC libraries (no debug), not executable total PT_LOAD size.','rows':rows},indent=2)+'\n')
(base/'size-comparison.txt').write_text('Variant       .so bytes     growth       .text bytes    growth\n'+'\n'.join(f'{r["variant"]:12s} {r["so_file_bytes"]:10d} {r["so_file_bytes_growth_percent"]:+9.2f}% {r["text_bytes"]:13d} {r["text_bytes_growth_percent"]:+9.2f}%' if r['measured'] else r['variant']+': UNMEASURED '+r['status'] for r in rows)+'\nAll three final libraries unstripped, same component set/ABI/O2. First failed full-source attempt excluded from table.\n')
for variant,s in scope.items():print(variant,'scope',s['annotated_definition_count'],'reported',s['reported_functions'],'changed',s['functions_any_pass_changed'],'skips',dict(s['skip_reasons']))
print((base/'size-comparison.txt').read_text())
