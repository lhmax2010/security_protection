# 报告用伪代码

并排使用 [板库原样伪代码](board-av_packet_rescale_ts.c) 与 [上游裸编译原样伪代码](upstream-av_packet_rescale_ts.c)。选 av_packet_rescale_ts，因为它完整、较短，两个时间戳的无效值判断、duration > 0 与三处 av_rescale_q 回写都容易说明。两份均为 REA+Ghidra 输出，没有手工整理分支或补变量名；Evidence ID、目标和节选哈希见 provenance.json。

解释标注（依据上游 AVPacket 定义/API，**不是 REA 自动恢复的字段名**）：0x08/0x0c 是 pts 低/高字，0x10/0x14 是 dts 低/高字，0x30/0x34 是 duration 低/高字。高字 0x80000000 且低字 0 对应 AV_NOPTS_VALUE。ARM32 的高低字比较和 goto 增加阅读成本，但调用和回写位置仍清楚。av_rescale_q 的内部算法在另一个库 libavutil，此处只验证时间戳缩放调度，未把那个库的算法算作已恢复。

推荐图注：“Tizen 11.0.0 ARMv7 开发板 libavcodec 8.0.1 虽已 strip，公开函数名与时间戳转换逻辑仍可由 REA+Ghidra直接取得；上游裸编译 strip 前后该函数伪代码逐字相同。”

说明限制：这是 PM 确认的 RPi4 LLVM 开源开发板；板库编译器未知，上游用 GCC13 回退；soft-float/hard-float ABI 及组件集合不同，仅做静态对照。结果代表所选公开 API，不代表完整解码器或其他产品镜像。更完整结论及证据索引见 ../comparison.md。
