#!/bin/bash

: ' README

This script runs and times 18 instrumented SPEC benchmarks using the Linux date command.

Example Invocation
./spectimer.sh 1 evaluation 10

NOTE: 
- The benchmarks are hard coded

'


REPO="AccPerf"


# Add runcpu to PATH
cd ~/cpu2017/
source shrc

# Clear the run folders
rm -Rf $SPEC/benchspec/C*/*/run 

# Process arguments
if [ $# -lt 3 ]; then # NOTE: Must update this conditional check if number of arguments change. $# does not count program name $0 in its value
  echo "Usage: $0 <core> <experiment root in home folder> <number of trials>" # NOTE: Keep in mind order of arguments if they change.
  exit 1
fi

BENCHMARKS=(
    "500" "502" "505" "520" "523" "525" "531" "541" "557" 
    "507" "508" "510" "511" "519" "521" "526" "538" "544"
)

for item in "${BENCHMARKS[@]}"
do
  echo "$item"
done
