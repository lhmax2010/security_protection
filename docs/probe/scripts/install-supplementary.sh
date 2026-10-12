#!/usr/bin/env bash
set -euxo pipefail
source "$(dirname "$0")/env.sh"
cd "$PROBE_ROOT"
curl -fL --retry 2 https://github.com/pionxzh/wakaru/releases/download/v1.14.0/wakaru-linux-x64.tar.gz -o .local-tools/wakaru.tar.gz
tar -xzf .local-tools/wakaru.tar.gz -C .local-tools wakaru
printf '%s\n' '664fa06782a61eda7ed15885134b52525fd565dd77607e642062ceb6cd927c38  .local-tools/wakaru' | sha256sum -c -
dotnet tool install ilspycmd --version 9.1.0.7988 --tool-path "$PROBE_ROOT/.local-tools/dotnet-tools"
