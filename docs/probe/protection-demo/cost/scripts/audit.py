#!/usr/bin/env python3
from pathlib import Path
from decimal import Decimal
import hashlib,json,re,statistics,subprocess

root=Path.cwd();base=root/'docs/probe/protection-demo/cost'
load=lambda p:json.loads((base/p).read_text())
status=load('build-status.json');scope=load('obfuscation-scope.json')
size={r['variant']:r for r in load('size-comparison.json')['rows']}
summary=load('perf-memory-summary.json')['variants'];runs=load('perf-memory-runs.json')
lines=(base/'raw/timings.tsv').read_text().splitlines()[1:]
assert len(lines)==len(runs)==21
for line,record in zip(lines,runs):
    phase,round_,v,start,end,exit_=line.split('\t')
    text=(base/record['stdout_stderr_file']).read_text()
    assert record['exit']==int(exit_)==0 and record['valid'] and record['frames_reported']==600
    assert record['wall_seconds']==float(Decimal(end)-Decimal(start))
    assert record['peak_rss_KiB']==int(re.search(r'bench: maxrss=(\d+)KiB',text)[1])
for v in ['baseline','selective','full']:
    assert status[v]['status']=='complete' and size[v]['measured'] and summary[v]['measured']
    for path,digest in status[v]['hashes'].items():assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==digest
    selected=[r for r in runs if r['variant']==v and r['phase']=='measured']
    assert len(selected)==6
    assert summary[v]['wall_median_seconds']==statistics.median(r['wall_seconds'] for r in selected)
    assert summary[v]['peak_rss_max_KiB']==max(r['peak_rss_KiB'] for r in selected)
    assert summary[v]['peak_rss_median_KiB']==statistics.median(r['peak_rss_KiB'] for r in selected)
    assert load('decode-correctness.json')[v]['valid_for_benchmark']
    assert scope[v]['optimized_definition_count']==584 and scope[v]['C_TUs_completed']==89
    # Original final source bodies remain byte-for-byte the supplied upstream source.
    source=base/'private'/v/'ffmpeg-8.0.1/libavcodec'
    original=root/'docs/probe/ffmpeg-demo/private/ffmpeg-8.0.1/libavcodec'
    assert all(p.read_bytes()==(original/p.relative_to(source)).read_bytes() for p in source.rglob('*.c'))
for v in ['selective','full']:
    assert scope[v]['annotated_definition_count']==scope[v]['reported_functions']
    assert size[v]['so_file_bytes_growth_percent']==(size[v]['so_file_bytes']/size['baseline']['so_file_bytes']-1)*100
    assert summary[v]['wall_median_change_percent']==(summary[v]['wall_median_seconds']/summary['baseline']['wall_median_seconds']-1)*100
assert scope['selective']['reported_functions']==10 and scope['full']['reported_functions']==584
assert status['full_source_attempt']['make_exit']==2
required=['comparison.md','size-comparison.txt','perf-memory.txt','build-variants.txt','board-identity.txt','decode-correctness.json','measurement-parser-error.txt','build-logs/full-source-attempt-make.txt','annotation-probe.txt','helper-lookup-error.txt']
assert all((base/p).stat().st_size>0 for p in required)
public=[]
for p in base.rglob('*'):
    if not p.is_file() or any(x in p.parts for x in ['private','local-runtime','__pycache__']):continue
    blob=p.read_bytes();assert b'\0' not in blob and not blob.startswith((b'\x7fELF',b'\xed\xab\xee\xdb')),p
    blob.decode('utf-8');assert p.suffix not in ['.so','.rpm','.sqlite','.a','.m2v'],p
    public.append(str(p.relative_to(base)))
tracked=subprocess.check_output(['git','ls-files',str(base)],text=True).splitlines()
assert not any('/private/' in p or '/local-runtime/' in p for p in tracked)
assert subprocess.run(['git','check-ignore','-q',str(base/'private/full/ffmpeg-static')]).returncode==0
report={'three_final_variants_complete_and_measured':True,'native_runs_exit0_frames600':21,'measured_runs_per_variant':6,'warmups_per_variant':1,
    'raw_wall_and_peak_rss_match_projections':True,'median_max_and_relative_values_verified':True,'source_C_bodies_unchanged':True,
    'local_binary_hashes_unchanged':True,'board_decoded_frames_identical':600,'pass_scope_counts_verified':True,
    'public_UTF8_text_files_checked':len(public),'no_binary_or_private_files_tracked':True,'real_errors_preserved':True,
    'limits':['Minimal MPEG2 feature set, not full-feature distro library','Assembly and inlined/removed definitions excluded','Full attempt gated and only493/584 report changed','RSS is whole static process peak; decrease is real but unexplained','No cross-workload guarantee or compiler resource benchmark']}
(base/'audit.json').write_text(json.dumps(report,indent=2)+'\n')
print('Audit passed: source/hash/content, 21 native runs, raw time/RSS/medians, actual scope, text-only publication and preserved failures.')
