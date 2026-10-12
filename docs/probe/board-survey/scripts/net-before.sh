#!/bin/sh
export LC_ALL=C
run() { printf '\nCOMMAND:'; printf ' %s' "$@"; printf '\n'; "$@" 2>&1; rc=$?; printf '\nEXIT_CODE: %s\n' "$rc"; }
run ip addr
run ip route
run ls -l /etc/resolv.conf
run cat /etc/resolv.conf
run systemctl is-active connman systemd-networkd NetworkManager networking
run systemctl is-enabled connman systemd-networkd NetworkManager networking
for unit in connman systemd-networkd NetworkManager networking; do run systemctl show "$unit" --property=ActiveState,UnitFileState,FragmentPath; done
run connmanctl services
run ls -ld /var/lib/connman /etc/connman /etc/systemd/network /run/systemd/network /etc/NetworkManager /etc/network
printf '\nCONNMAN_ETHERNET_CONFIG_PATHS_ONLY\n'
for path in /var/lib/connman/ethernet_*/settings; do [ -f "$path" ] && run ls -l "$path"; done
printf '\nEXTRA_EXISTING_ELF_TOOL_LOOKUPS\n'
for tool in eu-readelf eu-nm objdump llvm-objdump llvm-readobj python3 python perl; do command -v "$tool" 2>&1; printf 'TOOL_LOOKUP_EXIT_CODE %s: %s\n' "$tool" "$?"; done
printf '\nEXISTING_ELF_TOOLS_OUTSIDE_PATH\n'
run find /usr /opt -type f \( -name readelf -o -name llvm-readelf -o -name eu-readelf -o -name checksec -o -name nm -o -name llvm-nm -o -name llvm-readobj \)
