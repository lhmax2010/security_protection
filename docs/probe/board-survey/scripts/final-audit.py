#!/usr/bin/env python3
from pathlib import Path
import json,re,hashlib,subprocess,ast
r=Path(__file__).resolve().parents[1];workspace=r.parents[2];checks=[]
def check(name,condition,detail=None):checks.append({'check':name,'passed':bool(condition),'detail':detail})
rows=json.loads((r/'hardening-matrix.json').read_text())['rows'];summary=json.loads((r/'hardening-summary.json').read_text());symbols=json.loads((r/'symbol-exposure.json').read_text())['libraries'];net=json.loads((r/'net-config-after/validation.json').read_text());platform=json.loads((r/'platform-mechanisms-summary.json').read_text())
check('27 real ARM ELF rows',len(rows)==27 and all(x['elf_machine']=='ARM (EM_ARM=40)' for x in rows))
check('11 executable and 16 DSO',sum(x['kind']=='executable' for x in rows)==11 and len(symbols)==16)
for row in rows:
 raw=(r/row['raw_evidence']).read_text();fields={l.split('\t')[1]:l.split('\t')[2] for l in raw.splitlines() if l.startswith('FIELD\t')}
 check(row['id']+' actual decoder fields and preserved readelf failure',bool(re.search(r'(?m)^METADATA_READER_SUCCESS$',raw)) and 'READELF_EXIT_CODE: 127' in raw and all(fields.get(k)==row[k] for k in ['RELRO','canary','NX','PIE','RPATH','RUNPATH','stripped','FORTIFY']))
check('reference reader validation passed',json.loads((r/'validation/comparison.json').read_text())['all_agree'])
check('whole batch source integrity checked',bool(re.search(r'(?m)^SOURCE_INTEGRITY_VERIFIED [0-9a-f]{64}$',(r/'hardening-capture.txt').read_text())))
expected={'PIE (executables only)':(11,11),'Full RELRO':(8,27),'NX ELF GNU_STACK request':(27,27),'stripped (.symtab absent)':(27,27),'FORTIFY imported-helper evidence':(17,27),'canary imported-helper evidence':(21,27)}
check('summary denominators and positive counts',all((summary['stats'][k]['numerator'],summary['stats'][k]['denominator'])==v for k,v in expected.items()))
check('network prior backup and after config', (r/'net-config-backup/var/lib/connman/ethernet_2ccf67a072b5_cable/settings').is_file() and (r/'net-config-after/var/lib/connman/ethernet_2ccf67a072b5_cable/settings').is_file())
check('network fields syntax and no reboot',net['ini_syntax_parsed'] and net['runtime_nameservers_configuration_matches'] and not net['reboot_performed'])
check('current independent final readback succeeded','FINAL_READBACK_SUCCESS_NO_REBOOT' in (r/'final-readback.txt').read_text())
check('SMACK ASLR and readonly root observed',platform['smackfs_mounted'] and platform['ASLR_randomize_va_space']==2 and platform['root_readonly'])
check('candidate exclusion preserved',json.loads((r/'excluded-candidates.json').read_text())[0]['reason']=='not an ELF file')
state=(workspace/'docs/probe/STATE.md').read_text();links=re.findall(r'\]\((board-survey/[^)]+)\)',state)
check('STATE survey evidence links exist',all((workspace/'docs/probe'/x).is_file() for x in links),{'count':len(links),'missing':[x for x in links if not (workspace/'docs/probe'/x).is_file()]})
files=[]
for p in sorted(r.rglob('*')):
 if not p.is_file() or any(x in ['local-runtime','ssh','__pycache__'] for x in p.relative_to(r).parts) or p.name in ['metadata-manifest.json','final-audit.json']:continue
 data=p.read_bytes();check(str(p.relative_to(r))+' text metadata or authored source only',not data.startswith(b'\x7fELF') and b'\x00' not in data)
 try:data.decode('utf8');valid=True
 except UnicodeDecodeError:valid=False
 check(str(p.relative_to(r))+' UTF8 text',valid)
 files.append({'path':str(p.relative_to(workspace)),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
for p in (r/'scripts').glob('*.py'):ast.parse(p.read_text(),filename=str(p))
for p in (r/'scripts').glob('*.sh'):
 result=subprocess.run(['bash','-n',str(p)],capture_output=True,text=True);check(str(p.relative_to(r))+' host shell syntax',result.returncode==0,result.stderr or None)
manifest={'files':files,'excluded':['local-runtime (ignored SDB runtime)','ssh (ignored SSH trust runtime)','__pycache__','metadata-manifest.json','final-audit.json'],'policy':'All included files are textual board metadata/configuration or authored collector source. No board binary, firmware or private source payload was retrieved.'}
(r/'metadata-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
report={'passed':sum(x['passed'] for x in checks),'failed':sum(not x['passed'] for x in checks),'checks':checks,'limits':'No reboot was performed; board readelf/nm/checksec remain unavailable. The replacement decoder was independently compared against host readelf and executed on-board.'}
(r/'final-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'passed':report['passed'],'failed':report['failed'],'file_count':len(files)}));raise SystemExit(report['failed']!=0)
