#!/bin/bash
ulimit -s unlimited
export OMP_NUM_THREADS=1
export OMP_STACKSIZE=122880
taskset 1 ./xz_r_base.lienz-perf-m64 cld.tar.xz 160 19cf30ae51eddcbefda78dd06014b4b96281456e078ca7c13e1c0c9e6aaea8dff3efb4ad6b0456697718cede6bd5454852652806a657bb56e07d61128434b474 59796407 61004416 6 > cld.tar-160-6.out 2>> cld.tar-160-6.err  &
workload_pid=$!
echo "$workload_pid" > /tmp/workload.pid
wait $workload_pid 2>/dev/null
