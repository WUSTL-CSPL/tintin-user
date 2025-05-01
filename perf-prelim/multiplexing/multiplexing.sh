#!/bin/bash

: ' README

This script runs perfspec.py and graphs the data. There is the option to dynamically modify the event input file so the event of interest is first.

Example Invocation
~/AccPerf/perf-prelim/multiplexing/multiplexing.sh 1 multiplexing-study cache-misses ~/AccPerf/perf-prelim/sixteen.txt 30 

HACK: The number of multiplexed events is fixed at 1-4, 8, 16 events.

'

# Process arguments
if [ $# -lt 5 ]; then # NOTE: Must update this conditional check if number of arguments change. $# does not count program name $0 in its value
  echo "Usage: $0 <core> <folder with experiments> <event of interest> <event input file> <number of trials>" # NOTE: Keep in mind order of arguments if they change.
  exit 1
fi

# Assign arguments to variables
# NOTE: Must update if arguments change.
CORE="$1"
ROOTPATH="$2" # desired location in home directory
EVENT="$3"
INPUTFILE="$4"
TRIALS="$5"

REPO="AccPerf" # put the repo name in a variable in case the repo name changes

# Modify event input file so event of interest is on the first line
python3 ~/"${REPO}"/perf-prelim/targetevent.py "${INPUTFILE}" "${EVENT}"

# Run perfspec.py to generate data
taskset -c "${CORE}" python3 ~/"${REPO}"/perf-prelim/multiplexing/perfspec/perfspec.py --simple -e "${INPUTFILE}" -w ~/"${REPO}"/perf-prelim/one-workload.txt --rootpath "${ROOTPATH}" --perfcore "${CORE}" -t "${TRIALS}" --label 1_events --count 1 
taskset -c "${CORE}" python3 ~/"${REPO}"/perf-prelim/multiplexing/perfspec/perfspec.py --simple -e "${INPUTFILE}" -w ~/"${REPO}"/perf-prelim/one-workload.txt --rootpath "${ROOTPATH}" --perfcore "${CORE}" -t "${TRIALS}" --label 2_events --count 2 
taskset -c "${CORE}" python3 ~/"${REPO}"/perf-prelim/multiplexing/perfspec/perfspec.py --simple -e "${INPUTFILE}" -w ~/"${REPO}"/perf-prelim/one-workload.txt --rootpath "${ROOTPATH}" --perfcore "${CORE}" -t "${TRIALS}" --label 3_events --count 3 
taskset -c "${CORE}" python3 ~/"${REPO}"/perf-prelim/multiplexing/perfspec/perfspec.py --simple -e "${INPUTFILE}" -w ~/"${REPO}"/perf-prelim/one-workload.txt --rootpath "${ROOTPATH}" --perfcore "${CORE}" -t "${TRIALS}" --label 4_events --count 4 
taskset -c "${CORE}" python3 ~/"${REPO}"/perf-prelim/multiplexing/perfspec/perfspec.py --simple -e "${INPUTFILE}" -w ~/"${REPO}"/perf-prelim/one-workload.txt --rootpath "${ROOTPATH}" --perfcore "${CORE}" -t "${TRIALS}" --label 8_events --count 8
taskset -c "${CORE}" python3 ~/"${REPO}"/perf-prelim/multiplexing/perfspec/perfspec.py --simple -e "${INPUTFILE}" -w ~/"${REPO}"/perf-prelim/one-workload.txt --rootpath "${ROOTPATH}" --perfcore "${CORE}" -t "${TRIALS}" --label 16_events --count 16

# Graph the data
python3 ~/"${REPO}"/perf-prelim/multiplexing/mplx-grapher.py --experimentroot "${ROOTPATH}" --event "${EVENT}" --xlabel "Number of Multiplexed Events"