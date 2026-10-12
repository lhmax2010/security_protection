#!/bin/sh
# Sole authorized board write operation: existing Ethernet network settings.
# Original settings are already backed up locally and committed before execution.
set -eu
export LC_ALL=C SYSTEMD_PAGER=cat SYSTEMD_COLORS=0 TERM=dumb
service=ethernet_2ccf67a072b5_cable
settings=/var/lib/connman/$service/settings
[ "$(id -u)" = 0 ]
grep -qx 'IPv4.local_address=192.168.108.26' "$settings"
grep -qx 'IPv4.gateway=192.168.108.1' "$settings"
grep -qx 'Nameservers=221.131.143.69;' "$settings"
printf 'COMMAND: connmanctl config %s --ipv4 manual 192.168.108.26 255.255.255.0 192.168.108.1 --nameservers ipv4.manual 221.131.143.69 --autoconnect yes\n' "$service"
connmanctl config "$service" --ipv4 manual 192.168.108.26 255.255.255.0 192.168.108.1 --nameservers ipv4.manual 221.131.143.69 --autoconnect yes
printf '\nEXIT_CODE: 0\n'
printf '\n@@BEGIN_CONFIG %s\n' "$settings"
cat "$settings"
printf '\n@@END_CONFIG EXIT_CODE=0\n'
printf '\nCOMMAND: connmanctl services %s\n' "$service"
connmanctl services "$service"
printf '\nCOMMAND: busctl call GetProperties\n'
busctl call net.connman /net/connman/service/$service net.connman.Service GetProperties
printf '\nCOMMAND: ip addr show eth0\n'
ip addr show eth0
printf '\nCOMMAND: ip route\n'
ip route
printf '\nCOMMAND: cat /etc/resolv.conf\n'
cat /etc/resolv.conf
printf '\nCOMMAND: stat settings mode owner\n'
stat -c '%a %u %g %n' "$settings"
printf '\nNO_REBOOT_NO_SERVICE_RESTART_NO_BOARD_TOOL_INSTALL\n'
