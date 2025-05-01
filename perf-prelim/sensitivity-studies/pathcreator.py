# pathcreator.py
# Lien Zhu
# Builds path strings for use in perfstress.py result storing

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


### Directory Creation ###

# Creates directory that holds data for all
# invocations in one central directory
#
def mkdir_root_path():
    root_path = os.path.join(os.path.expanduser("~"), "prelim-root") 
    if not os.path.exists(root_path):
        os.mkdir(root_path)
    return root_path


# Creates directory specific for current invocation
#
def mkdir_cd_experiment_path(num_of_simultaneous_events, num_of_trials, events_input_file, workloads_input_file, interval):
    root_path = mkdir_root_path() # cd into root_path
    events_input_filename = events_input_file.split('.')[0]
    workloads_input_filename = workloads_input_file.split('.')[0]
    path_string = str(num_of_simultaneous_events) + "_events-" + str(num_of_trials) + "_trials-" + events_input_filename + "_" + workloads_input_filename + "_" + interval + "ms-interval"
    experiment_path = os.path.join(root_path, path_string)
    if os.path.exists(experiment_path):
        shutil.rmtree(experiment_path)
    os.mkdir(experiment_path)
    os.chdir(experiment_path)
    return experiment_path


# A place to store each trial's results_*.csv
#
def mkdir_results_path(experiment_path):
    results_path = os.path.join(experiment_path, "results")
    os.mkdir(results_path)
    return results_path



# Create folder for each trial
# 
def mkdir_cd_trial_path(experiment_path, trial):
    trial_string = "trial_" + str(trial)
    trial_path = os.path.join(experiment_path, trial_string)
    os.mkdir(trial_path)
    os.chdir(trial_path)
    return trial_path


# Create folder specific for one string of events
#
def mkdir_cd_event_path(trial_path, event_index):
    event_path = os.path.join(trial_path, str(event_index)) # use the event's index as the directory name
    os.mkdir(event_path)
    os.chdir(event_path)
    return event_path


# Creates folders for every event(s) --workload pair, each containing a text file
#
def mkdir_cd_event_workload_path(event_path, event_index, workload):
    workload_name = workload.split()[0].strip() # parses "--workload ops" into "--workload"
    event_workload_path_str = str(event_index) + "_" + workload_name
    event_workload_path = os.path.join(event_path, event_workload_path_str)
    os.mkdir(event_workload_path)
    os.chdir(event_workload_path)
    return event_workload_path
