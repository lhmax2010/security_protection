#!/bin/sh
export LC_ALL=C SYSTEMD_PAGER=cat SYSTEMD_COLORS=0 TERM=dumb
run() { printf '\nCOMMAND:'; printf ' %s' "$@"; printf '\n'; "$@" 2>&1; rc=$?; printf '\nEXIT_CODE: %s\n' "$rc"; }
printf '@@BEGIN_CONFIG /var/lib/connman/ethernet_2ccf67a072b5_cable/settings\n'
cat /var/lib/connman/ethernet_2ccf67a072b5_cable/settings
rc=$?
printf '\n@@END_CONFIG EXIT_CODE=%s\n' "$rc"
[ "$rc" -eq 0 ] || exit "$rc"
run stat -c '%a %u %g %n' /var/lib/connman/ethernet_2ccf67a072b5_cable/settings
run readlink -f /var/lib/connman/ethernet_2ccf67a072b5_cable/settings
run systemctl cat net-config
run systemctl show net-config --property=ActiveState,UnitFileState,FragmentPath,WantedBy,RequiredBy
run ls -l /etc/systemd/system/multi-user.target.wants/connman.service /usr/lib/systemd/system/multi-user.target.wants/connman.service
run busctl get-property net.connman /net/connman/service/ethernet_2ccf67a072b5_cable net.connman.Service Nameservers
run busctl get-property net.connman /net/connman/service/ethernet_2ccf67a072b5_cable net.connman.Service Nameservers.Configuration
