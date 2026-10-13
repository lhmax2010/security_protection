# obfuscation

入口：[comparison.md](comparison.md)。报告首选simple_checksum的完整原样伪代码对照：report/baseline18-simple_checksum.c 与 report/obfuscated22-simple_checksum.c。

工具链真实22.1.8预编译，详见toolchain.txt/selected-asset.json；pass/seed与编译命令在obf-build-flags.txt；运行对照在obf-run-equivalence.txt；原REA证据在control22/、obfuscated/；最终大小/CFG/分支口径在comparison-metrics.json；源码只增加真实pass annotation。两个小ELF在bin/，所有第三方工具在被忽略的.local-tools/。

复现先source docs/probe/scripts/env.sh；scripts/acquire-toolchain.py验收已有包或下载同一release，scripts/build-obfuscated.py构建并执行QEMU，node scripts/analyze.mjs执行REA，scripts/make-report.py核对证据并生成报告。脚本写入本目录；审计已存证据无需重跑。secret_transform的fla跳过已明确记录，不宣称三pass均有效。
