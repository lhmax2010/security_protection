#!/usr/bin/env python3
from pathlib import Path
import hashlib,json,shlex,subprocess

base=Path('docs/probe/protection-demo/cost')
private=base/'private';private.mkdir(exist_ok=True)
clip=private/'fixed-640x360-600frames.m2v'
cmd=['ffmpeg','-hide_banner','-y','-f','lavfi','-i','testsrc2=size=640x360:rate=30','-frames:v','600',
     '-an','-c:v','mpeg2video','-threads','1','-pix_fmt','yuv420p','-g','15','-bf','2','-b:v','4M',
     '-flags','+bitexact','-fflags','+bitexact','-f','mpeg2video',str(clip)]
version=subprocess.run(['ffmpeg','-version'],capture_output=True,text=True)
(base/'workload-host-version.txt').write_text(version.stdout+version.stderr)
p=subprocess.run(cmd,capture_output=True,text=True)
(base/'workload-generation.txt').write_text('$ '+shlex.join(cmd)+'\n'+p.stdout+p.stderr+f'\nexit={p.returncode}\n')
assert p.returncode==0,p.stderr
probe=subprocess.run(['ffprobe','-v','error','-count_frames','-show_streams','-of','json',str(clip)],capture_output=True,text=True)
(base/'workload-probe.json').write_text(probe.stdout)
assert probe.returncode==0,probe.stderr
stream=json.loads(probe.stdout)['streams'][0];assert stream['width']==640 and stream['height']==360 and stream['nb_read_frames']=='600',stream
record={'command':cmd,'clip':str(clip.resolve()),'sha256':hashlib.sha256(clip.read_bytes()).hexdigest(),'bytes':clip.stat().st_size,
        'generator':version.stdout.splitlines()[0],'encoder':'native mpeg2video, no external x264','resolution':'640x360','framerate':30,'frames':600,
        'scope':'All variants decode exactly this saved content; host generator version is independent of identical on-board FFmpeg8.0.1 decoders.'}
(base/'workload.json').write_text(json.dumps(record,indent=2)+'\n')
print('Fixed native MPEG2 workload: 640x360 / 30fps / 600 frames;',clip.stat().st_size,'bytes; SHA256',record['sha256'])
