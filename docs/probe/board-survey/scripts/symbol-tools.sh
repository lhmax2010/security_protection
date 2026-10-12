#!/bin/sh
export LC_ALL=C
for path in /usr/lib/libdlog.so.0 /usr/lib/libcynara-client.so.0 /usr/lib/libsecurity-manager-client.so.3; do
 printf '\nCOMMAND: nm -D %s\n' "$path"
 nm -D "$path" 2>&1
 printf 'EXIT_CODE: %s\n' "$?"
 printf 'COMMAND: readelf --dyn-syms %s\n' "$path"
 readelf --dyn-syms "$path" 2>&1
 printf 'EXIT_CODE: %s\n' "$?"
done
