#!/usr/bin/env python3
"""Parse only textual board readelf output; never read any board binary locally."""
import argparse,json,re,pathlib
root=pathlib.Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('capture');args=p.parse_args()
capture=pathlib.Path(args.capture).resolve()
if not capture.is_relative_to(root):raise SystemExit('Capture must be under board-survey')
text=capture.read_text(errors='replace')
selected=json.loads((root/'samples.json').read_text())
rows=[]
for sample in selected:
 sid=sample['id']
 match=re.search(r'(?ms)^@@BEGIN_SAMPLE '+re.escape(sid)+r'\n(.*?)^@@END_SAMPLE '+re.escape(sid)+r'\s*$',text)
 if not match:raise SystemExit('Incomplete capture for '+sid)
 raw=match[1];out=root/'raw'/(sid+'.txt')
 if out.exists():raise SystemExit('Will not overwrite raw evidence '+str(out))
 out.write_text(raw)
 commands={}
 for m in re.finditer(r'(?ms)^@@BEGIN_COMMAND (\S+)\nCOMMAND:([^\n]*)\n(.*?)^@@END_COMMAND \1 EXIT_CODE=(\d+)\s*$',raw):
  commands[m[1]]={'command':m[2].strip(),'stdout_stderr':m[3],'exit_code':int(m[4])}
 required=['header','program-headers','sections','dynamic','dynamic-symbols']
 failures=[k for k,v in commands.items() if v['exit_code']!=0]
 def get(k):
  v=commands.get(k)
  return v['stdout_stderr'] if v and v['exit_code']==0 else None
 header=get('header');ph=get('program-headers');sections=get('sections');dynamic=get('dynamic');dyn=get('dynamic-symbols')
 if header is None:raise SystemExit('Missing ELF header; keep capture and record failure '+sid)
 elf_type=re.search(r'^\s*Type:\s+(\S+)',header,re.M)
 machine=re.search(r'^\s*Machine:\s+(.+)',header,re.M)
 kind=sample['kind'];elf_type=elf_type[1] if elf_type else 'Unknown'
 if ph is None or dynamic is None:relro='Unknown'
 elif 'GNU_RELRO' not in ph:relro='None'
 elif re.search(r'\(BIND_NOW\)|\(FLAGS(?:_1)?\).*\bNOW\b',dynamic):relro='Full'
 else:relro='Partial'
 if ph is None:nx='Unknown'
 else:
  stack=next((line for line in ph.splitlines() if re.match(r'^\s*GNU_STACK\s',line)),None)
  if stack is None:nx='Unknown(no GNU_STACK)'
  else:
   fields=stack.split();flags=''.join(fields[6:-1]);nx='Disabled' if 'E' in flags else 'Enabled'
 if kind=='shared-library':pie='N/A(DSO)'
 elif elf_type=='EXEC':pie='No'
 elif elf_type=='DYN' and ((ph is not None and re.search(r'^\s*INTERP\s',ph,re.M)) or (dynamic is not None and re.search(r'\(FLAGS_1\).*\bPIE\b',dynamic))):pie='Yes'
 else:pie='Unknown'
 stripped='Unknown' if sections is None else ('No' if re.search(r'(?m)^\s*\[\s*\d+\]\s+\.symtab\s',sections) else 'Yes(no .symtab)')
 symbols=[]
 if dyn is not None:
  for line in dyn.splitlines():
   m=re.match(r'^\s*\d+:\s+([0-9a-fA-F]+)\s+(\d+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)',line)
   if m:symbols.append(dict(zip(['value','size','type','binding','visibility','index','name'],m.groups())))
 def plain(name):return name.split('@')[0]
 chk=lambda name:bool(re.fullmatch(r'__\w+_chk',plain(name)))
 canary=lambda name:plain(name) in ['__stack_chk_fail','__stack_chk_fail_local','__stack_chk_guard']
 imported=[x for x in symbols if x['index']=='UND']
 defined=[x for x in symbols if x['index']!='UND']
 def indicator(predicate):
  if dyn is None:return 'Unknown'
  if any(predicate(x['name']) for x in imported):return 'Detected(import)'
  if any(predicate(x['name']) for x in defined):return 'Provider-definition-only'
  return 'No dynamic evidence'
 rpath='Unknown' if dynamic is None else ('Present' if re.search(r'\(RPATH\)',dynamic) else 'Absent')
 runpath='Unknown' if dynamic is None else ('Present' if re.search(r'\(RUNPATH\)',dynamic) else 'Absent')
 exports=[x for x in defined if x['binding'] in ['GLOBAL','WEAK'] and x['visibility'] in ['DEFAULT','PROTECTED']]
 row={'id':sid,'path':sample['path'],'kind':kind,'elf_type':elf_type,'machine':machine[1].strip() if machine else 'Unknown','RELRO':relro,'canary':indicator(canary),'NX':nx,'PIE':pie,'RPATH':rpath,'RUNPATH':runpath,'stripped':stripped,'FORTIFY':indicator(chk),'command_failures':failures,'missing_sections':[k for k in required if k not in commands],'dynamic_export_count_including_ABS':len(exports) if dyn is not None else None,'dynamic_export_non_ABS_count':sum(x['index']!='ABS' for x in exports) if dyn is not None else None,'dynamic_export_function_count':sum(x['type'] in ['FUNC','IFUNC','GNU_IFUNC'] for x in exports) if dyn is not None else None,'fortify_imports':[x['name'] for x in imported if chk(x['name'])],'canary_imports':[x['name'] for x in imported if canary(x['name'])]}
 rows.append(row)
(root/'hardening-matrix.json').write_text(json.dumps({'rows':rows,'policy':'Readelf import-based canary/FORTIFY evidence is not proof of source compiler flags or all-function protection. Defined runtime helper symbols alone do not prove instrumentation. NX is an ELF GNU_STACK request, not observed runtime enforcement.'},indent=2)+'\n')
columns=['id','path','kind','RELRO','canary','NX','PIE','RPATH','RUNPATH','stripped','FORTIFY']
lines=['\t'.join(columns)]+['\t'.join(str(r[c]) for c in columns) for r in rows]
lines+=['','NOTES: PIE denominator must exclude shared libraries. No dynamic evidence does not prove -fno-stack-protector or _FORTIFY_SOURCE=0. Provider-definition-only means symbols supply helper APIs; instrumentation not proven. Unknown/missing sections remain explicit.','COMMAND_ERRORS:']
lines += [r['id']+': '+','.join(r['command_failures']+r['missing_sections']) for r in rows if r['command_failures'] or r['missing_sections']]
(root/'hardening-matrix.txt').write_text('\n'.join(lines)+'\n')
print(json.dumps({'samples':len(rows),'samples_with_command_errors':sum(bool(r['command_failures'] or r['missing_sections']) for r in rows)}))
