# utils.py
# Lien Zhu
# Miscellaneous files for perfstress.py

import os, sys
import argparse


# Makes a file that lists the indices for each event_string for user reference
#
def touch_key_file(experiment_path, events):
    os.chdir(experiment_path)
    key_file = open("key_file.txt", 'w')
    for event_string_index, event_string in enumerate(events):
        key_file.write(str(event_string_index) + "\t" + event_string + "\n")
    key_file.close()


# Get string of all cores
# 
def get_cores():
    nproc_file = "nproc.txt"
    cmd_str = "nproc > " + nproc_file
    os.system(cmd_str)
    with open(nproc_file) as f:
        num_of_cores = int(f.readline())
    cores_range = "0-" + str(num_of_cores-1)
    os.remove(nproc_file)
    return cores_range


def check_args(count, all_events):
    if count > len(all_events):
        sys.exit(f"User Error: not enough events in events input file")


def parse_args():
    parser = argparse.ArgumentParser()
    all_cores = get_cores()

    parser.add_argument('--scheduler', help='Scheduling policy to use. Default: "other". Options: "rr", "fifo", "deadline", "other"', type=str, default="other")
    parser.add_argument('--priority', help='Scheduling priority for this experiment. Default: 0. Note: Each policy supports different range of priorities', type=str, default="0")

    # perf specific arguments
    parser.add_argument('-p', '--perfversion', help='Version of perf to invoke. For embedded users.', type=str, default="perf")
    parser.add_argument('-e', '--eventsfile', help='Input file with desired events', type=str, required=True)
    parser.add_argument('-t', '--trials', help='Number of times to repeat perf invocation. Default is 10', type=int, default=10)
    parser.add_argument('--count', help='Number of events to count per perf invocation. Default is 1', type=int, default=1)
    parser.add_argument('--perfcore', help='perf will only count on these cpus', type=str, default=all_cores) 

    # stress-ng specific arguments
    parser.add_argument('--stresscore', help='Pin stress-ng workload on this list of comma separated list or hyphen denoted range of cores', type=str, default = all_cores)
    parser.add_argument('--stresscpu', help='Number of stress-ng cpu stressors. Default is "1"', type=str, default="1")
    parser.add_argument('--stressversion', help='Version of stress-ng to use. For embedded users.', type=str, default="stress-ng")
    parser.add_argument('-w', '--workloadsfile', help='Input file with desired workloads', type=str, required=True) # with Intel benchmark, might need to handle required arguments differently


    args = parser.parse_args()
    return args
