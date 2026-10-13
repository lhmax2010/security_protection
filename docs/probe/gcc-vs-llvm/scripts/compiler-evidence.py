#!/usr/bin/env python3
from pathlib import Path
import json,re,os,subprocess,hashlib,concurrent.futures,struct,zlib,importlib.util
from urllib.parse import urljoin,unquote
r=Path(__file__).resolve().parents[1];private=r/'private';packages=json.loads((private/'packages.json').read_text());samples=json.loads((private/'samples.json').read_text())
env=os.environ.copy();env.update(HOME=str(r/'local-runtime'),TMPDIR=str(r/'local-runtime/tmp'))
spec=importlib.util.spec_from_file_location('cpio_reader',r/'scripts/cpio-reader.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
projects={'base':'Tizen-Base','unified':'Tizen-Unified'};plan=[]
for p in packages:
 project=projects[p['repo']];base=f'https://download.tizen.org/snapshots/TIZEN/Tizen/{project}/reference/repos/standard/debug/'
 links=re.findall('href="([^"]+\\.rpm)"',(private/(project+'-debug.html')).read_text())
 q=p['rpm_query'].strip().split('\t');desired=q[0]+'-debuginfo-'+q[1]+'-'+q[2]+'.'+q[3]+'.rpm'
 matches=[n for n in links if unquote(n)==desired]
 plan.append({'package':p['filename'],'debug_filename':desired,'repo':p['repo'],'url':urljoin(base,matches[0]) if matches else None})
def download(p):
 if not p['url']:p['error']='Exact-NEVRA debug RPM not listed';return p
 path=private/'download'/p['debug_filename']
 with path.with_suffix('.curl.txt').open('w') as log:
  proc=subprocess.run(['curl','-fL','--retry','1','--connect-timeout','20','--max-time','180','-D',str(path.with_suffix('.headers')),p['url'],'-o',str(path)],stdout=log,stderr=subprocess.STDOUT,env=env)
 p['curl_exit']=proc.returncode
 if proc.returncode:p['error']='Debug download failed';return p
 p['sha256']=hashlib.sha256(path.read_bytes()).hexdigest();p['bytes']=path.stat().st_size
 cpio=private/'extract'/(p['debug_filename']+'.cpio')
 with cpio.open('wb') as f:proc=subprocess.run(['rpm2cpio',str(path)],stdout=f,stderr=subprocess.PIPE,env=env)
 p['rpm2cpio_exit']=proc.returncode;p['rpm2cpio_stderr']=proc.stderr.decode()
 if proc.returncode:return p
 extracted=[];directory=private/'debug'/p['debug_filename'];directory.mkdir(parents=True,exist_ok=True)
 for name,content in mod.regular_files(cpio.read_bytes()):
  relative=Path(name.removeprefix('./').lstrip('/'));assert '..' not in relative.parts
  if content.startswith(b'\x7fELF'):
   dest=directory/relative;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(content);extracted.append(str(dest.relative_to(r)))
 p['debug_elf_files']=extracted;print(p['debug_filename'],p['bytes'],len(extracted),flush=True);return p
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:debug=list(pool.map(download,plan))
(private/'debug-packages.json').write_text(json.dumps(debug,indent=2)+'\n')
def sections(path):
 data=path.read_bytes();assert data[:6]==b'\x7fELF\x01\x01'
 shoff=struct.unpack_from('<I',data,32)[0];ents,count,names=struct.unpack_from('<HHH',data,46)
 table=[struct.unpack_from('<10I',data,shoff+i*ents) for i in range(count)];names_blob=data[table[names][4]:table[names][4]+table[names][5]]
 return {names_blob[t[0]:names_blob.find(b'\0',t[0])].decode():data[t[4]:t[4]+t[5]] for t in table if t[1]!=8}
def readelf(args,path):
 proc=subprocess.run(['readelf',*args,str(path)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,env=env)
 return proc.returncode,proc.stdout.decode(errors='replace')
records=[]
for s in samples:
 target=r/s['local_path'];raw=[]
 for args in [['-p','.comment'],['-p','.GCC.command.line'],['--debug-dump=info','--dwarf-depth=1','--debug-dump=no-follow-links'],['-n'],['-S']]:
  code,text=readelf(args,target);raw.extend(['COMMAND readelf '+' '.join(args)+' <MAIN_ELF>', 'EXIT '+str(code),text])
 sec=sections(target);record={**s,'compiler':'Unknown','main_comment_missing':'.comment' not in sec,'main_debug_info_present':'.debug_info' in sec or '.zdebug_info' in sec,'producer_evidence':[]}
 if '.gnu_debuglink' in sec:
  blob=sec['.gnu_debuglink'];nul=blob.index(0);filename=blob[:nul].decode();offset=(nul+1+3)&~3;crc=struct.unpack_from('<I',blob,offset)[0]
  record.update(debuglink_filename=filename,debuglink_crc32=f'{crc:08x}')
  package=next(p for p in debug if p['package']==s['package'])
  candidates=[r/p for p in package.get('debug_elf_files',[]) if Path(p).name==filename]
  matches=[p for p in candidates if zlib.crc32(p.read_bytes())==crc]
  if len(matches)==1:
   debug_file=matches[0];record.update(debug_match='exact filename + CRC32',debug_sha256=hashlib.sha256(debug_file.read_bytes()).hexdigest(),debug_package=package['debug_filename'],debug_rpm_sha256=package['sha256'],debug_url=package['url'])
   code,notes=readelf(['-n'],debug_file);main_code,main_notes=readelf(['-n'],target)
   ids=lambda t:re.findall(r'Build ID: ([0-9a-f]+)',t)
   record['main_build_ids']=ids(main_notes);record['debug_build_ids']=ids(notes);record['build_id_match']=bool(ids(notes)) and ids(main_notes)==ids(notes)
   raw.extend(['DEBUG_MATCH exact filename+CRC32 '+filename,'DEBUG_SHA256 '+record['debug_sha256'],'COMMAND readelf -n <MATCHED_DEBUG_ELF>','EXIT '+str(code),notes])
   code,text=readelf(['--debug-dump=info','--dwarf-depth=1','--debug-dump=no-follow-links'],debug_file)
   (private/'debug'/(s['id']+'.cu-producers.raw.txt')).write_text(text)
   producers=[line for line in text.splitlines() if 'DW_AT_producer' in line]
   record['producer_evidence']=list(dict.fromkeys(producers))
   raw.extend(['COMMAND readelf --debug-dump=info --dwarf-depth=1 --debug-dump=no-follow-links <MATCHED_DEBUG_ELF>','EXIT '+str(code),'PROJECTION only DW_AT_producer lines (CU filenames/other attributes remain private):',*record['producer_evidence']])
   diagnostics=[line for line in text.splitlines() if line.startswith('readelf:')];raw.extend(diagnostics);record['producer_readelf_exit']=code;record['diagnostics']=diagnostics
   joined='\n'.join(producers)
   gcc=bool(re.search(r'GNU (C|C\+\+)',joined));clang='clang version' in joined or 'LLVM' in joined
   if gcc and not clang:record['compiler']='GCC'
   elif clang and not gcc:record['compiler']='LLVM/Clang'
   elif gcc and clang:record['compiler']='Mixed GCC/Clang'
  else:record['debug_match']='Unknown: '+str(len(matches))+' CRC matches';raw.append(record['debug_match'])
 else:record['debug_match']='Unknown(no .gnu_debuglink)'
 record['evidence_path']='raw/'+s['id']+'-compiler.txt'
 text='\n'.join(raw).replace(str(r.resolve()),'<SURVEY_ROOT>').replace(str(r),'<SURVEY_ROOT>');(r/record['evidence_path']).write_text(text+'\n');records.append(record)
(private/'compiler-records.json').write_text(json.dumps(records,indent=2)+'\n')
public=[{k:v for k,v in rec.items() if k not in ['local_path']} for rec in records]
(r/'gcc-compiler-evidence.json').write_text(json.dumps(public,indent=2)+'\n')
lines=['Compiler classification from matching debug ELF: .gnu_debuglink filename+CRC32 and GNU build-id compared; only producer lines published.','id\tmain package\tcompiler\tdebug package\tmatch\tbuild-id match\tunique producer strings\tevidence']
for rec in records:
 versions=list(dict.fromkeys(re.sub(r'^.*DW_AT_producer\s*:\s*(?:\([^)]*\):\s*)?','',line) for line in rec['producer_evidence']))
 lines.append('\t'.join([rec['id'],rec['package'],rec['compiler'],rec.get('debug_package','Unknown'),rec['debug_match'],str(rec.get('build_id_match','Unknown')),' | '.join(versions),rec['evidence_path']]))
(r/'gcc-compiler-evidence.txt').write_text('\n'.join(lines)+'\n')
(r/'debug-download-status.json').write_text(json.dumps([{k:v for k,v in p.items() if k!='debug_elf_files'} for p in debug],indent=2)+'\n')
print('Compiler counts:',{name:sum(rec['compiler']==name for rec in records) for name in ['GCC','LLVM/Clang','Mixed GCC/Clang','Unknown']})
