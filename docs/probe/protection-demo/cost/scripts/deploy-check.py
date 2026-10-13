#!/usr/bin/env python3
from pathlib import Path
import hashlib,json,shlex,subprocess,uuid

base=Path('docs/probe/protection-demo/cost');raw=base/'raw';raw.mkdir(exist_ok=True)
target=json.loads((base/'board-target.json').read_text());serial=target['serial']
if not target.get('run_directory'):
    target['run_directory']=target['target_directory']+'-'+uuid.uuid4().hex[:8]
    (base/'board-target.json').write_text(json.dumps(target,indent=2)+'\n')
remote=target['run_directory'];records=[]
def call(args,timeout=60):
    try:
        p=subprocess.run(args,capture_output=True,text=True,timeout=timeout)
        record={'command':shlex.join(args),'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
    except subprocess.TimeoutExpired as e:
        record={'command':shlex.join(args),'exit':124,'error':str(e),'stdout':(e.stdout or b'').decode() if isinstance(e.stdout,bytes) else e.stdout or '', 'stderr':(e.stderr or b'').decode() if isinstance(e.stderr,bytes) else e.stderr or ''}
    records.append(record);(base/'board-deploy.json').write_text(json.dumps(records,indent=2)+'\n')
    assert record['exit']==0,record
    return record['stdout']
def shell(script,timeout=60):return call(['sdb','-s',serial,'shell','sh -c '+shlex.quote(script)],timeout)
assert 'SETUP_OK' in shell('mkdir -p '+shlex.quote(remote)+' && echo SETUP_OK')
status=json.loads((base/'build-status.json').read_text());expected={}
for variant in ['baseline','selective','full']:
    assert status[variant]['status']=='complete'
    binary=Path(status[variant]['ffmpeg_static']);name='ffmpeg-'+variant
    expected[name]=hashlib.sha256(binary.read_bytes()).hexdigest();call(['sdb','-s',serial,'push',str(binary),remote+'/'+name])
clip=Path(json.loads((base/'workload.json').read_text())['clip'])
expected['workload.m2v']=hashlib.sha256(clip.read_bytes()).hexdigest()
call(['sdb','-s',serial,'push',str(clip),remote+'/workload.m2v'])
call(['sdb','-s',serial,'push',str(base/'scripts/check-board.sh'),remote+'/check-board.sh'])
hashes=shell('cd '+shlex.quote(remote)+' && chmod 755 ffmpeg-* && sha256sum ffmpeg-* workload.m2v')
(base/'board-artifact-hashes.txt').write_text(hashes)
actual={line.split()[-1]:line.split()[0] for line in hashes.splitlines() if len(line.split())==2}
assert actual==expected,(actual,expected)
text=call(['sdb','-s',serial,'shell','sh '+remote+'/check-board.sh '+remote],timeout=300)
(base/'board-content-check-run.txt').write_text(text);assert 'BOARD_CONTENT_CHECK_FINISHED' in text
for name in ['hash-status.tsv','conditions-before.txt']+[p+'-'+v+'.txt' for v in ['baseline','selective','full'] for p in ['hash','version']]+['hash-'+v+'-stderr.txt' for v in ['baseline','selective','full']]:
    call(['sdb','-s',serial,'pull',remote+'/'+name,str(raw/name)])
rows=[line.split() for line in (raw/'hash-status.tsv').read_text().splitlines()]
valid={};contents={}
for variant,version_exit,decode_exit in rows:
    path=raw/('hash-'+variant+'.txt')
    lines=[l.strip() for l in path.read_text().splitlines() if l.strip() and not l.startswith('#')]
    contents[variant]=lines
    valid[variant]={'version_exit':int(version_exit),'decode_exit':int(decode_exit),'frames':len(lines),
        'aggregate_frame_rows_sha256':hashlib.sha256('\n'.join(lines).encode()).hexdigest(),
        'content_matches_baseline':lines==contents.get('baseline'),
        'valid_for_benchmark':version_exit==decode_exit=='0' and len(lines)==600 and lines==contents.get('baseline')}
(base/'decode-correctness.json').write_text(json.dumps(valid,indent=2)+'\n')
assert valid['baseline']['valid_for_benchmark'],'Baseline decode failed; stop'
print('Native board content verification:',{v:(r['frames'],r['valid_for_benchmark']) for v,r in valid.items()})
