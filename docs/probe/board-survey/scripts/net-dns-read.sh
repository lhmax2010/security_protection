#!/bin/sh
export LC_ALL=C SYSTEMD_PAGER=cat SYSTEMD_COLORS=0 TERM=dumb
printf 'COMMAND: busctl call net.connman /net/connman/service/ethernet_2ccf67a072b5_cable net.connman.Service GetProperties\n'
busctl call net.connman /net/connman/service/ethernet_2ccf67a072b5_cable net.connman.Service GetProperties
printf '\nEXIT_CODE: %s\n' "$?"
