# FFmpeg ARMv7 出厂库与上游裸编译：REA 对照

**所采样的三个公开 API 在已 strip 板库中仍能按导出名直接定位，并恢复主要分支、字段访问和调用；strip 没有遮住这些逻辑。** 音频内部助手能追进去，但类型误推明显；这份证据不能证明整库没有混淆，也不能代表完整解码器已被重建。

板子是 PM 确认的上一轮 RPi4 LLVM 开源开发板，不将本结果扩展为另一个未采集 SR 产品镜像。Tizen 11.0.0 Unified / armv7l，预装 FFmpeg 8.0.1，目标 libavcodec.so.62.11.100，3,062,768 bytes。版本、包信息与开源构建字符串见 [board-target-info.txt](board-target-info.txt)、[board-ffmpeg-inventory.txt](board-ffmpeg-inventory.txt)。板库编译器未知；.comment 缺失，不能由内核 LLVM 编译器推断用户态库编译器。

上游使用官方 **同版本 8.0.1** 源码、GCC 13.3、ARMv7 -O2、最小共享库构建。显式关闭工具链默认 SSP/FORTIFY/RELRO；保持 FFmpeg 默认 NX、DSO 必需 PIC。不混淆、无 debug，原始库不 strip，副本 --strip-unneeded。完整命令、编译日志与版本差异见 [upstream-build.txt](upstream-build.txt)、[upstream-source.txt](upstream-source.txt)。板库 soft-float ABI，上游 hard-float ABI；仅对整数/指针 API 做静态对照，不作为可直接替换的板端运行产物。发行版 patches、编译器及组件集合未匹配，不能把差异归因于保护。

分析器：REA 6.4.0，唯一原生 provider 为 Ghidra 12.1.4；没有 Hopper/IDA。未执行目标库。下表可读性为人工评述，不是 REA 自动评分。函数体无业务明文字符串锚点时记为 N/A；整库字符串另看下表。

| 函数 | 板子出厂库（已 strip） | 上游裸编译（未 strip） | 上游裸编译（strip 后） |
|---|---|---|---|
| `avcodec_align_dimensions2` | **主要逻辑可读**：像素格式 switch、codec 条件、`(n+a-1)&-a` 向上对齐、最小宽度与附加行可辨。导出名保留；函数体字符串 N/A。可读性中：数值枚举、param 字段偏移、goto、NEON 向量表达式仍需解释。[伪代码/证据](board/avcodec_align_dimensions2/pseudocode.decoded.json) | **主要逻辑可读**，名称保留；字段/枚举名仍缺失，部分分支与向量表达式复杂。函数体字符串 N/A。可读性中。[伪代码/证据](upstream/avcodec_align_dimensions2/pseudocode.decoded.json) | **主要逻辑可读**；导出名保留，函数体字符串 N/A。伪代码与未 strip **逐字相同**。[伪代码/证据](upstream-stripped/avcodec_align_dimensions2/pseudocode.decoded.json) |
| `av_packet_rescale_ts` | **逻辑清楚**：两个 64-bit 无效时间戳判断、duration 正数判断、三处 `av_rescale_q` 调用与结果回写可见。导出名保留，函数体字符串 N/A。可读性中上：32-bit 拆分 64-bit 比较、goto，比上游绕一些。[伪代码/证据](board/av_packet_rescale_ts/pseudocode.decoded.json) | **逻辑清楚**：三个条件分支、三处缩放回写清楚；导出名保留，函数体字符串 N/A。可读性较高，但类型仍是 param/undefined，需要源码/API 对照解释字段名。[伪代码/证据](upstream/av_packet_rescale_ts/pseudocode.decoded.json) | **逻辑清楚**；导出名保留，函数体字符串 N/A。伪代码与未 strip **逐字相同**。[伪代码/证据](upstream-stripped/av_packet_rescale_ts/pseudocode.decoded.json) |
| `av_get_audio_frame_duration2` + 唯一内部助手 | **包装逻辑清楚，内部算法部分恢复**：字段取值、调用与负数截为0清楚；内部函数 `FUN_0023d794` 的 PCM 位深/声道/字节数计算、codec 分支常量可见。公开名保留、内部名丢失；函数体业务明文 N/A。助手可读性较低：codec 整数被误推为 char*，生成空/短字符串伪影，整数除法助手也匿名，不能直接当正确 C 编译。[包装](board/av_get_audio_frame_duration2/pseudocode.decoded.json)、[内部助手](board/av_get_audio_frame_duration2/helper/pseudocode.decoded.json) | **包装清楚，内部算法部分恢复**；公开名与 `get_audio_frame_duration` 内部名保留，部分算术助手名字也在。无自动结构体/枚举类型；同样有 char* 误推，不能称完整类型恢复。函数体业务明文 N/A。[包装](upstream/av_get_audio_frame_duration2/pseudocode.decoded.json)、[内部助手](upstream/av_get_audio_frame_duration2/helper/pseudocode.decoded.json) | **包装清楚，内部算法部分恢复**；公开名保留，内部助手变成 `FUN_0002c180`；部分算术仍可辨，类型伪影同未 strip。函数体业务明文 N/A。[包装](upstream-stripped/av_get_audio_frame_duration2/pseudocode.decoded.json)、[内部助手](upstream-stripped/av_get_audio_frame_duration2/helper/pseudocode.decoded.json) |

音频助手通过包装函数唯一直接 callee 定位；“对应源码内部助手”来自调用参数与上游对照推断，板子的原始名字没有被恢复。函数选择和范围见 [function-selection.md](function-selection.md)。所有调用图均为静态已解析直接调用/引用，间接或计算调用不保证覆盖。

| 整库属性 | 板库（已 strip） | 上游未 strip | 上游 strip 后 |
|---|---:|---:|---:|
| RELRO | None | None | None |
| NX / GNU_STACK | Enabled | Enabled | Enabled |
| PIE | N/A（DSO，不计作 PIE 可执行文件） | N/A（DSO/PIC） | N/A（DSO/PIC） |
| canary 导入证据 | 有 | 无 | 无 |
| FORTIFY 导入证据 | 有 | 无 | 无 |
| .symtab | 无 | 有 | 无 |
| RPATH / RUNPATH | 均无 | 均无 | 均无 |
| 定义动态导出项，不含 ABS 版本节点 | 145 | 141 | 141 |
| 其中函数项 | 144 | 140 | 140 |
| Ghidra 本地非 external/非 thunk 函数 | 3156 | 389 | 305 |
| 其中非 FUN 标签 | 147（4.66%） | 389（100%） | 143（46.89%） |
| REA 定义字符串条目 | 5386 | 2412 | 1742 |
| 实测明文样本 | `FFmpeg version 8.0.1`、三个 API 名、错误信息 | `FFmpeg version 8.0.1`、三个 API 名 | `FFmpeg version 8.0.1`、三个 API 名 |

加固原始证据：[板端 RPM Lua ELF 元数据](board-target-elf-metadata.txt)、[板库本机 readelf](board-target-local-readelf.txt)、[上游元数据](upstream-lua-metadata.txt)、[strip 后元数据](upstream-stripped-lua-metadata.txt)。Lua decoder 使用板上已有 RPM Lua，只读读取 ELF；没有在板上安装工具。Canary/FORTIFY 只证明存在相关导入，不代表全部函数都受到保护。

REA 符号/字符串统计证据：[board](board/symbol-string-statistics.json)、[upstream](upstream/symbol-string-statistics.json)、[stripped](upstream-stripped/symbol-string-statistics.json)，每个目录都有完整 list_procedures Evidence 与标明投影范围的 strings-samples.json。**非 FUN 比例只是命名标签代理，不是原始函数名恢复率**；strip 后函数边界识别也会变化，跨大小不同的两库不能据此定量比较逆向总工作量。上游已保留部分 API 可见性控制，裸编译并不自动导出所有内部实现。

[verification.json](verification.json) 独立核对三组 Evidence 的样本 SHA256、provider/version、所有伪代码与 decoded 文本一致；上游两份库 `.text/.rodata/.dynsym/.dynstr` 的大小和 SHA256 **完全一致**。因此本次 strip 对照是去掉静态符号后的同一代码，不是两次不同构建；公开 API 的名字和相关算法没有因 strip 消失。

可放报告的结论：**当前采集的 Tizen 开发板 libavcodec 虽已 strip，并存在 NX/canary/FORTIFY，仍能通过公开 API 直接定位并恢复所选辅助函数的关键逻辑；strip 和这些内存加固没有构成这些函数的代码保密屏障。** 内部名称、枚举/结构体类型和复杂控制流增加人工解释成本。证据支持“这些函数的逆向门槛较低”，不支持“全库完全无保护”“完整解码器已恢复”或“另一个产品镜像已被验证”。

失败/限制：首次 MCP 60s 超时真实错误在 [mcp-first-attempt-error.txt](mcp-first-attempt-error.txt)，修正客户端参数后成功；板库 compiler/发行版 patches 未知；ABI 与组件集合不同；没有运行等价性验证。板库原始二进制、本机缓存和完整字符串采集留在 gitignored private/local-runtime，公开仓中的 ELF 仅是本机从官方上游编出的产物。
