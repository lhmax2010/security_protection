#!/usr/bin/env python3
from pathlib import Path
import json,collections
r=Path(__file__).resolve().parents[1];rows=json.loads((r/'hardening-matrix.json').read_text())['rows'];libs=[x for x in rows if x['kind']=='shared-library'];results=[]
for row in libs:
 raw=(r/row['raw_evidence']).read_text();exports=[l.split('\t') for l in raw.splitlines() if l.startswith('EXPORT\t')];symbols=[l.split('\t') for l in raw.splitlines() if l.startswith('DYNAMIC_SYMBOL\t')]
 assert len(exports)==int(row['dynamic_export_count_including_ABS'])
 nonabs=[s for s in exports if s[4]!='65521'];assert len(nonabs)==int(row['dynamic_export_non_ABS_count'])
 vis=collections.Counter(s[8] for s in symbols if len(s)>=13 and s[10]!='0')
 names=[s[5] for s in nonabs];helper_names=[x for x in names if x.startswith('__') or x.startswith('_')]
 results.append({'path':row['path'],'exported_GLOBAL_WEAK_DEFAULT_PROTECTED_including_ABS':len(exports),'exported_non_ABS':len(nonabs),'exported_FUNC_IFUNC':int(row['dynamic_export_function_count']),'defined_dynamic_symbol_visibility_distribution':dict(vis),'exported_Cpp_mangled_names':sum(x.startswith('_Z') for x in names),'example_export_names':names[:12],'underscore_prefixed_examples':helper_names[:12],'raw_evidence':row['raw_evidence']})
report={'libraries':results,'export_policy_inference':'Mixed exposure. Every sampled DSO retains public/global/weak dynamic names, with counts ranging from small APIs to thousands. Stripping .symtab does not erase .dynsym. Counts alone cannot identify private/internal implementation symbols, original -fvisibility flags, or ABI export intent.','method':'Exact SHT_DYNSYM entries decoded on board by existing RPM Lua; all nm/readelf attempts explicitly unavailable, no binary copied.'}
(r/'symbol-exposure.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
lines=['METHOD: board-only RPM embedded Lua reads SHT_DYNSYM. nm -D/readelf --dyn-syms absent; real errors in symbol-tool-errors.txt.','EXPORT: defined GLOBAL/WEAK with DEFAULT/PROTECTED visibility; UND imports excluded; absolute version-label nodes reported separately.','path\texports excluding ABS\tfunction/IFUNC exports\texports including ABS\tC++ mangled exports\tfirst export examples']
for x in results:lines.append('\t'.join([x['path'],str(x['exported_non_ABS']),str(x['exported_FUNC_IFUNC']),str(x['exported_GLOBAL_WEAK_DEFAULT_PROTECTED_including_ABS']),str(x['exported_Cpp_mangled_names']),', '.join(x['example_export_names'])]))
lines+=['','结论：本批没有统一收缩到极少量动态接口的现象；部分Tizen API库仅几十个名字，基础库可达几百至几千。','所有样本删除.symtab，但动态API/运行库名字仍暴露。不能仅凭数量断言这些名字均为内部符号，也不能反推出源码默认-fvisibility设置。','通过原始EXPORT列表审计具体名称；JSON还保留underscore前缀示例与visibility计数。']
(r/'symbol-exposure.txt').write_text('\n'.join(lines)+'\n');print('\n'.join(lines))
