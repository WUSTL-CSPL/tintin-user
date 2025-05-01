#!/bin/bash

cd ~/cpu2017
source shrc

# Clear the run folders
rm -Rf $SPEC/benchspec/C*/*/run 

read target_pid <<< $(ps -ef | awk '$8=="runcpu 502 --noreportable --iterations 1 --deletework --tune base --action onlyrun" {print $2}')

echo $target_pid

while [ 1 ]
do
    taskset -p -c 0 $target_pid
    sleep 0.1
    taskset -p -c 1 $target_pid
    sleep 0.1
    taskset -p -c 2 $target_pid
    sleep 0.1
    taskset -p -c 3 $target_pid
    sleep 0.1
done
