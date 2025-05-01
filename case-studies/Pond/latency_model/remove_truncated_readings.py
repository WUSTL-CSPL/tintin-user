'''
The Pond benchmarking scripts kills the program that is measuring events when the benchmark
is done. This can interrupt the measuring's program stdout. This script will remove the last set
of measurements of every file in a folder, to remove those potentially incomplete measurements.

Warning: This script does not check if the set of measurements is incomplete. It only removes
the last measurement. Every time you run it you will delete the last set of measurements.
'''

import os

def remove_last_chunk(file_path):
    try:
        # Read the content of the file
        with open(file_path, 'r') as file:
            content = file.read()

        # Split the content into chunks using newline as the delimiter
        chunks = content.split('\n\n')

        # Remove the last chunk
        if chunks:
            chunks.pop()

        # Join the remaining chunks back into a string
        updated_content = '\n\n'.join(chunks)

        #Write the updated content back to the file
        with open(file_path, 'w') as file:
            file.write(updated_content)

        print("Last chunk removed successfully.")

    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

folder_path = os.path.join(os.getcwd(), "counter_data/elastic_weights")
for folder in os.listdir(folder_path):
    l100_file = os.path.join(folder_path, folder, "L100-1-tintin.dat")
    l0_file = os.path.join(folder_path, folder, "L0-1-tintin.dat")

    # Check if the path is a file (not a subfolder)
    if os.path.isfile(l100_file):
        remove_last_chunk(l100_file)
    if os.path.isfile(l0_file):
        remove_last_chunk(l0_file)