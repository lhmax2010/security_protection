#!/usr/bin/env bash
set -euo pipefail
demo="$(pwd)/docs/probe/ffmpeg-demo"
mkdir -p "$demo/private/download"
export TMPDIR="$demo/local-runtime/tmp"
curl -fL --retry 2 https://ffmpeg.org/releases/ffmpeg-8.0.1.tar.xz -o "$demo/private/download/ffmpeg-8.0.1.tar.xz"
sha256sum "$demo/private/download/ffmpeg-8.0.1.tar.xz"
tar -xJf "$demo/private/download/ffmpeg-8.0.1.tar.xz" -C "$demo/private"
