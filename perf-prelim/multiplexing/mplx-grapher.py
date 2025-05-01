# mplx-grapher.py
# Graphs multiplexing study data

'''
Example using multiplexing study

                        ~/multiplexing-study/
                                |
                                |
        _______________________________________________________
        |                |                |                   | 
        |                |                |                   | 
    1_events/       2_events/       3_events/           4_events/
    results.csv     results.csv     results.csv         results.csv
'''


import os
import matplotlib.pyplot as plt
import numpy as np
import argparse


HOME_PATH = os.path.expanduser("~")

def read_data(root_dir, EVENT_OF_INTEREST):
    # initialize data_dict
    root_dir = os.path.join(HOME_PATH, root_dir)
    # sub_dirs = [name for name in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, name))]
    sub_dirs = ["1_events", "2_events", "3_events", "4_events", "8_events", "16_events"]
    data_dict = {name: [] for name in sub_dirs}

    for name in sub_dirs:
        print(name)
        curr_datafile = os.path.join(root_dir, name, "results.csv")

        with open(curr_datafile) as f:
            for line in f:
                line = line.strip()
                line_contents = line.split(',')
                if line_contents[0] == EVENT_OF_INTEREST and len(line_contents) > 1 and line_contents[1].isnumeric():
                    data_values = line_contents[1:] # After the event is the data
                    data_dict[name] = [int(value) for value in data_values]

    return data_dict


def graph_errorbars(datadict, xlabel):
    plt.style.use('fivethirtyeight')
    x_labels = datadict.keys()
    means = np.zeros(len(datadict))
    errs = np.zeros(len(datadict))
    for index, (key, values) in enumerate(datadict.items()):
        means[index] = np.mean(values)
        errs[index] = np.std(values)

    _, ax = plt.subplots()
    ax.errorbar(x_labels, means, errs, fmt='rx:', ecolor='black', linewidth=1, capsize=6, capthick=2, markersize=8)
    ax.set_ylabel('Counter Value', fontsize=16)
    ax.set_xlabel(xlabel, fontsize=16)
    ax.set_facecolor('white')

    ratio = float(226.5 / 422)
    x_left, x_right = ax.get_xlim()
    y_low, y_high = ax.get_ylim()
    ax.set_aspect(abs((x_right-x_left)/(y_low-y_high))*ratio)

    plt.savefig('multiplexing.eps', format='eps', bbox_inches='tight', facecolor='white')
    plt.savefig('multiplexing.png', format='png', bbox_inches='tight', facecolor='white')
    plt.clf()


def main():
    parser = argparse.ArgumentParser(description='This program produces the errorbar plot for perf studies')
    parser.add_argument('--experimentroot', help='Provide the directory in your home directory containing the experiments you want graphed togther.', required=True, type=str)
    parser.add_argument('--event', help='Event of interest', required=True, type=str)
    parser.add_argument('--xlabel', help='Desired x axis title', required=True, type=str)
    args = parser.parse_args()

    data_dict = read_data(args.experimentroot, args.event)
    graph_errorbars(data_dict, args.xlabel)

if __name__ == "__main__":
    main()
