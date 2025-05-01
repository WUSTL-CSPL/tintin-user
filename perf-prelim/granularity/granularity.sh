#!/bin/bash

: ' README

This script conducts the granularity study on system vs task vs instrumented vs core-migrating perf_event subsystem usage.
System and Task experiments use the perf user space tool.

Example Invocation
./granularity.sh 1 granularity-study LLC-load-misses 10 ~/multiplexing-study/1_events 502

NOTE: 
- Make sure SPEC cpu2017 502.gcc_r has the original copy of src/toplev.c for system-wide

'


REPO="AccPerf"


# Add runcpu to PATH
cd ~/cpu2017/
source shrc

# Clear the run folders
rm -Rf $SPEC/benchspec/C*/*/run 
cd ~/${REPO}/perf-prelim/granularity/


# Process arguments
if [ $# -lt 6 ]; then # NOTE: Must update this conditional check if number of arguments change. $# does not count program name $0 in its value
  echo "Usage: $0 <core> <folder with experiments> <event of interest> <number of trials> <path to multiplexing study one event data> <SPEC benchmark>" # NOTE: Keep in mind order of arguments if they change.
  exit 1
fi

# Assign arguments to variables
# NOTE: Must update if arguments change.
CORE="$1"
ROOTPATH="$2" # desired location in home directory
EVENT="$3"
TRIALS="$4"
MULTIPLEXING_ONE_EVENT_DATA_PATH="$5"
BENCHMARK="$6"


# Remove old $ROOTPATH
if [ -d "${ROOTPATH}" ]; then
  rm -rf "${ROOTPATH}"
fi
# Create the directory
mkdir "${ROOTPATH}"


# Run system wide experiment first
./systemperf.sh "${CORE}" "${ROOTPATH}" "${EVENT}" "${TRIALS}"

# Write data from perf stat files into csv file that resembles the results.csv file from multiplexing study
# TODO: Decide on best approach for this
# python3 ~/"${REPO}"/perf-prelim/statwriter.py --sourcepath ~/"${ROOTPATH}"/system-wide --sourcetype stat


# Get one event data from multiplexing study and use it for task wide data
# HACK: requires user to have desirable data from the multiplexing study first
cp -r ~/"${MULTIPLEXING_ONE_EVENT_DATA_PATH}" ~/"${ROOTPATH}"/task-wide


# Run Instrumented SPEC
# NOTE: Must ensure the correct instrumented benchmark source file is in the correct folder
./onespec.sh "${ROOTPATH}"
# if --sourcetype == spec then we need more arguments to be specified like the benchmark



