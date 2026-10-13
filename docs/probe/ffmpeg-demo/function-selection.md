# 函数选择与定位

三个公开 FFmpeg API 在板子和上游的动态符号中均存在；REA search_procedures 按精确导出名定位，无手工改名。

- `avcodec_align_dimensions2`：像素格式/codec 分支、宽高向上对齐和行跨度约束，真实编解码缓冲区逻辑。来源：FFmpeg 8.0.1 libavcodec/utils.c。
- `av_packet_rescale_ts`：PTS、DTS 的 AV_NOPTS_VALUE 判断，duration > 0 检查和 av_rescale_q 调用，时间基转换。来源：libavcodec/packet.c。
- `av_get_audio_frame_duration2`：参数字段提取、调用内部帧长度助手、结果负数截为 0。进一步沿唯一直接 callee 定位助手；板子为 `0x23d794` / `FUN_0023d794`，并不假称原始内部名字由 REA 恢复。上游未 strip 助手保留 get_audio_frame_duration 名称；strip 后成为 FUN 地址。

对应源码：[utils.c](https://github.com/FFmpeg/FFmpeg/blob/n8.0.1/libavcodec/utils.c)、[packet.c](https://github.com/FFmpeg/FFmpeg/blob/n8.0.1/libavcodec/packet.c)。这些都是库中的实函数；选择偏向可复核的公开辅助 API，不能代表完整 H.264/HEVC 解码器的逆向难度。

REA 原始函数查询与 decoded Evidence、原样伪代码、反汇编、已解析 callers/callees 在各函数目录。内部音频助手伪代码存在 codec 枚举被误推为 char* 的问题，生成的空字符串/短字符串不是原库明文证据；算法恢复评估必须单独扣减。
