# REA + Ghidra 逆向裸基线台账

日期：2026-10-12（Asia/Shanghai）。目录：`/home/linhao/Toolchain/development/security_optimization_rea`。远端：`https://github.com/lhmax2010/security_protection.git`；分支：`poc/probe`。本轮实验已完成，明确的工具能力缺口仍挂账。

## 计划与进度

| 子步骤 | 状态 | 证据入口 |
|---|---|---|
| 初始化 Git、远端、台账 | 完成，空远端首推已成功 | [bootstrap](evidence/bootstrap.txt) |
| 安装 Node/npm/JDK/Ghidra/REA | 完成，安装于本地用户可写目录 | [安装日志](evidence/install-runtime.txt)、[版本](evidence/installed-tool-versions.txt)、[JDK复验](evidence/jdk-verification.txt) |
| 官方 setup、Ghidra provider、doctor | 完成；Codex+Ghidra 专项健康，全量审计失败保留 | [setup计划](evidence/rea-setup-plan.json)、[执行](evidence/rea-setup-applied.json)、[doctor原输出](evidence/doctor.txt)、[专项](evidence/doctor-codex.json) |
| GCC、Clang ARMv7 ELF | 完成；ARM32 EABI5，-O2，未 strip | [GCC file](evidence/target_c_gcc_armv7l-file.txt)、[LLVM file](evidence/target_c_llvm_armv7l-file.txt) |
| Rust ARMv7 ELF | 完成；ARM32，opt-level=2，strip=none | [Rust file](evidence/target_rust_armv7l-file.txt)、[构建](evidence/target_rust_armv7l-build-retry.txt) |
| Python pyc、JS、.NET DLL | 完成 | [pyc file](evidence/target_py.pyc-file.txt)、[JS file](evidence/target_js.js-file.txt)、[DLL file](evidence/target_dotnet.dll-file.txt) |
| 每个样本 REA 主分析 | 完成；pyc 实测不支持 | 各样本目录 `analysis-run.txt`、`requests.json`、原始 MCP `.json` |
| 必要补查及 JS/.NET 补充能力 | 完成；原错误保留 | [Rust补查](evidence/target_rust_armv7l/supplemental/requests.json)、[JS recovery](evidence/target_js.js/recovery-with-wakaru.json)、[NET import](evidence/target_dotnet.dll/supplemental/imported-reconstruction.decoded.json) |
| 样本等价性与审计收尾 | 完成；30次执行成功、五组输入输出一致 | [执行汇总](evidence/runtime-smoke-summary.json)、[样本hash](evidence/runtime-artifact-hashes.txt) |

## 安装版本、路径及配置

所有相对路径均相对于工作目录。环境入口：`source docs/probe/scripts/env.sh`。用户不具备无密码 sudo，使用官方归档或 Ubuntu deb 解包安装，不改系统软件包。证据：[权限与宿主](evidence/bootstrap.txt)、[本地deb包版本](evidence/local-deb-package-versions.txt)。

| 组件 | 实测版本 | 实际路径 | 证据 |
|---|---|---|---|
| Node / npm | 24.21.0 / 11.19.0 | `.local-tools/node-v24.21.0-linux-x64/bin/` | [版本](evidence/node-rea-versions.txt)、[归档校验/安装](evidence/install-runtime.txt) |
| REA | npm `rea-agents` 6.4.0；MCP catalog 170 tools | `.local-tools/rea/node_modules/rea-agents/` | [版本](evidence/node-rea-versions.txt)、[真实tools/list](evidence/rea-mcp/tools-list.json)、[server](evidence/rea-mcp/server-version.json) |
| Ghidra | 12.1.4 PUBLIC，官方 20260921 发布包 | `.local-tools/ghidra_12.1.4_PUBLIC/` | [官方release元数据](evidence/ghidra-release.json)、[归档hash匹配](evidence/ghidra-archive-hash.json) |
| JDK | OpenJDK 21.0.12.1，64-bit，含 javac | `.local-tools/sysroot/usr/lib/jvm/java-21-openjdk-amd64/` | [版本/启动复验](evidence/jdk-verification.txt) |
| ARM GCC | 13.3.0 | `.local-tools/sysroot/usr/bin/arm-linux-gnueabihf-gcc-13` | [版本](evidence/installed-tool-versions.txt) |
| Clang/LLVM | 18.1.3 | `.local-tools/sysroot/usr/bin/clang-18` | [版本](evidence/installed-tool-versions.txt) |
| Rust | 1.99.0；target `armv7-unknown-linux-gnueabihf` | `.local-tools/cargo/bin/`、`.local-tools/rustup/` | [版本/targets](evidence/installed-tool-versions.txt)、[安装](evidence/install-rust-dotnet.txt) |
| .NET | SDK 8.0.425 / runtime 8.0.31 | `.local-tools/dotnet/` | [版本](evidence/installed-tool-versions.txt) |
| Wakaru | 1.14.0，官方Linux x64 binary | `.local-tools/wakaru` | [版本/hash](evidence/wakaru-install.txt)、[REA provider记录](evidence/target_js.js/recovery-with-wakaru.json) |
| ILSpy CLI | 9.1.0.7988（适配已安装 .NET8） | `.local-tools/dotnet-tools/ilspycmd` | [版本](evidence/target_dotnet.dll/ilspy-version.txt)、[安装](evidence/ilspy-install.txt) |
| QEMU ARM user-mode / Python / checksec | 8.2.2 / 3.12.3 / 2.6.0 | `.local-tools/sysroot/usr/bin/qemu-arm`、`/usr/bin/python3`、本地deb checksec | [实测版本](evidence/runtime-artifact-hashes.txt)、[QEMU安装](evidence/qemu-install.txt) |

`REA_ANALYSIS_PROVIDER=ghidra`，每次原生 `open_binary` 另传 `provider_id=ghidra`。`GHIDRA_INSTALL_DIR`、`JAVA_HOME` 使用绝对本地路径。Linux x64 decompiler 存在且 header 与宿主匹配；没有调用 Hopper/IDA。证据：[providers](evidence/providers.json)、[doctor-ghidra](evidence/doctor-ghidra.json)、[GCC open](evidence/target_c_gcc_armv7l/open.decoded.json)。

setup 仅配置 Codex：`~/.codex/config.toml` 中注册 `npx -y rea-agents@6.4.0 mcp`，写入 Ghidra/JDK 环境；官方技能位于 `~/.agents/skills/reverse-engineer-anything/`。Node/npm/npx 有 `~/.local/bin/` 链接，普通注册runner已实际运行；本次用独立 stdio MCP 客户端实测，当前聊天不会因 setup 自动重新连接。证据：[REA注册摘录](evidence/rea-registered-config.json)、[用户PATH链接](evidence/node-user-path-links.txt)、[注册runner版本](evidence/registered-runner-version.txt)、[MCP发现](evidence/rea-mcp-discovery-retry.txt)。

## 样本设计与比较口径

- 源码与产物都提交在 `docs/probe/samples/`。可识别函数为 `secret_transform`、`simple_checksum`，明文为 `LICENSE_KEY_CHECK_V1`。共同逻辑：`((x ^ 0x5a17) * 33 + 7) & 0xffff`；校验逐ASCII字节计算 `(sum * 31 + b) & 0xffff`。默认 x=1234；Rust 校验ABI是指针+长度，C是NUL终止，所测固定ASCII数据一致。执行证据：[六产物五输入汇总](evidence/runtime-smoke-summary.json)。
- C 使用同一份源码分别由 GCC/Clang 交叉编译；本任务“C/C++”槽位选 C，没有额外 C++ 产物。两个原生锚点函数用 noinline 保留边界；Rust 额外使用 no_mangle 保留可识别函数名。这些是样本可测性设置，未加入混淆或保护。命令：[GCC](evidence/target_c_gcc_armv7l-build-retry.txt)、[LLVM](evidence/target_c_llvm_armv7l-build-retry.txt)、[Rust](evidence/target_rust_armv7l-build-retry.txt)。
- 原生均 `-O2` / Rust `opt-level=2`，不 strip；没有额外关闭默认 PIE/NX/RELRO/FORTIFY。GCC有默认FORTIFY/Full RELRO，LLVM为Partial RELRO、无FORTIFY，Rust为Full RELRO。证据：[GCC checksec](evidence/target_c_gcc_armv7l-checksec.txt)、[LLVM checksec](evidence/target_c_llvm_armv7l-checksec.txt)、[Rust checksec](evidence/target_rust_armv7l-checksec.txt)。
- Python没有原生-O2对应项，本轮`py_compile optimize=0`；JS原始无混淆源码；.NET Release `Optimize=true`、保留元数据/PDB。Rust标准库带debug_info，C不额外加-g；因此不推断消除所有工具链差异后的语言难度。证据：[pyc构建](evidence/target_py-build.txt)、[JS准备](evidence/target_js-build.txt)、[NET构建](evidence/target_dotnet-build.txt)、[Rust file](evidence/target_rust_armv7l-file.txt)。
- 原生比例分母为readelf中**已定义STT_FUNC的唯一（入口地址、符号名）**，排除UND/ABS，合并重复dynsym/symtab行，清除ARM Thumb地址低位，再用实测Ghidra image slide=0x10000比对。不是全部数据符号比例，也不是“反编译正确率”。JSON逐条保留原名字、入口、观察名字及是否匹配：[GCC](evidence/target_c_gcc_armv7l/symbol-recovery-metrics.json)、[LLVM](evidence/target_c_llvm_armv7l/symbol-recovery-metrics.json)、[Rust](evidence/target_rust_armv7l/symbol-recovery-metrics.json)。

## 六类样本恢复表

“强”指本轮逆向恢复清楚、容易审读。均为静态观察；不能把伪代码类型推断或外部reconstruction当成原始源码真值。

| 样本 | 函数名锚点 | 明文锚点 | 算法逻辑与可读性 | 函数名/入口比例 | 可用REA工具、错误/限制 | 实际证据 |
|---|---|---|---|---|---|---|
| `target_c_gcc_armv7l` | 两函数名称完整 | 库存与搜索找到 `.rodata` 字符串 | 两算法简短清楚；short/ushort推断不等同源码uint32；main有多余参数/错误返回组合，可读性低于LLVM | 精确名字11/11；入口11/11；库存32含imports/thunks | overview、procedures、strings、search、info、pseudo、assembly、instructions、callers/callees、references、dossier均成功；无独立list_symbols工具 | [伪代码](evidence/target_c_gcc_armv7l/secret_transform-pseudocode.c)、[校验](evidence/target_c_gcc_armv7l/simple_checksum-pseudocode.c)、[main](evidence/target_c_gcc_armv7l/main-pseudocode.c)、[汇编](evidence/target_c_gcc_armv7l/secret_transform-assembly.asm)、[字符串](evidence/target_c_gcc_armv7l/marker-search.decoded.json)、[请求清单](evidence/target_c_gcc_armv7l/requests.json) |
| `target_c_llvm_armv7l` | 两函数名称完整 | 库存与搜索找到明文 | 两算法清楚；main调用参数自然；仍有short/ushort与undefined4推断 | 精确名字11/11；入口11/11；库存32 | 与GCC相同的原生操作全部成功；全局数据符号不单独计比率 | [伪代码](evidence/target_c_llvm_armv7l/secret_transform-pseudocode.c)、[校验](evidence/target_c_llvm_armv7l/simple_checksum-pseudocode.c)、[main](evidence/target_c_llvm_armv7l/main-pseudocode.c)、[字符串](evidence/target_c_llvm_armv7l/marker-search.decoded.json)、[请求清单](evidence/target_c_llvm_armv7l/requests.json) |
| `target_rust_armv7l` | 两锚点函数完整 | 库存搜索为[]；按文件位置补查REA `read_bytes`得到完整ASCII bytes，main引用DAT地址+长度20 | 两锚点算法清楚；Rust main 127行、有运行库/格式化与未知__rustcall；源码局部变量名未恢复 | 入口595/595；精确linkage拼写20/595=3.36%，其余同入口观察到反修饰名（不是575函数丢失）；库存768 | 原生操作可用；初次按main查询8次均歧义报错；按0x17798/0x17b18补查成功。字符串库存只覆盖已定义Data | [算法](evidence/target_rust_armv7l/secret_transform-pseudocode.c)、[校验](evidence/target_rust_armv7l/simple_checksum-pseudocode.c)、[空搜索](evidence/target_rust_armv7l/marker-search.decoded.json)、[明文bytes](evidence/target_rust_armv7l/supplemental/marker-bytes.decoded.json)、[main](evidence/target_rust_armv7l/supplemental/rust-main-pseudocode.c)、[初次错误](evidence/target_rust_armv7l/main-info.decoded.json)、[比例明细](evidence/target_rust_armv7l/symbol-recovery-metrics.json) |
| `target_py.pyc` | REA未恢复 | REA未恢复 | REA不支持该字节码格式，无伪代码/模块/导入可报告 | N/A（不能用0%暗示算法难逆向） | open_binary报unsupported binary format；overview报无active target；170工具列表无Python专用解码器 | [拒绝](evidence/target_py.pyc/open.decoded.json)、[后续报错](evidence/target_py.pyc/overview.decoded.json)、[能力列表](evidence/target_py.pyc/capability-names.json) |
| `target_js.js` | 两名称完整，语义图可见绑定/导出 | REA+Wakaru恢复文本完整 | 两算法源码级清楚；Wakaru重写为export default，运行等价未验证 | 原始命名函数2/2（仅样本函数，不数语义图全部节点） | 单文件application路由拒绝；同字节源码置最小目录后application/语义分析成功；recover最初缺Wakaru，装1.14.0后成功 | [application图](evidence/target_js.js/application.decoded.json)、[单文件拒绝](evidence/target_js.js/single-file-analysis.decoded.json)、[缺依赖](evidence/target_js.js/recovery.json)、[REA recovery](evidence/target_js.js/recovery-with-wakaru.json)、[恢复代码](evidence/target_js.js/recovered/modules/bundle.js) |
| `target_dotnet.dll` | 内置parser完整保留3个方法/签名 | 内置parser仅ldstr token；ILSpy实际C#/IL明文恢复后导入REA | 内置REA提供CIL常量/操作计数/分支锚点/调用边，非完整IL文本；补充ILSpy与REA import后算法为高可读C# | 内置方法名3/3；三个外部反编译方法按token/signature/IL digest成功导入3/3 | inspect_managed_artifact/members/native_boundaries成功；import_managed_reconstruction成功。C#由ILSpy生成，REA import输出confidence=inferred、executed=false，不声称内置REA反编译C# | [artifact](evidence/target_dotnet.dll/artifact.decoded.json)、[CIL与calls](evidence/target_dotnet.dll/members.decoded.json)、[ILSpy C#原输出](evidence/target_dotnet.dll/ilspy-decompiled.cs)、[完整IL](evidence/target_dotnet.dll/ilspy-full-il.txt)、[REA导入](evidence/target_dotnet.dll/supplemental/imported-reconstruction.decoded.json) |

## 已闭合结论

1. **本机REA+Ghidra可以实际反汇编/反编译armv7l兼容ELF**：三个ARM32样本核心函数均有真实ARM/Thumb指令与C样式伪代码，provider是Ghidra12.1.4；没有退回x86_64样本。证据：[GCC汇编](evidence/target_c_gcc_armv7l/secret_transform-assembly.asm)、[LLVM汇编](evidence/target_c_llvm_armv7l/secret_transform-assembly.asm)、[Rust汇编](evidence/target_rust_armv7l/secret_transform-assembly.asm)、[带profile的Rust原始响应](evidence/target_rust_armv7l/secret_transform-pseudocode.json)。
2. **裸样本三锚点易于取得，但方式不同**：C直接从符号/字符串/伪代码；Rust字符串需bytes补查；JS需Wakaru恢复文本；.NET完整C#/IL需ILSpy，REA内置元数据/CIL与导入证据分开保留。证据：上述六类恢复表各行具体文件。
3. **Codex+Ghidra配置已健康，全量doctor不是本任务范围健康判定**：专项healthy=true；全量exit1要求Hopper/IDA及其他agent，skill stale源于全量还检查缺失的Claude技能副本，Codex副本canonical=true。未安装这些无关provider以掩盖失败。证据：[专项](evidence/doctor-codex.json)、[全量原始](evidence/doctor.txt)、[全量最终](evidence/doctor-final.txt)、[范围诊断](evidence/rea-skill-scope-diagnosis.json)。
4. **JDK解包故障已修复**：conf中绝对软链指向宿主不存在的`/etc/java-21-openjdk`，按本地deb配置重定位后javac正常。证据：[首次版本/报错](evidence/installed-tool-versions.txt)、[根因](evidence/jdk-symlink-diagnosis.txt)、[修复](evidence/jdk-symlink-relocation.txt)、[复验](evidence/jdk-verification.txt)。
5. **ARM首次链接失败已闭合**：libc.so链接脚本指定`/usr/arm-linux-gnueabihf/...`，初次sysroot过深；改为解包根并为Clang明确include/lib后成功。证据：[链接脚本](evidence/arm-libc-linker-script.txt)、[GCC失败](evidence/target_c_gcc_armv7l-build.txt)、[GCC成功](evidence/target_c_gcc_armv7l-build-retry.txt)、[LLVM成功](evidence/target_c_llvm_armv7l-build-retry.txt)、[Rust成功](evidence/target_rust_armv7l-build-retry.txt)。
6. **所测六产物逻辑一致**：三ARM产物经QEMU、其余经对应runtime，默认/0/1/65535/4294967295共30次均exit0、stdout一致；.NET执行路径DLL hash与提交的target DLL相同。没有运行并证明反编译文本的全部输入等价。证据：[汇总](evidence/runtime-smoke-summary.json)、[hash](evidence/runtime-artifact-hashes.txt)、[Rust执行](evidence/target_rust_armv7l/runtime-smoke.json)、[NET执行](evidence/target_dotnet.dll/runtime-smoke.json)。
7. **实测恢复易读性强→弱**：含明确的可选provider/外部重建链时，**JS ≈ .NET > C LLVM > C GCC > Rust > Python pyc（工具不支持）**。按REA+Ghidra及内置parser、不含Wakaru/ILSpy文本补充时，C LLVM > C GCC > Rust；JS仅语义结构、.NET仅元数据/CIL锚点，二者与原生伪代码不作单一等价排名。该排序是本样本/本版本的审读判断，不是语言安全强度结论。证据：[JS恢复代码](evidence/target_js.js/recovered/modules/bundle.js)、[NET重建](evidence/target_dotnet.dll/supplemental/imported-reconstruction.decoded.json)、[LLVM main](evidence/target_c_llvm_armv7l/main-pseudocode.c)、[GCC main](evidence/target_c_gcc_armv7l/main-pseudocode.c)、[Rust main](evidence/target_rust_armv7l/supplemental/rust-main-pseudocode.c)、[Python拒绝](evidence/target_py.pyc/open.decoded.json)。

## 需人工裁决的前提

当前没有阻断本轮交付的人工执行项。沿用PM授权：本地安装、编译/执行自建样本，所有结果只用git push同步。既定口径是保留默认工具链安全属性与可识别锚点；未来若要比较去掉noinline/no_mangle、strip或开启保护后的基线，需另建实验批次，不能覆盖本轮证据。

## 挂账未决项与能力边界

- **Python3.12 pyc未被REA6.4.0支持**，需后续provider/工具支持才能闭合该类别REA逆向恢复；本轮已完成实际尝试，不假装成功。证据：[open错误](evidence/target_py.pyc/open.decoded.json)、[能力列表](evidence/target_py.pyc/capability-names.json)。
- **全量doctor仍exit1**，缺Hopper/IDA、其他agent/Claude技能副本；这是保留的范围外项。本任务Codex+Ghidra专项已通过，无需PM手动安装。证据：[最终doctor](evidence/doctor-final.txt)、[专项doctor](evidence/doctor-codex.json)、[skill范围](evidence/rea-skill-scope-diagnosis.json)。
- **Rust string inventory不是全字节搜索**，对本例返回空；bytes补查成功并不提升库存覆盖到100%。证据：[空结果](evidence/target_rust_armv7l/marker-search.decoded.json)、[bytes](evidence/target_rust_armv7l/supplemental/marker-bytes.decoded.json)。
- **伪代码ABI/类型误推断**未修改REA/Ghidra来隐藏，未知__rustcall、short/ushort、GCC main参数误判保留；未验证伪代码全输入语义等价。证据：[GCC main](evidence/target_c_gcc_armv7l/main-pseudocode.c)、[Rust main](evidence/target_rust_armv7l/supplemental/rust-main-pseudocode.c)。
- **.NET外部重建归属与JS重写等价性**：ILSpy输出含版本更新提示，原合并stdout/stderr照存；REA导入按方法范围提取实际文本。Wakaru将CommonJS导出改写为ESM，其文本易读性高但运行等价尚未验证。证据：[ILSpy原输出](evidence/target_dotnet.dll/ilspy-decompiled.cs)、[REA导入限制](evidence/target_dotnet.dll/supplemental/imported-reconstruction.decoded.json)、[JS实际重写](evidence/target_js.js/recovered/modules/bundle.js)。
- **全部数据符号恢复比例不适用当前工具库存**：REA无独立list_symbols，本轮给出严格函数符号比例，完整readelf/nm作外部对照；不宣称数据符号完整恢复。证据：[真实tools/list](evidence/rea-mcp/tools-list.json)、[Rust外部symbols](evidence/target_rust_armv7l-readelf.txt)、[函数比例](evidence/target_rust_armv7l/symbol-recovery-metrics.json)。
- 首次审计脚本用了旧MCP SDK包路径而报ERR_MODULE_NOT_FOUND，已改用真实依赖`@modelcontextprotocol/client 2.3.1`并成功；保留该已闭合过程错误。证据：[失败](evidence/rea-mcp-discovery.txt)、[成功](evidence/rea-mcp-discovery-retry.txt)。

## 复现与新session入口

新session先`git pull --ff-only`，读取本文件；`AGENTS.md`也记录了此约定。工具在本机`.local-tools/`，大依赖归档不纳入Git；安装脚本和实测deb版本清单用于审计与重装，已提交六个样本产物，pull后可直接核对证据。

```bash
source docs/probe/scripts/env.sh
npx --prefix .local-tools/rea --no-install rea-agents doctor --client codex --provider ghidra --json
# 已安装本机环境下，单次原生分析示例
npx --prefix .local-tools/rea --no-install rea-agents function "$PWD/docs/probe/samples/bin/target_c_gcc_armv7l" secret_transform --provider ghidra --json
```

安装：`install-runtime.sh`（Node固定24.21.0/Ghidra固定12.1.4，apt包版本见证据）、`relocate-jdk.py`、`install-rust-dotnet.sh`（固定Rust1.99.0/.NET SDK8.0.425）、`install-supplementary.sh`、`install-qemu.sh`。构建：`build-one.sh gcc|llvm|rust|python|js|dotnet`。分析：`analyze-one.mjs native|python|js|managed <样本文件名>`，有明确证据缺口时`followup <样本> <请求JSON>`。分析脚本会写结果，重跑需选择新证据目录或先备份，不应覆盖这批已提交原始记录。

原始MCP响应在`*.json`，解析出的REA完整Evidence在`*.decoded.json`，`.c/.asm`是从normalized_result直接提取的阅读版；CLI日志的`.meta.json`记录argv、exit_code、耗时。索引：[完整证据文件SHA-256清单](evidence/artifact-manifest.json)。Git提交历史保留每个子步骤的STATE更新与同步记录。

## 最终审计与同步

最终静态审计25项通过、0失败，检查了所有STATE证据链接、产物hash、三个ARM后端profile、样本会话关闭、JS恢复锚点、.NET推断导入、Rust明文字节及必须保留的失败记录。证据：[最终审计](evidence/final-audit.json)。执行等价性已有30次真实运行证据，不重复重跑无变更样本。所有子步骤以独立commit推送，最后本台账、AGENTS会话规则、固定版本补充安装脚本与证据清单一并推送；不使用文件上传或GitHub写入API。

## board-survey 进度与结论

本轮目标：只读调查 Tizen 开发板 `192.168.108.26` 上20~40份平台ELF的现有加固与平台机制。所有新审计文件只写 `docs/probe/board-survey/`；板上不安装、不编译、不执行选中二进制、不写入任何文件；不取回二进制/固件/源码，仅采集版本、ELF符号/头部、加固表等文本元数据。只用普通 git push 同步。

- 开场已执行 `git pull --ff-only`，已核对上一轮STATE：REA/Ghidra ARM基线完成，Python pyc不支持等限制保留。当前基点48710eb。证据：[会话开始](board-survey/session-start.txt)。
- [阻塞] 步骤1 SSH连接与板子身份；PM已提供用户名root，实际连接192.168.108.26:22超时（SSH exit255），未进入认证、未执行板上命令。证据：[原始SSH错误](board-survey/board-identity-ssh-timeout.txt)、[命令及退出状态](board-survey/board-identity-ssh-timeout.txt.meta.json)。
- [待执行] 步骤2 选择20~40个/usr/bin、/usr/lib样本并说明选择理由。
- [待执行] 步骤3 每样本只读readelf原输出与加固矩阵。
- [待执行] 步骤4 属性比例（共享库不误判为可执行PIE，未知项显式保留）。
- [待执行] 步骤5 共享库动态符号暴露。
- [待执行] 步骤6 SMACK、ASLR、只读根/verity痕迹。
- 人工前提：SSH用户名已闭合为root；需要PM处理板子到本机的SSH连接可达性后通知继续。“LLVM开源板”仍需实测身份/构建元数据或PM映射确认，不能单凭IP或内核clang字符串作结论。

board-survey 上一次连接前暂停（历史记录）：当时用户名提示已发出但尚未收到答复；未尝试用本机默认账号linhao或root猜测登录，尚无板上身份/加固数据，不将准备脚本记为实测结果。只读身份、readelf采集、文本判定与平台机制脚本已准备并通过语法检查。后续由执行器将脚本直接通过SSH stdin送入`sh -s`，原输出只落本机board-survey；共享库PIE为N/A，helper仅定义不算canary/FORTIFY已启用。需PM输入仅为SSH用户名；凭据走本机密码窗口。

### board-survey 当前挂账：SSH连接失败，按PM要求停止

- PM已提供SSH账号`root`，本次开场再次`git pull --ff-only`，仓库已是最新。
- 已执行一次SSH连接：`root@192.168.108.26`，端口22，ConnectTimeout=10、ConnectionAttempts=1；返回255。原始错误为`ssh: connect to host 192.168.108.26 port 22: Connection timed out`。证据：[board-identity.txt](board-survey/board-identity-ssh-timeout.txt)、[执行元数据](board-survey/board-identity-ssh-timeout.txt.meta.json)。
- 身份信息尚未取得；Tizen版本、CPU架构、是否LLVM开源板全部未知。密码窗口没有进入认证流程；没有把任何凭据写入脚本或仓库。
- 按任务原文“如果连不上或登录失败，原样记录错误、在STATE.md挂账、停下等我处理”，停止后续连接/采样/统计。步骤2~6均未执行，样本数为0；不生成假样本表或加固比例，不把网络超时解释成具体板子故障。
- 本次只新增本机SSH文本错误及执行元数据，均位于`docs/probe/board-survey/`；未执行板上命令，未取回二进制/固件/源码。后续等待PM处理连接并通知继续；再次尝试应保存新证据文件，不覆盖首次错误。

### board-survey 新授权与SDB阶段（取代上一轮SSH连接前提）

PM明确改用SDB连接192.168.108.26，授权仅对网络持久化配置进行写入；其余调查仍只读、不安装板上工具、不回传二进制/固件/源码、不重启。登录账号为root；凭据不写入仓库或脚本。所有新调查文件位于docs/probe/board-survey/。

- [完成] 新步骤1：本机已有Tizen Studio SDB 4.2.25，无需安装。证据：[sdb版本与路径](board-survey/sdb-version.txt)、[本机CLI帮助](board-survey/sdb-help.txt)。
- [待执行] 新步骤2：按192.168.108.26及必要时:26101连接并检查devices；失败即记录并停下。
- [待执行] 新步骤3：sdb root on与身份确认。前轮board-identity.txt保留为SSH失败历史，新身份另存归档后使用要求的固定路径。
- [待执行] 新步骤4~6：现状采集、识别管理器、备份、持久化当前IP/网关/DNS、只验证落盘语法；不重启。
- [待执行] 新步骤7~11：20~40个样本加固表、比例、动态符号、SMACK/ASLR/根挂载痕迹。

- [完成] 新步骤2：`sdb connect 192.168.108.26` 首次即成功，SDB实际使用默认端口26101；devices为`192.168.108.26:26101 device rpi4`。无需执行失败回退尝试，SSH超时历史不改写。证据：[连接原输出](board-survey/sdb-connect.txt)、[连接状态](board-survey/sdb-connect.txt.meta.json)、[明确目标](board-survey/sdb-target.json)。

- [完成] 新步骤3：sdb root on成功，id确认uid=0；板子为Raspberry Pi4 ModelB Rev1.5、Tizen11.0.0 Unified、armv7l，build_id=tizen-unified-toolchain_20261007.084717_tizen-headed-armv7l；内核6.12.80-arm-rpi4-v7l由clang22.1.8/LLD22.1.8构建。PM称其LLVM开源板；实测硬件/内核LLVM构建信息吻合，尚不能把内核编译器等同全部用户态编译器。证据：[SDB root](board-survey/sdb-root.txt)、[当前身份](board-survey/board-identity.txt)。旧SSH超时证据已归档board-identity-ssh-timeout.txt，未删除。
- 新挂账：板子PATH中checksec、readelf、llvm-readelf、nm、llvm-nm、file均不可用（command-v返回1）。后续只读检查既有等价工具/路径，不在板上安装工具、不取回二进制。证据：[身份中的工具查询](board-survey/board-identity.txt)。

- [完成] 新步骤4：采集到eth0=192.168.108.26/24，网关192.168.108.1；/etc/resolv.conf指向/opt/etc/resolv.conf，内容由ConnMan生成、nameserver=127.0.0.1（本地DNS代理，不能误设成上游DNS）。ConnMan active、systemd unit显示disabled，需进一步核对开机启动链与上游DNS。证据：[网络原现状](board-survey/net-before.txt)。
- 已保留缺失记录：systemd-networkd单位、NetworkManager/ifupdown目录及所有标准ELF工具均未找到。未安装板上工具；尚未得出加固比例。证据：[现状与工具查询](board-survey/net-before.txt)。

- 网络持久化写入前备份完成：原文件`/var/lib/connman/ethernet_2ccf67a072b5_cable/settings`已按原路径保存到board-survey/net-config-backup/；原权限0600，network_fw所有，当前手动IP/24、网关192.168.108.1、AutoConnect=true、上游DNS221.131.143.69。未在备份前改网络。证据：[原配置](board-survey/net-config-backup/var/lib/connman/ethernet_2ccf67a072b5_cable/settings)、[备份清单](board-survey/net-config-backup/manifest.json)、[采集及启动链](board-survey/net-backup-capture.txt)。
- 配置探查首次systemctl cat触发SDB终端pager，日志保留；后续显式禁用pager，全部只读查询已完成。证据：[首次](board-survey/net-manager-inspection.txt)、[无pager复查](board-survey/net-manager-inspection-no-pager.txt)。

- [完成] 新步骤5网络持久化：通过板上既有connmanctl重新明确配置manual IPv4=192.168.108.26、mask255.255.255.0、gateway192.168.108.1、typed nameservers ipv4.manual 221.131.143.69、autoconnect=yes。唯一配置文件为`/var/lib/connman/ethernet_2ccf67a072b5_cable/settings`，实际落在`/opt/var/lib/connman/.../settings`；原IP/DNS本来已存盘，文件除Modified外未改变。运行时DNS由unknown变为ipv4.manual+221.131.143.69；保留resolv.conf本地127.0.0.1代理。证据：[执行与读回](board-survey/net-persist.txt)、[新配置](board-survey/net-config-after/var/lib/connman/ethernet_2ccf67a072b5_cable/settings)、[差异与语法验证](board-survey/net-config-after/validation.json)。
- [完成] 新步骤6：本地INI语法/必需字段校验成功、板上API读回符合配置、权限0600/uid551/gid551保留、IP和route未变，vendor multi-user.target.wants已有connman.service启动链接。未重启、未重启服务、未新增enable链接，不声明已验证重启后联网。证据：[网络读回](board-survey/net-persist.txt)、[启动链接](board-survey/net-backup-capture.txt)、[校验](board-survey/net-config-after/validation.json)。
- D-Bus初次使用标准Properties.Get不被此ConnMan实现支持，错误完整保留；改用其真实GetProperties只读API，实际读回成功。证据：[Get错误](board-survey/net-backup-capture.txt)、[GetProperties](board-survey/net-dns-before.txt)。

- [独立复验完成] 新步骤6：另一次只读SDB查询再次检查六个磁盘配置字段、vendor启动链接、实时eth0/route/ConnMan服务，均满足预期并输出PERSISTENCE_VERIFY_SUCCESS_NO_REBOOT。没有重启验证，重启后的实际连通性继续由PM决定。证据：[独立复验](board-survey/net-verification.txt)。

- [完成] 新步骤7：按真实/usr/bin、/usr/lib库存选28份代表样本（12可执行、16共享库），覆盖服务/IPC/日志/安全/网络/包管理/数据库/基础库；只读readlink/stat确认均为文件且底层device+inode不重复。非随机普查，比例只适用于本批。证据：[样本理由清单](board-survey/sample-list.txt)、[解析路径及stat](board-survey/sample-resolution.txt)、[原目录库存](board-survey/platform-file-inventory.txt)。
- 采集方式明确挂账：readelf/nm/checksec/等价工具均不存在，不能生成这些工具的成功原输出。为继续只读摸底，使用已存在RPM4.14.1内嵌Lua5.1直接读取ELF头/动态表/符号元数据；代码通过sdb命令传入内存，不安装、不保存板上脚本、不读出指令或二进制本体。标准工具缺失继续作为限制；后续raw会明确区分失败的readelf命令与替代解码器输出。证据：[工具实际缺失](board-survey/net-before.txt)、[RPM/Lua能力](board-survey/net-manager-inspection-no-pager.txt)。

- 采集执行器遇到SDB内联命令长度限制：首次样本解析返回`error: service name too long`，真实失败保留。改为既有SDB stdin流式执行，禁用shell history，未在板上落脚本文件；样本路径/stat采集已成功。证据：[长度错误](board-survey/sample-resolution.txt)、[stdin验证](board-survey/sdb-stdin-test.txt)、[成功路径采集](board-survey/sample-resolution-streamed.txt)。

- [完成，替代方法明确] 新步骤8：27份真正ELF（11系统可执行、16共享库）均在板上由既有RPM/Lua只读解码成功，ELF32/EM_ARM=40；八项属性表及每样本raw已生成。原28候选中的vconftool不是ELF，已排除并保留错误，没有读取/回传其脚本正文。每份raw均真实保留readelf不存在的exit127及独立RPM/Lua元数据，**不是成功readelf输出**，标准工具板上复验挂账。证据：[矩阵](board-survey/hardening-matrix.txt)、[结构化表及限制](board-survey/hardening-matrix.json)、[被排除候选](board-survey/excluded-candidates.json)、[真实raw示例](board-survey/raw/systemctl.txt)、[非ELF错误](board-survey/raw/vconftool.txt)。
- 替代解码器验证：本机三ARM裸基线及ELF64 ls与真实readelf在RELRO/NX/PIE/strip/RPATH/RUNPATH/canary/FORTIFY/动态导出计数全部一致；板上Lua5.1实际运行成功。传输源码在板上内存中核对SHA256后才执行。证据：[独立对照](board-survey/validation/comparison.json)、[板上成功实测](board-survey/elf-reader-board-validation-direct.txt)、[整批采集](board-survey/hardening-capture.txt)。
- 执行器错误均保留：SDB长service名、交互tab/回显破坏、最初Lua shell heredoc旧解释器解析错误/超时。已改为分段、限速、hash校验、直接shell引用RPM Lua；不以这些失败作为属性结论。证据：[传输失败](board-survey/elf-reader-board-validation.txt)、[hash后shell解析错误](board-survey/elf-reader-board-validation-verified.txt)、[实际成功](board-survey/elf-reader-board-validation-direct.txt)。

- [完成] 新步骤9：27 ELF中可执行PIE=11/11(100%，16 DSO不适用)、Full RELRO=8/27(29.63%)、Partial=18/27、None=1/27（libdbus-1）；NX请求=27/27(100%)；无.symtab=27/27(100%)；FORTIFY导入helper证据=17/27(62.96%)，libc仅helper定义提供者1份不算正例，其余9份没有动态导入证据；canary导入helper21/27(77.78%)。RPATH0，RUNPATH8。这不是随机全平台比例，FORTIFY/canary不等于编译旗标或函数覆盖率。证据：[统计](board-survey/hardening-summary.txt)、[分母和分布](board-survey/hardening-summary.json)、[逐样本表](board-survey/hardening-matrix.json)。

- [完成，替代方法限制] 新步骤10：16份共享库动态导出数量及名称从板上真实SHT_DYNSYM元数据汇总，排除UND、只数定义GLOBAL/WEAK且DEFAULT/PROTECTED，并单列ABS版本标签。nm-D/readelf-dyn-syms真实尝试均exit127，原错保留。结论是动态接口暴露程度不统一、strip不消除动态名字；是否某个名字本应内部、源码visibility默认旗标不能由数量单独断定。证据：[符号数量/例名](board-survey/symbol-exposure.txt)、[精确计数及visibility](board-survey/symbol-exposure.json)、[标准工具错误](board-survey/symbol-tool-errors.txt)、[原始libdlog动态表](board-survey/raw/libdlog_so_0.txt)。

- [完成] 新步骤11平台痕迹：smackfs真实挂载/sys/fs/smackfs，目录含access/access2/load/load2/ambient等接口，只ls文件名未dump规则；内核randomize_va_space=2；根/dev/mmcblk0p2 ext4为ro，/opt ext4为rw，与ConnMan实际/opt持久存储相容。mount未见verity字样、sys/block未见dm目录，限于这些查询范围不推断所有验证启动缺失。/sys/kernel/security/lsm不存在的报错保留，SMACK结论依赖实际挂载与身份context。证据：[原始平台查询](board-survey/platform-mechanisms.txt)、[解析结论与范围](board-survey/platform-mechanisms-summary.json)。
