#!/bin/sh
# Runs on the board over SSH. No file writes, target execution or installation.
export LC_ALL=C
run() {
 printf '\nCOMMAND:'
 printf ' %s' "$@"
 printf '\n'
 "$@" 2>&1
 result=$?
 printf 'EXIT_CODE: %s\n' "$result"
}
run id
run uname -a
run uname -m
run cat /etc/tizen-release
run cat /etc/os-release
run cat /proc/version
for p in /proc/device-tree/model /proc/device-tree/compatible; do
 if [ -r "$p" ]; then
  printf '\nCOMMAND: tr NUL to newline < %s\n' "$p"
  tr '\000' '\n' < "$p"
  printf '\nEXIT_CODE: %s\n' "$?"
 else
  printf '\nIDENTITY_FIELD_UNAVAILABLE: %s\n' "$p"
 fi
done
printf '\nEXISTING_TOOL_PATHS\n'
for tool in checksec readelf llvm-readelf nm llvm-nm file find awk sed sort head readlink mount stat rpm; do
 command -v "$tool" 2>&1
 printf 'TOOL_LOOKUP_EXIT_CODE %s: %s\n' "$tool" "$?"
done
printf '\nCOMPILER_IDENTIFIER_SCOPE: /proc/version is kernel build provenance only; not proof of userspace compiler or LLVM open-board model.\n'
