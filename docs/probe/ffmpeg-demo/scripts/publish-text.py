#!/usr/bin/env python3
"""Project reviewed REA text; never copy artifacts or full board string inventories."""
from pathlib import Path
import json,sys,hashlib,re
r=Path(__file__).resolve().parents[1];variant=sys.argv[1]
assert variant in ('board','upstream','upstream-stripped')
src=r/'private/rea'/variant;dst=r/variant;dst.mkdir(exist_ok=True)
workspace=str(r.parents[2])
def sanitize(text):
 return text.replace(str(r/'private/board-libavcodec.so'),'<LOCAL_BOARD_SAMPLE_A>').replace(str(r),'<DEMO_ROOT>').replace(workspace,'<WORKSPACE>')
def copy(p,base):
 q=dst/p.relative_to(base);q.parent.mkdir(parents=True,exist_ok=True);q.write_text(sanitize(p.read_text()))
for name in ['open','overview','procedures','close']:
 for suffix in ['.json','.decoded.json']:
  p=src/(name+suffix)
  if p.exists():copy(p,src)
for name in ['identity.json','requests.json','server-version.json']:copy(src/name,src)
for fn in ['avcodec_align_dimensions2','av_get_audio_frame_duration2','av_packet_rescale_ts']:
 for p in (src/fn).glob('*.json'):copy(p,src)
 o=json.loads((src/fn/'pseudocode.decoded.json').read_text());assert isinstance(o['normalized_result'],str) and o['normalized_result'].strip()
 (dst/fn/'pseudocode.c').write_text(o['normalized_result'])
helper=r/'private/rea'/(variant+'-helper')
if helper.exists():
 for p in (helper/'av_get_audio_frame_duration2/helper').glob('*.json'):copy(p,helper)
 o=json.loads((helper/'av_get_audio_frame_duration2/helper/pseudocode.decoded.json').read_text())
 (dst/'av_get_audio_frame_duration2/helper/pseudocode.c').write_text(o['normalized_result'])
p=src/'strings.decoded.json';obj=json.loads(p.read_text());allstrings=obj['normalized_result']
# Explicit public FFmpeg strings only; other strings remain local, not treated as absent.
whitelist={'avcodec_align_dimensions2','av_get_audio_frame_duration2','av_packet_rescale_ts','FFmpeg version 8.0.1','Lavc62.11.100','pcm_s16le','h264','Invalid packet stream index: %d\n','Invalid extradata size: %d\n'}
samples=[s for s in allstrings if s.get('value') in whitelist]
assert samples
projection={k:obj[k] for k in ['evidence_id','subject','provider','operation','limitations']}
projection.update(projection='whitelisted samples from original list_strings Evidence, not the complete raw response',raw_local_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),total_defined_strings=len(allstrings),samples=samples)
(dst/'strings-samples.json').write_text(sanitize(json.dumps(projection,indent=2))+'\n')
procs=json.loads((src/'procedures.decoded.json').read_text())
local=[p for p in procs['normalized_result'] if not p.get('procedure',{}).get('external') and not p.get('procedure',{}).get('thunk')]
named=[p for p in local if not re.match(r'^(FUN_|thunk_FUN_)',p['value'])]
metrics={'variant':variant,'procedure_evidence_id':procs['evidence_id'],'all_procedures_including_imports_and_thunks':len(procs['normalized_result']),'local_non_thunk_procedures':len(local),'local_non_FUN_labels':len(named),'non_FUN_label_ratio_percent':round(100*len(named)/len(local),2),'ratio_limit':'Provider label proxy, not ground-truth original name recovery rate; synthetic entry/runtime labels can be included. Auto-analysis detects fewer boundaries after stripping.','string_evidence_id':obj['evidence_id'],'defined_strings':len(allstrings),'selected_string_samples':len(samples)}
(dst/'symbol-string-statistics.json').write_text(json.dumps(metrics,indent=2)+'\n')
(dst/'README.md').write_text('REA 6.4.0 + Ghidra 12.1.4 static analysis. Complete focused MCP replies and decoded Evidence retained for procedures; pseudocode.c is exact normalized pseudocode without manual renaming. Absolute local paths replaced with placeholders. Complete list_procedures is included; strings-samples is a labeled whitelist projection of list_strings, whose full raw record is retained locally. No board binary is included. Callee/caller results cover resolved references only; missing indirect calls remain unknown. The audio-duration helper was located via its sole direct callee, with a separate ephemeral import after closing the main session.\n')
print(json.dumps(metrics))
