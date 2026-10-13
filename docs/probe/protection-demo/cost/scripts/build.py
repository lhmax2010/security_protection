#!/usr/bin/env python3
"""Sequential resumable builds; each make has a finite deadline and raw log."""
from pathlib import Path
import hashlib,json,os,re,shlex,subprocess,time

root=Path.cwd();base=root/'docs/probe/protection-demo/cost'
archive=root/'docs/probe/ffmpeg-demo/private/download/ffmpeg-8.0.1.tar.xz'
wrapper=base/'scripts/cc-wrapper.py'
annotation='obf: substitution(prob=50,loop=1), bcf(prob=30,loop=1,maxBlocks=200), flattening(minBlocks=3,maxBlocks=200)'
selected={
 'libavcodec/avcodec.c':{'avcodec_receive_frame':'Public output API / frame handoff'},
 'libavcodec/decode.c':{'avcodec_send_packet':'Public input/API validation',
    'ff_decode_receive_frame_internal':'Decode dispatch and buffer/error handling',
    'decode_receive_frame_internal':'Frame properties/error/discard checks'},
 'libavcodec/mpeg12dec.c':{'mpeg_decode_frame':'MPEG2 frame dispatch',
    'mpeg_decode_postinit':'Sequence properties and decoder reinitialization',
    'mpeg1_decode_picture':'Picture header validation',
    'mpeg1_decode_sequence':'Sequence header validation',
    'mpeg_decode_sequence_extension':'MPEG2 profile/dimension extension',
    'mpeg_decode_picture_coding_extension':'Picture coding extension/flags'}}
(base/'selected-functions.json').write_text(json.dumps({'annotation':annotation,'functions':selected,'rationale':'10 real pipeline/header parsing functions; avoids inner pixel/IDCT/macroblock kernels. Source annotations may be inlined before pass execution; actual reports decide surviving scope. This selection does not protect the whole decoder algorithm.'},indent=2)+'\n')
(base/'build-variants.txt').write_text('FFmpeg8.0.1; xollvm22.1.8; identical minimal MPEG2 decoder, parser, mpegvideo demuxer, null/framemd5 muxers, file protocol, wrapped_avframe/rawvideo encoders; -O2 ARMv7 hard-float PIC, NEON/assembly retained, no debug/strip.\nBaseline: no pass. Selective: annotate10 pipeline/header functions; full: balanced pragma on all libavcodec C source TUs, including header functions that survive inlining; assembly and other FFmpeg libraries not obfuscated.\n'+annotation+'\nFixed seed1, verify; IR hard cap12000 per function and default advisory multiplier50; fla maxBlocks200; actual skipped/rollback/function reports will be aggregated. Full build deadline1200s, per affected C TU180s; builds use -j2.\nSelf-contained ffmpeg statically relinked from these same PIC objects; shared .so kept for size measurement. All binaries/source trees/media private/.\n')
records={}
statuspath=base/'build-status.json'
if statuspath.exists():records=json.loads(statuspath.read_text())
def save():statuspath.write_text(json.dumps(records,indent=2)+'\n')
for variant in ['baseline','selective','full']:
    work=base/'private'/variant;source=work/'ffmpeg-8.0.1';build=work/'build'
    work.mkdir(parents=True,exist_ok=True);build.mkdir(exist_ok=True)
    marker=work/'complete.json'
    if marker.exists():
        complete=json.loads(marker.read_text())
        if all(Path(p).is_file() and hashlib.sha256(Path(p).read_bytes()).hexdigest()==h for p,h in complete['hashes'].items()):
            print(variant,'completed artifact hashes verified; no rebuild',flush=True);continue
    if not source.exists():subprocess.run(['tar','-xf',str(archive),'-C',str(work)],check=True)
    if variant=='selective' and not (work/'annotated.marker').exists():
        for rel,functions in selected.items():
            p=source/rel;text=p.read_text()
            for name in functions:
                pattern=r'(?m)^([^\n;{}]*\b'+re.escape(name)+r'\s*\([^;{}]*?\)\s*)(\{)'
                matches=list(re.finditer(pattern,text));assert len(matches)==1,(rel,name,len(matches))
                m=matches[0];text=text[:m.start()]+'__attribute__((annotate("'+annotation+'")))\n'+text[m.start():]
            p.write_text(text)
        (work/'annotated.marker').write_text(annotation+'\n')
    cc=work/'cc';cc.write_text('#!/bin/sh\nexec python3 '+shlex.quote(str(wrapper))+' '+variant+' "$@"\n');cc.chmod(0o755)
    config=[str(source/'configure'),'--prefix='+str(work/'install'),'--arch=arm','--cpu=cortex-a7','--target-os=linux','--enable-cross-compile',
       '--cross-prefix=arm-linux-gnueabihf-','--cc='+str(cc),'--sysroot='+str(root/'.local-tools/sysroot'),
       '--extra-cflags=-mfpu=neon -fno-stack-protector -U_FORTIFY_SOURCE -D_FORTIFY_SOURCE=0','--optflags=-O2',
       '--extra-ldflags=-Wl,-z,norelro -Wl,-z,lazy','--enable-shared','--enable-static','--enable-pic','--disable-stripping','--disable-debug',
       '--disable-autodetect','--disable-doc','--disable-network','--disable-avdevice','--disable-swscale','--disable-swresample',
       '--disable-ffplay','--disable-ffprobe','--disable-everything','--enable-ffmpeg','--enable-decoder=mpeg2video',
       '--enable-parser=mpegvideo','--enable-demuxer=mpegvideo','--enable-muxer=null,framemd5',
       '--enable-protocol=file','--enable-encoder=wrapped_avframe,rawvideo','--enable-filter=null']
    logs=base/'build-logs';logs.mkdir(exist_ok=True)
    records[variant]={'source':str(source),'build':str(build),'configure_command':config,'status':'configuring'};save()
    if not (build/'ffbuild/config.mak').exists():
        with (logs/(variant+'-configure.txt')).open('wb') as f:p=subprocess.run(config,cwd=build,stdout=f,stderr=subprocess.STDOUT)
        records[variant]['configure_exit']=p.returncode;save()
        if p.returncode:records[variant]['status']='configure_failed';save();print(variant,'configure failed',flush=True);continue
    make=['timeout','--signal=TERM','--kill-after=15','1200','make','-j2','V=1']
    records[variant].update(make_command=make,status='building',started=time.time());save();print(variant,'building',flush=True)
    with (logs/(variant+'-make.txt')).open('ab') as f:p=subprocess.run(make,cwd=build,stdout=f,stderr=subprocess.STDOUT)
    records[variant].update(make_exit=p.returncode,build_elapsed_seconds=time.time()-records[variant]['started']);save()
    if p.returncode:
        records[variant]['status']='make_failed_or_timed_out';save();print(variant,'make exit',p.returncode,flush=True);continue
    # Same objects, same archive set; -static forces self-contained cross-glibc runtime.
    obj=sorted(str(p) for p in (build/'fftools').rglob('*.o'))
    libs=[build/(name+'/lib'+name.removeprefix('lib')+'.a') for name in ['libavfilter','libavformat','libavcodec','libavutil']]
    link=[str(cc),'-static','-o',str(work/'ffmpeg-static'),*obj,'-Wl,--start-group',*[str(p) for p in libs],'-Wl,--end-group','-lm','-pthread','-ldl','-latomic']
    records[variant]['static_link_command']=link;save()
    with (logs/(variant+'-static-link.txt')).open('wb') as f:p=subprocess.run(link,cwd=build,stdout=f,stderr=subprocess.STDOUT)
    records[variant]['static_link_exit']=p.returncode
    so=build/'libavcodec/libavcodec.so.62'
    records[variant]['library_complete']=so.is_file()
    if p.returncode:records[variant]['status']='shared_complete_static_link_failed';save();print(variant,'static link failed',flush=True);continue
    binary=work/'ffmpeg-static'
    check=subprocess.run(['readelf','-l',str(binary)],capture_output=True,text=True)
    (logs/(variant+'-static-layout.txt')).write_text(check.stdout+check.stderr)
    assert check.returncode==0 and 'INTERP' not in check.stdout,'Not self-contained'
    complete={'hashes':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [so,binary]},'finished':time.time()}
    marker.write_text(json.dumps(complete,indent=2)+'\n')
    records[variant].update(status='complete',shared_library=str(so),ffmpeg_static=str(binary),hashes=complete['hashes']);save()
    print(variant,'complete',round(records[variant]['build_elapsed_seconds'],1),'seconds',flush=True)
