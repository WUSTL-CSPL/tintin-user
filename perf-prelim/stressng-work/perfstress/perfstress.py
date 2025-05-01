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

from ExperimentResults import *
from EventStringData import *
from EventStringWorkloadData import *
from DataPoint import *


# Preps the command to invoke perf on stress-ng
# Expected txt file name format: "event_index_--workload_trial.txt"
# Returns path to the <output_file>.txt
#
def run_perf(experiment_obj, string_workload_obj, event_string_index):
    workload_name = string_workload_obj.workload.split()[0].strip() # parses "--workload #ops" into "--workload"
    datafile = str(event_string_index) + "_" + workload_name + ".txt" # create output file name
    
    chrt_cmd_str = "sudo chrt --" + experiment_obj.scheduler + " " + experiment_obj.priority 
    perf_cmd_str = experiment_obj.perfversion + " stat -o " + datafile + " -e " + string_workload_obj.eventstring + " -x ," + " -C " + experiment_obj.perfcore
    workload_arg_str = experiment_obj.stressversion + " -q" + " --taskset " + experiment_obj.stresscore + " --cpu " + experiment_obj.stresscpu + " " + string_workload_obj.workload 

    full_cmd = chrt_cmd_str + " " + perf_cmd_str + " " + workload_arg_str

    os.system(full_cmd) # run command, creating output text file for trial
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

    # processed_events_arr = process_events_arr(all_events, args.count)
    processed_events_arr = simple_process_events_arr(all_events, args.count)

    experiment_obj = ExperimentResults(
        args.trials, 
        args.count, 
        args.eventsfile, 
        args.workloadsfile, 
        processed_events_arr, 
        all_workloads,
        args.scheduler,
        args.priority,
        args.perfversion,
        args.perfcore,
        args.stressversion,
        args.stresscore,
        args.stresscpu
    )

    experiment_path = mkdir_cd_simple_experiment_path(experiment_obj.num_of_events_together)

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
        run_trial(experiment_obj, trial_path)
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