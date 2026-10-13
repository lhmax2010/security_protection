# cost

入口：[comparison.md](comparison.md)。三档最终均已完成体积与真实板测，每档1次暖机+6次计时，解码600帧内容一致。

size-comparison.txt/json：总.so与.text绝对值/增长；perf-memory.txt、perf-memory-runs.json、perf-memory-summary.json：原始样本/中位数/波动/RSS；raw/：板上原始benchmark/framemd5/条件；compiler-reports/与obfuscation-scope.json：真实pass结果；build-logs/、build-status.json：每次尝试及原错误。初次全源码失败与最终优化IR方法区分，不是无条件全部函数混淆。

所有.so、ffmpeg、媒体、第三方源码、IR与运行缓存在被忽略private/；工具链在被忽略.local-tools/。不替换板子系统文件。脚本路径/原始命令可审计。

复现先source docs/probe/scripts/env.sh；board-connect.py确认指定板子，build.py核对已有完成marker/hash后复用；变更方法时须明确把旧产物/记录另存为新批次，脚本不会仅因源码脚本变动自动重编，summarize-builds.py测体积与范围，make-workload.py生成固定片，deploy-check.py推送并校验内容，measure-board.py运行暖机/6轮板测。已有测量只用measure-board.py --saved重新解析，make-report.py生成总表；audit.py验证文本/原始数据/哈希一致性。会写本目录及指定独立板上目录，审计无需重跑板测。
