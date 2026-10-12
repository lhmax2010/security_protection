#!/usr/bin/env python3
import json,re,hashlib
from pathlib import Path
root=Path.cwd();d=root/'docs/probe/evidence/target_dotnet.dll'
evidence=json.loads((d/'members.decoded.json').read_text())
text=(d/'ilspy-decompiled.cs').read_text()
version=(d/'ilspy-version.txt').read_text()
methods=[]
for m in evidence['normalized_result']['methods']:
 pattern=r'(?m)^\s*public static [^\n]*\b'+re.escape(m['name'])+r'\([^\n]*\)\s*$'
 match=re.search(pattern,text)
 if not match:raise RuntimeError('Cannot locate ILSpy method: '+m['name'])
 start=match.start();brace=text.index('{',match.end());depth=1;end=brace+1
 # This small fixture has no brace literals in its method body except interpolated expressions;
 # paired interpolation braces are balanced and do not change the final boundary.
 while depth:
  if text[end]=='{':depth+=1
  elif text[end]=='}':depth-=1
  end+=1
 method_text=text[start:end]
 methods.append({'token':m['token'],'signature_sha256':m['signature']['raw_sha256'],'normalized_il_sha256':m['body']['normalized_il_sha256'],'reconstruction':{'kind':'decompiled-csharp','language':'csharp','text':method_text,'text_sha256':hashlib.sha256(method_text.encode()).hexdigest(),'source_path':str(d/'ilspy-decompiled.cs'),'start_line':text[:start].count('\n')+1,'end_line':text[:end].count('\n')+1}})
request={'static_members':evidence,'decompiler':{'name':'ilspycmd','version':re.search(r'9\.1\.0\.7988',version)[0],'family':'ilspy','executable_sha256':hashlib.sha256((root/'.local-tools/dotnet-tools/ilspycmd').read_bytes()).hexdigest(),'options':['-t','BareBaseline']},'methods':methods,'notes':['External ILSpy C# is imported as reconstruction inference, not REA canonical parser source recovery. Original combined stdout/stderr log retained; method text sliced from actual ILSpy output.']}
(d/'followup-plan.json').write_text(json.dumps([{'label':'imported-reconstruction','tool':'import_managed_reconstruction','arguments':request}],indent=2)+'\n')
print([(m['token'],m['reconstruction']['start_line'],m['reconstruction']['end_line']) for m in methods])
