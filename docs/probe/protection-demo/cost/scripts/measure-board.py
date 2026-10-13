#!/usr/bin/env python3
from pathlib import Path
from decimal import Decimal
import json,re,shlex,statistics,subprocess,sys

base=Path('docs/probe/protection-demo/cost');raw=base/'raw'
target=json.loads((base/'board-target.json').read_text());serial=target['serial'];remote=target['run_directory']
valid=json.loads((base/'decode-correctness.json').read_text())
assert all(valid[v]['valid_for_benchmark'] for v in ['baseline','selective','full']), 'Skip invalid decoders; never benchmark wrong output'
saved='--saved' in sys.argv
calls=json.loads((base/'board-measure-commands.json').read_text()) if saved else []
def call(args,timeout=60):
    try:
        p=subprocess.run(args,capture_output=True,text=True,timeout=timeout)
        r={'command':shlex.join(args),'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
    except subprocess.TimeoutExpired as e:
        r={'command':shlex.join(args),'exit':124,'error':str(e),'stdout':(e.stdout or b'').decode() if isinstance(e.stdout,bytes) else e.stdout or '', 'stderr':(e.stderr or b'').decode() if isinstance(e.stderr,bytes) else e.stderr or ''}
    calls.append(r);(base/'board-measure-commands.json').write_text(json.dumps(calls,indent=2)+'\n')
    assert r['exit']==0,r
    return r['stdout']
if not saved:
    call(['sdb','-s',serial,'push',str(base/'scripts/run-board.sh'),remote+'/run-board.sh'])
    output=call(['sdb','-s',serial,'shell','sh '+remote+'/run-board.sh '+remote],timeout=600)
    (base/'board-measure-run.txt').write_text(output)
    assert 'BOARD_PERF_MEASUREMENT_FINISHED' in output
    for name in ['timings.tsv','perf-context.txt']:
        call(['sdb','-s',serial,'pull',remote+'/'+name,str(raw/name)])
records=[]
for line in (raw/'timings.tsv').read_text().splitlines()[1:]:
    phase,round_,variant,start,end,code=line.split('\t')
    name=f'perf-{phase}-{round_}-{variant}.txt'
    if not saved:call(['sdb','-s',serial,'pull',remote+'/'+name,str(raw/name)])
    text=(raw/name).read_text()
    timing=re.search(r'bench: utime=([0-9.]+)s stime=([0-9.]+)s rtime=([0-9.]+)s',text)
    rss=re.search(r'bench: maxrss=(\d+)(?:KiB|kB)',text)
    frames=re.findall(r'frame=\s*(\d+)',text)
    record={'phase':phase,'round':int(round_),'variant':variant,'exit':int(code),
        'wall_seconds':float(Decimal(end)-Decimal(start)),'stdout_stderr_file':str((raw/name).relative_to(base)),
        'utime_seconds':float(timing[1]) if timing else None,'stime_seconds':float(timing[2]) if timing else None,
        'ffmpeg_rtime_seconds':float(timing[3]) if timing else None,'peak_rss_KiB':int(rss[1]) if rss else None,
        'frames_reported':int(frames[-1]) if frames else None}
    record['valid']=record['exit']==0 and record['wall_seconds']>0 and record['peak_rss_KiB'] is not None and record['frames_reported']==600
    records.append(record)
(base/'perf-memory-runs.json').write_text(json.dumps(records,indent=2)+'\n')
summary={}
for variant in ['baseline','selective','full']:
    selected=[r for r in records if r['phase']=='measured' and r['variant']==variant and r['valid']]
    if len(selected)<5:
        summary[variant]={'measured':False,'valid_runs':len(selected),'reason':'Fewer than 5 valid runs'};continue
    walls=[r['wall_seconds'] for r in selected];rsses=[r['peak_rss_KiB'] for r in selected]
    summary[variant]={'measured':True,'valid_runs':len(selected),'warmups':1,'wall_median_seconds':statistics.median(walls),
        'wall_min_seconds':min(walls),'wall_max_seconds':max(walls),'wall_CV_percent':statistics.stdev(walls)/statistics.mean(walls)*100,
        'utime_median_seconds':statistics.median(r['utime_seconds'] for r in selected),
        'ffmpeg_rtime_median_seconds':statistics.median(r['ffmpeg_rtime_seconds'] for r in selected),
        'peak_rss_median_KiB':statistics.median(rsses),'peak_rss_max_KiB':max(rsses),'peak_rss_min_KiB':min(rsses)}
ref=summary['baseline'];assert ref['measured']
for v,r in summary.items():
    if r['measured']:
        r['wall_median_change_percent']=(r['wall_median_seconds']/ref['wall_median_seconds']-1)*100
        r['peak_rss_median_change_percent']=(r['peak_rss_median_KiB']/ref['peak_rss_median_KiB']-1)*100
        r['peak_rss_max_change_percent']=(r['peak_rss_max_KiB']/ref['peak_rss_max_KiB']-1)*100
(base/'perf-memory-summary.json').write_text(json.dumps({'method':'Native open board. Same saved MPEG2 workload verified 600 frame hashes identical across three. One warmup per variant, 6 rotating interleaved rounds. Single codec/filter threads; taskset CPU2 when present; governor unchanged. Wall from on-board date around process (SDB latency excluded); FFmpeg benchmark utime/rtime and getrusage maxrss. Table peak memory is median of per-run peak RSS (KiB), also report max/range; includes whole static ffmpeg, not just libavcodec. No process/VFS cache flush.', 'variants':summary},indent=2)+'\n')
(base/'perf-memory.txt').write_text('Native board; 600 frames of 640x360 MPEG2; warmup1, measured6 per variant, rotating order; CPU2 affinity, single codec/filter thread, governor unchanged.\nMemory: median of per-process peak RSS, not total machine/free memory. Time: on-board wall, excludes SDB transport.\nVariant       wall median(s) change      min..max(s)       CV%       peak RSS median(KiB) change      max\n'+'\n'.join(f'{v:12s} {r["wall_median_seconds"]:12.6f} {r["wall_median_change_percent"]:+8.2f}% {r["wall_min_seconds"]:.6f}..{r["wall_max_seconds"]:.6f} {r["wall_CV_percent"]:7.2f} {r["peak_rss_median_KiB"]:14.0f} {r["peak_rss_median_change_percent"]:+8.2f}% {r["peak_rss_max_KiB"]:8d}' if r['measured'] else v+': UNMEASURED '+r['reason'] for v,r in summary.items())+'\nMaximum observed peak RSS across measured runs and change from baseline:\n'+'\n'.join(f'{v}: {r["peak_rss_max_KiB"]} KiB ({r["peak_rss_max_change_percent"]:+.2f}%)' for v,r in summary.items() if r['measured'])+'\nRaw runs and benchmark outputs preserved; no single-run conclusions.\n')
print((base/'perf-memory.txt').read_text())
