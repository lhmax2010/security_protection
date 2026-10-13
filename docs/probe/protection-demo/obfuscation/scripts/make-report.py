#!/usr/bin/env python3
from pathlib import Path
import hashlib
import json
import re
import subprocess

root=Path.cwd()
base=root/'docs/probe/protection-demo/obfuscation'
baseline=root/'docs/probe/evidence/target_c_llvm_armv7l'
report=base/'report';report.mkdir(exist_ok=True)
elfdir=base/'elf';elfdir.mkdir(exist_ok=True)
load=lambda p:json.loads(p.read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
manifest=load(base/'artifact-manifest.json')
groups={'baseline18':(baseline,root/'docs/probe/samples/bin/target_c_llvm_armv7l'),
        'control22':(base/'control22',base/'bin/target_c_llvm22_control'),
        'obfuscated22':(base/'obfuscated',base/'bin/target_c_llvm22_obfuscated')}
metrics={'method':'Ghidra12.1.4 procedure_info/basicblock_count and read_function_instructions. Direct branch count is static ARM b/b<condition>/cbz/cbnz instruction rows, excluding calls, bx/returns, and implicit PC transfers; not CFG-edge counts or dynamic execution counts.', 'targets':{}}
provenance={}
for group,(folder,binary) in groups.items():
    assert sha(binary)==manifest[str(binary.relative_to(root))]['sha256']
    p=subprocess.run(['readelf','-Ws',str(binary)],capture_output=True,text=True)
    (elfdir/(group+'-symbol-sizes.txt')).write_text(p.stdout+p.stderr+f'\nexit={p.returncode}\n')
    assert p.returncode==0,p.stderr
    symbols={}
    for line in p.stdout.splitlines():
        fields=line.split()
        if len(fields)==8 and fields[-1] in ['secret_transform','simple_checksum']:
            symbols[fields[-1]]={'elf_address':fields[1],'bytes':int(fields[2]),'bind':fields[4],'visibility':fields[5]}
    metrics['targets'][group]={};provenance[group]={}
    for fn in ['secret_transform','simple_checksum']:
        evidence={}
        for op in ['info','pseudocode','assembly','instructions']:
            rawpath=folder/(fn+'-'+op+'.json');decodedpath=folder/(fn+'-'+op+'.decoded.json')
            raw,ev=load(rawpath),load(decodedpath)
            assert not raw.get('isError') and not raw.get('transport_error')
            original=raw.get('structuredContent')
            if original is None:original=next(json.loads(c['text']) for c in raw['content'] if c['type']=='text')
            assert original==ev
            assert ev['provider']['id']=='ghidra' and ev['provider']['version']=='12.1.4'
            assert ev['subject']['digest']['sha256']==sha(binary)
            evidence[op]=ev
            provenance[group][fn+'-'+op]={'evidence_id':ev['evidence_id'],'raw_path':str(rawpath.relative_to(root)),
                'raw_sha256':sha(rawpath),'decoded_path':str(decodedpath.relative_to(root)),'decoded_sha256':sha(decodedpath)}
        info=evidence['info']['normalized_result'];text=evidence['pseudocode']['normalized_result']
        pseudo=folder/(fn+'-pseudocode.c');assert pseudo.read_text()==text
        copy=report/(group+'-'+fn+'.c');copy.write_bytes(pseudo.read_bytes())
        assert info['length']==info['body']['total_bytes']==symbols[fn]['bytes']
        instructions=evidence['instructions']['normalized_result']['instructions']
        branches=[]
        for line in instructions:
            mnemonic=line.split(':',1)[1].strip().split()[0].lower().split('.')[0]
            if re.fullmatch(r'b(?:eq|ne|cs|hs|cc|lo|mi|pl|vs|vc|hi|ls|ge|lt|gt|le|al)?|cbz|cbnz',mnemonic):branches.append(line)
        metrics['targets'][group][fn]={'function_bytes':info['length'],'basic_blocks':info['basicblock_count'],
            'direct_branch_instructions':len(branches),'instruction_rows':len(instructions),
            'pseudocode_lines':len(text.splitlines()),'pseudocode_nonempty_lines':sum(bool(l.strip()) for l in text.splitlines()),
            'pseudocode_if_count':len(re.findall(r'\bif\s*\(',text)),
            'pseudocode_goto_count':len(re.findall(r'\bgoto\s+',text)),
            'direct_branch_rows':branches,'elf_symbol':symbols[fn],
            'info_evidence_id':evidence['info']['evidence_id'],'pseudocode_evidence_id':evidence['pseudocode']['evidence_id'],
            'report_copy':str(copy.relative_to(root)),'report_copy_sha256':sha(copy)}
for fn in ['secret_transform','simple_checksum']:
    assert (baseline/(fn+'-pseudocode.c')).read_bytes()==(base/'control22'/(fn+'-pseudocode.c')).read_bytes()
    for field in ['function_bytes','basic_blocks','direct_branch_instructions']:
        assert metrics['targets']['baseline18'][fn][field]==metrics['targets']['control22'][fn][field]
(base/'comparison-metrics.json').write_text(json.dumps(metrics,indent=2)+'\n')
(report/'provenance.json').write_text(json.dumps(provenance,indent=2)+'\n')
passes=load(base/'pass-report.json')
checks={f['name']:f for f in passes['functions']}
assert all(p['status']=='ran' and p['changed'] for p in checks['simple_checksum']['passes'])
assert next(p for p in checks['secret_transform']['passes'] if p['id']=='flattening')['skip_reason']=='too few blocks'
def row(fn,field):
    return ' | '.join(str(metrics['targets'][group][fn][field]) for group in groups)
secret=metrics['targets']['obfuscated22']['secret_transform']
checksum=metrics['targets']['obfuscated22']['simple_checksum']
(base/'comparison.md').write_text(f'''# LLVM22.1.8 真实代码混淆对比

本批用 **xollvm v0.11.1 的上游 Linux x86_64 预编译 clang/opt 22.1.8**，版本与PM给定Tizen平台22.1.8相同，ARM后端真实交叉编译成功；无需把该实现从旧LLVM移植到22。工具源码commit `eb0850bd7cc87f551ad2948826605e518f5b8aa2`，LLVM base `ca7933e47d3a3451d81e72ac174dcb5aa28b59d1`，获取方式/二进制哈希见 [toolchain.txt](toolchain.txt)。匹配上游版本不等于已验证Tizen供应商补丁、GBS打包或板子集成，这些本轮未做。

**可支持的结论：这两个函数的反编译可读性下降，simple_checksum最明显；没有证明算法不可恢复或量化人工逆向耗时。** Ghidra仍成功生成完整伪代码，两函数名字也保留。本轮专门隔离代码混淆，没有strip、字符串编码、额外栈保护等混入变化。

## 公平对照与参数

旧裸版Clang18.1.3及其REA证据完全复用（未重编/重分析）。另编相同源码、相同-O2/ARM ABI、**相同22.1.8工具链但不开pass**的控制版，分别用REA6.4.0/Ghidra12.1.4分析。两个函数在18裸版与22控制版的伪代码逐字相同、字节/基本块/直接分支数相同；这支持把本批变化归于混淆，而非18→22版本升级。

仅给两个noinline助手加 `annotate("obf: substitution(prob=100,loop=2), bcf(prob=100,loop=1,maxBlocks=200), flattening(minBlocks=2,maxBlocks=200)")`，算法源码表达式不变；按该实现对应关系 sub=substitution、bcf=bcf、fla=flattening。clang使用 `-mllvm -enable-obfuscation`、固定seed1、deterministic、verify。完整命令在 [obf-build-flags.txt](obf-build-flags.txt)，编译器真实pass/CFG报告在 [pass-report.json](pass-report.json) 与 [pass-report/](pass-report/)。没有用上游普通Clang的同名普通优化pass冒充混淆。

## secret_transform

| 指标 | 裸版18（已有） | 无pass控制22 | 混淆22 |
|---|---:|---:|---:|
| 函数字节（Ghidra与ELF符号尺寸一致） | {row('secret_transform','function_bytes')} |
| Ghidra基本块 | {row('secret_transform','basic_blocks')} |
| 静态直接分支指令 | {row('secret_transform','direct_branch_instructions')} |
| 完整伪代码行数（含空行） | {row('secret_transform','pseudocode_lines')} |
| 指令行数 | {row('secret_transform','instruction_rows')} |

裸版仅一行 `(param_1 ^ 0x5a17) * 0x21 + 7`；混淆版变成多个中间变量、栈地址掩码、AND/OR/XOR/NOT等组合，最终返回表达式不再直接呈现原式，尺寸 **29倍**。但 `0x5a17`、乘 `0x21`、加7仍可见，熟悉位运算恒等式的分析者仍可化简，不能说秘密算法被隐藏到无法还原。

**pass限制**：substitution确实把IR8条扩为313条；bcf报告changed=true但指令增量为0，最终仍1块/0直接分支，没有观察到持久的虚假控制流增量；flattening明确skipped/too few blocks。单行算术没有可平坦化的多块结构，本函数主要是**数据流替换**效果，不冒称fla/bcf三者全部有效。

原样节选：[裸版](report/baseline18-secret_transform.c) / [混淆版](report/obfuscated22-secret_transform.c)，伪代码Evidence `{secret['pseudocode_evidence_id']}`。

## simple_checksum（报告首选）

| 指标 | 裸版18（已有） | 无pass控制22 | 混淆22 |
|---|---:|---:|---:|
| 函数字节（Ghidra与ELF符号尺寸一致） | {row('simple_checksum','function_bytes')} |
| Ghidra基本块 | {row('simple_checksum','basic_blocks')} |
| 静态直接分支指令 | {row('simple_checksum','direct_branch_instructions')} |
| 完整伪代码行数（含空行） | {row('simple_checksum','pseudocode_lines')} |
| 指令行数 | {row('simple_checksum','instruction_rows')} |
| 伪代码if数量 | {row('simple_checksum','pseudocode_if_count')} |
| 伪代码goto数量 | {row('simple_checksum','pseudocode_goto_count')} |

裸版是短小的逐字节do/while乘31累加循环；混淆版出现 `do ... while(true)` **调度循环**、多层嵌套条件、状态编码/状态指针选择、冗余恒等条件和goto。阅读者需先恢复分派状态和真路径，再区分校验更新与干扰表达式。尺寸 **71.4倍**，基本块5→39、直接分支2→28、伪代码20→311行，图与伪代码均支持“明显更难读”的定性结论。

实际substitution/bcf/flattening三pass均changed：IR24→217→846→1834。IR报告环路复杂度代理2→17是**编译器IR层度量**，不代替最终Ghidra基本块或人工难度；工具的difficulty score也不作为效果证明。最终仍能在混淆伪代码找到 `local_8c * 0x1f + (uint)*local_78`（原样文件第155行），不是全部逻辑消失。不能承诺抗自动去混淆或保护密钥。

原样报告图内容：[裸版](report/baseline18-simple_checksum.c) / [混淆版](report/obfuscated22-simple_checksum.c)，伪代码Evidence `{checksum['pseudocode_evidence_id']}`；同版本对照也放在 [report/](report/)。所有副本与REA normalized_result逐字相同，来源/哈希见 [report/provenance.json](report/provenance.json)。

## 核验、范围与失败记录

QEMU三版对照11组（默认、0/1/1234、65535/65536、uint32边界、strtoul溢出、负数、非法输入、多参数），stdout/退出码全部一致、stderr为空，见 [obf-run-equivalence.txt](obf-run-equivalence.txt)。本次main的checksum入参始终是marker字符串，不能据此声称所有字符串/所有输入已形式化证明等价；不含性能基准、实板运行或人工逆向计时。相同-O2但编译器后端仍会对变换优化，pass报告的“changed”不等于所有IR结构都留到机器码。

所有最终字节尺寸都与GNU readelf独立核对，所有基本块来自Ghidra procedure_info；分支行是Ghidra read_function_instructions中ARM直接b/b条件/cbz/cbnz静态指令数，**不含调用、bx返回、隐式PC转移，不是CFG边数或运行次数**。原始MCP响应与decoded投影均保存，见 [obfuscated/](obfuscated/) 和 [control22/](control22/)，派生统计见 [comparison-metrics.json](comparison-metrics.json)。

真实失败完整留存：web release页timeout（随后API成功）；旧Pluto URL和猜测workflow URL HTTP404；验收断言错误地要求opt --print-passes列出扩展pass，且当次shell随后继续checkpoint，已在STATE纠正。原trace见 [toolchain-validation-error.txt](toolchain-validation-error.txt)，实际opt pipeline调用及后续真实ARM构建/报告证实可用；没有抹去失败或把失败当pass成功。调研来源在 [toolchain-survey.txt](toolchain-survey.txt)，上游 [项目](https://github.com/und3ath/xollvm) / [v0.11.1 release](https://github.com/und3ath/xollvm/releases/tag/v0.11.1)。

交付范围仅本目录文本与两份自建小ELF；第三方clang/opt/发布压缩包只在忽略.local-tools/。**LLVM22移植不需要另做；Tizen构建体系/供应商版本集成与更广等价验证是独立后续工作，本轮未做。**
''')
(base/'README.md').write_text('''# obfuscation

入口：[comparison.md](comparison.md)。报告首选simple_checksum的完整原样伪代码对照：report/baseline18-simple_checksum.c 与 report/obfuscated22-simple_checksum.c。

工具链真实22.1.8预编译，详见toolchain.txt/selected-asset.json；pass/seed与编译命令在obf-build-flags.txt；运行对照在obf-run-equivalence.txt；原REA证据在control22/、obfuscated/；最终大小/CFG/分支口径在comparison-metrics.json；源码只增加真实pass annotation。两个小ELF在bin/，所有第三方工具在被忽略的.local-tools/。

复现先source docs/probe/scripts/env.sh；scripts/acquire-toolchain.py验收已有包或下载同一release，scripts/build-obfuscated.py构建并执行QEMU，node scripts/analyze.mjs执行REA，scripts/make-report.py核对证据并生成报告。脚本写入本目录；审计已存证据无需重跑。secret_transform的fla跳过已明确记录，不宣称三pass均有效。
''')
(base/'report-check.json').write_text(json.dumps({'raw_MCP_equals_decoded':True,'Ghidra_provider_and_target_digests_verified':True,
    'ELF_symbol_sizes_equal_Ghidra_body_lengths':True,'LLVM18_vs_22_control_pseudocode_byte_identical':True,
    'simple_checksum_all_three_passes_changed':True,'secret_transform_flattening_skipped':True,
    'QEMU_cases_equal':11,'LLVM22_port_required':False,'representative':'simple_checksum',
    'limitations':['No measured human reverse-engineering time','No full-input equivalence proof','Ghidra successfully decompiled both','secret_transform no CFG growth']},indent=2)+'\n')
print('Verified raw/decoded provenance, ELF function sizes, unchanged LLVM22 control, real pass statuses, and generated comparison/report copies.')
