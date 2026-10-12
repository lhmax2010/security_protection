#!/bin/sh
# The board is read-only. Output is streamed; no files are created on the board.
export LC_ALL=C
reader=
for tool in readelf llvm-readelf; do
 if command -v "$tool" >/dev/null 2>&1; then reader=$tool; break; fi
done
if [ -z "$reader" ]; then
 printf 'REQUIRED_TOOL_UNAVAILABLE: neither readelf nor llvm-readelf is installed\n'
 exit 127
fi
emit() {
 tag=$1; shift
 printf '\n@@BEGIN_COMMAND %s\nCOMMAND:' "$tag"
 printf ' %s' "$@"
 printf '\n'
 "$@" 2>&1
 rc=$?
 printf '\n@@END_COMMAND %s EXIT_CODE=%s\n' "$tag" "$rc"
}
# Sample loop is appended only after board inventory has been read and reviewed.
