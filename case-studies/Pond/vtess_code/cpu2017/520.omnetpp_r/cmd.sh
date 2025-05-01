#!/bin/bash
ulimit -s unlimited
export OMP_NUM_THREADS=1
export OMP_STACKSIZE=122880
taskset 1 ./omnetpp_r_base.lienz-perf-m64 -c General -r 0 > omnetpp.General-0.out 2>> omnetpp.General-0.err &
workload_pid=$!
echo "$workload_pid" > /tmp/workload.pid
wait $workload_pid 2>/dev/null
