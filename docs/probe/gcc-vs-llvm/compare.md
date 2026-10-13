# GCC 参考构建与 LLVM 开发板：现有保护对照

**核心观察：同名16样本的 NX、PIE、strip、canary/FORTIFY 导入比例完全相同；RELRO 有双向差异。GCC参考FFmpeg启用了 hardened 配置和广覆盖栈检查，但这些攻击面加固并未阻止 REA 恢复选定算法。**

边界：参考侧16 ELF经精确NEVRA debuginfo、debuglink文件名+CRC32、GNU build-id配对确认 **GCC14.2.0**，见 [编译器证据](gcc-compiler-evidence.txt)、[debug下载元数据](debug-download-status.json)、[逐样本raw](raw/)。主包和debug包均来自用户指定reference repo及其相邻 standard/debug目录；只抽取分析，不安装/执行目标。公共reference是公司GCC构建的代理，并不证明公司内部镜像采用同一配置。

LLVM侧按PM给定板环境归类，复用 Tizen11.0.0 armv7l/RPi4 的27样本 + libavcodec，**没有连接或重测板子**。用户态各库编译器未被历史证据确认；不能把内核Clang或板环境标签当作每库Clang producer。两侧按同名组件配对，仍有release/版本/构建参数差异，统计不能当作编译器因果实验。

## 防被攻击（加固）

主判断使用同名16样本。另列历史27与加FFmpeg后的28样本，避免由样本组成差异制造假差距。DSO不计进PIE分母；libc保护helper定义提供者不当作“导入正例”；canary与stack-protector是同一证据轴，不重复计两项。strip按任务要求列此区，但它是减少静态命名/调试信息的反逆向卫生措施，不是漏洞利用防护。

| 指标 | GCC参考16 | LLVM板同名16 | LLVM历史27 | LLVM历史27+codec（28） |
|---|---:|---:|---:|---:|
| Full RELRO | 4/16 (25.00%) | 3/16 (18.75%) | 8/27 (29.63%) | 8/28 (28.57%) |
| NX | 16/16 (100.00%) | 16/16 (100.00%) | 27/27 (100.00%) | 28/28 (100.00%) |
| PIE executable | 6/6 (100.00%) | 6/6 (100.00%) | 11/11 (100.00%) | 11/11 (100.00%) |
| canary / stack-protector import | 13/16 (81.25%) | 13/16 (81.25%) | 21/27 (77.78%) | 22/28 (78.57%) |
| FORTIFY import | 12/16 (75.00%) | 12/16 (75.00%) | 17/27 (62.96%) | 18/28 (64.29%) |
| stripped | 16/16 (100.00%) | 16/16 (100.00%) | 27/27 (100.00%) | 28/28 (100.00%) |

GCC16 RELRO分布 Full4/Partial9/None3；同名LLVM16 Full3/Partial11/None2。因此不存在“所有GCC包Full RELRO、所有LLVM包没开”的结论。逐样本差异：

| 同名样本 | GCC参考 | LLVM板 | 判断 |
|---|---|---|---|
| libavcodec | Full | None | GCC参考更强，板侧可补齐 |
| libdbus_1_so_3 | Partial | None | GCC参考更强，板侧可补齐 |
| libsqlite3_so_0 | None | Partial | LLVM板更强，参考GCC也需补齐 |
| rpm | None | Partial | LLVM板更强，参考GCC也需补齐 |
| libdlog_so_0 | None | Partial | LLVM板更强，参考GCC也需补齐 |

原始判定：[GCC矩阵](gcc-hardening-matrix.txt)、[逐样本readelf/Lua投影](raw/)、[板侧历史矩阵](../board-survey/hardening-matrix.txt)、[板库libavcodec](../ffmpeg-demo/board-target-hardening.txt)。精确统计分母、同名配对与历史raw哈希见 [comparison-data.json](comparison-data.json)、[LLVM证据复用投影](raw/llvm-evidence-reuse.json)。

**栈保护的精度区别**：主ELF导入helper只证明某处用了保护，不能推断 strong/all 或每个函数覆盖。GCC匹配producer里有明确旗标（FFmpeg同时观察到 strong/all）；LLVM板只有历史导入证据。REA对 `avcodec_align_dimensions2` 和 `av_packet_rescale_ts` 的GCC伪代码可见 `__stack_chk_guard` 检查及失败调用；板侧对应原样伪代码未见这种检查。不能因此说整个LLVM板没有canary。

## 防被读懂（反逆向）

导出数指定义GLOBAL/WEAK、DEFAULT/PROTECTED、非UND、排除ABS版本节点的动态条目数，包含符号版本产生的重复项；C++数量用 `_Z` 前缀计数，不是“内部函数泄漏”的精确数。无需发布完整符号列表。

| 指标/代表样本 | GCC参考 | LLVM板（历史证据） | 可下结论的范围 |
|---|---|---|---|
| .symtab / debug信息 | 16/16主ELF无.symtab，.comment被移除，producer需匹配独立debug包读取 | 历史27与codec均无.symtab；codec无.comment | 两侧已strip，公开动态接口不受此影响；不能称debug内容绝无其他载体 |
| 实际 visibility 旗标 | 7/16样本匹配CU观察到 `-fvisibility=hidden`：dbus-daemon、libdbus、glib、bash、systemctl、dlog、pkgmgr-info | 历史未取得对应producer，旗标未知 | GCC部分已有；无旗标记录不证明没有隐藏，板侧不能仅凭导出数反推旗标 |
| libavcodec | 145动态项，其中144函数，0 C++mangled | 同样145/144/0 | 公开API可见，内部名字大量缺失，存在接口边界；不是完整导出所有实现，也不能证明具体隐藏旗标 |
| libdlog | 11动态项，0 C++ | 同样11/0 | 少量API已收敛，两侧都不是完全没符号控制 |
| GLib | 1879动态项，0 C++ | 同样1879/0 | 大API表面不自动等于内部实现泄漏 |
| libstdc++ | 5898动态项，5816 C++mangled | 同样5898/5816 | 标准C++运行库ABI很大，不能简单当保护漏洞 |
| libcrypto | 5790动态项，0 C++ | 同样5790/0 | 大量公开密码API名字仍可读，是否应隐藏须接口契约 |
| pkgmgr-info | 1371动态项，1073 C++mangled，producer中有hidden旗标 | 1456动态项，1158 C++mangled | 两侧都有大量类/模板命名线索；GCC即便开hidden也非仅少量C API。要判定“内部”需导出白名单/源码接口裁决 |
| 明文字符串 | 每个样本.rodata都有ASCII明文候选，最少8字节连续打印字符计数48–7824；每样本仅公开3条安全样本 | 历史27未做同口径.rodata计数，记未知；codec已REA取得版本/API/错误信息明文 | 两侧codec明文暴露真实；不能将GCC.rodata计数与旧Ghidra定义字符串数直接相减 |
| 代码混淆 | 参考codec两选API主要算法可读，栈保护增加guard但不掩盖关键分支/调用 | 同名API主要算法可读，更多goto/匿名字段仍可解释 | 所选函数没有形成有效阅读阻碍；不能证明整库/全部包完全没有任何混淆 |

16同名样本里，15个动态导出计数完全相同，只有pkgmgr-info不同；这不支持“LLVM普遍多泄漏符号”。[矩阵](gcc-hardening-matrix.json)有精确计数，但没有完整名称清单；[producer raw](raw/)给hidden旗标实证，不能由数量冒认编译旗标。

### FFmpeg 同版本的具体对照

| 项目 | GCC公开参考libavcodec 8.0.1-1 | LLVM板libavcodec 8.0.1-0 |
|---|---|---|
| 主ELF大小 | 5,049,684 bytes | 3,062,768 bytes |
| Full RELRO | 有 | 无RELRO |
| 栈保护 | producer有 `-fstack-protector-all/strong`；两选API均有guard/fail | 整库有canary导入，但两选API未见guard/fail |
| FORTIFY | 有导入证据 | 有导入证据 |
| strip / NX | 都有 | 都有 |
| 动态导出函数 | 144 | 144 |
| configure明文 | 含 `--toolchain=hardened`，额外开启VP8/VP9等组件 | 旧配置没有 `--toolchain=hardened` |
| REA定义字符串数（相同工具口径） | 5577 | 5386 |
| `av_packet_rescale_ts` | 无效PTS/DTS判断、正duration检查、三次缩放回写清楚，另有栈检查 | 同样关键逻辑可读，多一些goto |
| `avcodec_align_dimensions2` | 像素格式/codec分支、向上对齐可辨；枚举/结构体名未恢复，向量表达式复杂 | 同样主逻辑可辨，字段/枚举名缺失 |

配置原始证据：[GCC配置明文](raw/libavcodec-config-string.txt)、[板库旧配置](../ffmpeg-demo/board-target-info.txt)。GCC `--toolchain=hardened` 与实际RELRO/SSP相互支持；可归为**FFmpeg包构建策略的补齐项**，并不证明Clang工具链本身不支持这些措施。组件和构建版本不同，不能按二进制大小评判混淆强弱。

REA原始证据：[GCC时间戳伪代码](rea/upstream/av_packet_rescale_ts/pseudocode.decoded.json)、[GCC尺寸对齐伪代码](rea/upstream/avcodec_align_dimensions2/pseudocode.decoded.json)、[板时间戳伪代码](../ffmpeg-demo/board/av_packet_rescale_ts/pseudocode.decoded.json)、[板尺寸对齐伪代码](../ffmpeg-demo/board/avcodec_align_dimensions2/pseudocode.decoded.json)、[GCC overview](rea/upstream/overview.decoded.json)、[板overview](../ffmpeg-demo/board/overview.decoded.json)。这里是未加载debuginfo的主库静态分析；没有执行库、也没有保证完整解码器或所有间接调用已恢复。

## 逐项保护结论

以下保留“既有”“局部补齐”“新增候选”“未知”四种状态。强行把全部项目二分为“GCC已有/LLVM补课”或“两边都没有”会违反实际证据。

| 计划项 | GCC参考侧已有？ | LLVM板已有？ | 本轮可支持的判定 |
|---|---|---|---|
| 符号收敛 | **部分已有**：7样本producer有hidden；dlog仅11导出；codec保留145动态项。但pkgmgr仍1073个C++mangled条目 | **部分已有的接口形态**：dlog/codec同量级；pkgmgr1158个C++mangled条目，hidden旗标未知 | 不支持“LLVM完全没做”。现有接口收敛不是新增；进一步对白名单之外C++实现严格隐藏是**共同加强/新增策略候选**，必须先审接口契约，不归为单纯LLVM补课 |
| 完整strip | **主ELF已做**：16/16无.symtab，均无嵌入.debug_info/.zdebug_info | **主ELF已做**：旧27和codec均strip | **两边既有**，不能报作新增或LLVM补课；单独审debug侧车/发布流程，不能靠再strip隐藏动态ABI |
| Full RELRO | 4/16已有；codec/libc为Full，仍有其他Partial/None | 同名3/16已有；codec None、libc Partial；sqlite Full甚至强于参考GCC | **codec/libc向GCC基线补齐（LLVM板包构建补课）**；其余缺口按包处理，也有GCC更弱项。这是攻击面加固，不是新增代码保密能力 |
| FORTIFY | 12/16导入正例，libc provider另算；缺导入不证明旗标关闭 | 同名同样12/16；codec两侧均有 | **两边部分既有、需覆盖核验**；没有同名统计缺口证据，不能统称LLVM补课，也不能称两边都没有 |
| 栈保护 | 13/16导入正例；codec有all/strong producer，两选API有guard/fail | 同名同样13/16，codec整体已有canary，但两选API未见guard/fail；exact flag未知 | **基本SSP已在两边存在**；codec这两路径的更广栈检查属于**GCC已有/LLVM板补齐候选**，应移植验证all/strong策略，而不是宣称首次给LLVM加SSP |
| 字符串处理 | 每个样本均有.rodata打印串；codec版本/config/诊断仍明文 | codec版本/config/诊断仍明文；其他库同口径数量未知 | 对本轮明确暴露、计划选择的字面量实施隐藏/运行时解码，可列**真正新增的反逆向能力候选**；不能断言两侧从未处理任何别的字符串，也不应承诺清除动态ABI所需名字 |
| 代码混淆 | REA所选两API主要算法可读，没有形成有效阻碍；未穷尽全部代码/旗标 | 同名主要算法同样可读；类型、匿名名和goto有成本，不自动等于混淆 | 在这些路径加可验证的变换可列**真正新增候选**，不是补memory-hardening；“全库任何混淆均不存在”仍**未知**，需受保护前后同函数对照验证 |

**报告建议**：把“恢复FFmpeg hardened构建效果（Full RELRO和更广SSP）”列为构建策略补齐；把“业务敏感字符串处理、使所选算法更难恢复的代码变换、按API契约进一步收紧C++实现可见性”列为新增反逆向能力候选。已有strip、部分hidden、FORTIFY、基本SSP不能包装为从零新增。

公开reference的**debug包也确实可下载并与16 ELF匹配**（[CRC/build-id/producer证据](gcc-compiler-evidence.json)）。因此“主ELF完整strip”不意味着参考构建的全部调试/内部命名信息不可取得。公司是否向外分发相同debug侧车未在本轮输入中，不能照搬成公司产品结论。

所有分类由前面的逐样本raw/REA结果支撑；这里只判定本批与选定路径。公共GCC与LLVM板非同一构建实验，公司内部GCC实际配方、LLVM用户态compiler/精确旗标、接口白名单、全库选择性字符串保护/混淆是否存在，仍需相应证据。并未通过新测板子补齐这些未知。
