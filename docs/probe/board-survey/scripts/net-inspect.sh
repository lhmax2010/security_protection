#!/bin/sh
export LC_ALL=C SYSTEMD_PAGER=cat SYSTEMD_COLORS=0 TERM=dumb
run() { printf '\nCOMMAND:'; printf ' %s' "$@"; printf '\n'; "$@" 2>&1; rc=$?; printf '\nEXIT_CODE: %s\n' "$rc"; }
run connmanctl services ethernet_2ccf67a072b5_cable
run connmanctl help
run cat /var/lib/connman/ethernet_2ccf67a072b5_cable/settings
run ls -l /etc/connman
run systemctl cat connman
run systemctl show connman --property=WantedBy,RequiredBy,TriggeredBy,Before,After
run systemctl list-dependencies multi-user.target
run systemctl get-default
printf '\nEXISTING_STREAMED_METADATA_READER_PREREQUISITES\n'
run rpm --version
run rpm --eval '%{lua:print(_VERSION); print(type(string.unpack))}'
for p in od dd tr; do command -v "$p"; printf 'TOOL_LOOKUP_EXIT_CODE %s: %s\n' "$p" "$?"; done
