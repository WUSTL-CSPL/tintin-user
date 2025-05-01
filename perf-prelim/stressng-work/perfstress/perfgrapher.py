# This script runs vanilla/perfstress.py many times with different number of concurrent perf events
# and graphs them using matplotlib

import os
import matplotlib.pyplot as plt
import numpy as np

TRIALS = 100
ROOT_PATH = os.path.join(os.path.expanduser("~"), "multiplexing-data") 
EVENT_OF_INTEREST = "LLC-load-misses"

COUNTS_ARR = [1,2,3,4,5,6,12,24]


### Actual Functions ###

def runperfstress():
    for count in COUNTS_ARR:
        cmd_str = "python3 perfstress.py -p perf_5.10 -e kobe.txt -w workloads.txt --perfcore 1 --stresscore 1 -t " + str(TRIALS) + " --count " + str(count)
        os.system(cmd_str)


def read_data():
    data_dict = {}
    for curr_count in COUNTS_ARR:
        curr_datafile = os.path.join(ROOT_PATH, str(curr_count) + "_events", "results.csv")

        with open(curr_datafile) as f:
            for line in f:
                line = line.strip()
                line_contents = line.split(',')
                if line_contents[0] == EVENT_OF_INTEREST and len(line_contents) > 1 and line_contents[1].isnumeric():
                    data_values = line_contents[1:]
                    data_dict[str(curr_count)] = [int(value) for value in data_values]

    return data_dict


def graph_boxes(data_dict):
    fig, ax = plt.subplots()
    ax.boxplot(data_dict.values())
    ax.set_xticklabels(data_dict.keys())
    plt.savefig('boxplots.png')
    plt.clf()


def graph_errorbars(datadict):
    plt.style.use('fivethirtyeight')
    x_labels = datadict.keys()
    means = np.zeros(len(datadict))
    errs = np.zeros(len(datadict))
    for index, (key, values) in enumerate(datadict.items()):
        means[index] = np.mean(values)
        errs[index] = np.std(values)

    fig, ax = plt.subplots()
    ax.errorbar(x_labels, means, errs, fmt='rx:', ecolor='black', linewidth=1, capsize=6, capthick=2, markersize=8)
    ax.set_ylabel('Counter Value', fontsize=16)
    ax.set_xlabel('Number of Multiplexed Events', fontsize=16)
    ax.set_facecolor('white')

    ratio = float(226.5 / 422)
    x_left, x_right = ax.get_xlim()
    y_low, y_high = ax.get_ylim()
    ax.set_aspect(abs((x_right-x_left)/(y_low-y_high))*ratio)

    plt.savefig('multiplexing.eps', format='eps', bbox_inches='tight', facecolor='white')
    plt.clf()


def graph_bar(datadict):
    # plt.style.use('fivethirtyeight')
    x_labels = datadict.keys()
    means = np.zeros(len(datadict))
    errs = np.zeros(len(datadict))
    for index, (key, values) in enumerate(datadict.items()):
        means[index] = np.mean(values)
        errs[index] = np.std(values)

    fig, ax = plt.subplots()
    ax.bar(
        x_labels, 
        means, 
        yerr=errs, 
        align='center',
        alpha=0.8,
        ecolor='black',
        capsize=8,
        color='red',
        error_kw={
            "linewidth":1,
            "capthick":3
        }
    )

    ax.set_ylabel('Counter Value', fontsize=12)
    ax.set_xlabel('Number of Events Counted Concurrently', fontsize=12)
    ax.yaxis.grid(True)
    ax.set_axisbelow(True)

    plt.savefig('bars.png', bbox_inches='tight')
    plt.clf()




def main():
    # runperfstress()
    data_dict = read_data()
    graph_errorbars(data_dict)

if __name__ == "__main__":
    main()