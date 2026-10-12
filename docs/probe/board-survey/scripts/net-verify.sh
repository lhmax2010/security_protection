#!/bin/sh
set -eu
export LC_ALL=C SYSTEMD_PAGER=cat SYSTEMD_COLORS=0 TERM=dumb
settings=/var/lib/connman/ethernet_2ccf67a072b5_cable/settings
printf 'READONLY_PERSISTENCE_VERIFICATION\n'
cat "$settings"
for line in 'AutoConnect=true' 'IPv4.method=manual' 'IPv4.netmask_prefixlen=24' 'IPv4.local_address=192.168.108.26' 'IPv4.gateway=192.168.108.1' 'Nameservers=221.131.143.69;'; do grep -qx "$line" "$settings"; printf 'CONFIG_FIELD_VERIFIED: %s\n' "$line"; done
readlink /usr/lib/systemd/system/multi-user.target.wants/connman.service
ip addr show eth0
ip route
connmanctl services ethernet_2ccf67a072b5_cable
printf 'PERSISTENCE_VERIFY_SUCCESS_NO_REBOOT\n'
