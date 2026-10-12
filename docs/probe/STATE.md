# REA 裸基线状态台账

日期：2026-10-12（Asia/Shanghai）；分支：poc/probe。

## 计划与进度
1. [完成] 初始化台账、获取官方文档、安装本地 Node/JDK/Ghidra/REA。
2. [完成（全量 doctor 异常已挂账）] 配置 Ghidra native provider，运行 doctor。
3. [完成] 编译 GCC/LLVM/Rust ARM32 ELF、Python pyc、JS、.NET DLL。
4. [待执行] 逐样本运行 REA，记录恢复质量、错误与能力边界。
5. [待执行] 汇总真实证据、复现脚本与强弱排序，完成 push。

## 已闭合结论（须附证据）
- 远端为空，本工作目录原先未初始化 Git；已初始化 poc/probe 并设 origin。证据：`evidence/bootstrap.txt`。
- 当前普通用户无法无密码 sudo；本轮采用工作目录 `.local-tools/` 安装，不需要人工执行命令。证据：`evidence/bootstrap.txt`。
- REA 官方文档当前声明支持 Node 22.19+/24.11+，Ghidra 12.1.x 与 JDK21+；实际版本稍后用安装输出确认。证据：`evidence/rea-official-installation.md`、`evidence/ghidra-release.json`。

- 已确认 JDK 报错根因：Ubuntu deb 的 conf 绝对软链仍指向宿主 `/etc/java-21-openjdk`；仅把本地 JDK conf 软链重定位到已解包配置，javac 复验成功。证据：`evidence/installed-tool-versions.txt`、`evidence/jdk-symlink-diagnosis.txt`、`evidence/jdk-symlink-relocation.txt`、`evidence/jdk-verification.txt`。
- Ghidra 范围 doctor 返回 0、available=true；REA MCP 真实 tools/list 已成功。证据：`evidence/doctor-ghidra.json`、`evidence/rea-mcp/tools-list.json`、`evidence/rea-mcp/server-version.json`。

## 需人工裁决的前提
- 暂无。样本均为本任务创建的无保护程序；仅用 git push 同步。
- 编译器默认安全属性（如 PIE/NX）属于裸工具链基线，不额外关闭；不 strip，不加入商业保护/混淆。

## 挂账未决项
- `npx rea-agents doctor` 全量检查返回 1：包括未安装 Hopper/IDA、未配置其他 agent，以及 setup 刚安装的 skill 仍被判 stale。保留原样，不声明全量 doctor 健康；Ghidra scoped 检查成功。证据：`evidence/doctor.txt` 及 meta、`evidence/doctor-ghidra.json`。
- 审计脚本首次误用旧 MCP SDK 路径，ERR_MODULE_NOT_FOUND；已改用 REA 包实际依赖 @modelcontextprotocol/client 2.3.1，复验成功。证据：`evidence/rea-mcp-discovery.txt`、`evidence/rea-mcp-discovery-retry.txt`。
- 尚未验证 Ghidra 对 ARM32 ELF 的实际反汇编/反编译效果。
- Python pyc 是否属于已发布 REA 版本支持范围待实测，不能以外部工具替代 REA 成功结论。

## 安装版本与路径
环境入口：`source docs/probe/scripts/env.sh`。版本证据：`evidence/node-rea-versions.txt`、`evidence/installed-tool-versions.txt`、`evidence/jdk-verification.txt`。
- Node 24.21.0 / npm 11.19.0：`.local-tools/node-v24.21.0-linux-x64/`。
- REA npm 6.4.0：`.local-tools/rea/node_modules/rea-agents/`；通过 npx --prefix .local-tools/rea --no-install rea-agents 调用。
- Ghidra 官方 12.1.4 PUBLIC：`.local-tools/ghidra_12.1.4_PUBLIC/`。
- OpenJDK 21.0.12.1（Ubuntu 完整 JDK）：`.local-tools/sysroot/usr/lib/jvm/java-21-openjdk-amd64/`。
- ARM GCC 13.3.0 / Clang 18.1.3：`.local-tools/sysroot/usr/bin/`；Rust 1.99.0 与 ARMv7 target：`.local-tools/cargo/`、`.local-tools/rustup/`；.NET SDK 8.0.425/runtime 8.0.31：`.local-tools/dotnet/`。
- `setup --client codex --yes` 已写入用户 REA MCP 注册与官方技能；计划/执行证据：`evidence/rea-setup-plan.json`、`evidence/rea-setup-applied.json`。未配置 Hopper/IDA。

## 样本恢复表
待实际分析后填入；符号恢复比例采用明确的分母，不以主观百分比代替测量。

## 子步骤提交日志

- C GCC/LLVM 两份 ARM32 ELF 已构建；不 strip、-O2，ARMv7 hard-float。证据：evidence/target_c_gcc_armv7l-file.txt、evidence/target_c_llvm_armv7l-file.txt 及各自 build-retry/readelf/nm/strings/checksec；初次 sysroot 链接错误保留在 build.txt，根因证据 evidence/arm-libc-linker-script.txt。

- Rust 1.99.0 armv7-unknown-linux-gnueabihf 构建成功，opt-level=2、strip=none；证据 evidence/target_rust_armv7l-file.txt、build-retry/readelf/nm/strings/checksec。Rust ABI 的校验函数用指针+长度，ASCII 样本算法与 C 一致。

- Python 3.12 pyc 已生成（Python 无 -O2 对应选项；optimize=0、无混淆）；证据 evidence/target_py-build.txt、evidence/target_py.pyc-file.txt。

- JS 原始源码已保存，并提供仅含该样本的目录 package.json 包装用于 REA application 工作流；证据 evidence/target_js-build.txt、evidence/target_js.js-file.txt；无转译/混淆。

- .NET Release Optimize=true（无原生 -O2 对应项）、保留元数据与 PDB，DLL 已生成；证据 evidence/target_dotnet-build.txt、evidence/target_dotnet.dll-file.txt。

- GCC ARM32 REA 完成，32 项 procedure 库存，两锚点函数及明文均可见，核心伪代码清晰；main 出现错误签名/参数推断。证据 evidence/target_c_gcc_armv7l/{requests.json,marker-search.decoded.json,secret_transform-pseudocode.c,simple_checksum-pseudocode.c,main-pseudocode.c,secret_transform-assembly.asm,symbol-recovery-metrics.json}。

- LLVM ARM32 REA 完成，32 项 procedure 库存，函数/明文/算法可见，main 调用清晰；返回/参数被缩窄为 short/ushort。证据 evidence/target_c_llvm_armv7l/{requests.json,marker-search.decoded.json,secret_transform-pseudocode.c,simple_checksum-pseudocode.c,main-pseudocode.c,secret_transform-assembly.asm,symbol-recovery-metrics.json}。

- Rust ARM32 REA 主分析完成，768 项 procedure 库存，两个锚点算法可反编译；字符串搜索为 []（仅 Ghidra 已定义 string data 库存），main 名称歧义导致8项聚焦调用报错，待地址选择补查。证据 evidence/target_rust_armv7l/{requests.json,marker-search.decoded.json,main-info.decoded.json,secret_transform-pseudocode.c,simple_checksum-pseudocode.c,symbol-recovery-metrics.json}。

- Python pyc REA 实测拒绝 unsupported binary format，后续 overview 因无 active target 报错；未用 Python dis 或外部反编译器充当 REA 成功。三锚点恢复均 N/A，不代表 pyc 有保护。证据 evidence/target_py.pyc/{open.decoded.json,overview.decoded.json,capability-names.json,requests.json}。

- JS application 目录分析成功；single .js 路由拒绝保留原错。REA recover_javascript_sources 缺 Wakaru 的原错保留，安装官方 Wakaru1.14.0、hash 与文档一致后成功恢复完整源码，两个函数/字符串/算法清晰。证据 evidence/target_js.js/{application.decoded.json,single-file-analysis.decoded.json,recovery.json,recovery-with-wakaru.json,recovered/}，evidence/wakaru-install.txt。

- .NET 内置 parser 完整读取3个方法及CIL统计/常量/ldstr token/调用边；不自动输出C#或ldstr全文。补装 ilspycmd9.1.0.7988，实际 C#/全IL 输出已存，再经 REA import_managed_reconstruction 按真实 token、signature_sha256、normalized_il_sha256 导入3方法为推断证据；三锚点在此补充路线可读。证据 evidence/target_dotnet.dll/{members.decoded.json,ilspy-decompiled.cs,ilspy-full-il.txt,supplemental/imported-reconstruction.decoded.json}，evidence/ilspy-install.txt。
