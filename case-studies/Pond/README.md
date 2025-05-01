
This repo contains the code used to replicate Pond's Latency Insensitivity Model. The entire codebase has been tested only on Ubuntu 20.04. For best results and to avoid compatibility issues, please use this version for reproduction.




## Important Files

 - **`vtess_code/`:** Clone of https://github.com/vtess/Pond. This is the code used to emulate the CXL memory and orchestrate the benchmarks. We augmented `cpu2017/run-cpu2017.sh` and `gapbs/run-gapbs.sh` with the functionality to measure event counts with `Tintin`. The functionality to measure with `emon` was already included. 
 - **`latency_model/counter_data/`:** Folder with the measurements for every experiment. Experiment have measurements for each workload. The workloads are the same across all experiments. Each workload contains a set of `L100` and `L0` files. `L100` files are the ones generated when running the workload on 100% local DRAM memory, whereas `L0` corresponds to 0% local DRAM and 100% (emulated) CXL memory. The `tintin.dat` or `emon.dat` files contain the event measurements. The `.time` files contain the running time of the workload, which is then used to compute relative slowdowns.
 - **`latency_model/model.py`**: Main script that trains the model and tests its accuracy. Run it with `conda activate pond_latency_model` and `python model.py`. 
 - **`latency_model/results.txt`:** Experiment results.
 - **`latency_model/counters.py`:** Events measured for the experiments. 
 - **`latency_model/pond_model_events_uncertainty.c`:** Program that uses `Tintin` to measure the set of events given in `counter.py`. Takes in a `pid` and a read frequency in milliseconds.
 - **`latency_model/pond_model_events_uncertainty_weights.c`:** Same as `latency_model/pond_model_events_uncertainty.c` but also passes weights to the `Tintin` scheduler for each event being measured. The weights are hardcoded based on the weights that the model assigned to each event when being trained.

## How to run an experiment

### Set up environment (Optional)

Note: If you are using the remote machine we have set up, you can skip this section.


0. Install the pre-quisite packages
    ```bash
    $ sudo apt install numactl
    $ conda env create -f tintin-user/case-studies/Pond/pond_conda_env.yml
    ```

1. Install `libpfm4` by following the steps here: https://sourceforge.net/p/perfmon2/libpfm4/ci/master/tree/

2. Install `Vtune` (which includes `EMon`) by following the steps here: https://www.intel.com/content/www/us/en/docs/vtune-profiler/installation-guide/2023-1/overview.html

3. Build `latency_mode/pond_model_events_uncertainty.c` (and `latency_mode/pond_model_events_uncertainty_weights.c`) by:
    ```bash
    gcc -o pond_model_events_uncertainty pond_model_events_uncertainty.c -lpfm -Wall -O2
    ```

4. In `vtess_code` run `sudo ./pmqos`.
 <!-- 4. For a `cpu2017` experiment, go to `cpu2017/run-cpu2017.sh`. For a `gapbs` experiment, go to `gapbs/run-gapbs.sh` .  -->

5. Go to`cpu2017/run-cpu2017.sh`, modify the following variables according to your setting:
    ```
    # Change the following global variables based on your environment
    #-------------------------------------------------------------
    EMON="/opt/intel/oneapi/vtune/xxxx/bin64/" # Emon path
    TINTIN="/home/xxx/pond_model_events_uncertainty_weights" # Tintin-user's binary for collecting HPC data
    RUNDIR="/home/xxx/vtess_code" #

    # Output folder
    #RSTDIR="rst/emon-$(date +%F-%H%M)-$(uname -n | awk -F. '{printf("%s.%s\n", $1, $2)}')"
    MEMEATER="$RUNDIR/memeater"
    CPU2017_RUN_DIR="${RUNDIR}/cpu2017"
    RSTDIR="${CPU2017_RUN_DIR}/rst/"

    RUN_EMON=1 # whether to run emon together
    RUN_TINTIN=0
    ```
<!-- 
 The other benchmarks suites were not augmented to measure with `Tintin`. Modify the global variables based on your environment. Set `RUN_EMON` or `RUN_TINTIN` (not both).  -->
 6. Build all workloads in CPU 2017 SPEC benchmark, and copy the executable to the directory `vtess_code/cpu2017/xxx/`. For example:
    ```bash
    $ cp ~/cpu2017//benchspec/CPU/503.bwaves_r/exe/bwaves_r_base.mytest-m64 vtess_code/cpu2017/503.bwaves_r/
    ```

 7. Install the conda environment for Pond's latency model
    ```bash
    $ conda env create -f tintin-user/case-studies/Pond/pond_conda_env.yml
    ```
### Run the workloads and collect data

8. For `cpu2017`, run `sudo ./run-cpu2017.sh w.txt`. This will run the workloads one by one and collect runtime and event counts. These results will be located in the `cpu2017/rst/` directory.  This will take around 6-12 hours to complete. If running from an `ssh` session, use `sudo nohup sudo ./run-cpu2017.sh w.txt &` to ensure the command outlives the session. For `gapbs`, replace `./run-cpu2017.sh w.txt` with `./run-gapbs.sh` (omit the `w.txt`). This will take around 18-24 hours.


9. The bash script will run each workload twice, once in 100% DRAM memory and once in 0% DRAM and 100% CXL. Once the first workload is complete, check the `rst` folder to make sure everything is in order. There should be a `L0-1.time` and a `L100-1.time` file. The runtime for `L0` should be equal or greater than `L100`. Some `cpu2017` workloads fail to run. The time investment to get them to work was not worth it. The workloads that work (and should work for future experiments) are the ones that can be found in `counter_data` already.


10. Once the benchmarks complete, results for all the workloads should be in the `rst` folder. Make a new folder in `latency_model/counter_data/` and copy the contents of `rst` to that new folder. 

### Process the data

11. `cd` to `counter_data` and run `remove_cxl_folder.sh`. Make sure to adjust the script since some paths are hardcoded. This will remove the `CXL` folder from every workload's data.
 
12. Run `python remove_truncated_readings.py`. Again, make sure to check the script for any hardcoded values. This will remove the last measurement for all workloads, which may be truncated due to the workload finishing.

13. Now that the data is loaded into `counter_data`, replicate the existing code in `model.py` to read in that new data and train a new model. Run this file with `python model.py`. Make sure to be in the `pond_latency_model` conda environment. **Note:** `model.py` expects all datasets to have the exact same workloads. Your new dataset might have more workloads than the existing datasets. This is because some workloads were removed from the existing datasets because they were flaky or would fail to run. All existing datasets have the same 41 workloads. If your dataset has more than that, delete the additional workloads that are not present in the original datasets.

    After the run completes, it will generate a log file named **results.txt**. You can replace the original file in the plotting scripts under `tintin-user/plots/` with this one to visualize the results.

### Extra Information: Modifications to the existing Pond Code
We made modifications to the provided Pond code to facilitate running the artifact and integrate it with Tintin.


This modification was limited to the `run-cpu2017.sh` and `run-gapbs.sh` scripts, and the `cmd.sh` file for every workload. 


+ Modification #1: The `run-cpu2017.sh` and `run-gapbs.sh` scripts are the main scripts responsible for orchestrating the process of emulating the CXL memory and running the benchmarks. These scripts were able to measure a workload's events using `Emon`, and we augmented them to use `Tintin`. 

To measure with `Tintin`, we make the script call `pond_model_events_uncertainty`, which monitors a running program using `Tintin`. `pond_model_events_uncertainty` requires the `pid` of the workload in order to monitor it.

These scripts are not very straightforward, which make obtaining that `pid` not trivial. In a nutshell, the `run-cpu2017.sh` script (and its `gapbs` equivalent) create a temporary file `r.sh`, which in turn executes the corresponding `cmd.sh` file for that workload. The `cmd.sh` file is what then runs the workload's binary. To send the `pid` back to the main script, the `cmd.sh` file writes the `pid` to `tmp/workload.pid`, and the main script reads it from there. Once the `pid` is obtained, it initialized `pond_model_events_uncertainty`.

The `cmd.sh` file for each individual workload had to be modified to perform this. Note that for `cpu2017` we only ran the `5xx` workloads, so the `6xx` workloads were left untouched.

+ Modification #2: Other modifications include pinning all the workloads to one core when measuring with `Emon`. Since `Emon` only supports system-wide scoping, we were forced to pin all workloads to one core and have `Emon` measure that core. This was achieved by using `taskset` in `cmd.sh`. **Note:** When running `cpu2017` or `gapbs` workloads, if measuring with `Emon` make sure to pin all workloads to the first core. And if measuring with `Tintin`, make sure to not pin the workloads (by not including `taskset` in `cmd.sh`).
 