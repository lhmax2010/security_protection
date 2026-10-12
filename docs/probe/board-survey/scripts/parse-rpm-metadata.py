#!/usr/bin/env python3
from pathlib import Path
import re,json
r=Path(__file__).resolve().parents[1];capture=(r/'hardening-capture.txt').read_text();candidates=json.loads((r/'samples.json').read_text());rows=[];excluded=[]
assert re.search(r'(?m)^SOURCE_INTEGRITY_VERIFIED [0-9a-f]{64}$',capture),'No actual transport integrity success'
for s in candidates:
 match=re.search(r'(?ms)^@@BEGIN_SAMPLE '+re.escape(s['id'])+r'\n(.*?)^@@END_SAMPLE '+re.escape(s['id'])+r'\s*$',capture);assert match,s['id']
 raw=match[1];path=r/'raw'/(s['id']+'.txt');assert not path.exists();path.write_text(raw)
 fields={l.split('\t')[1]:l.split('\t')[2] for l in raw.splitlines() if l.startswith('FIELD\t')}
 if not re.search(r'(?m)^METADATA_READER_SUCCESS$',raw):
  excluded.append({**s,'reason':'not an ELF file' if 'not an ELF file' in raw else 'metadata reader failed','raw_evidence':str(path.relative_to(r))});continue
 assert re.search(r'(?m)^RPM_LUA_EXIT_CODE: 0$',raw);assert re.search(r'(?m)^READELF_EXIT_CODE: 127$',raw)
 header=next(l for l in raw.splitlines() if l.startswith('HEADER\t')).split('\t');assert header[2]=='ELF32' and header[8]=='40',header
 for key in ['RELRO','canary','NX','PIE','RPATH','RUNPATH','stripped','FORTIFY']:assert key in fields
 rows.append({**s,**fields,'elf_class':'ELF32','elf_machine':'ARM (EM_ARM=40)','method':'existing RPM4.14.1 Lua5.1 direct metadata; readelf unavailable','readelf_exit_code':127,'metadata_reader_exit_code':0,'raw_evidence':str(path.relative_to(r))})
(r/'samples-candidates.json').write_text(json.dumps(candidates,ensure_ascii=False,indent=2)+'\n')
(r/'excluded-candidates.json').write_text(json.dumps(excluded,ensure_ascii=False,indent=2)+'\n')
valid=[s for s in candidates if s['id'] in {x['id'] for x in rows}];assert 20<=len(valid)<=40
(r/'samples.json').write_text(json.dumps(valid,ensure_ascii=False,indent=2)+'\n')
lines=[f'实际ELF样本：{len(valid)}份（{sum(s["kind"]=="executable" for s in valid)}系统可执行、{sum(s["kind"]=="shared-library" for s in valid)}平台共享库）。非随机全平台抽样。','原先28候选中vconftool经板上魔数读取判为非ELF，排除但保留原始错误，不读取或回传其脚本正文。','id\t原路径\t类别\t选择理由\t真实路径']+['\t'.join([s['id'],s['path'],s['kind'],s['reason'],s['resolved_path']]) for s in valid]
(r/'sample-list.txt').write_text('\n'.join(lines)+'\n')
(r/'hardening-matrix.json').write_text(json.dumps({'rows':rows,'excluded':excluded,'method':'NO BOARD READELF/NM/CHECKSEC AVAILABLE. Explicitly labeled direct ELF metadata decoded on board by preexisting RPM embedded Lua. No decoder installed or written to board.','limitations':['Raw files contain actual readelf command-not-found errors and separate actual replacement metadata output; they are not successful readelf output.','Canary/FORTIFY reflect dynamic imported helper evidence, not source compiler flags or all-function coverage. Definition-only runtime providers are not counted as instrumentation.','NX describes GNU_STACK executable flag request, not runtime verification.','PIE is N/A for DSOs; stripped means .symtab absent, not dynamic names hidden.']},ensure_ascii=False,indent=2)+'\n')
columns=['id','path','kind','RELRO','canary','NX','PIE','RPATH','RUNPATH','stripped','FORTIFY']
text=['METHOD: board existing RPM embedded Lua direct ELF metadata; readelf/nm/checksec unavailable. Actual failures and alternative output both preserved in raw/.','\t'.join(columns)]+['\t'.join(str(x[k]) for k in columns) for x in rows]
text+=['','LIMITATIONS: DSO PIE=N/A; dynamic helper imports are evidence only; definition-only libc does not prove FORTIFY/canary; NX is ELF request; .symtab removal does not remove .dynsym.','EXCLUDED: '+json.dumps(excluded,ensure_ascii=False)]
(r/'hardening-matrix.txt').write_text('\n'.join(text)+'\n');print(json.dumps({'actual_elf_samples':len(rows),'excluded':excluded},ensure_ascii=False))
