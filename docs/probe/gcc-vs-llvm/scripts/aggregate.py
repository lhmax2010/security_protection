#!/usr/bin/env python3
from pathlib import Path
import json,re,collections,hashlib
r=Path(__file__).resolve().parents[1];probe=r.parent
gcc=json.loads((r/'gcc-hardening-matrix.json').read_text())['rows']
llvm27=json.loads((probe/'board-survey/hardening-matrix.json').read_text())['rows']
codec=[]
for line in (probe/'ffmpeg-demo/board-target-elf-metadata.txt').read_text().splitlines():
 if line.startswith('FIELD\t'):k,v=line.split('\t')[1:3];codec.append((k,v))
codec=dict(codec);codec.update(id='libavcodec',path='/usr/lib/libavcodec.so.62.11.100',kind='shared-library',raw_evidence='../ffmpeg-demo/board-target-elf-metadata.txt',compiler='Unknown (LLVM board label only)')
llvm28=llvm27+[codec]
for row in llvm28:
 original=(probe/'board-survey'/row['raw_evidence']) if row['id']!='libavcodec' else probe/'ffmpeg-demo/board-target-elf-metadata.txt'
 text=original.read_text();exports=[line.split('\t') for line in text.splitlines() if line.startswith('EXPORT\t') and line.split('\t')[4]!='65521']
 row['export_Cpp_mangled']=sum(x[5].startswith('_Z') for x in exports)
 row['raw_evidence_source']=str(original.relative_to(probe))
 row['source_sha256']=hashlib.sha256(original.read_bytes()).hexdigest()
lookup={x['id']:x for x in llvm28};matched=[lookup[x['id']] for x in gcc]
def stats(rows):
 result={};rules=[('Full RELRO','RELRO','Full'),('NX','NX','Enabled'),('stripped','stripped','Yes(no .symtab)'),('FORTIFY import','FORTIFY','Detected(import)'),('canary / stack-protector import','canary','Detected(import)'),('PIE executable','PIE','Yes')]
 for title,key,value in rules:
  group=[x for x in rows if x['kind']=='executable'] if key=='PIE' else rows
  positives=sum(x[key]==value for x in group);result[title]={'numerator':positives,'denominator':len(group),'percent':round(100*positives/len(group),2),'distribution':dict(collections.Counter(x[key] for x in group))}
 return result
pairs=[]
for g in gcc:
 b=lookup[g['id']];pairs.append({'id':g['id'],'GCC':{k:g.get(k) for k in ['RELRO','NX','PIE','canary','FORTIFY','stripped','dynamic_export_non_ABS_count','export_Cpp_mangled','rodata_ascii_min8_runs','raw_evidence','compiler','compiler_version','producer_stack_protector_flags','producer_visibility_flags']},'LLVM_board':{k:b.get(k) for k in ['RELRO','NX','PIE','canary','FORTIFY','stripped','dynamic_export_non_ABS_count','export_Cpp_mangled','raw_evidence_source','source_sha256']}})
result={'GCC16':stats(gcc),'LLVM_board_27_historical':stats(llvm27),'LLVM_board_28_with_codec':stats(llvm28),'LLVM_board_matched16':stats(matched),'matched_pairs':pairs,'cohort_limits':['Non-random, targeted samples; package versions/releases/config differ','Reference GCC16 confirmed from matching debug; LLVM board userland compilers unconfirmed, no new board commands','DSOs excluded from PIE denominator','canary and stack protector share one import-evidence axis','provider-only libc excluded from positive FORTIFY/canary numerators','historical board .rodata min8 count unavailable; never invent same-metric counts']}
(r/'comparison-data.json').write_text(json.dumps(result,indent=2)+'\n')
(r/'raw/llvm-evidence-reuse.json').write_text(json.dumps({'method':'existing saved evidence read locally only; no board connection/measurement','rows':[{k:x.get(k) for k in ['id','RELRO','NX','PIE','canary','FORTIFY','stripped','dynamic_export_non_ABS_count','export_Cpp_mangled','raw_evidence_source','source_sha256']} for x in llvm28]},indent=2)+'\n')
(r/'gcc-hardening-summary.txt').write_text('GCC verified reference sample: 16 ELF (6 executable, 10 DSO).\n'+'\n'.join(f'{k}: {v["numerator"]}/{v["denominator"]} = {v["percent"]}%; {v["distribution"]}' for k,v in result['GCC16'].items())+'\n')
print(json.dumps({k:result[k] for k in ['GCC16','LLVM_board_matched16']},indent=2))
