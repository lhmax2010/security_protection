#!/bin/sh
set -eu
export LC_ALL=C SYSTEMD_PAGER=cat SYSTEMD_COLORS=0 TERM=dumb
printf 'FINAL_READONLY_READBACK\n'
id
uname -m
ip addr show eth0
ip route
cat /var/lib/connman/ethernet_2ccf67a072b5_cable/settings
connmanctl services ethernet_2ccf67a072b5_cable
readlink /usr/lib/systemd/system/multi-user.target.wants/connman.service
printf 'FINAL_READBACK_SUCCESS_NO_REBOOT\n'
