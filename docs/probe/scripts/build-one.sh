#!/usr/bin/env bash
set -euxo pipefail
source "$(dirname "$0")/env.sh"
cd "$PROBE_ROOT"
S=docs/probe/samples
T="$PROBE_ROOT/.local-tools/sysroot/usr"
mkdir -p "$S/bin"
case "$1" in
 gcc)
  arm-linux-gnueabihf-gcc-13 --sysroot="$T/.." -O2 -march=armv7-a -mfpu=vfpv3-d16 "$S/target.c" -o "$S/bin/target_c_gcc_armv7l" ;;
 llvm)
  clang-18 --target=arm-linux-gnueabihf --sysroot="$T/.." --gcc-toolchain="$T" -isystem "$T/arm-linux-gnueabihf/include" -L"$T/arm-linux-gnueabihf/lib" -O2 -march=armv7-a -mfpu=vfpv3-d16 "$S/target.c" -o "$S/bin/target_c_llvm_armv7l" ;;
 rust)
  rustc --edition=2024 --target armv7-unknown-linux-gnueabihf -C opt-level=2 -C strip=none -C linker=arm-linux-gnueabihf-gcc-13 -C link-arg=--sysroot="$T/.." "$S/target.rs" -o "$S/bin/target_rust_armv7l" ;;
 python)
  python3 -c 'import py_compile; py_compile.compile("docs/probe/samples/target_py.py",cfile="docs/probe/samples/bin/target_py.pyc",doraise=True,optimize=0)' ;;
 js)
  cp "$S/target_js.js" "$S/bin/target_js.js"
  mkdir -p "$S/bin/target_js_app"
  cp "$S/target_js.js" "$S/bin/target_js_app/target_js.js"
  printf '%s\n' '{"name":"bare-baseline","version":"1.0.0","main":"target_js.js"}' > "$S/bin/target_js_app/package.json" ;;
 dotnet)
  dotnet build "$S/dotnet/target_dotnet.csproj" -c Release -o "$S/bin/dotnet-out"
  cp "$S/bin/dotnet-out/target_dotnet.dll" "$S/bin/target_dotnet.dll" ;;
 *) exit 2 ;;
esac
