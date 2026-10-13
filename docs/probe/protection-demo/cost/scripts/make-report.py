#!/usr/bin/env python3
from pathlib import Path
import json

base=Path('docs/probe/protection-demo/cost')
load=lambda p:json.loads((base/p).read_text())
sizes={r['variant']:r for r in load('size-comparison.json')['rows']}
perf=load('perf-memory-summary.json')['variants']
scope=load('obfuscation-scope.json')
selection=load('selected-functions.json')['functions']
context=(base/'raw/perf-context.txt').read_text().splitlines()
temps=[int(context[i])/1000 for i in range(2,len(context),4) if context[i].isdigit()]
freqs=[int(context[i]) for i in range(3,len(context),4) if context[i].isdigit()]
table=[];variation=[]
for v in ['baseline','selective','full']:
    s,p=sizes[v],perf[v]
    table.append(f'| {v} | {s["so_file_bytes"]:,} B ({s["so_file_bytes_growth_percent"]:+.2f}%) | {s["text_bytes"]:,} B ({s["text_bytes_growth_percent"]:+.2f}%) | {p["wall_median_seconds"]:.6f} s ({p["wall_median_change_percent"]:+.2f}%) | {p["peak_rss_max_KiB"]:,} KiB ({p["peak_rss_max_change_percent"]:+.2f}%) | 本机静态体积 + 板上6次 |')
    variation.append(f'| {v} | {p["valid_runs"]} | {p["wall_min_seconds"]:.6f}–{p["wall_max_seconds"]:.6f} s | {p["wall_CV_percent"]:.2f}% | {p["peak_rss_median_KiB"]:.0f} KiB ({p["peak_rss_median_change_percent"]:+.2f}%) | {p["peak_rss_min_KiB"]}–{p["peak_rss_max_KiB"]} KiB | {p["utime_median_seconds"]:.4f} s | {p["ffmpeg_rtime_median_seconds"]:.4f} s |')
functions='\n'.join('| '+name+' | '+file+' | '+why+' |' for file,fs in selection.items() for name,why in fs.items())
(base/'comparison.md').write_text(f'''# FFmpeg 8.0.1：代码混淆的体积、时间和峰值内存

**三档最终都完成了静态体积测量和真实开源板运行，各6次有效测量。** 在本批固定MPEG2软件解码负载下，选择10个管线/属性/生命周期函数的档位，`.so`增加12.80%、墙钟增加2.50%；全C函数尝试档`.so`增加403.48%、墙钟增加332.87%。这支持本批“选择性混淆代价较可控”，不支持“任意10个热点函数、任何codec/负载都只有2.50%开销”。

| 档位 | libavcodec.so总大小 | .text大小 | 解码墙钟中位数 | 进程峰值RSS（6次最大观测） | 测量状态 |
|---|---:|---:|---:|---:|---|
'''+ '\n'.join(table)+f'''

所有百分比均相对本批baseline；文件容量用B，RSS用FFmpeg原输出KiB（1024 B）。`.so`都是无debug、**未strip**的同配置产物，容量包含普通符号等；`.text`是代码节，非全部可执行PT_LOAD段。RSS列是**整份静态ffmpeg进程**的峰值，非libavcodec独立常驻内存，不含机器页缓存或所有系统进程。

全档相比选择性档，`.so`为 **{sizes['full']['so_file_bytes']/sizes['selective']['so_file_bytes']:.2f}倍**、`.text`为 **{sizes['full']['text_bytes']/sizes['selective']['text_bytes']:.2f}倍**、时间为 **{perf['full']['wall_median_seconds']/perf['selective']['wall_median_seconds']:.2f}倍**。这次进程峰值RSS**没有随容量增加**：选择档最大峰值不变，全档最大峰值下降11.90%。不能把容量增长等同于内存增长，也不把本次下降解释为“混淆省内存”；运行时驻留/缓冲队列/调度等会影响RSS，本轮未用smaps或队列分析确定原因。

## 重复测量与波动

| 档位 | 有效次数 | 墙钟min–max | CV（样本标准差/均值） | 每次峰值RSS的中位数 | 峰值RSSmin–max | benchmark utime中位 | benchmark rtime中位 |
|---|---:|---:|---:|---:|---:|---:|---:|
'''+ '\n'.join(variation)+f'''

每档先1次暖机，再6轮三档交替顺序，每档在每个顺序位置出现2次；21次null解码执行均exit0且报告600帧。codec/filter线程均设1，所有ffmpeg线程通过`taskset -c 2`继承CPU2亲和；未改governor（schedutil）、未清页缓存、未关板上服务。板上date在进程前后计时，**不包含sdb传输延时**；FFmpeg自身benchmark另提供utime/stime/rtime和getrusage峰值。墙钟含进程启动/退出，故可高于内部rtime。只用中位数作时间比较，原始6次及暖机也全部保留，详见 [perf-memory.txt](perf-memory.txt)、[perf-memory-runs.json](perf-memory-runs.json)、[raw/timings.tsv](raw/timings.tsv)。

测前采样CPU0频率范围{min(freqs)}–{max(freqs)} kHz、温度{min(temps):.3f}–{max(temps):.3f}°C；这是运行前采样，不证明整个测量期间恒频。原始负载/温度/频率在 [raw/perf-context.txt](raw/perf-context.txt)，实时板子版本/架构/设备树见 [board-identity.txt](board-identity.txt)：RPi4 ModelB、Tizen11、ARMv7，root连接成功。结论限于本板、本批构建和负载，没有统计置信区间或跨设备/生产负载保证。

## 构建公平性与实际覆盖

复用官方FFmpeg8.0.1归档（SHA256 `05ee0b03119b45c0bdb4df654b96802e909e0a752f72e4fe3794f487229e5a41`）和xollvm v0.11.1预编译Clang/opt **22.1.8**。已有ffmpeg-demo仅PCM，不够测视频，本批三档统一启用最小mpeg2video decoder/parser、mpegvideo demuxer、file、null/framemd5 muxer及wrapped_avframe/rawvideo encoder和ffmpeg必要filter；**不是全功能发行版libavcodec**。

三档同ARMv7 hard-float/PIC/NEON与-O2、同源码和组件集、相同裸基线加固覆盖（沿旧记录显式关闭SSP/FORTIFY/RELRO，NX保留）、不strip、不debug。libavcodec C先编优化IR，再按范围仅挂LLVM annotation元数据，真实xollvm opt执行sub/bcf/fla，最后相同-O2后端（disable-llvm-passes防止重新中端优化）生成对象；baseline走相同IR/后端但不开pass。原C函数体没有人工改写。其他FFmpeg库与fftools均不开混淆。

所有89个libavcodec C TU完成。每档在前置优化后均有584个IR函数定义（按函数/TU计，含真正存活的header函数，不是唯一源函数数）：

| 档位 | 注解函数定义 | report函数 | 至少一个pass报告changed | 实际限制 |
|---|---:|---:|---:|---|
| baseline | 0 | 0 | 0 | 不开pass |
| selective | 10 | 10 | 9 | fla跳过2个间接调用、1个少块函数 |
| full | 584 | 584 | 493 | fla跳过135少块、63间接调用、9过多块函数；91个定义未报告实际变换 |

使用相同 `substitution(prob=50,loop=1), bcf(prob=30,loop=1,maxBlocks=200), flattening(minBlocks=3,maxBlocks=200)`，固定seed1、verify，IR硬上限12000/函数、默认增长倍率50。保持原ARM汇编/NEON：**汇编函数不受LLVM IR pass覆盖**，已内联/消除的独立函数也不能再按原名保护。因此full是本最小组件集、这些门限下的“全部存活C定义尝试”，**不是整个FFmpeg所有codec、汇编和函数都成功三pass，也不是无门限理论最坏上界**。`changed`是编译器报告，不等于强度保证。

完整选择/原因如下（10/584定义约1.7%，刻意避开像素/IDCT/宏块内核）：

| 函数 | 源文件 | 选择原因 |
|---|---|---|
'''+functions+'''

真实范围、每函数pass结果和跳过清单：[obfuscation-scope.json](obfuscation-scope.json)；未删减编译器报告：[compiler-reports/](compiler-reports/)；命令/参数：[build-variants.txt](build-variants.txt)、[build-status.json](build-status.json)、[scripts/cc-wrapper.py](scripts/cc-wrapper.py)、[build-logs/](build-logs/)。选择的是开放FFmpeg逻辑的代表，不声称这组函数就是公司实际敏感算法。

## 负载与运行正确性

本机原生mpeg2video（不依赖x264）编码testsrc2，固定640×360、30fps、600帧，single-thread/bitexact、GOP15/B帧2/4M目标码率。生成版本、命令、ffprobe和唯一内容哈希见 [workload.json](workload.json)、[workload-generation.txt](workload-generation.txt)。三档用**同一8,383,885 B文件**：SHA256 `595ea153ee063e90ced2404f00fe0467d4bd37ef1ceeffdd8cd7b3d2a2de58d1`。帧数控制固定，原生raw mpegvideo demuxer有默认avg帧率显示，实际输出/比对均600帧/20秒。

每档静态ffmpeg从与其.so相同PIC对象/静态archive链接，含交叉glibc，ELF无INTERP，在板上真实运行，避免历史板库soft-float ABI与开发机hard-float运行时依赖混用；**不替换板上系统libavcodec，不声明这些.so可直接作为系统替代库**。文件只推入独立/opt/protection-cost-20261013-随机目录。板上SHA256与本地一致，三个程序native解码600帧framemd5逐行相同，详见 [board-artifact-hashes.txt](board-artifact-hashes.txt)、[decode-correctness.json](decode-correctness.json)、[raw/](raw/)。性能测同文件解码到null，包含demux/parser/解码/null输出封包及进程启动退出，不是孤立内核函数耗时；不含负载生成编码/媒体传输/framemd5计算时间。

## 真实失败及未测边界

首次-force-include全局pragma测试因push未配对pop报错，原文 [annotation-probe.txt](annotation-probe.txt)，同文件配对后通过。首次全源码注解构建生成.so但ffmpeg链接 `undefined reference to ff_mspel_motion`，nm证实mpegvideo_motion.o新增该引用；未放宽未定义检查或改源码功能来掩盖，原日志/报告保存于 [build-logs/full-source-attempt-make.txt](build-logs/full-source-attempt-make.txt)、compiler-reports/full-source-attempt/、build-status的full_source_attempt。本配置关闭WMV2，推断早期变换/强制保留使本应消去的配置/内联路径留下，故一次改为优化后实际定义注解。旧direct baseline/source selective完成产物明确存档，因公平管线改变才重新构建；其数据**没有混入最终总表**。

定位helper时查询不存在mpegvideo_motion.h的真实错误也留在 [helper-lookup-error.txt](helper-lookup-error.txt)。首次性能汇总误按旧kB匹配新FFmpeg KiB，触发AssertionError；原trace及错误投影保留 [measurement-parser-error.txt](measurement-parser-error.txt)、[perf-memory-runs-parser-failure.json](perf-memory-runs-parser-failure.json)，仅用--saved重解析原始日志，**未重跑或改原数字**。

最终三档**没有未测的表格单元**；首次full-source失败档没有有效可运行性能值，未作为“全库档”冒充成功。生产全功能FFmpeg、其他codec/分辨率/线程、多轮不同seed、更强参数、完整ASM保护、编译期资源、内存原因剖析和长期运行均未测。本实验显示选择范围是重要成本控制手段，不能用这一次负载作通用开销承诺。
''')
(base/'README.md').write_text('''# cost

入口：[comparison.md](comparison.md)。三档最终均已完成体积与真实板测，每档1次暖机+6次计时，解码600帧内容一致。

size-comparison.txt/json：总.so与.text绝对值/增长；perf-memory.txt、perf-memory-runs.json、perf-memory-summary.json：原始样本/中位数/波动/RSS；raw/：板上原始benchmark/framemd5/条件；compiler-reports/与obfuscation-scope.json：真实pass结果；build-logs/、build-status.json：每次尝试及原错误。初次全源码失败与最终优化IR方法区分，不是无条件全部函数混淆。

所有.so、ffmpeg、媒体、第三方源码、IR与运行缓存在被忽略private/；工具链在被忽略.local-tools/。不替换板子系统文件。脚本路径/原始命令可审计。

复现先source docs/probe/scripts/env.sh；board-connect.py确认指定板子，build.py核对已有完成marker/hash后复用；变更方法时须明确把旧产物/记录另存为新批次，脚本不会仅因源码脚本变动自动重编，summarize-builds.py测体积与范围，make-workload.py生成固定片，deploy-check.py推送并校验内容，measure-board.py运行暖机/6轮板测。已有测量只用measure-board.py --saved重新解析，make-report.py生成总表；audit.py验证文本/原始数据/哈希一致性。会写本目录及指定独立板上目录，审计无需重跑板测。
''')
print('Wrote comparison.md: all three measured, scope/skips/errors explicit, maximum and median peak RSS distinguished.')
