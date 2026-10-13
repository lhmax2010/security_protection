#!/usr/bin/env python3
from pathlib import Path
import json,struct,hashlib,re,subprocess
r=Path(__file__).resolve().parents[1]
variants=['board','upstream','upstream-stripped'];functions=['avcodec_align_dimensions2','av_get_audio_frame_duration2','av_packet_rescale_ts']
result={'variants':{},'unstripped_vs_stripped_pseudocode_identical':{},'strip_section_identity':{},'public_binary_provenance':{},'limits':'Static-only audit; no original source parameter names recovered; no dynamic testing or full-library code-equivalence proof.'}
for v in variants:
 d=r/v;identity=json.loads((d/'identity.json').read_text());out={**identity,'metrics':json.loads((d/'symbol-string-statistics.json').read_text()),'functions':{}}
 for fn in functions:
  detail={}
  for op in ['search','info','pseudocode','assembly','callees','callers']:
   raw=json.loads((d/fn/(op+'.json')).read_text());assert not raw.get('isError') and not raw.get('transport_error'),(v,fn,op)
   obj=json.loads((d/fn/(op+'.decoded.json')).read_text());assert obj.get('confidence')=='observed',(v,fn,op)
   assert obj['subject']['digest']['sha256']==identity['sha256']
   assert obj['provider']['id']=='ghidra' and obj['provider']['version']=='12.1.4'
   if op=='pseudocode':assert obj['normalized_result']==(d/fn/'pseudocode.c').read_text();assert len(obj['normalized_result'])>100
   detail[op+'_evidence_id']=obj['evidence_id']
   if op=='info':detail['address']=obj['normalized_result']['entrypoint']
  helper=d/fn/'helper'
  if helper.exists():
   obj=json.loads((helper/'pseudocode.decoded.json').read_text());assert obj['subject']['digest']['sha256']==identity['sha256']
   assert obj['normalized_result']==(helper/'pseudocode.c').read_text();detail['helper_evidence_id']=obj['evidence_id']
  out['functions'][fn]=detail
 result['variants'][v]=out
for fn in functions:
 result['unstripped_vs_stripped_pseudocode_identical'][fn]=(r/'upstream'/fn/'pseudocode.c').read_bytes()==(r/'upstream-stripped'/fn/'pseudocode.c').read_bytes()
def sections(p):
 data=p.read_bytes();assert data[:6]==b'\x7fELF\x01\x01'
 shoff=struct.unpack_from('<I',data,32)[0];size,count,names=struct.unpack_from('<HHH',data,46)
 table=[struct.unpack_from('<10I',data,shoff+i*size) for i in range(count)]
 strings=data[table[names][4]:table[names][4]+table[names][5]];out={}
 for row in table:
  end=strings.find(b'\0',row[0]);name=strings[row[0]:end].decode()
  if name in ['.text','.rodata','.dynsym','.dynstr']:out[name]={'bytes':row[5],'sha256':hashlib.sha256(data[row[4]:row[4]+row[5]]).hexdigest()}
 return out
un=sections(r/'upstream-artifacts/libavcodec-unstripped.so');st=sections(r/'upstream-artifacts/libavcodec-stripped.so')
assert un==st
result['strip_section_identity']={'identical':True,'unstripped':un,'stripped':st}
manifest=json.loads((r/'upstream-artifacts/manifest.json').read_text())
boardsha=result['variants']['board']['sha256']
for name,info in manifest.items():
 p=r/'upstream-artifacts'/name;sha=hashlib.sha256(p.read_bytes()).hexdigest();assert sha==info['sha256'] and sha!=boardsha
 result['public_binary_provenance'][name]=info
tracked=subprocess.check_output(['git','ls-files','docs/probe/ffmpeg-demo']).decode().splitlines()
assert not any('/private/' in n or '/local-runtime/' in n for n in tracked)
for n in tracked:
 p=Path(n)
 if p.read_bytes().startswith(b'\x7fELF'):assert p.name in manifest and '/upstream-artifacts/' in n
result['git_audit']={'private_or_runtime_files_tracked':False,'tracked_ELF_files':list(manifest),'board_binary_gitignored':subprocess.run(['git','check-ignore','-q',str((r/'private/board-libavcodec.so').relative_to(Path.cwd()))]).returncode==0}
assert result['git_audit']['board_binary_gitignored']
(r/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print('Verified three variants, all focused Evidence, identical code/rodata/dynsym/dynstr after strip, public ELF provenance, ignored board binary.')
