# statwriter.py
# This program takes data either from perf stat files or instrumented SPEC output files 
# and writes to csv file that is formatted functionally similar to results.csv in perfspec.py output.
# The resulting csv file is placed in the source_path argument


'''
Example for sourcetype = stat using system-wide assuming 3 trials
                /home/cspl/experiment_root/system-wide
                                |
                                |
        _______________________________________________________
        |                |                |                   | 
        |                |                |                   | 
    0.txt           1.txt           2.txt               results.csv

Example for sourcetype = spec using system-wide again assuming 3 trials

'''


import argparse
import csv
import os


HOME_DIR = os.path.expanduser("~")

def parse_stat(source_path):
    # iterate over every trial's file

    file_path = os.path.join(source_path, "results.csv") # ensures the csv file is written to the source_path
    with open(file_path, 'w', newline="") as file:
        csv_writer = csv.writer(file)


def parse_spec(source_path, benchmark):
    # need to make an dictionary of all 18 benchmarks output files
    pass


def main():
    parser = argparse.ArgumentParser(description='This program writes data from perf stat and instrumented SPEC output files')
    parser.add_argument('--sourcepath', help='Provide the FULL PATH to the directory containing the experiment you want to be processed.', required=True, type=str)
    parser.add_argument('--sourcetype', help='Either stat or spec', required=True, type=str)
    parser.add_argument('--benchmark', help='If sourcetype == spec, specify the benchmark you would like processed', required=False, default="", type=str)
    args = parser.parse_args()

    if args.sourcetype == "stat":
        parse_stat(args.sourcepath)
    else:
        parse_spec(args.sourcepath, args.benchmark)


if __name__ == "__main__":
    main()