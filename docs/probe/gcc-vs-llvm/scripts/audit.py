#!/usr/bin/env python3
from pathlib import Path
import json,hashlib,re,subprocess
r=Path(__file__).resolve().parents[1];metrics=json.loads((r/'gcc-hardening-matrix.json').read_text())['rows'];compilers=json.loads((r/'gcc-compiler-evidence.json').read_text());data=json.loads((r/'comparison-data.json').read_text());checks={}
assert len(metrics)==len(compilers)==16
for c in compilers:
 assert c['compiler']=='GCC' and c['debug_match']=='exact filename + CRC32' and c['build_id_match']
 assert any(re.search(r'GNU (?:C[^ ]*|GIMPLE) 14\.2\.0',p) for p in c['producer_evidence']),c['id']
 assert (r/c['evidence_path']).exists()
checks['compiler_matched_debug_GCC14_2_0']=16
for row in metrics:
 source=r/row['local_path'];assert hashlib.sha256(source.read_bytes()).hexdigest()==row['sha256']
 raw=(r/row['raw_evidence']).read_text();assert 'METADATA_READER_SUCCESS' in raw and row['sha256'] in raw
 assert not re.search(r'^(DYNAMIC_SYMBOL|EXPORT)\t',raw,re.M)
 private=json.loads((r/'private/extract'/(row['id']+'.rodata-strings.json')).read_text());assert len(private)==row['rodata_ascii_min8_runs']
 assert row['stripped']=='Yes(no .symtab)' and row['NX']=='Enabled'
 assert row['canary']==row['stack_protector_evidence']
 assert row['rodata_sample_count']<=3
checks['ELF_hashes_and_raw_count_projections']=16
assert data['GCC16']['Full RELRO']['numerator']==4 and data['LLVM_board_matched16']['Full RELRO']['numerator']==3
for prop in ['NX','PIE executable','stripped','FORTIFY import','canary / stack-protector import']:
 assert data['GCC16'][prop]==data['LLVM_board_matched16'][prop]
assert len(data['matched_pairs'])==16
same=sum(p['GCC']['dynamic_export_non_ABS_count']==p['LLVM_board']['dynamic_export_non_ABS_count'] for p in data['matched_pairs']);assert same==15
assert sum('-fvisibility=hidden' in row['producer_visibility_flags'] for row in metrics)==7
checks['matched_pair_distribution_verified']=True;checks['equal_export_counts_in_matched16']=same
checks['REA_focused']={}
identity=json.loads((r/'rea/upstream/identity.json').read_text());codec=next(x for x in metrics if x['id']=='libavcodec');assert identity['sha256']==codec['sha256']
for fn in ['avcodec_align_dimensions2','av_packet_rescale_ts']:
 folder=r/'rea/upstream'/fn
 for op in ['search','info','pseudocode','assembly','callees','callers']:
  raw=json.loads((folder/(op+'.json')).read_text());ev=json.loads((folder/(op+'.decoded.json')).read_text())
  assert not raw.get('isError') and not raw.get('transport_error')
  assert ev['subject']['digest']['sha256']==codec['sha256'] and ev['provider']['id']=='ghidra' and ev['provider']['version']=='12.1.4'
 ev=json.loads((folder/'pseudocode.decoded.json').read_text());assert ev['normalized_result']==(folder/'pseudocode.c').read_text()
 board=json.loads((r.parent/'ffmpeg-demo/board'/fn/'pseudocode.decoded.json').read_text())
 assert '__stack_chk_guard' in ev['normalized_result'] and '__stack_chk_fail' in ev['normalized_result']
 assert '__stack_chk_guard' not in board['normalized_result'] and '__stack_chk_fail' not in board['normalized_result']
 checks['REA_focused'][fn]={'gcc_evidence':ev['evidence_id'],'board_reused_evidence':board['evidence_id'],'gcc_guard_and_fail_observed':True,'board_guard_and_fail_not_in_decompiled_function':True,'limit':'Only these two decompiled bodies; not whole-library SSP coverage or compiler flags.'}
checks['no_REA_full_symbol_or_string_inventory_requested']=not any(x['name'] in ['list_procedures','list_strings'] for x in json.loads((r/'rea/upstream/requests.json').read_text()))
assert checks['no_REA_full_symbol_or_string_inventory_requested']
tracked=subprocess.check_output(['git','ls-files','docs/probe/gcc-vs-llvm']).decode().splitlines();public=[]
for p in r.rglob('*'):
 if not p.is_file() or any(t in p.relative_to(r).parts for t in ['private','local-runtime','__pycache__']):continue
 blob=p.read_bytes();assert not blob.startswith((b'\x7fELF',b'\xed\xab\xee\xdb')) and b'\0' not in blob,p
 assert p.suffix not in ['.rpm','.so','.cpio','.sqlite'],p
 if p.parent==r/'raw':assert not re.search(r'^\s*\d+:\s+[0-9a-f]+\s+\d+\s+(?:FUNC|OBJECT|IFUNC|NOTYPE)',blob.decode(),re.M),p
 public.append(str(p.relative_to(r)))
assert not any('/private/' in p or '/local-runtime/' in p for p in tracked)
assert subprocess.run(['git','check-ignore','-q',str(r/'private/download/libavcodec-8.0.1-1.armv7l.rpm')]).returncode==0
checks.update(public_text_files_reviewed=len(public),no_private_or_runtime_files_tracked=True,no_new_board_connection='No sdb/ssh invoked; saved evidence only; see raw/llvm-evidence-reuse.json',limitations=['Public reference is proxy for company GCC products','LLVM userland compiler/flags unknown, no board remeasurement','Whole-library selective obfuscation/string handling and interface whitelist unavailable','Chat model-stream backend error remains unresolved; diagnostic logs/request IDs private only'])
(r/'audit.json').write_text(json.dumps(checks,indent=2)+'\n');print('Audit passed: 16 compiler matches, all ELF hashes/counts, matched denominators, focused REA evidence, text-only publication, ignored RPM/ELF/logs.')
