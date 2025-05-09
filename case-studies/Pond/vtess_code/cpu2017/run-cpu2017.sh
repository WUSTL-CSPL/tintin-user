#!/bin/bash
#
# Run CXL-memory experiments for SPEC CPU 2017 workloads
#
# Huaicheng Li <lhcwhu@gmail.com>
#

# Change the following global variables based on your environment
#-------------------------------------------------------------------------------
EMON="/opt/intel/oneapi/vtune/2023.2.0/bin64/" # Emon path
TINTIN="/home/cspl/ao_ws/Tintin/tests/build/pond_model_events_uncertainty_weights"
RUNDIR="/home/cspl/pond/vtess_code" # top dir of this repo

# Output folder
#RSTDIR="rst/emon-$(date +%F-%H%M)-$(uname -n | awk -F. '{printf("%s.%s\n", $1, $2)}')"
MEMEATER="$RUNDIR/memeater"
CPU2017_RUN_DIR="${RUNDIR}/cpu2017"
RSTDIR="${CPU2017_RUN_DIR}/rst/"

RUN_EMON=1 # whether to run emon together
RUN_TINTIN=0
#-------------------------------------------------------------------------------


# Reserve newlines during command substitution
#IFS=

#
# Usage:
# ./run-cpu2017.sh w.txt --> run all the workloads in w.txt
# ./run-cpu2017.sh w.txt 1 --> run the 1st workload in w.txt
#
if [[ $# != 1 && $# != 2 ]]; then
    echo ""
    echo "Run all workloads: $0 w.txt"
    echo "Run one workload:  $0 w.txt 2 --> run the 2nd workload in w.txt"
    echo ""
    exit
fi

WF=$1
WID=$2

if [[ $# == 1 ]]; then
    warr=($(cat $WF | awk '{print $1}'))
    marr=($(cat $WF | awk '{print $2}'))
elif [[ $# == 2 ]]; then
    warr=($(cat w.txt | awk -vline=$WID 'NR == line {print $1}'))
    marr=($(cat w.txt | awk -vline=$WID 'NR == line {print $2}'))
fi

echo "==> Result directory: $RSTDIR"


# Suppose the host server has 2 nodes, [Node 1: 8c/32g + Node 2: 8c/32g]
# (1).
# Emulated CXL-memory cases
# (N1:8c/32g + N2:0c/32g)
# "100" -> 100% local memory configuration
# "50"  -> 50% local memory
# "0"   -> 0% local memory
#
# (2).
# NUMA baseline cases
# (N1:8c/32g + N2:8c/32g)
# "Interleave" -> round robin memory allocation across NUMA nodes


# Global emualtion environment setup
source $RUNDIR/cxl-global.sh || exit

[[ $RUN_EMON == 0 || ($RUN_EMON == 1 && -e $EMON) ]] || echo "==> Error: RUN_EMON=$RUN_EMON, Emon: $EMON"
[[ $RUN_TINTIN == 0 || ($RUN_TINTIN == 1 && -e $TINTIN) ]] || echo "==> Error: RUN_TINTIN=$RUN_TINTIN, TINTIN: $TINTIN"


TIME_FORMAT="\n\n\nReal: %e %E\nUser: %U\nSys: %S\nCmdline: %C\nAvg-total-Mem-kb: %K\nMax-RSS-kb: %M\nSys-pgsize-kb: %Z\nNr-voluntary-context-switches: %w\nCmd-exit-status: %x"

if [[ ! -e /usr/bin/time ]]; then
    echo "Please install GNU time first!"
    exit
fi

# Must be called under the corresponding workload folder (e.g. 519.lbm_r/)
# $1: workload
# $2: exp type (L100, L50, L0, "CXL-Interleave")
# $3: exp ID
# $4: workload wss, required for running more splits (L95 -- L75)
# Require taking all CPUs on Node 1 offline
run_one_exp()
{
    local w=$1
    local et=$2
    local id=$3
    local mem=$4
    #local run_cmd="$(cat cmd.sh | grep -v "^#")"
    local run_cmd="bash cmd.sh" # the command line string
    local MEM_SHOULD_RESERVE=0
    flush_fs_caches

    echo "    => Running [$w - $et - $id], date:$(date) ..."

    if [[ $et == "L100" ]]; then
        run_cmd="numactl --cpunodebind 0 --membind 0 -- ""${run_cmd}"
    elif [[ $et == "L0" ]]; then
        run_cmd="numactl --cpunodebind 0 --membind 1 -- ""${run_cmd}"
    elif [[ $et == "CXL-Interleave" ]]; then
        run_cmd="numactl --cpunodebind 0 --interleave=all -- ""${run_cmd}"
    elif [[ $et == "Base-Interleave" ]]; then
        # The difference with L50 is that all CPUs on Node 1 are online
        # --cpunodebind 0: this param was errorneously added, need to fix for
        # those multi-threaded workloads!!!! (re-run workloads >600)
        run_cmd="numactl --interleave=all -- ""${run_cmd}"
    else
        # Other base splits (e.g. 90 means 90% of the workload memory will be
        # backed by local DRAM while the remaining 10% will be from CXL memory)
        run_cmd="numactl --cpunodebind 0 -- ${run_cmd}"
        #NODE0_TT_MEM=$(sudo numactl --hardware | grep 'node 0 size' | awk '{print $4}')
        NODE0_FREE_MEM=$(sudo numactl --hardware | grep 'node 0 free' | awk '{print $4}')
        ((NODE0_FREE_MEM -= 520))
        APP_MEM_ON_NODE0=$(echo "$mem*$et/100.0" | bc)
        MEM_SHOULD_RESERVE=$((NODE0_FREE_MEM - APP_MEM_ON_NODE0))
        MEM_SHOULD_RESERVE=${MEM_SHOULD_RESERVE%.*}
    fi

    echo "${run_cmd}"
    cat cmd.sh

    local output_dir="$RSTDIR/$w/CXL"
    [[ ! -d ${output_dir} ]] && mkdir -p ${output_dir}

    local logf=${output_dir}/${et}-${id}.log
    local timef=${output_dir}/${et}-${id}.time
    local output=${output_dir}/${et}-${id}.output
    local memf=${output_dir}/${et}-${id}.mem
    local pidstatf=${output_dir}/${et}-${id}.pidstat
    local sysinfof=${output_dir}/${et}-${id}.sysinfo
    local emondatf=${output_dir}/${et}-${id}-emon.dat
    local tintindatf=${output_dir}/${et}-${id}-tintin.dat
    local sarf=${output_dir}/${et}-${id}.sar


    {
        echo "===> MemEater reserving [$MEM_SHOULD_RESERVE] MB on Node 0..."
        if [[ $MEM_SHOULD_RESERVE -gt 0 ]]; then
            sudo killall memeater >/dev/null 2>&1
            sleep 10
            # Make sure that MemEater is reserving memory from Node 0
            numactl --cpunodebind 0 --membind 0 -- $MEMEATER ${MEM_SHOULD_RESERVE} &
            mapid=$!
            # Wait until memory eater consume all destined memory
            sleep 120
        fi

        echo "$run_cmd" | tee r.sh
        echo "Start: $(date)"
        get_sysinfo > $sysinfof 2>&1
        workload_pid_file="/tmp/workload.pid"
        sudo rm -f $workload_pid_file
        /usr/bin/time -f "${TIME_FORMAT}" --append -o ${timef} bash r.sh > $output 2>&1 &
        cpid=$!
        
        while [ ! -f "$workload_pid_file" ]; do
            echo "Waiting for the file to exist: $workload_pid_file"
        done
        
        workload_pid=$(cat $workload_pid_file)
        echo "Obtained workload pid $workload_pid"
        #pidstat -r -u -d -l -v -p ALL -U -h 5 1000000 > $pidstatf &
        #pstatpid=$!

        if [[ "${RUN_EMON}" == 1 ]]; then
            # sudo numactl --membind 1 $EMON -i $RUNDIR/cspl_events.txt -f "$emondatf" >/dev/null 2>&1 &            sar -o ${sarf} -bBdHqSwW -I SUM -n DEV -r ALL -u ALL 1 >/dev/null 2>&1 &
            sudo numactl --membind 1 $EMON -i $RUNDIR/clx-2s-events.txt -f "$emondatf" >/dev/null 2>&1 &            sar -o ${sarf} -bBdHqSwW -I SUM -n DEV -r ALL -u ALL 1 >/dev/null 2>&1 &
            sarpid=$!
            disown $sarpid       
        fi

        if [[ "${RUN_TINTIN}" == 1 ]]; then
            tintin_read_freq_ms=100
            sudo numactl --membind 1 $TINTIN $workload_pid $tintin_read_freq_ms > $tintindatf &
        fi

        #sar -o ${sarf} -bBdHqSwW -I SUM -n DEV -r ALL -u ALL 1 >/dev/null 2>&1 &
        #sarpid=$!
        monitor_resource_util >>$memf 2>&1 &
        mpid=$!

        #disown $pstatpid
        #disown $sarpid
        disown $mpid # avoid the "killed" message
        wait $cpid 2>/dev/null
        if [[ "${RUN_EMON}" == 1 ]]; then
            echo "Stopping emon"
            sudo $EMON -stop
        fi

        if [[ "${RUN_TINTIN}" == 1 ]]; then
            echo "Stopping Tintin"
            sudo killall -SIGUSR1 $TINTIN
            sudo rm -f $workload_pid_file
        fi

        #kill -9 $sarpid
        kill -9 $mpid >/dev/null 2>&1
        #kill -9 $pstatpid >/dev/null 2>&1
        if [[ $MEM_SHOULD_RESERVE -gt 0 ]]; then
            disown $mapid
            kill -9 $mapid >/dev/null 2>&1
        fi
        echo "End: $(date)"
        echo "" && echo "" && echo "" && echo ""
        cat r.sh
        echo ""
        cat cmd.sh
        rm -rf r.sh
        cat "Finished!"
        sleep 10
    } >> $logf
}

# run "L100" "CXL-Interleave" "L0" in one shot
# $1: "workload"
# $2: id
# $3: Memory (MB)
run_one_workload_cxl()
{
    local w=$1
    local id=$2
    local mem=$3

    run_one_exp "$w" "L100" $id $mem
    run_one_exp "$w" "L0" $id
    # More Splits
    # run_one_exp "$w" "95" $id $mem
    # run_one_exp "$w" "90" $id $mem
    # run_one_exp "$w" "85" $id $mem
    # run_one_exp "$w" "80" $id $mem
    # run_one_exp "$w" "75" $id $mem
    # run_one_exp "$w" "70" $id $mem
    # run_one_exp "$w" "60" $id $mem
    # run_one_exp "$w" "50" $id $mem
    # run_one_exp "$w" "40" $id $mem
    # run_one_exp "$w" "30" $id $mem
    # run_one_exp "$w" "25" $id $mem
    # run_one_exp "$w" "CXL-Interleave" $id
}

# run baseline experiments (e.g. "Base-Interleave"), we put this into a seperate
# function as it does not require any hacks to take cores offline
# $1: "workload"
# $2: id
run_one_workload_base()
{
    local w=$1
    local id=$2

    #run_one_exp "$w" "Base-Interleave" $id
}

# Run all 43 SPEC CPU workloads on one server one by one Params:
# $1 -> the experiment type to run.
#
# "L100", "L50", "L0" -> represent the CXL-based exp
# "B50" -> Baseline interleave mode, "L100" <=> "B100"
run_seq_cxl()
{
    check_cxl_conf

    for id in 1; do # 5 runs for each experiment
        for ((i = 0; i < ${#warr[@]}; i++)); do
            w=${warr[$i]}
            m=${marr[$i]}
            cd "$w"
            run_one_workload_cxl "$w" "$id" "$m"
            cd ../
        done
    done
}

run_seq_base()
{
    check_base_conf

    for id in 1 2 3 4 5; do
        for ((i = 0; i < ${#warr[@]}; i++)); do
            w=${warr[$i]}
            cd "$w"
            run_one_workload_base "$w" "$id"
            cd ../
        done
    done
}

#-------------------------------------------------------------------------------
# MAIN
#-------------------------------------------------------------------------------

main()
{
    run_seq_cxl
    run_seq_base
}

main

echo "Congrats! All done!"
exit
