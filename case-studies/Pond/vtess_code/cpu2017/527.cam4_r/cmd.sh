#!/bin/bash
ulimit -s unlimited
export OMP_NUM_THREADS=1
export OMP_STACKSIZE=122880
taskset 1 ./cam4_r_base.lienz-perf-m64 > cam4_r_base.mytest-m64.txt 2>> cam4_r_base.mytest-m64.err &
workload_pid=$!
echo "$workload_pid" > /tmp/workload.pid
wait $workload_pid 2>/dev/null
