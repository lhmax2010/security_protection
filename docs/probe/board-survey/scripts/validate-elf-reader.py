#!/usr/bin/env python3
from pathlib import Path
import json,subprocess,re
r=Path(__file__).resolve().parents[1];workspace=r.parents[2];code=(r/'scripts/elf-metadata.lua').read_text();v=r/'validation';v.mkdir(exist_ok=True);checks=[]
files=[workspace/'docs/probe/samples/bin'/name for name in ['target_c_gcc_armv7l','target_c_llvm_armv7l','target_rust_armv7l']]+[Path('/usr/bin/ls')]
for path in files:
 name=path.name;source=v/(name+'.lua');source.write_text('TARGET_PATH='+json.dumps(str(path))+'\nTARGET_KIND="executable"\n'+code)
 p=subprocess.run(['python3',str(r/'scripts/lua-host-run.py'),str(source)],capture_output=True,text=True);(v/(name+'-decoder.txt')).write_text(p.stdout+p.stderr);assert p.returncode==0,p.stderr
 ref=subprocess.run(['readelf','-W','-h','-l','-S','-d','--dyn-syms',str(path)],capture_output=True,text=True);(v/(name+'-readelf.txt')).write_text(ref.stdout+ref.stderr);assert ref.returncode==0
 fields={line.split('\t')[1]:line.split('\t')[2] for line in p.stdout.splitlines() if line.startswith('FIELD\t')};text=ref.stdout
 expected={}
 expected['RELRO']= 'None' if 'GNU_RELRO' not in text else ('Full' if re.search(r'\(BIND_NOW\)|\(FLAGS(?:_1)?\).*\bNOW\b',text) else 'Partial')
 stack=next(l for l in text.splitlines() if re.match(r'^\s*GNU_STACK\s',l));expected['NX']='Disabled' if 'E' in ''.join(stack.split()[6:-1]) else 'Enabled'
 expected['PIE']='Yes' if re.search(r'\bDYN\b',text) and ('INTERP' in text or re.search(r'\(FLAGS_1\).*\bPIE\b',text)) else 'No'
 expected['stripped']='No' if re.search(r'(?m)^\s*\[\s*\d+\]\s+\.symtab\s',text) else 'Yes(no .symtab)'
 expected['RPATH']='Present' if '(RPATH)' in text else 'Absent';expected['RUNPATH']='Present' if '(RUNPATH)' in text else 'Absent'
 sym=[]
 for line in text.splitlines():
  m=re.match(r'^\s*\d+:\s+([0-9a-fA-F]+)\s+(\d+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)',line)
  if m:sym.append(dict(zip(['value','size','type','bind','vis','ndx','name'],m.groups())))
 for key,predicate in [('canary',lambda n:n.split('@')[0] in ['__stack_chk_fail','__stack_chk_fail_local','__stack_chk_guard']),('FORTIFY',lambda n:bool(re.fullmatch(r'__[A-Za-z0-9_]+_chk',n.split('@')[0])))]:
  expected[key]='Detected(import)' if any(s['ndx']=='UND' and predicate(s['name']) for s in sym) else ('Provider-definition-only' if any(s['ndx']!='UND' and predicate(s['name']) for s in sym) else 'No dynamic evidence')
 exports=[s for s in sym if s['ndx']!='UND' and s['bind'] in ['GLOBAL','WEAK'] and s['vis'] in ['DEFAULT','PROTECTED']]
 expected['dynamic_export_count_including_ABS']=str(len(exports));expected['dynamic_export_non_ABS_count']=str(sum(s['ndx']!='ABS' for s in exports));expected['dynamic_export_function_count']=str(sum(s['type'] in ['FUNC','IFUNC'] for s in exports))
 mismatches={k:{'decoder':fields.get(k),'readelf':x} for k,x in expected.items() if fields.get(k)!=x}
 checks.append({'artifact':str(path),'elf32_or_64':'ELF32' if 'ELF32' in text else 'ELF64','expected_from_real_readelf':expected,'mismatches':mismatches})
report={'cases':checks,'all_agree':all(not x['mismatches'] for x in checks),'limitation':'Independent host readelf comparison on three existing ARM baselines plus host ELF64; board runtime separately verified on existing systemctl. Does not replace unavailable board readelf execution.'}
(v/'comparison.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report));raise SystemExit(not report['all_agree'])
