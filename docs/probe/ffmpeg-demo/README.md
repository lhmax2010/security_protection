# FFmpeg 逆向门槛报告证据

从 [comparison.md](comparison.md) 阅读三列结论；报告截图/排版用 [report/](report/README.md) 的两份原样伪代码。状态与未决限制在 ../STATE.md 的 ffmpeg-demo 一节。

- 板子身份、清单、库版本/编译器和加固：board-identity.txt、board-ffmpeg-inventory.txt、board-target-info.txt、board-target-hardening.txt。
- 实际 REA 原始 MCP/decoded Evidence 与伪代码：board/、upstream/、upstream-stripped/。按函数名子目录保存反汇编及调用关系。
- 自己编的上游 ELF：upstream-artifacts/，manifest 哈希与源码/许可证随附。来源、完整 configure/build、默认加固发现及最终覆盖见 upstream-source.txt、upstream-build*.txt。
- 审计：verification.json；复核命令 `python3 docs/probe/ffmpeg-demo/scripts/audit-results.py`。

本机复现：先 source docs/probe/scripts/env.sh；在工作目录运行 scripts/download-upstream.sh，再 scripts/build-upstream.sh（重定向日志必须放本目录）。REA 主分析用 `node docs/probe/ffmpeg-demo/scripts/analyze.mjs <variant> <本目录内样本路径>`，variant 为 board/upstream/upstream-stripped；已有输出拒绝覆盖，可用 REA_RUN_LABEL 设置新的本地 run 目录。先执行主分析再 scripts/analyze-helper.py，由首轮 callee 定位内部助手。完成后 scripts/publish-text.py 生成经白名单筛选字符串的文本投影；公开前审阅，绝不提交 private/。这些重跑会重建本机分析数据库，不会改板库。

板库本体在忽略目录 private/，不在公开仓。板上没有安装/编译/写入/删除任何文件；只通过 SDB 读取与明确授权 pull。Ghidra 数据库、缓存、原始暂存输出留在忽略目录。静态查询不等于运行观察，详细限制见 comparison.md。
