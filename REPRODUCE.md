
# Reproduce Tintin

To guide users in reproducing the results, we will first explain the plotting scripts for each figure in the paper. Then we will guide how to generate experimental data. Users can replace the original data with their own generated data to plot their own results.

We divide this into two parts. The first part covers how to reproduce the general results, which involves **Figures 13, 14, 15, and 16**. The second part explains how to reproduce the case studies (**Figures 10 and 11**).

The only missing figure is **Figure 12b**, which corresponds to case study 3 on FIRM. This case study requires two server-class PCs and Intel CAT support. Although we previously set up this environment, we later lost access to the machines, so we omit this case study from the artifact evaluation. Moreover, case study 3 is similar to case study 1, as both are resource orchestration scenarios. We hope that the results from case study 1 sufficiently support the claims made in the paper.


## Part I - General Evaluation

The following evaluation are conducted on SPEC 2017 CPU benchmark and princeton PARSEC-3.0 benchmark. SPEC 2017 is not an open source benchmark and PARSEC is not available anymore in the website (for some unknown reasons, the webstie is down). Thus, we cannot share the benchmark publicly, but we have set up in the machine we provided for artifact evaluation.


### Figure 13 - Measurement errors (20 minutes of manual time + {0.5–5} hours of machine time)

1. First, let's plot the figure 13 in the paper. The figure shows the results of 26 workloads from the two benchmarks (SPEC 2017 and PARSEC-3.0).

    ```bash
    $ cd tintin-user
    $ cd plots
    $ python3 figure-13_plot_accuracy_bar.py
    # A figure will show up
    ```

    If you open the script, you will see that the workload names and data are there as follows. Each workload has four data entries, located in four arraries `accuracy_linux_perf`, `accuracy_counterminer`, `accuracy_uncertainty_first`, and `accuracy_tintin_elastic`, which correspond to the four bars in the figure. 
    ```python
    workloads = ['perlbench',     # -> 0
                  'gcc',          # -> 1
                  'mcf',          # -> 2
                  'omnetpp',      # -> 3
                  'xalancbmk',    # -> 4
    ...
    ``` 

    ```python
    accuracy_linux_perf = [16.529447,  # -> 0
                            6.062688,  # -> 1	
                            1.457191,  # -> 2
                            5.32018,   # -> 3
    ...
    ``` 

    The comment `# -> 0` indicates which workload the value corresponds to. In this case, `-> 0` means the value is for `perlbench`. Since  it appears in `accuracy_linux_perf`, it represents the accuracy of Linux perf on the `perlbench` workload.


2. Next, we proceed to generate the results. Please note that running all 26 workloads may take several hours. We recommend that evaluators randomly select a few workloads as validation examples. However, if time permits, a launch script is also provided to generate results for all workloads.


3. To generate results for a single workload, start by configuring the benchmark to use Tintin’s system calls.

    ```bash
    $ cd ~/cpu2017_instrumented
    # Edit the configuration file
    $ vim config/tintin-gcc-linux-x86.cfg
    # you can also uses gedit, nano or other editors 
    # $ gedit config/tintin-gcc-linux-x86.cfg
    ```
    Locate the following compiler flags section and modify it to:
    - Disable PERF_SYSCALL (comment this line)
    - Enale TINTIN_SYSCALL (uncomment out this line)

    The final configuration should look like:
    ```makefile
    default=base:     # Base compilation flags
       OPTIMIZE       = -g -O3 -march=native -DTINTIN_SYSCALL   # <- Make sure this line is active
    #  OPTIMIZE       =  -g -O3 -march=native  -DPERF_SYSCALL  # <- Ensure this line is commented
    ```

4. Run the workload. In the commands below, `500` represents the workload number. The full list of available workloads includes: `500.perlbench_r`, `502.gcc_r`, `505.mcf_r`, `520.omnetpp_r`, `523.xalancbmk_r`, `525.x264_r`, `531.deepsjeng_r`, `541.leela_r`, `557.xz_r`, `507.cactuBSSN_r`, `508.namd_r`, `510.parest_r`, `519.lbm_r`, `538.imagick_r`, and `544.nab_r`.


    ```bash
    $ cd ~/cpu2017_instrumented
    $ ./bin/runcpu --config=tintin-gcc-linux-x86.cfg  --size=ref --rebuild  --action run 500
    ```
    This will take approximately 5 to 15 minutes. It may print some errors, but that’s normal and nothing to worry about.


5. Obtain the results. Once the workload finishes running, it will generate a log file in `/tmp`. 

    ```bash
    $ cat /tmp/tintin_cpu2017_spec_perlbench_500.log
    #  It will show the log like:
    [Multiplexed] Cache misses:  124100918 
    [Ground Truth] Cache misses: 124627294 
    **Error** : 0.422360 % 
    # Here 0.422360 %  is the error value
    ```
6. Go to the script and replace the original data with the generated data.
    ```bash
    vim tintin-user/plots/figure-13_plot_accuracy_bar.py
    ```

    The workload used in our experiments is **500.perlbench**, which corresponds to the following lines:

    ```python
    workloads = ['perlbench',     # -> 0
    ...

    accuracy_tintin_elastic = [4.163906,   # -> 0
    ...
    # So lets replace the 4.163906 by 0.422360
    ```
    The modifed version should look like this:
    ```python
    accuracy_tintin_elastic = [0.422360,      # -> 0
    ```

    We would like to clarify that the reported accuracy refers specifically to the cache-misses event. In the original paper, we calculated the average accuracy across five different events. To simplify the AE process, we focus only on the cache-misses event here. The expected outcome of the evaluation is that Tintin consistently outperforms Linux perf, typically achieving 2–3X higher accuracy.


7. Now that you have modified one data entry, you can replot the figure by running:

    ```bash
    $ cd ~/tintin-user/plots
    $ python3 figure-13_plot_accuracy_bar.py
    ```
    This will display the figure again.

8. To reproduce the results for all 26 workloads, we have prepared scripts to automate the process.

    ```bash
    $ cd ~/cpu2017_instrumented
    $ ./tintin_launch.sh
    ```

    Also for PARSEC benchmark:
    ```bash
    $ cd ~/parsec_instrumented
    $ ./tintin_launch.sh
    ```
    Once the two scripts have finished running, log files will be generated in `/tmp/` as follows:

    ```bash
    $ ls -l /tmp
    -rw-rw-r--  1 cspl cspl    790 Apr 23 10:58 tintin_cpu2017_spec_cactuBSSN_507.log
    -rw-rw-r--  1 cspl cspl    791 Apr 23 10:37 tintin_cpu2017_spec_deepsjeng_531.log
    -rw-rw-r--  1 cspl cspl   3920 Apr 23 10:04 tintin_cpu2017_spec_gcc_502.log
    -rw-rw-r--  1 cspl cspl    791 Apr 23 11:38 tintin_cpu2017_spec_imagick_538.log
    -rw-rw-r--  1 cspl cspl    790 Apr 23 11:27 tintin_cpu2017_spec_lbm_519.log
    -rw-rw-r--  1 cspl cspl    825 Apr 23 10:46 tintin_cpu2017_spec_leea_541.log
    -rw-rw-r--  1 cspl cspl    797 Apr 23 10:11 tintin_cpu2017_spec_mcf_505.log
    -rw-rw-r--  1 cspl cspl    793 Apr 23 11:46 tintin_cpu2017_spec_nab_544.log
    -rw-rw-r--  1 cspl cspl    789 Apr 23 11:03 tintin_cpu2017_spec_namd_508.log
    -rw-rw-r--  1 cspl cspl    797 Apr 23 10:18 tintin_cpu2017_spec_omnetpp_520.log
    -rw-rw-r--  1 cspl cspl    800 Apr 23 11:20 tintin_cpu2017_spec_parest_510.log
    -rw-rw-r--  1 cspl cspl   4718 Apr 23 09:58 tintin_cpu2017_spec_perlbench_500.log
    -rw-rw-r--  1 cspl cspl   2427 Apr 23 10:31 tintin_cpu2017_spec_x264_525.log
    -rw-rw-r--  1 cspl cspl    792 Apr 23 10:23 tintin_cpu2017_spec_xalancbmk_523.log
    -rw-rw-r--  1 cspl cspl   2358 Apr 23 10:52 tintin_cpu2017_spec_xz_557.log
    -rw-rw-r--  1 cspl cspl    772 Apr 23 12:46 tintin_parsec_blackscholes.log
    -rw-rw-r--  1 cspl cspl    769 Apr 23 12:49 tintin_parsec_bodytrack.log
    -rw-rw-r--  1 cspl cspl    775 Apr 23 12:52 tintin_parsec_canneal.log
    ...
    ```

    You may need to extract the results from the log files and replace the corresponding data in the plotting script.

    A heads-up is that this may take several hours. You can also run individual workloads to save time. In the **SPEC 2017** benchmark, the used workloads are: `500.perlbench_r`, `502.gcc_r`, `505.mcf_r`, `520.omnetpp_r`, `523.xalancbmk_r`, `525.x264_r`, `531.deepsjeng_r`, `541.leela_r`, `557.xz_r`, `507.cactuBSSN_r`, `508.namd_r`, `510.parest_r`, `519.lbm_r`, `538.imagick_r`, and `544.nab_r`. In the **PARSEC-3.0** benchmark, the workloads include: `blackscholes`, `bodytrack`, `canneal`, `ferret`, `fluidanimate`, `freqmine`, `raytrace`, `streamcluster`, `swaptions`, `vips`, and `x264`.




    To run a single PARSEC-3.0 workload, use the following commands.


    Clean the stateful obj files and executables:
    ```bash
    $ cd ~/parsec_instrumented/
    $ rm -rf pkgs/libs/*/obj
    $ rm -rf pkgs/libs/*/inst
    $ source env.sh
    $ parsecmgmt -a fullclean
    $ parsecmgmt -a fulluninstall
    ```

    Also, we need to modify the macro in PARSEC 3.0 to use Tintin's system calls:  
    ```bash
    $ cd ~/parsec_instrumented
    $ vim ./pkgs/libs/hooks/src/hooks.c
    ```
    Modify the macros as follows:
    ```c
    // #define PERF_SYSCALL
    #define TINTIN_SYSCALL
    ```  

    Then build and run the workload:
    ```
    $ parsecmgmt -a build -p blackscholes -i native -c gcc-hooks
    $ parsecmgmt -a run -p blackscholes -i native -c gcc-hooks
    ```

    The log files will be generated under the `/tmp` directory.


9. So far, we have generated the results for Tintin with elastic scheduling. To generate the results for Tintin using the Uncertainty-First policy, we need to configure the kernel accordingly.
    
    ```bash
    $ echo 2 >  /proc/sys/tintin/tintin_sched_policy
    # This configures the kernel to use the Uncertainty-First policy.
    ```

    Next, repeat steps 4, 5, and 6 (or step 8) to generate the results. The log files will still be saved in `/tmp`.


10. So far, we have generated the results for Tintin with elastic scheduling. To generate the results for Linux perf, you will need to modify the configuration and re-run the experiments.
    
    ```bash
    # This disables Tintin scheduling in kernel
    $ echo 0 >  /proc/sys/tintin/tintin_sched_switch_on
    ```

    Modify the configuration file in SPEC 2017 to use native Linux perf system calls
    ```bash
    $ cd ~/cpu2017_instrument
    # Edit the configuration file
    $ vim config/tintin-gcc-linux-x86.cfg
    ```
    Locate the following compiler flags section and modify it to:
    - Enable PERF_SYSCALL (uncomment this line)
    - Disable TINTIN_SYSCALL (comment out this line)

    The final configuration should look like:
    ```makefile
    default=base:     # Base compilation flags
    # OPTIMIZE       =  -g -O3 -march=native -DTINTIN_SYSCALL  # <- Ensure this line is commented
      OPTIMIZE       = -g -O3 -march=native -DPERF_SYSCALL   # <- Make sure this line is active
    ```

    Modify the system calls in PARSEC 3.0:  

    ```bash
    $ cd ~/parsec_instrumented
    $ vim ./pkgs/libs/hooks/src/hooks.c
    ```
    Modify the macros as follows:
    ```c
    #define PERF_SYSCALL
    // #define TINTIN_SYSCALL
    ```  

    Then you may need to repeat steps 4, 5, 6 (or 8) to generate the results. The log files are still in `/tmp`.

11. So far, we have generated the results for Tintin-elastic scheduling, Tintin Uncertainty-First, Linux Perf. To generate the results for CounterMiner, we need to configure kernel.

    ```bash
    $ echo 1 > /proc/sys/tintin/counterminer_on
    ```
    Then you may need to repeat steps 4, 5, 6 (or 8) to generate the results. The log files are still in `/tmp`.

    After that, please turn off countermine by:

    ```bash
    $ echo 0 >  /proc/sys/tintin/counterminer_on
    ```

### Figure 14 - Overhead (30 minutes of manual time + {0.5–5} hours of machine time)


1. First, let's plot the figure 13 in the paper. The figure shows the results of 26 workloads from the two benchmarks (SPEC 2017 and PARSEC-3.0).

    ```bash
    $ cd tintin-user
    $ cd plots
    $ python3 figure-14_plot_overhead_bar.py
    ```

    If you inspect the script, you will see that the workload names and data are there as follows. Each workload has four data entries, located in `exe_times_baseline`, `exe_times_bayes`, `exe_times_linux_perf`, and `exe_times_tintin`, which correspond to the four bars in the figure.


    ```python
    workloads = ['perlbench',     # -> 0
                 'gcc',          # -> 1
                 'mcf',          # -> 2
                 'omnetpp',      # -> 3
                 'xalancbmk',    # -> 4
    ...
    ``` 

    ```python
    exe_times_tintin = [85.480826,   # -> 0
                        67.164979,   # -> 1
                        382.30594,   # -> 2
    ...
    ``` 

2. Next, we generate the results. The process is similar to that of the previous figure, and we will repeat the steps. Any steps that differ from the previous ones will be marked in **BOLD**.


3. To generate the results for a single workload, you first need to configure the benchmark to use Tintin system calls.


    For SPEC 2017 benchmark:
    ```bash
    $ cd ~/cpu2017_instrument
    # Edit the configuration file
    $ vim config/tintin-gcc-linux-x86.cfg
    ```
    Locate the following compiler flags section and modify it to:
    - Disable PERF_SYSCALL (comment this line)
    - Enale TINTIN_SYSCALL (uncomment out this line)

    The final configuration should look like:
    ```makefile
    default=base:     # Base compilation flags
       OPTIMIZE       = -g -O3 -march=native -DTINTIN_SYSCALL   # <- Make sure this line is active
    # OPTIMIZE       =  -g -O3 -march=native  -DPERF_SYSCALL  # <- Ensure this line is commented
    ```

    For PARSEC 3.0:  

    ```bash
    $ cd ~/parsec_instrumented
    $ vim ./pkgs/libs/hooks/src/hooks.c
    ```
    Modify the macros as follows:
    ```c
    #define PERF_SYSCALL
    // #define TINTIN_SYSCALL
    ```  


4. Run the workload:

    ```bash
    $ cd cpu2017_instrumented
    $ ./bin/runcpu --config=tintin-gcc-linux-x86.cfg  --size=ref --rebuild  --action run 500
    ```

5. **Obtain the results**. Once the workload finishes running, it will generate a log file in `/tmp`.

    ```bash
    $ cat /tmp/tintin_cpu2017_spec_perlbench_500.log
    #  It will show the log like:
    ---------- 
    CPU time used: 86.375428 seconds
    ---------- 
    ```
6. Go to the script and **replace the original data with the generated data**.
    ```bash
    vim tintin-user/plots/figure-14_plot_overhead_bar.py
    ```

    The workload used in our experiments is **500.perlbench**, which corresponds to the following lines:

    ```python
    workloads = ['perlbench',     # -> 0
    ...

    exe_times_tintin =     [85.480826,   # -> 0
    ...
    # So lets replace the 85.480826 by 86.375428 
    ```
    The modifed version should like:
    ```python
    exe_times_tintin = [86.375428,      # -> 0
    ```

7. Now you have modified one data, you can replot the figure by:

    ```bash
    $ cd ~/tintin-user/plots
    $ python3 figure-14_plot_overhead_bar.py
    ```

8. To reproduce the results for all 26 workloads, we have prepared scripts to automate the process.

    ```bash
    $ cd ~/cpu2017_instrumented
    $ ./tintin_launch.sh
    ```

    Also for PARSEC benchmark:
    ```bash
    $ cd ~/parsec_instrumented
    $ ./tintin_launch.sh
    ```
    Once both scripts have finished running, log files will be generated in `/tmp/`. You may need to copy the relevant results from these log files into the plotting script.

9. So far, we have generated the results for Tintin. To generate the results for BayesPerf, we need to configure the kernel accordingly.

    ```bash
    $ echo 1 > /proc/sys/tintin/bayesperf_on
    ```
    Then, repeat steps 4, 5, and 6 (or step 8) to generate the results. The log files will still be located in `/tmp`.

10. So far, we have generated the results for Tintin and BayesPerf. To generate the results for the original benchmark, you need to **configure it so that no performance monitoring events are opened**.


    For SPEC 2017 benchmark:
    ```bash
    $ cd ~/cpu2017_instrument
    # Edit the configuration file
    $ vim config/tintin-gcc-linux-x86.cfg
    ```
    Locate the following compiler flags section and modify it to:
    - Disable PERF_SYSCALL (comment this line)
    - Disable TINTIN_SYSCALL (comment out this line)

    The final configuration should look like:
    ```makefile
    default=base:     # Base compilation flags
    #   OPTIMIZE       = -g -O3 -march=native -DTINTIN_SYSCALL   # <- Ensure this line is commented
    #   OPTIMIZE       = -g -O3 -march=native  -DPERF_SYSCALL    # <- Ensure this line is commented
    OPTIMIZE       = -g -O3 -march=native -DORIGINAL_BENCHMARK   # <- Make sure this line is active
    ```

    For PARSEC 3.0:  
    ```bash
    $ cd ~/parsec_instrumented
    $ vim ./pkgs/libs/hooks/src/hooks.c
    ```
    Modify the macros as follows:
    ```c
    #define ORIGINAL_BENCHMARK
    // #define PERF_SYSCALL
    // #define TINTIN_SYSCALL
    ```  

    Then you may need to repeat steps 4, 5, 6 (or 8) to generate the results. The log files are still in `/tmp`.

11. So far, we have generated the results for Tintin, BayesPerf and original benchmark. To generate the results for Linux Perf, you will need to modify the configuration and re-run the experiments. 
    ```bash
    # This disable Tintin scheduling in kernel
    $ echo 0 >  /proc/sys/tintin/tintin_sched_switch_on
    $ echo 0 >  /proc/sys/tintin/bayesperf_on
    ```

    Modify the system calls in SPEC 2017
    ```bash
    $ cd ~/cpu2017_instrument
    # Edit the configuration file
    $ vim config/tintin-gcc-linux-x86.cfg
    ```
    Locate the following compiler flags section and modify it to:
    - Enable PERF_SYSCALL (uncomment this line)
    - Disable TINTIN_SYSCALL (comment out this line)

    The final configuration should look like:
    ```makefile
    default=base:     # Base compilation flags
    # OPTIMIZE       =  -g -O3 -march=native -DTINTIN_SYSCALL    # <- Ensure this line is commented
      OPTIMIZE       = -g -O3 -march=native -DPERF_SYSCALL       # <- Make sure this line is active
    # OPTIMIZE       = -g -O3 -march=native -DORIGINAL_BENCHMARK # <- Ensure this line is commented
    ```

    Modify the system calls in PARSEC 3.0:  
    ```bash
    $ cd ~/parsec_instrumented
    $ vim ./pkgs/libs/hooks/src/hooks.c
    ```
    Modify the macros as follows  
    ```c
    #define PERF_SYSCALL
    // #define TINTIN_SYSCALL
    ```  

    Then you may need to repeat steps 4, 5, 6 (or 8) to generate the results. The log files are still in `/tmp`.


## Figure 15 - Scalability Analysis of Scheduling Hyperperiods (25 minutes of manual time + {0.1 - 1} hour of machine time)

Figure 15 consists of two subfigures, **15-a** and **15-b**, both of which we will reproduce in this section.  
We evaluate Tintin and Linux perf on the `505.mcf` workload from the SPEC 2017 benchmark, using various scheduling hyperperiods.

The scheduling hyperiod can be configured via the file `/proc/sys/tintin/tintin_sched_interval`: 

1. First, let's plot the two figures

    ```bash
    $ cd tintin-user/plots
    $ python3 figure-15-a_sched_hyperperiod.py 
    $ python3 figure-15-b_sched_hyperperiod.py
    ```
    
    If you open the script, you will see the data as follows:

    In `figure-15-a_sched_hyperperiod_accuracy.py`, the accuracies of Tintin and Linux perf are as follows:
    ```python
    labels = ["15ms", "10ms", "8ms", "6ms", "4ms", "2ms", "1ms"]
    tintin_acc = [1.016529, # -> 15ms
                  1.002772, # -> 10ms
                  1.03464,  # -> 8ms
    ```

    In `figure-15-b_sched_hyperperiod_overhead.py`, the execution times are as follows:
    ```python
    labels = ["15ms", "10ms", "8ms", "6ms", "4ms", "2ms", "1ms"]

    baseline_exe_time = 373.297467

    tintin_overhead = [384.085075,	# -> 15ms
                       385.160049,	# -> 10ms
    ```

2. Let's modify the scheduling hyperperiod and generate the results.

    ```bash
    # Ensure we are using Tintin's scheduler
    $ echo 1 > /proc/sys/tintin/tintin_sched_switch_on
    # Set the hyperperiod to 1 ms
    $ echo 1 > /proc/sys/tintin/tintin_sched_interval
    ```

    Also we need to make sure the workload benchmark is using Tintin system calls, in file `~/cpu2017_instrumented/config/tintin-gcc-linux-x86.cfg`.

    ```makefile
    default=base:     # Base compilation flags
    OPTIMIZE       =  -g -O3 -march=native -DTINTIN_SYSCALL  # <- Make sure this line is active
    #  OPTIMIZE       = -g -O3 -march=native -DPERF_SYSCALL   # <- Ensure this line is commented
    #  OPTIMIZE       = -g -O3 -march=native -DORIGINAL_BENCHMARK  # <- Ensure this line is commented
    ```

3. Then you can launch the workload by 

    ```bash
    $ cd cpu2017_instrumented/
    $ ./bin/runcpu --config=tintin-gcc-linux-x86.cfg  --size=ref --rebuild  --action run 505
    ```
4. After the workload completes, retrieve the error and execution time from the log file at `/tmp/tintin_cpu2017_spec_mcf_505.log`. You can then replace the original data in the plotting scripts with the newly generated results. 

5. We also provide a script that generates results for hyperperiods ranging from 1 ms to 15 ms. You can optionally run it by:

    ```bash
    $ cd cpu2017_instrumented/
    $ ./tintin_scalability_hyperperiod.sh
    ```

    All log files can be found in the `/tmp/` directory:

    ```bash
    -rw-rw-r--  1 cspl cspl    797 Apr 29 22:46 interval_10_ms.log
    -rw-rw-r--  1 cspl cspl    797 Apr 29 22:53 interval_15_ms.log
    -rw-rw-r--  1 cspl cspl    797 Apr 29 22:13 interval_1_ms.log
    -rw-rw-r--  1 cspl cspl    797 Apr 29 22:20 interval_2_ms.log
    -rw-rw-r--  1 cspl cspl    797 Apr 29 22:27 interval_4_ms.log
    -rw-rw-r--  1 cspl cspl    797 Apr 29 22:33 interval_6_ms.log
    ```


6. So far, we have results on Tintin on different scheduling hyperperiod. To generate the results of Linux perf

    ```bash
    # Diable Tintin's scheduler and switch to the Linux perf
    $ echo 0 > /proc/sys/tintin/tintin_sched_switch_on
    ```
    Also we need to make sure the workload benchmark is using Linux perf system calls, in file `~/cpu2017_instrumented/config/tintin-gcc-linux-x86.cfg`.

    ```makefile
    default=base:     # Base compilation flags
    # OPTIMIZE       =  -g -O3 -march=native -DTINTIN_SYSCALL  # <- Ensure this line is commented
      OPTIMIZE       = -g -O3 -march=native -DPERF_SYSCALL   # <- Make sure this line is active
    # OPTIMIZE       =  -g -O3 -march=native -DORIGINAL_BENCHMARK  # <- Ensure this line is commented
    ```

    Then, follow the instructions in the previous sections to run the benchmark workload, measure the errors, and calculate the runtime overhead.

    After that, please turn on Tintin' scheduler again for next experiments.

    ```bash
    # Enable Tintin's scheduler back
    $ echo 1 > /proc/sys/tintin/tintin_sched_switch_on
    ```

## Figure 16(a) - Scalability of Scheduling Quantum (10 minutes of manual time + 1 hours of machine time)
This figure shows how different scheduling quanta affect accuracy and performance. The scheduling quantum can be configured via `/proc/sys/tintin/tintin_sched_quantum`.


1. First, let's plot the figure:

    ```bash
    $ cd tintin-user/plots
    $ python3 figure-16-a_sched_quantum.py
    ```

    If you open the script, you’ll see the accuracy and overhead values for different scheduling quantums listed as follows:
    ```python
    tintin_exe_times = [
         371.036586,  # -> 4ms
         372.776459,  # -> 2ms
    ...
    tintin_acc = [
        7.362423,  # -> 4ms
        2.294223,  # -> 2ms
    ...
    ```

    Then we are going to generate the results.

2. Configure the scheduling quantum:

    ```bash
    $ cat /proc/sys/tintin/tintin_sched_quantum  
    400000  
    # The unit is nanoseconds (ns), meaning the scheduling quantum is 0.4 ms—one-tenth of the scheduling hyperperiod.
    ```  

    To configure it with a different value: 
    ```bash 
    $ echo 100000 > /proc/sys/tintin/tintin_sched_quantum  
    $ cat /proc/sys/tintin/tintin_sched_quantum  
    100000  
    # The scheduling quantum is now 100,000 ns (0.1 ms).
    ``` 

    Also we need to make sure the workload benchmark is using Tintin system calls, in file `~/cpu2017_instrumented/config/tintin-gcc-linux-x86.cfg`.

    ```makefile
    default=base:     # Base compilation flags
    OPTIMIZE       =  -g -O3 -march=native -DTINTIN_SYSCALL  # <- Make sure this line is active
    #  OPTIMIZE       = -g -O3 -march=native -DPERF_SYSCALL   # <- Ensure this line is commented
    #  OPTIMIZE       = -g -O3 -march=native -DORIGINAL_BENCHMARK  # <- Ensure this line is commented
    ```

3. Run the workload:

    ```bash
    $ cd cpu2017_instrumented/
    $ ./bin/runcpu --config=tintin-gcc-linux-x86.cfg  --size=ref --rebuild  --action run 505
    ```
4. After the workload finishes, get the errors and execution time in log file.

    ```bash
    ---------- 
    CPU time used: 442.036586 seconds
    ---------- 
    [Multiplexed] Cache misses:  17334969197 
    [Ground Truth] Cache misses: 17101968051 
    **Error** : 1.362423 % 
    ```

5. Go to the script and **replace the original data with the generated data**.
    ```bash
    vim ~/tintin-user/plots/figure-16-a_sched_quantum.py
    ```

    The workload used in our experiments is **0.1ms**, which corresponds to the following lines:

    ```python
    tintin_exe_times = [
    ...
                  441.389778,  # -> 0.1ms
    ...
    # So let's replace the  441.389778 by 442.036586
    ```
    The same for the accuracy:
    ```python
    tintin_acc = [
    ...
                  1.77174,   # -> 0.1ms
    # So let's replace the 1.77174 by 1.362423
    ``` 

6. Now you have modified one data entry, you can replot the figure by:

    ```bash
    $ cd ~/tintin-user/plots
    $ python3 figure-16-a_sched_quantum.py
    ```
 
7. Figure 16(a) presents results for scheduling quantum values ranging from **4ms to 0.05ms**. You can select any value within this range to verify the results.

 
## Figure 16(b) - Scalability of Event Numbers (10 minutes of manual time + 1 hours of machine time)

This figure shows how the number of events impacts on the accuracy of Tintin and Linux perf.


1. First, let's plot the figure 16(b) in the paper.

    ```bash
    $ cd tintin-user/plots
    $ python3 figure-16-b_num_events.py
    ```

    If you go the script you will find the data are there:
    ```python
    linux_perf_errors = [1.080109, # -> 8 events
                        4.314312,  # -> 16 events
                        16.585817, # -> 48 events
    ...

    tintin_errors = [0.042007,     # -> 8 events
                     0.192172,    # -> 16 events
                     0.87899,     # -> 48 events
    ...
    ```


2. Modify the number of events.

    We need to enable the macro in the code by:

    ```bash
    $ cd cpu2017_instrumented
    $ vim ./benchspec/CPU/505.mcf_r/src/mcf.c
    ```
    Find the following line and uncomment it.
    ```C
    #define SCALABILITY_EVAL // Make this is active
    ```

    We also have a code snippet that allows you to adjust the number of events.
    ```C
    #ifdef SCALABILITY_EVAL
       for (int j = 23; j < 514; j++)
       {
         fd[j] = tintin_event_open(&attr[3], 0, -1, -1, 0);
       }
    #endif
    ```

    In the above code snippet, 514 is the number of events to be measured. You can modify this value from 26 to 1026 (1024+2) to verify the results reported in the paper. PS: 1026 = (1024+2) because there are 2 events that are not opened successfully.

3. Run the workload and then get the results.

    ```bash
    $ cd cpu2017_instrumented/
    $ ./bin/runcpu --config=tintin-gcc-linux-x86.cfg  --size=ref --rebuild  --action run 505
    ```
    Wait for the workload to finish.

4. Go to the script and **replace the original data with the generated data**.
    ```bash
    vim ~/tintin-user/plots/figure-16-a_sched_quantum.py
    ```

    The workload used in our experiments is **512** events, which corresponds to the following lines:

    ```python
    tintin_errors = [
    ...
                  5.416915,    # -> 512
    # So let's replace the 5.416915 by the data you generated
    ``` 

5. Figure 16(b) presents results for the number of events ranging from **8 to 1024**. You can choose any value within this range to verify the results. Please note that configuring 1024 events for Tintin may cause the kernel to hang (panic). If this happens, please notify us so we can reboot the machine.


6. So far, we have generated the accuracy results for Tintin. To obtain the results for Linux perf, you need to configure both the kernel and the workload, then re-run the experiments.

    ```bash
    # Disable Tintin's scheduler back
    $ echo 0 > /proc/sys/tintin/tintin_sched_switch_on
    ```

    Also we need to make sure the workload benchmark is using Tintin system calls, in file `~/cpu2017_instrumented/config/tintin-gcc-linux-x86.cfg`.

    ```makefile
    default=base:     # Base compilation flags
    # OPTIMIZE       = -g -O3 -march=native -DTINTIN_SYSCALL      # <- Ensure this line is commented
      OPTIMIZE       = -g -O3 -march=native -DPERF_SYSCALL         # <- Make sure this line is active 
    # OPTIMIZE       = -g -O3 -march=native -DORIGINAL_BENCHMARK  # <- Ensure this line is commented
    ```

## Part II - Case Study

### Figure 10 - Case Study on Pond (15 minutes of manual time + 10 hours machine time)

1. First, let's plot the figure:

    ```bash
    $ cd tintin-user/plots
    $ python3 figure-10_pond_study.py
    ```

    If we open the scripts, we can see the data is loaded from the file `results.txt`.

    ```python
    with open("results.txt", "r") as f:
        for line in f:        
            seed = int(re.search(r'seed=([\-0-9.]+)', line).group(1))
            emon_value = float(re.search(r'emon=([\-0-9.]+)', line).group(1))
            emon_res.append(emon_value)
            rr_value = float(re.search(r'tintin_rr=([\-0-9.]+)', line).group(1))
            tintin_rr_res.append(rr_value)
    ```

2. To reproduce the results, please follow the instructions in `case-studies/Pond/README.md` to rerun the experiments. This will generate a `results.txt` file, which you can then move to this directory to replace the original. 


### Figure 11 - Case Study on DMon (5 minutes of manual time and machine time)

To reproduce the results, please follow the instructions in `case-studies/DMon/README.md`. This will generate the logs used in the paper (Figure 11).