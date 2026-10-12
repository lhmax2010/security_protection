#!/bin/sh
export LC_ALL=C
run() {
 printf '\nCOMMAND:'; printf ' %s' "$@"; printf '\n'
 "$@" 2>&1; result=$?
 printf '\nEXIT_CODE: %s\n' "$result"
}
run cat /proc/sys/kernel/randomize_va_space
run ls -ld /sys/fs/smackfs
if [ -d /sys/fs/smackfs ]; then run ls -la /sys/fs/smackfs; fi
run cat /sys/kernel/security/lsm
printf '\nMOUNTS: full mount listing (metadata only; no dmsetup table or filesystem contents)\n'
run mount
printf '\nROOT_AND_VERITY_MOUNT_METADATA\n'
run awk '$2=="/" || $0 ~ /verity/ {print}' /proc/mounts
printf '\nDM_NAME_AND_UUID_METADATA_ONLY\n'
found=no
for dir in /sys/block/dm-*/dm; do
 [ -d "$dir" ] || continue
 found=yes
 run cat "$dir/name"
 run cat "$dir/uuid"
done
printf '\nDM_DEVICE_DIRECTORY_OBSERVED: %s\n' "$found"
printf '\nSMACK_POLICY_CONTENTS_NOT_READ\n'
