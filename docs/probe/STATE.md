# REA 裸基线状态台账

日期：2026-10-12（Asia/Shanghai）；分支：poc/probe。

## 计划与进度
1. [进行中] 初始化台账、获取官方文档、安装本地 Node/JDK/Ghidra/REA。
2. [待执行] 配置 Ghidra native provider，运行 doctor。
3. [待执行] 编译 GCC/LLVM/Rust ARM32 ELF、Python pyc、JS、.NET DLL。
4. [待执行] 逐样本运行 REA，记录恢复质量、错误与能力边界。
5. [待执行] 汇总真实证据、复现脚本与强弱排序，完成 push。

## 已闭合结论（须附证据）
- 远端为空，本工作目录原先未初始化 Git；已初始化 poc/probe 并设 origin。证据：`evidence/bootstrap.txt`。
- 当前普通用户无法无密码 sudo；本轮采用工作目录 `.local-tools/` 安装，不需要人工执行命令。证据：`evidence/bootstrap.txt`。
- REA 官方文档当前声明支持 Node 22.19+/24.11+，Ghidra 12.1.x 与 JDK21+；实际版本稍后用安装输出确认。证据：`evidence/rea-official-installation.md`、`evidence/ghidra-release.json`。

## 需人工裁决的前提
- 暂无。样本均为本任务创建的无保护程序；仅用 git push 同步。
- 编译器默认安全属性（如 PIE/NX）属于裸工具链基线，不额外关闭；不 strip，不加入商业保护/混淆。

## 挂账未决项
- 尚未验证 Ghidra 对 ARM32 ELF 的实际反汇编/反编译效果。
- Python pyc 是否属于已发布 REA 版本支持范围待实测，不能以外部工具替代 REA 成功结论。

## 安装版本与路径
待安装后填入。环境入口将为 `docs/probe/scripts/env.sh`。

## 样本恢复表
待实际分析后填入；符号恢复比例采用明确的分母，不以主观百分比代替测量。
