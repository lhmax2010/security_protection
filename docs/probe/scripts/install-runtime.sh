#!/usr/bin/env bash
set -euxo pipefail
cd "$(dirname "$0")/../../.."
cd .local-tools
curl -fL --retry 2 https://nodejs.org/dist/latest-v24.x/node-v24.21.0-linux-x64.tar.xz -o node.tar.xz
grep 'node-v24.21.0-linux-x64.tar.xz$' node-sha.txt | sed 's/node-v24.21.0-linux-x64.tar.xz/node.tar.xz/' | sha256sum -c -
tar -xf node.tar.xz
curl -fL --retry 2 https://github.com/NationalSecurityAgency/ghidra/releases/download/Ghidra_12.1.4_build/ghidra_12.1.4_PUBLIC_20260921.zip -o ghidra.zip
unzip -q ghidra.zip
mkdir -p debs sysroot
cd debs
apt-get download openjdk-21-jdk-headless openjdk-21-jre-headless gcc-13-arm-linux-gnueabihf cpp-13-arm-linux-gnueabihf gcc-13-arm-linux-gnueabihf-base binutils-arm-linux-gnueabihf libgcc-13-dev-armhf-cross libgcc-s1-armhf-cross libc6-armhf-cross libc6-dev-armhf-cross linux-libc-dev-armhf-cross libstdc++6-armhf-cross libgomp1-armhf-cross libatomic1-armhf-cross libasan8-armhf-cross libubsan1-armhf-cross libisl23 libmpc3 clang-18 libclang-cpp18 libllvm18 libclang1-18 libclang-common-18-dev llvm-18-linker-tools libobjc-13-dev libobjc4 checksec
for p in *.deb; do dpkg-deb -x "$p" ../sysroot; done
