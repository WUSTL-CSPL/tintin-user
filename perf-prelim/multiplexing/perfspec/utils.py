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

    parser.add_argument('--rootpath', help='Specify desired root path for all experiments. Must be within user\'s home directory', type=str, required=True)
    parser.add_argument('--label', help="A label for this experiment to facilitate easier result processing", type=str, required=True)

    # perf specific arguments
    parser.add_argument('-p', '--perfversion', help='Version of perf to invoke. For embedded users.', type=str, default="perf")
    parser.add_argument('-e', '--eventsfile', help='Input file with desired events', type=str, required=True)
    parser.add_argument('-t', '--trials', help='Number of times to repeat perf invocation. Default is 10', type=int, default=10)
    parser.add_argument('--count', help='Number of events to count per perf invocation. Default is 1', type=int, default=1)
    parser.add_argument('--perfcore', help='perf profiles these cpus only', type=str, default=all_cores) 
    parser.add_argument('--simple', action='store_true', help='enable simplified event input file processing')

    # SPEC CPU2017 specific arguments
    parser.add_argument('-w', '--workloadsfile', help='Input file with desired workloads', type=str, required=True) 


    args = parser.parse_args()
    return args
