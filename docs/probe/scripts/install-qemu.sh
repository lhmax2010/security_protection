#!/usr/bin/env bash
set -euxo pipefail
cd "$(dirname "$0")/../../../.local-tools/debs"
apt-get download qemu-user libcapstone4 liburing2
for p in qemu-user_*.deb libcapstone4_*.deb liburing2_*.deb; do dpkg-deb -x "$p" ../sysroot; done
