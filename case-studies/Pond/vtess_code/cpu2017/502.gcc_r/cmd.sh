#!/bin/bash
ulimit -s unlimited
export OMP_NUM_THREADS=1
export OMP_STACKSIZE=122880
taskset 1 ./cpugcc_r_base.lienz-perf-m64 gcc-pp.c -O3 -finline-limit=0 -fif-conversion -fif-conversion2 -o gcc-pp.opts-O3_-finline-limit_0_-fif-conversion_-fif-conversion2.s > gcc-pp.opts-O3_-finline-limit_0_-fif-conversion_-fif-conversion2.out 2>> gcc-pp.opts-O3_-finline-limit_0_-fif-conversion_-fif-conversion2.err &
workload_pid=$!
echo "$workload_pid" > /tmp/workload.pid
wait $workload_pid 2>/dev/null
