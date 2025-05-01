#!/bin/bash
ulimit -s unlimited
export OMP_NUM_THREADS=1
export OMP_STACKSIZE=122880
taskset 1 ./roms_r_base.lienz-perf-m64 < ocean_benchmark2.in.x > ocean_benchmark2.log 2>> ocean_benchmark2.err &
workload_pid=$!
echo "$workload_pid" > /tmp/workload.pid
wait $workload_pid 2>/dev/null
