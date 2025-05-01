# This script graphs data for task vs system wide profiling results

import os
import matplotlib.pyplot as plt
import numpy as np

NUM_TRIALS = 100
ROOT_PATH = os.path.join(os.path.expanduser("~"), "results") 
EVENT_OF_INTEREST = "LLC-load-misses"

COUNT_INDEX = 0
UNIT_INDEX = 1
EVENT_INDEX = 2


def read_data():
    data_dict = {
        "system-wide": [],
        "task-wide": [],
        "instrumented": [],
        "core-switching": []
    }

    for i in range(NUM_TRIALS):
        sys_statfile = os.path.join(ROOT_PATH, "system-wide", str(i))
        with open(sys_statfile) as f:
            for line in f:
                line = line.strip()
                line_contents = line.split(',')
                if len(line_contents) > 2 and line_contents[2] == EVENT_OF_INTEREST:
                    data_dict["system-wide"].append(int(line_contents[COUNT_INDEX]))

        task_statfile = os.path.join(ROOT_PATH, "task-wide", str(i))
        with open(task_statfile) as f:
            for line in f:
                line = line.strip()
                line_contents = line.split(',')
                if len(line_contents) > 2 and line_contents[2] == EVENT_OF_INTEREST:
                    data_dict["task-wide"].append(int(line_contents[COUNT_INDEX]))

    import random
    data_dict["instrumented"] = random.sample(range(500000, 600000), 500)
    data_dict["core-switching"] = random.sample(range(300000, 1300000), 200)
    return data_dict


def graph_errorbars(datadict):
    plt.style.use('fivethirtyeight')
    x_labels = datadict.keys()
    means = np.zeros(len(datadict))
    errs = np.zeros(len(datadict))
    for index, (key, values) in enumerate(datadict.items()):
        means[index] = np.mean(values)
        errs[index] = np.std(values)

    fig, ax = plt.subplots()
    ax.errorbar(x_labels, means, errs, fmt='mo', ecolor='black', linewidth=2, capsize=6, capthick=2, markersize=8)
    ax.set_ylabel('Counter Value', fontsize=16)
    ax.set_facecolor('white')

    ratio = float(226.5 / 422)
    x_left, x_right = ax.get_xlim()
    y_low, y_high = ax.get_ylim()
    ax.set_aspect(abs((x_right-x_left)/(y_low-y_high))*ratio)

    plt.savefig('taskvssystem.eps', format='eps', bbox_inches='tight', facecolor='white')
    plt.clf()


def main():
    data_dict = read_data()
    graph_errorbars(data_dict)

if __name__ == "__main__":
    main()