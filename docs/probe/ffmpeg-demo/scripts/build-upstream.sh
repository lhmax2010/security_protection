#!/usr/bin/env bash
set -euo pipefail
workspace=$(pwd)
source "$workspace/docs/probe/scripts/env.sh"
demo="$workspace/docs/probe/ffmpeg-demo"
export HOME="$demo/local-runtime" TMPDIR="$demo/local-runtime/tmp"
export XDG_CACHE_HOME="$demo/local-runtime/cache"
source_dir="$demo/private/ffmpeg-8.0.1"
build_dir="$demo/private/build-no-hardening"
mkdir -p "$build_dir" "$demo/upstream-artifacts"
cd "$build_dir"
set -x
"$source_dir/configure" \
 --prefix="$demo/private/install" \
 --arch=arm --cpu=cortex-a7 --target-os=linux --enable-cross-compile \
 --cross-prefix=arm-linux-gnueabihf- --cc=arm-linux-gnueabihf-gcc-13 \
 --sysroot="$workspace/.local-tools/sysroot" \
 --extra-cflags='-mfpu=neon -fno-stack-protector -U_FORTIFY_SOURCE -D_FORTIFY_SOURCE=0' --optflags=-O2 \
 --extra-ldflags='-Wl,-z,norelro -Wl,-z,lazy' \
 --enable-shared --disable-static --disable-stripping --disable-debug \
 --disable-autodetect --disable-programs --disable-doc --disable-network \
 --disable-avdevice --disable-avformat --disable-avfilter --disable-swscale --disable-swresample \
 --disable-everything --enable-decoder=pcm_s16le
make -j4 V=1
cp libavcodec/libavcodec.so.62 "$demo/upstream-artifacts/libavcodec-unstripped.so"
cp libavcodec/libavcodec.so.62 "$demo/upstream-artifacts/libavcodec-stripped.so"
arm-linux-gnueabihf-strip --strip-unneeded "$demo/upstream-artifacts/libavcodec-stripped.so"
cp libavutil/libavutil.so.60 "$demo/upstream-artifacts/libavutil-unstripped.so"
cp "$source_dir/COPYING.LGPLv2.1" "$demo/upstream-artifacts/COPYING.LGPLv2.1"
sha256sum "$demo/upstream-artifacts/"*.so
file "$demo/upstream-artifacts/"*.so
