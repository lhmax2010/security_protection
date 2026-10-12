#!/usr/bin/env bash
set -euxo pipefail
cd "$(dirname "$0")/../../.."
export RUSTUP_HOME="$PWD/.local-tools/rustup"
export CARGO_HOME="$PWD/.local-tools/cargo"
curl -fL --retry 2 https://sh.rustup.rs -o .local-tools/rustup-init.sh
bash .local-tools/rustup-init.sh -y --no-modify-path --profile minimal --default-toolchain 1.99.0
.local-tools/cargo/bin/rustup target add armv7-unknown-linux-gnueabihf
curl -fL --retry 2 https://dot.net/v1/dotnet-install.sh -o .local-tools/dotnet-install.sh
bash .local-tools/dotnet-install.sh --version 8.0.425 --install-dir "$PWD/.local-tools/dotnet"
