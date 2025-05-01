#!/bin/bash


REPO="AccPerf"

# Add runcpu to PATH
cd ~/cpu2017/
source shrc

# Clear the run folders
rm -Rf $SPEC/benchspec/C*/*/run 
cd ~/"${REPO}"/perf-prelim/granularity/


# Process arguments
if [ $# -lt 5 ]; then # NOTE: Must update this conditional check if number of arguments change. $# does not count program name $0 in its value
  echo "Usage: $0 <core> <folder with experiments> <event of interest> <benchmark> <number of trials>" # NOTE: Keep in mind order of arguments if they change.
  exit 1
fi

# Assign arguments to variables 
# NOTE: Must update if arguments change
CORE=$1
ROOTPATH=$2
EVENT=$3
BENCH=$4
TRIALS=$5

if [ -d "${ROOTPATH}/system-wide/" ]; then
    rm -rf "${ROOTPATH}"/system-wide/
    mkdir "${ROOTPATH}"/system-wide/
fi

for i in {1..${TRIALS}}
do
    sudo perf stat -e "${EVENT}" -C "${CORE}" -x, -o "${ROOTPATH}"/system-wide/$i &
    runcpu "${BENCH}" --noreportable --iterations 1 --deletework --tune base --action onlyrun
    sudo pkill --signal SIGINT perf
done

