# perflist.py
# Lien Zhu
# Development Started January 1, 2023
# Last Updated March 4, 2023

import sys, os
import argparse
import re

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--perfversion', help='specify perf version', type=str, default="perf")
    parser.add_argument('-o', '--output', help='specify output location', type=str, required=True)
    args = parser.parse_args()

    
    temp_file_path = "perflistoutputfile.txt"
    os.system(args.perfversion + " list > " + temp_file_path) # temporary txt file receives output

    with open(temp_file_path) as read_file:
        with open(args.output, "w") as output_file:
            for line in read_file:
                regex_result = re.findall("event]", line) # use regex to target "[foo bar event]"
                if len(regex_result) != 0:
                    event_str = line.split()[0]
                    output_file.write(event_str + "\n")

    os.remove(temp_file_path)

if __name__ == "__main__":
    main()
