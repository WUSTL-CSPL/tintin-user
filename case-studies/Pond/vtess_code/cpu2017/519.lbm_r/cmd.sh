#!/bin/bash
ulimit -s unlimited
export OMP_NUM_THREADS=1
export OMP_STACKSIZE=122880
taskset 1 ./lbm_r_base.lienz-perf-m64 3000 reference.dat 0 0 100_100_130_ldc.of > lbm.out 2>> lbm.err &
workload_pid=$!
echo "$workload_pid" > /tmp/workload.pid
wait $workload_pid 2>/dev/null
