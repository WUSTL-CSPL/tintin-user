# perfstress.py
# Lien Zhu
# Development Started December 27, 2022
# Last Updated February 14, 2023
# Driver module for perfstress.py program

import os, sys
import subprocess
import numpy as np
import re           # for parsing data
import shutil       # rm -rf functionality
import csv
import datetime
import argparse
import itertools    # event combinations
import random

from utils import *
from inputprocessor import *
from pathcreator import *
from statcalc import *
from grapher import *


# Preps the command to invoke perf on stress-ng
# Expected txt file name format: "event_index_--workload_trial.txt"
# Returns path to the <output_file>.txt
#
def run_perf(policy, priority, event_string, event_index, interval, workload, perf_version, perf_core_affinity, stress_ng_version, stress_core_affinity, num_of_stress_cpus):
    workload_name = workload.split()[0].strip() # parses "--workload ops" into "--workload"
    data_file = str(event_index) + "_" + workload_name + ".txt" # create output file name
    
    chrt_cmd_str = "sudo chrt --" + policy + " " + priority 
    
    perf_cmd_str = perf_version + " stat -o " + data_file + " -e " + event_string  + " -x," + " -I " + interval + " -C " + perf_core_affinity

    workload_arg_str = stress_ng_version + " -q" + " --taskset " + stress_core_affinity + " --cpu " + num_of_stress_cpus + " " + workload 

    full_cmd = chrt_cmd_str + " " + perf_cmd_str + " " + workload_arg_str

    os.system(full_cmd) # run command, creating output text file for trial
    return data_file 


### Run Experiment ###
def run_trial(trial, scheduler, priority, processed_events_arr, all_workloads, trial_path, perf_version, perf_core_affinity, stress_ng_version, stress_core_affinity, num_of_stress_cpus, interval):

    print()
    print("Starting trial", trial)

    os.chdir(trial_path) # sanity check in case the program moved out of experiment_path

    # results_arr is a complex array that contains all results for a SINGLE TRIAL
    # see notes.txt for structure details
    results_arr = [] 

    for event_index, event_string in enumerate(processed_events_arr):

        event_path = mkdir_cd_event_path(trial_path, event_index) # get event_path and cd into event_path

        event_string_data_arr = [] # list of all data points for current event_string

        for workload in all_workloads:
            _ = mkdir_cd_event_workload_path(event_path, event_index, workload) # cd into event_--workload path to store the stat.txt file

            data_file = run_perf(scheduler, priority, event_string, event_index, interval, workload, perf_version, perf_core_affinity, stress_ng_version, stress_core_affinity, num_of_stress_cpus)
            data_point_arr = parse_counts_from_file(data_file)
            event_string_data_arr.append(data_point_arr)

        results_arr.append(event_string_data_arr) # data for this event_string is added to overall results

        os.chdir(trial_path)

    print()
    print("Trial", str(trial), "Finished")
    print()

    return results_arr



def main():
    args = parse_args()

    # run experiment
    all_events, all_workloads = process_input(args.eventsfile, args.workloadsfile)

    if args.count > len(all_events):
        sys.exit(f"User Error: not enough events in events input file for the desired concurrent event count")
    
    if int(args.interval) < 10:
        sys.exit(f"Interval length must be greater than 1 ms")

    processed_events_arr = process_events_arr(all_events, args.count) # generates combinations of events

    experiment_path = mkdir_cd_experiment_path(args.count, args.trials, args.eventsfile, args.workloadsfile, args.interval)
    results_path = mkdir_results_path(experiment_path)

    # file for convenience in decoding events to numeric label
    touch_key_file(experiment_path, processed_events_arr)
    print()
    print("Starting Experiment...")

    for trial in range(args.trials):
        trial_path = mkdir_cd_trial_path(experiment_path, trial)
        results_arr = run_trial(trial, args.scheduler, args.priority, processed_events_arr, all_workloads, trial_path, args.perfversion, args.perfcore, args.stressversion, args.stresscore, args.stresscpu, args.interval)
        write_to_csv(results_path, trial, args.count, results_arr, processed_events_arr, all_workloads) 

    print()
    print("Experiment Finished")
    print(args.trials, "trials were conducted")
    print(args.count, "events were counted concurrently each perf invocation")
    print()
    print("Find results files at", results_path)
    print()



if __name__ == "__main__":
    main()
