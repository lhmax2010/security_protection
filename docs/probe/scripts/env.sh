#!/usr/bin/env bash
PROBE_ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)
export PROBE_ROOT
export JAVA_HOME="$PROBE_ROOT/.local-tools/sysroot/usr/lib/jvm/java-21-openjdk-amd64"
export GHIDRA_INSTALL_DIR="$PROBE_ROOT/.local-tools/ghidra_12.1.4_PUBLIC"
export REA_ANALYSIS_PROVIDER=ghidra
export RUSTUP_HOME="$PROBE_ROOT/.local-tools/rustup"
export CARGO_HOME="$PROBE_ROOT/.local-tools/cargo"
export DOTNET_ROOT="$PROBE_ROOT/.local-tools/dotnet"
export DOTNET_CLI_TELEMETRY_OPTOUT=1
export DOTNET_NOLOGO=1
export LD_LIBRARY_PATH="$PROBE_ROOT/.local-tools/sysroot/usr/lib/x86_64-linux-gnu${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
export PATH="$PROBE_ROOT/.local-tools/node-v24.21.0-linux-x64/bin:$JAVA_HOME/bin:$PROBE_ROOT/.local-tools/sysroot/usr/bin:$CARGO_HOME/bin:$DOTNET_ROOT:$PATH"
export REA_WAKARU_COMMAND="$PROBE_ROOT/.local-tools/wakaru"
