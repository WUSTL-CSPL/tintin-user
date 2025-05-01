# pathcreator.py
# Lien Zhu
# Builds path strings for use in perfstress.py result storing


import os
import shutil       # rm -rf functionality


### Directory Creation ###

# Creates directory that holds data for all
# invocations in one central directory
#
def mkdir_root_path(desired_root_path):
    root_path = os.path.join(os.path.expanduser("~"), desired_root_path) 
    if not os.path.exists(root_path):
        os.mkdir(root_path)
    return root_path


# Create the experiment path using the provided label
def mkdir_cd_experiment_path(desired_root_path, label):
    root_path = mkdir_root_path(desired_root_path) # cd into root_path
    experiment_path = os.path.join(root_path, label)
    if os.path.exists(experiment_path):
        shutil.rmtree(experiment_path)
    os.mkdir(experiment_path)
    os.chdir(experiment_path)
    return experiment_path


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
def mkdir_cd_event_string_path(experiment_path, event_index):
    event_path = os.path.join(experiment_path, str(event_index)) # use the event's index as the directory name
    os.mkdir(event_path)
    os.chdir(event_path)
    return event_path


# Creates folders for every event(s) --workload pair, containing text files for every trial
#
def mkdir_cd_event_string_workload_path(event_path, event_index, workload):
    workload_name = workload.split()[0].strip() # parses "--workload ops" into "--workload"
    event_workload_path_str = str(event_index) + "_" + workload_name
    event_workload_path = os.path.join(event_path, event_workload_path_str)
    os.mkdir(event_workload_path)
    os.chdir(event_workload_path)
    return event_workload_path
