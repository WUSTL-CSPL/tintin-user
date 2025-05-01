#!/bin/bash
ulimit -s unlimited
export OMP_NUM_THREADS=1
export OMP_STACKSIZE=122880
taskset 1 ./namd_r_base.lienz-perf-m64 --input apoa1.input --output apoa1.ref.output --iterations 65 > namd.out 2>> namd.err &
workload_pid=$!
echo "$workload_pid" > /tmp/workload.pid
wait $workload_pid 2>/dev/null
