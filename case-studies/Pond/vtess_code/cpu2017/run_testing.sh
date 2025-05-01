TINTIN="/home/cspl/tobi/Tintin/tests/build/pond_model_events"
tintindatf="tintin_out.txt"
tintin_read_freq=10
workload_pid=1
sudo numactl --membind 1 $TINTIN $workload_pid $tintin_read_freq > $tintindatf &
# sarpid=$!
# disown $sarpid
# sudo numactl --membind 1 $TINTIN $workload_pid $tintin_read_freq