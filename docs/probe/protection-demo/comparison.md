# 第三层演示：合成 ARMv7 靶子的保护效果

本批验证了“隐藏名字与静态明文锚点、加强攻击面防护”，**没有证明秘密算法明显更难读**。XOR 是可逆编码，Ghidra甚至已把marker还原为字符常量；不能把它表述为密钥保密或“逻辑无法恢复”。这是用户指定flag组合的玩具演示，不代表已集成任何专有保护产品/pass。

| 项目 | 裸编译版（已有基线） | 加我们保护版 |
|---|---|---|
| secret_transform 按名字定位 | REA命中1项：0x10534 / secret_transform | REA命中0项；按已知地址0x105d0仍可读取 FUN_000105d0 |
| LICENSE_KEY_CHECK_V1 明文搜索 | REA命中1项：0x10688；GNU strings命中1项 | REA和GNU strings均0命中；整文件也无这段连续明文字节 |
| marker 内容是否仍可恢复 | 直接读字符串 | **可以**：Ghidra的main伪代码已输出0x4c、0x49等20个ASCII常量，顺序恢复为完整marker；运行输出也保留明文 |
| secret_transform 伪代码可读性 | `(param_1 ^ 0x5a17) * 0x21 + 7` | 同一表达式；仅函数标识符不同，替换名字后两份伪代码逐字相同；均24字节函数 |
| RELRO | Partial | Full（GNU_RELRO + NOW） |
| NX请求 | Enabled | Enabled（既有能力保留） |
| PIE | Yes | Yes（既有能力保留，显式-fPIE/-pie） |
| canary | 无动态helper证据 | 有__stack_chk_guard/__stack_chk_fail导入，main伪代码有guard/fail；不承诺每个函数都插桩 |
| FORTIFY | 无动态helper证据 | _FORTIFY_SOURCE=2，真实__printf_chk导入/调用；不代表所有操作都受保护 |
| 完整strip | 含.symtab | --strip-all，已无.symtab |
| 符号可见性 | .symtab中两助手GLOBAL DEFAULT，main GLOBAL DEFAULT | 编译后两助手LOCAL DEFAULT、main GLOBAL HIDDEN；strip后这些名字不在最终符号表 |
| 动态导出（非ABS定义GLOBAL/WEAK且DEFAULT/PROTECTED） | 0 | 0；裸版本来就没有动态导出，不能声称从有导出变成无导出 |
| Ghidra本地非thunk函数 / FUN标签 | 10 / 0 | 10 / 6；仅命名代理，不能等同函数恢复率 |
| REA字符串行数 | 88 | 43；包括符号字符串等，不是敏感信息保护率 |
| 运行结果 | 既有二进制 | QEMU默认值、边界/溢出/非法输入等11组stdout/exit一致；stderr均空，非全输入形式化证明 |
| 代码混淆 | 本轮不重测基线 | 本轮没有添加混淆；已有工具能力检查另见 obfuscator-availability.json |

名字/字符串搜索的Evidence IDs：裸版 ev_25a077038799906f972f4240cf71eb01249047bbe1fc57af4a483aec6d70871c / ev_5829230885c0fbd0af26e2e96b48bf8679f5dee6985a646697c447fa3b1c5cef；保护版 ev_f767ca2540f937e6c4ffa61f1f2cb462e7b7a422fa109db7ed9b2c56b0d66d44 / ev_c209b1e952555ee087ece6df309918fe94790e8ef3d7e617e74151d3c98e5a18。完整目标哈希、原始响应哈希、Ghidra版本与报告节选来源见 [report/provenance.json](report/provenance.json)。裸版直接复用 [既有证据](../evidence/target_c_llvm_armv7l/)，未重新编译或运行REA分析。

算法节选：[裸版](report/baseline-secret_transform.c) / [保护版](report/protected-secret_transform.c)。地址定位使用strip前GNU readelf的构建真值，加上REA overview里的.text映射偏移，见 [function-addresses.json](function-addresses.json) 与 [protected/address-provenance.json](protected/address-provenance.json)；**这是已知地址下的可读性对照，未测量盲逆向发现时间**。Ghidra推断short/ushort不等于原C源码uint32_t签名已被恢复。

加固结论由既有通过验证的只读Lua ELF解码器与GNU readelf独立对照（两份文件所有字段相同）支撑，见 [hardening-summary.json](hardening-summary.json) 与 [elf/](elf/)；它们不是REA结果。全部指定flag均被Clang18接受、没有诊断警告，完整构建/strip命令见 [build-flags.txt](build-flags.txt)、[build-log.txt](build-log.txt)，执行证据见 [run-equivalence.txt](run-equivalence.txt)。编码数据仍可读取，运行时局部缓冲区与stdout包含解码结果。

报告可用结论：名字与静态字符串的一步定位锚点减少，RELRO、栈保护和FORTIFY增强；算法恢复与marker恢复仍容易。若要演示算法变难读，下一步需要真实混淆器和同函数前后实测，本轮不以手工扰乱代码替代。
