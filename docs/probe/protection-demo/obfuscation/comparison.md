# LLVM22.1.8 真实代码混淆对比

本批用 **xollvm v0.11.1 的上游 Linux x86_64 预编译 clang/opt 22.1.8**，版本与PM给定Tizen平台22.1.8相同，ARM后端真实交叉编译成功；无需把该实现从旧LLVM移植到22。工具源码commit `eb0850bd7cc87f551ad2948826605e518f5b8aa2`，LLVM base `ca7933e47d3a3451d81e72ac174dcb5aa28b59d1`，获取方式/二进制哈希见 [toolchain.txt](toolchain.txt)。匹配上游版本不等于已验证Tizen供应商补丁、GBS打包或板子集成，这些本轮未做。

**可支持的结论：这两个函数的反编译可读性下降，simple_checksum最明显；没有证明算法不可恢复或量化人工逆向耗时。** Ghidra仍成功生成完整伪代码，两函数名字也保留。本轮专门隔离代码混淆，没有strip、字符串编码、额外栈保护等混入变化。

## 公平对照与参数

旧裸版Clang18.1.3及其REA证据完全复用（未重编/重分析）。另编相同源码、相同-O2/ARM ABI、**相同22.1.8工具链但不开pass**的控制版，分别用REA6.4.0/Ghidra12.1.4分析。两个函数在18裸版与22控制版的伪代码逐字相同、字节/基本块/直接分支数相同；这支持把本批变化归于混淆，而非18→22版本升级。

仅给两个noinline助手加 `annotate("obf: substitution(prob=100,loop=2), bcf(prob=100,loop=1,maxBlocks=200), flattening(minBlocks=2,maxBlocks=200)")`，算法源码表达式不变；按该实现对应关系 sub=substitution、bcf=bcf、fla=flattening。clang使用 `-mllvm -enable-obfuscation`、固定seed1、deterministic、verify。完整命令在 [obf-build-flags.txt](obf-build-flags.txt)，编译器真实pass/CFG报告在 [pass-report.json](pass-report.json) 与 [pass-report/](pass-report/)。没有用上游普通Clang的同名普通优化pass冒充混淆。

## secret_transform

| 指标 | 裸版18（已有） | 无pass控制22 | 混淆22 |
|---|---:|---:|---:|
| 函数字节（Ghidra与ELF符号尺寸一致） | 24 | 24 | 696 |
| Ghidra基本块 | 1 | 1 | 1 |
| 静态直接分支指令 | 0 | 0 | 0 |
| 完整伪代码行数（含空行） | 7 | 7 | 42 |
| 指令行数 | 6 | 6 | 174 |

裸版仅一行 `(param_1 ^ 0x5a17) * 0x21 + 7`；混淆版变成多个中间变量、栈地址掩码、AND/OR/XOR/NOT等组合，最终返回表达式不再直接呈现原式，尺寸 **29倍**。但 `0x5a17`、乘 `0x21`、加7仍可见，熟悉位运算恒等式的分析者仍可化简，不能说秘密算法被隐藏到无法还原。

**pass限制**：substitution确实把IR8条扩为313条；bcf报告changed=true但指令增量为0，最终仍1块/0直接分支，没有观察到持久的虚假控制流增量；flattening明确skipped/too few blocks。单行算术没有可平坦化的多块结构，本函数主要是**数据流替换**效果，不冒称fla/bcf三者全部有效。

原样节选：[裸版](report/baseline18-secret_transform.c) / [混淆版](report/obfuscated22-secret_transform.c)，伪代码Evidence `ev_ba700644b0cbdc6950d45e4fd29b48a366df36bd2dd3de093557a0fd84ee4460`。

## simple_checksum（报告首选）

| 指标 | 裸版18（已有） | 无pass控制22 | 混淆22 |
|---|---:|---:|---:|
| 函数字节（Ghidra与ELF符号尺寸一致） | 60 | 60 | 4284 |
| Ghidra基本块 | 5 | 5 | 39 |
| 静态直接分支指令 | 2 | 2 | 28 |
| 完整伪代码行数（含空行） | 20 | 20 | 311 |
| 指令行数 | 15 | 15 | 1071 |
| 伪代码if数量 | 1 | 1 | 36 |
| 伪代码goto数量 | 0 | 0 | 4 |

裸版是短小的逐字节do/while乘31累加循环；混淆版出现 `do ... while(true)` **调度循环**、多层嵌套条件、状态编码/状态指针选择、冗余恒等条件和goto。阅读者需先恢复分派状态和真路径，再区分校验更新与干扰表达式。尺寸 **71.4倍**，基本块5→39、直接分支2→28、伪代码20→311行，图与伪代码均支持“明显更难读”的定性结论。

实际substitution/bcf/flattening三pass均changed：IR24→217→846→1834。IR报告环路复杂度代理2→17是**编译器IR层度量**，不代替最终Ghidra基本块或人工难度；工具的difficulty score也不作为效果证明。最终仍能在混淆伪代码找到 `local_8c * 0x1f + (uint)*local_78`（原样文件第155行），不是全部逻辑消失。不能承诺抗自动去混淆或保护密钥。

原样报告图内容：[裸版](report/baseline18-simple_checksum.c) / [混淆版](report/obfuscated22-simple_checksum.c)，伪代码Evidence `ev_6fd2466cf340889e01e41a8a56df56b193ab7e05dd4b71d651c386a532191933`；同版本对照也放在 [report/](report/)。所有副本与REA normalized_result逐字相同，来源/哈希见 [report/provenance.json](report/provenance.json)。

## 核验、范围与失败记录

QEMU三版对照11组（默认、0/1/1234、65535/65536、uint32边界、strtoul溢出、负数、非法输入、多参数），stdout/退出码全部一致、stderr为空，见 [obf-run-equivalence.txt](obf-run-equivalence.txt)。本次main的checksum入参始终是marker字符串，不能据此声称所有字符串/所有输入已形式化证明等价；不含性能基准、实板运行或人工逆向计时。相同-O2但编译器后端仍会对变换优化，pass报告的“changed”不等于所有IR结构都留到机器码。

所有最终字节尺寸都与GNU readelf独立核对，所有基本块来自Ghidra procedure_info；分支行是Ghidra read_function_instructions中ARM直接b/b条件/cbz/cbnz静态指令数，**不含调用、bx返回、隐式PC转移，不是CFG边数或运行次数**。原始MCP响应与decoded投影均保存，见 [obfuscated/](obfuscated/) 和 [control22/](control22/)，派生统计见 [comparison-metrics.json](comparison-metrics.json)。

真实失败完整留存：web release页timeout（随后API成功）；旧Pluto URL和猜测workflow URL HTTP404；验收断言错误地要求opt --print-passes列出扩展pass，且当次shell随后继续checkpoint，已在STATE纠正。原trace见 [toolchain-validation-error.txt](toolchain-validation-error.txt)，实际opt pipeline调用及后续真实ARM构建/报告证实可用；没有抹去失败或把失败当pass成功。调研来源在 [toolchain-survey.txt](toolchain-survey.txt)，上游 [项目](https://github.com/und3ath/xollvm) / [v0.11.1 release](https://github.com/und3ath/xollvm/releases/tag/v0.11.1)。

交付范围仅本目录文本与两份自建小ELF；第三方clang/opt/发布压缩包只在忽略.local-tools/。**LLVM22移植不需要另做；Tizen构建体系/供应商版本集成与更广等价验证是独立后续工作，本轮未做。**
