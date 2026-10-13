# protection-demo

入口：[comparison.md](comparison.md)。自建玩具保护ELF位于 bin/target_c_llvm_armv7l_protected；原基线不改动。报告原样伪代码与来源在 report/；REA原始响应及decoded投影在 protected/；非REA的ELF解码/readelf对照在 elf/。

复现先 source docs/probe/scripts/env.sh，再分别运行 scripts/build-and-run.py、scripts/analyze-protected.mjs（node）、scripts/collect-elf.py、scripts/make-report.py；这些脚本会写入本目录，审计既有证据时无需重跑。REA使用已安装6.4.0和Ghidra12.1.4，不联网、不连板、不用GBS。local-runtime/仅本机忽略，不提交第三方二进制。

本演示没有代码混淆；效果与限制以comparison.md为准。辅助文件查询的真实非零退出记录在diagnostic-errors.txt。
