import argparse

# Define the command-line arguments
parser = argparse.ArgumentParser(description='Move a target string to the last line of a file')
parser.add_argument('filename', help='the name of the input file')
parser.add_argument('target', help='the target string to move to the first line')
args = parser.parse_args()

# Read in the contents of the file
with open(args.filename, 'r') as f:
    lines = f.readlines()

# Remove any newline characters from the end of each line
lines = [line.strip() for line in lines]

# Find the index of the target string in the list of lines
try:
    index = lines.index(args.target)
except ValueError:
    print(f"{args.target} not found in {args.filename}")
    exit(1)

# Move the target string to the first line of the list
lines.insert(0, lines.pop(index))

# Write the modified list of lines back to the file
with open(args.filename, 'w') as f:
    f.write('\n'.join(lines))
    f.write('\n')
