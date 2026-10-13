#!/bin/sh
set -u
cd "$1" || exit 9
{ uname -a; cat /proc/loadavg; cat /proc/meminfo | head -n 8; cat /sys/class/thermal/thermal_zone0/temp; cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor; date +%s.%N; } > conditions-before.txt 2>&1
: > hash-status.tsv
for variant in baseline selective full; do
    ./ffmpeg-$variant -version > version-$variant.txt 2>&1
    version_exit=$?
    ./ffmpeg-$variant -hide_banner -y -nostdin -nostats -loglevel error -threads 1 -filter_threads 1 -filter_complex_threads 1 \
      -i workload.m2v -map 0:v:0 -an -sn -dn -threads 1 -c:v rawvideo -f framemd5 hash-$variant.txt 2> hash-$variant-stderr.txt
    code=$?
    printf '%s\t%s\t%s\n' "$variant" "$version_exit" "$code" >> hash-status.tsv
done
printf 'BOARD_CONTENT_CHECK_FINISHED\n'
