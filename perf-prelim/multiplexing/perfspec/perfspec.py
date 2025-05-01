# perfstress.py
# Lien Zhu
# Development Started December 27, 2022
# Last Updated March 6, 2023
# Driver module for perfstress.py 


import os

from utils import *
from inputprocessor import *
from pathcreator import *
from statcalc import *
import subprocess

from ExperimentResults import *
from EventStringData import *
from EventStringWorkloadData import *
from DataPoint import *


# Preps the command to invoke perf on SPEC CPU2017
# Expected txt file name format: "event_index_--workload_trial.txt"
# Returns path to the <output_file>.txt
#
def run_perf(experiment_obj, event_string_workload_obj, event_string_index):
    # set up PATH env var to contain runcpu binary
    path_restore = os.getcwd()
    os.chdir(os.path.join(os.path.expanduser('~'), 'cpu2017'))
    subprocess.run("bash -c 'source shrc'", shell=True)
    cpu2017_bin = os.path.join(os.path.expanduser('~'), 'cpu2017/bin')
    env = os.environ.copy()
    if 'PATH' in env:
        env['PATH'] = f"{cpu2017_bin}:{env['PATH']}"  # use ':' as path separator on Unix/Linux
    else:
        env['PATH'] = cpu2017_bin
    os.chdir(path_restore)

    workload_name = event_string_workload_obj.workload
    datafile = str(event_string_index) + "_" + workload_name + ".txt" # create output file name
    
    perf_cmd_str = experiment_obj.perfversion + " stat -o " + datafile + " -e " + event_string_workload_obj.eventstring + " -x ," + " -C " + experiment_obj.perfcore
    workload_arg_str = os.path.join(os.path.expanduser('~'), "cpu2017/bin/runcpu") + " " + workload_name + " --noreportable --iterations 1 --deletework --tune base --action onlyrun"

    full_cmd = perf_cmd_str + " " + workload_arg_str

    # os.system(full_cmd) # run command, creating output text file for trial
    subprocess.run(full_cmd, env=env, shell=True)
    return datafile 


def run_trial(experiment_obj, trial_path):
    os.chdir(trial_path) # sanity check in case the program moved out of experiment_path

    for event_string_index, event_string_obj in enumerate(experiment_obj.EventStringData_arr):
        event_string_path = mkdir_cd_event_string_path(trial_path, event_string_index) # get event_path and cd into event_path
        for string_workload_obj in event_string_obj.EventStringWorkloadData_arr:
            _ = mkdir_cd_event_string_workload_path(event_string_path, event_string_index, string_workload_obj.workload) # cd into event_--workload path to store the perf stat output file
            datafile = run_perf(experiment_obj, string_workload_obj, event_string_index) # generate a datafile with the eventstring, workload pairing
            parse_counts_from_file(datafile, string_workload_obj) # parse data from datafile into DataPoints that are appended into string_workload_obj.DataPoint_arr
        os.chdir(trial_path)


def main():
    args = parse_args()
    all_events, all_workloads = process_input(args.eventsfile, args.workloadsfile)
    check_args(args.count, all_events)


    # This conditional flow conducts simple processing of events if args.simple is passed
    # !!!CRITICAL!!! for saving time and making sure the program can actually run on the machine's resources
    if args.simple:
        processed_events_arr = simple_process_events_arr(all_events, args.count)
    else:
        processed_events_arr = process_events_arr(all_events, args.count)

    experiment_obj = ExperimentResults(
        args.label,
        args.trials, 
        args.count, 
        args.eventsfile, 
        args.workloadsfile, 
        processed_events_arr, 
        all_workloads,
        args.perfversion,
        args.perfcore
    )

    experiment_path = mkdir_cd_experiment_path(args.rootpath, experiment_obj.label)

    touch_key_file(experiment_path, experiment_obj.event_strings)

    print()
    print("Experiment Running...")


    # Initialize data structures to reduce code complexity later
    for event_string in experiment_obj.event_strings:
        event_string_obj = EventStringData(event_string)
        experiment_obj.EventStringData_arr.append(event_string_obj)
        for workload in experiment_obj.workloads:
            string_workload_obj = EventStringWorkloadData(event_string, workload)
            event_string_obj.EventStringWorkloadData_arr.append(string_workload_obj)
            individual_events = event_string.split(',')
            for event in individual_events: # this relies on the ordering of events in an event string to persist
                empty_data_point = DataPoint(event, event_string, workload)
                string_workload_obj.DataPoint_arr.append(empty_data_point)


    # For each trial, iterate through the data structures to get the appropriate arguments
    # which are sent to the helper functions to run perf and get data
    for trial in range(experiment_obj.num_of_trials):
        trial_path = mkdir_cd_trial_path(experiment_path, trial)
        print("Running Trial", trial)
        print()
        run_trial(experiment_obj, trial_path)
        print()
        print("Trial", trial, "Finished")
        os.chdir(experiment_path)


    write_results_to_csv(experiment_obj, experiment_path)

    print()
    print("Experiment Finished")
    print(experiment_obj.num_of_trials, "trials were conducted")
    print(experiment_obj.num_of_events_together, "events were counted concurrently each perf invocation")
    print("Find results at", experiment_path + "/results.csv")
    print()


if __name__ == "__main__":
    main()