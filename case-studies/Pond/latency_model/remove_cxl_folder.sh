#!/bin/bash

# Iterate through each subdirectory in the current working directory
for dir in "counter_data/elastic_weights"/*/; do
    if [ -d "$dir" ]; then
        # Check if a "CXL" directory exists within the subdirectory
        if [ -d "${dir}CXL" ]; then
            # Move files from "CXL" to the containing directory
            mv "${dir}/CXL"/* "$dir/"
            # # Remove the empty "CXL" directory
            rmdir "${dir}/CXL"
        fi
    fi
done