#!/usr/bin/env python3
import json,re,sys
from pathlib import Path
name=sys.argv[1];base=Path('docs/probe/evidence');d=base/name
ps=json.loads((d/'procedures.decoded.json').read_text())['normalized_result']
syms={}
for l in (base/(name+'-readelf.txt')).read_text().splitlines():
 m=re.match(r'\s*\d+:\s+([0-9a-fA-F]+)\s+\d+\s+FUNC\s+\S+\s+\S+\s+(\S+)\s+(\S+)',l)
 if m and m[2] not in ['UND','ABS']:
  a=int(m[1],16)&~1; syms[(a,m[3])]=True
secret=[(a,n) for a,n in syms if n=='secret_transform'][0]
probe=next(x for x in ps if x['value']=='secret_transform')
slide=int(probe['address'],16)-secret[0]
byaddr={}
for p in ps:
 if p['address'].startswith('0x'):byaddr.setdefault(int(p['address'],16),[]).append(p['value'])
rows=[]
for a,n in sorted(syms):
 observed=byaddr.get(a+slide,[])
 rows.append({'elf_address':hex(a),'ghidra_address':hex(a+slide),'elf_name':n,'observed_names':observed,'entry_recovered':bool(observed),'exact_name_recovered':n in observed})
metrics={'method':'unique defined ELF STT_FUNC (entry with ARM Thumb low bit cleared, symbol name); UND/ABS excluded; duplicate dynsym/symtab rows deduplicated; Ghidra image slide measured from secret_transform. Exact name is stricter than demangled-name recovery; aliases count separately. This is not all data-symbol recovery.','image_slide':hex(slide),'denominator':len(rows),'entry_recovered':sum(r['entry_recovered'] for r in rows),'exact_name_recovered':sum(r['exact_name_recovered'] for r in rows),'rea_procedure_count_including_imports_thunks':len(ps),'rows':rows}
(d/'symbol-recovery-metrics.json').write_text(json.dumps(metrics,indent=2)+'\n')
for f in d.glob('*-pseudocode.decoded.json'):
 j=json.loads(f.read_text());v=j.get('normalized_result')
 if isinstance(v,str):(d/(f.name.replace('-pseudocode.decoded.json','-pseudocode.c'))).write_text(v)
for f in d.glob('*-assembly.decoded.json'):
 j=json.loads(f.read_text());v=j.get('normalized_result')
 if isinstance(v,str):(d/(f.name.replace('-assembly.decoded.json','-assembly.asm'))).write_text(v+'\n')
print(name,{k:v for k,v in metrics.items() if k!='rows'})
