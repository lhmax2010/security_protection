#!/usr/bin/env python3
from pathlib import Path
import json,hashlib,re,subprocess
root=Path.cwd();base=root/'docs/probe';e=base/'evidence'
manifest_path=e/'artifact-manifest.json';audit_path=e/'final-audit.json'
files=sorted(p for directory in [e,base/'samples'] for p in directory.rglob('*') if p.is_file() and p not in [manifest_path,audit_path] and 'obj' not in p.parts and not (base/'samples/dotnet/bin') in p.parents)
manifest={'excludes':['artifact-manifest.json','final-audit.json','dotnet/obj','dotnet/bin'], 'files':[{'path':str(p.relative_to(root)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files]}
manifest_path.write_text(json.dumps(manifest,indent=2)+'\n')
checks=[]
def check(label,okay,detail):checks.append({'check':label,'pass':bool(okay),'detail':detail})
links=re.findall(r'\]\((evidence/[^)]+)\)',(base/'STATE.md').read_text())
check('STATE evidence links exist',all((base/x).is_file() for x in links),{'count':len(links),'missing':[x for x in links if not (base/x).is_file()]})
check('manifest bytes and hashes',all((root/f['path']).stat().st_size==f['bytes'] and hashlib.sha256((root/f['path']).read_bytes()).hexdigest()==f['sha256'] for f in manifest['files']),{'file_count':len(manifest['files'])})
for name in ['target_c_gcc_armv7l','target_c_llvm_armv7l','target_rust_armv7l']:
 p=e/name;j=json.loads((p/'target-identity.json').read_text());b=base/'samples/bin'/name
 check(name+' identity',j['sha256']==hashlib.sha256(b.read_bytes()).hexdigest(),j)
 for fn in ['secret_transform','simple_checksum']:
  j=json.loads((p/(fn+'-pseudocode.decoded.json')).read_text())
  check(name+' '+fn+' actual Ghidra pseudocode',j['provider']['id']=='ghidra' and j['provider']['version']=='12.1.4' and isinstance(j['normalized_result'],str),{'evidence_id':j['evidence_id']})
 check(name+' ARM32 unstripped',all(t in (e/(name+'-file.txt')).read_text() for t in ['ELF 32-bit','ARM','not stripped']),str(e/(name+'-file.txt')))
 check(name+' session closed',not json.loads((p/'close.json').read_text()).get('isError'),str(p/'close.json'))
check('Python rejection preserved',json.loads((e/'target_py.pyc/open.json').read_text()).get('isError') is True,str(e/'target_py.pyc/open.json'))
check('Codex Ghidra scoped readiness',json.loads((e/'doctor-codex.json').read_text())['healthy'] is True,str(e/'doctor-codex.json'))
check('unscoped doctor failure preserved',json.loads((e/'doctor.txt.meta.json').read_text())['exit_code']==1,str(e/'doctor.txt'))
check('Ghidra official archive hash',json.loads((e/'ghidra-archive-hash.json').read_text())['matches_official'] is True,str(e/'ghidra-archive-hash.json'))
text=(e/'target_js.js/recovered/modules/bundle.js').read_text()
check('JS recovered anchors',all(t in text for t in ['secret_transform','simple_checksum','LICENSE_KEY_CHECK_V1','23063','33','65535']),str(e/'target_js.js/recovered/modules/bundle.js'))
j=json.loads((e/'target_dotnet.dll/supplemental/imported-reconstruction.decoded.json').read_text())
check('NET REA import inference retained',j['confidence']=='inferred' and j['normalized_result']['summary']['imported_methods']==3 and not j['normalized_result']['executed'],str(e/'target_dotnet.dll/supplemental/imported-reconstruction.decoded.json'))
j=json.loads((e/'target_rust_armv7l/supplemental/marker-bytes.decoded.json').read_text())['normalized_result']
check('Rust REA marker bytes',j['complete'] and bytes.fromhex(j['bytes_hex'])==b'LICENSE_KEY_CHECK_V1',j)
j=json.loads((e/'runtime-smoke-summary.json').read_text())
check('30 runtime cases agree',j['case_count']==30 and j['all_six_artifacts_equal_stdout_and_zero_exit'],j)
report={'checks':checks,'passed':sum(x['pass'] for x in checks),'failed':sum(not x['pass'] for x in checks),'scope':'Artifact integrity, references, required measured results and preserved known failures; not all-input proof of reconstructed code.'}
audit_path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='checks'}));raise SystemExit(report['failed']!=0)
