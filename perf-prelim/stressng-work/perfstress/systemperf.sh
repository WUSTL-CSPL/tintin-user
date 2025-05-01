#!/usr/bin/bash

if [ $1 == 0 ] ;
then
    rm -rf ~/results
    mkdir ~/results
    mkdir ~/results/system-wide
    mkdir ~/results/task-wide
fi

sudo perf_5.10 stat -e LLC-load-misses -x, -o ~/results/system-wide/$1 &
stress-ng --cpu 1 --quiet --cache-ops 300
sudo pkill --signal SIGINT perf