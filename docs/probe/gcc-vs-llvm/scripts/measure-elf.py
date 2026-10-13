#!/usr/bin/env python3
from pathlib import Path
import json,subprocess,re,hashlib,os,struct
r=Path(__file__).resolve().parents[1];private=r/'private';rows=[]
samples=json.loads((private/'samples.json').read_text());compilers={x['id']:x for x in json.loads((r/'gcc-compiler-evidence.json').read_text())};env=os.environ.copy();env.update(HOME=str(r/'local-runtime'),TMPDIR=str(r/'local-runtime/tmp'),LC_ALL='C')
(r/'scripts/elf-metadata.lua').write_text(Path('docs/probe/board-survey/scripts/elf-metadata.lua').read_text().replace('RPM_EMBEDDED_LUA_DIRECT_ELF_METADATA','HOST_LUA_SAME_VALIDATED_ELF_METADATA_DECODER'))
(r/'scripts/lua-host-run.py').write_text(Path('docs/probe/board-survey/scripts/lua-host-run.py').read_text())
for s in samples:
 target=(r/s['local_path']).resolve();code='TARGET_PATH='+json.dumps(str(target))+'; TARGET_KIND='+json.dumps(s['kind'])+';\n'+(r/'scripts/elf-metadata.lua').read_text()
 lua=private/'extract'/(s['id']+'.lua');lua.write_text(code)
 p=subprocess.run(['python3',str(r/'scripts/lua-host-run.py'),str(lua)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,env=env);text=p.stdout.decode(errors='replace')
 (private/'extract'/(s['id']+'.lua-full.txt')).write_text(text)
 assert p.returncode==0 and 'METADATA_READER_SUCCESS' in text,s['id']
 fields={line.split('\t')[1]:line.split('\t')[2] for line in text.splitlines() if line.startswith('FIELD\t')}
 exports=[line.split('\t') for line in text.splitlines() if line.startswith('EXPORT\t') and line.split('\t')[4]!='65521']
 mangled=sum(x[5].startswith('_Z') for x in exports)
 # ELF32 allocated non-writable .rodata only; never count .dynstr/.strtab as business plaintext.
 data=target.read_bytes();assert data[:6]==b'\x7fELF\x01\x01'
 shoff=struct.unpack_from('<I',data,32)[0];ents,count,names=struct.unpack_from('<HHH',data,46)
 table=[struct.unpack_from('<10I',data,shoff+i*ents) for i in range(count)];strs=data[table[names][4]:table[names][4]+table[names][5]]
 rodata=[];byte_count=0
 for sec in table:
  name=strs[sec[0]:strs.find(b'\0',sec[0])].decode()
  if name=='.rodata' or name.startswith('.rodata.'):
   content=data[sec[4]:sec[4]+sec[5]];byte_count+=len(content)
   rodata.extend((name,sec[3]+match.start(),match.group().decode()) for match in re.finditer(rb'[\x20-\x7e]{8,}',content))
 (private/'extract'/(s['id']+'.rodata-strings.json')).write_text(json.dumps(rodata,indent=2)+'\n')
 candidates=[x for x in rodata if re.search(r'(version|error|invalid|usage|failed|license)',x[2],re.I) and len(x[2])<140 and not re.search(r'(/home/|/build/|https?://)',x[2])]
 sample=candidates[:3]
 public=['SAMPLE '+s['id'],'SHA256 '+s['sha256'],'METHOD main ELF GNU readelf plus independently validated Lua ELF decoder; full dynsym/strings local-only.']
 for args in [['-W','-h','-l','-d','-S'],['-n']]:
  q=subprocess.run(['readelf',*args,str(target)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,env=env)
  public.extend(['COMMAND readelf '+' '.join(args)+' <ELF>','EXIT '+str(q.returncode),q.stdout.decode(errors='replace')]);assert q.returncode==0
 # Independently corroborate symbol counts from GNU readelf, without publishing any symbol list.
 q=subprocess.run(['readelf','--dyn-syms','--wide',str(target)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,env=env)
 dynamic=q.stdout.decode(errors='replace');(private/'extract'/(s['id']+'.dynsym-readelf.txt')).write_text(dynamic)
 counts={'export_non_ABS':0,'export_FUNC_IFUNC':0,'Cpp_mangled':0}
 for line in dynamic.splitlines():
  tokens=line.split()
  if len(tokens)<8 or not re.fullmatch(r'\d+:',tokens[0]):continue
  _,value,size,kind,bind,vis,ndx,name=tokens[:8]
  if bind in ['GLOBAL','WEAK'] and vis in ['DEFAULT','PROTECTED'] and ndx not in ['UND','ABS']:
   counts['export_non_ABS']+=1;counts['export_FUNC_IFUNC']+=kind in ['FUNC','IFUNC'];counts['Cpp_mangled']+=name.startswith('_Z')
 assert counts['export_non_ABS']==int(fields['dynamic_export_non_ABS_count']) and counts['export_FUNC_IFUNC']==int(fields['dynamic_export_function_count']) and counts['Cpp_mangled']==mangled,(s['id'],counts,fields)
 filtered=[line for line in text.splitlines() if not line.startswith(('DYNAMIC_SYMBOL\t','EXPORT\t'))]
 public.extend(['RAW_LUA_PROJECTION: full symbol-name records withheld; all other emitted metadata follows.','\n'.join(filtered),'GNU_READELF_DYNSYM_COUNT_PROJECTION '+json.dumps(counts),'FULL_PRIVATE_DYNSYM_SHA256 '+hashlib.sha256(dynamic.encode()).hexdigest(),'RODATA_ASCII_PRINTABLE_RUNS_MIN8_COUNT '+str(len(rodata)),'RODATA_SCANNED_BYTES '+str(byte_count),'RODATA_SAMPLE_PROJECTION '+json.dumps(sample)])
 raw='\n'.join(public).replace(str(r.resolve()),'<SURVEY_ROOT>');(r/'raw'/(s['id']+'-elf.txt')).write_text(raw+'\n')
 compiler=compilers[s['id']];producer='\n'.join(compiler['producer_evidence']);stack_flags=sorted(set(re.findall(r'-f(?:no-)?stack-protector[^ \n]*',producer)));visibility_flags=sorted(set(re.findall(r'-fvisibility=[^ \n]*',producer)))
 (r/'raw'/(s['id']+'-elf.txt')).write_text(raw+'\nMATCHED_DEBUG_PRODUCER_FLAGS_PROJECTION '+json.dumps({'stack_protector_flags':stack_flags,'visibility_flags':visibility_flags,'compiler_evidence':'raw/'+s['id']+'-compiler.txt'})+'\n')
 rows.append({**s,**fields,'compiler':compiler['compiler'],'compiler_version':'14.2.0','producer_stack_protector_flags':stack_flags,'producer_visibility_flags':visibility_flags,'export_Cpp_mangled':mangled,'rodata_ascii_min8_runs':len(rodata),'rodata_bytes_scanned':byte_count,'rodata_sample_count':len(sample),'rodata_samples':sample,'raw_evidence':'raw/'+s['id']+'-elf.txt','stack_protector_evidence':fields['canary'],'stack_protector_level':('Flags observed in matched CUs: '+', '.join(stack_flags) if stack_flags else 'No explicit stack-protector flag recorded in matched producers; not proof disabled'),'visibility_flag':('-fvisibility=hidden observed in matched CUs' if '-fvisibility=hidden' in visibility_flags else 'Unknown: counts/no producer flag do not prove absence'),'obfuscation':'Unknown from ELF headers; no whole-library absence proof','method':'validated Lua5.3 host decoder + GNU readelf cross-check'});print(s['id'],fields['RELRO'],fields['canary'],fields['FORTIFY'],len(rodata),flush=True)
(r/'gcc-hardening-matrix.json').write_text(json.dumps({'rows':rows,'limits':['canary and stack-protector are the same evidence axis, not independent protections','FORTIFY imports only; libc provider definitions counted separately','No exact hidden-visibility flag or original-name recovery rate inferred from counts','rodata strings metric: ASCII printable runs min8 in .rodata sections; may include accidental data, excludes dynamic/static symbol names','LLVM historical board has no same-metric rodata counts for most samples; do not invent them']},indent=2)+'\n')
fields=['id','compiler','compiler_version','RELRO','NX','PIE','canary','FORTIFY','stripped','RPATH','RUNPATH','producer_stack_protector_flags','producer_visibility_flags','dynamic_export_non_ABS_count','dynamic_export_function_count','export_Cpp_mangled','rodata_ascii_min8_runs','rodata_sample_count','raw_evidence']
(r/'gcc-hardening-matrix.txt').write_text('Verified GCC14.2.0 reference cohort; compiler confirmed from matched debug producers. Canary is stack-protector import evidence, not exact flags or full coverage.\n'+'\t'.join(fields)+'\n'+'\n'.join('\t'.join(str(row[k]) for k in fields) for row in rows)+'\n')
