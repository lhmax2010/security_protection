#!/bin/sh
set -u
cd "$1" || exit 9
prefix=""
if command -v taskset >/dev/null 2>&1; then prefix="taskset -c 2"; fi
printf 'phase\tround\tvariant\tstart_epoch\tend_epoch\texit\n' > timings.tsv
: > perf-context.txt
run_one() {
    phase=$1; round=$2; variant=$3
    log="perf-$phase-$round-$variant.txt"
    {
        printf '%s %s %s\n' "$phase" "$round" "$variant"
        cat /proc/loadavg
        cat /sys/class/thermal/thermal_zone0/temp
        cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq
    } >> perf-context.txt 2>&1
    start=$(date +%s.%N)
    $prefix ./ffmpeg-$variant -hide_banner -nostdin -nostats -loglevel info -benchmark \
      -threads 1 -filter_threads 1 -filter_complex_threads 1 -i workload.m2v \
      -map 0:v:0 -an -sn -dn -threads 1 -f null - > "$log" 2>&1
    code=$?
    end=$(date +%s.%N)
    printf '%s\t%s\t%s\t%s\t%s\t%s\n' "$phase" "$round" "$variant" "$start" "$end" "$code" >> timings.tsv
    printf 'RUN_FINISHED %s %s %s %s\n' "$phase" "$round" "$variant" "$code"
}
for variant in baseline selective full; do run_one warmup 0 "$variant"; done
round=1
while [ "$round" -le 6 ]; do
    case "$round" in
      1|4) order="baseline selective full" ;;
      2|5) order="selective full baseline" ;;
      3|6) order="full baseline selective" ;;
    esac
    for variant in $order; do run_one measured "$round" "$variant"; done
    round=$((round+1))
done
printf 'BOARD_PERF_MEASUREMENT_FINISHED\n'
