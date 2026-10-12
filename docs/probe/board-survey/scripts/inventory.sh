#!/bin/sh
export LC_ALL=C
printf 'COMMAND: find /usr/bin -maxdepth 1 -type f -o -type l (selected filename metadata)\n'
find /usr/bin -maxdepth 1 \( -type f -o -type l \) -printf '%f\n' | sort
printf '\nLIBRARY_FILENAME_METADATA\n'
find /usr/lib -maxdepth 2 \( -type f -o -type l \) -name '*.so*' -printf '%p\n' | sort
