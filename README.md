# Tintin: A Performance Monitoring System to Uncover and Manage Uncertainty

Tintin’s implementation is primarily built on top of the Linux perf subsystem. The source code is available at: https://github.com/WUSTL-CSPL/tintin-kernel

This repository contains user-space libraries, tools, and scripts to help users utilize or reproduce Tintin's functionality.

## Code structure

The main files of `tintin-user` and `tintin-kernel` are listed below, with key functions documented in the source code.


**Tintin-kernel**:

```
...
├── arch/
    ├── x86/
        ├── events/
            ├── core.c # Modified for Tintin on x86 CPU arch
├── include/
├── kernel/
    ...
    ├── trace/
    ├── sched/
    ├── events/
    │   ├── tintin_vector.c
    │   ├── tintin_utils.h
    │   ├── tintin_utils.c
    │   ├── tintin_uncertainty.h
    │   ├── tintin_uncertainty.c
    │   ├── tintin_sched_event_handler.c
    │   ├── tintin_profiling_context.h
    │   ├── tintin_profiling_context.c
    │   ├── tintin_interface.h
    │   ├── tintin_interface.c
    │   ├── tintin_hopcroft-karp.h
    │   ├── tintin_hopcroft-karp.c
    │   ├── tintin_estimation.h
    │   ├── tintin_estimation.c
    │   ├── tintin_elastic.h
    │   ├── tintin_elastic.c
    │   ├── core.c  # The main file of the original Linux perf subsystem

```

**Tintin-user**:

```
├── include/      # Header files
├── llvm-passes/  # Compiler passes
├── plots/        # Plotting scripts for the evaluation results in the paper
├── README.md
├── REPRODUCE.md  # Instructions to reproduce the results in the paper
├── tests/        # Some toy program that test Tintin's syscalls in userspace
├── case-studies/ # Case study I and II in the paper

```


## How to reproduce results in OSDI'25 Tintin Paper

To reproduce the paper results, see :point_right: [`REPRODUCE.md`](./REPRODUCE.md).


## Set up


#### Pre-requiresite packages


```
pip install seaborn
```


#### Disable NMI watchdog (Optional)

By default, the Linux system uses one hardware performance counter (HPC) for the NMI watchdog. You can disable it to free up more HPCs for your experiments.

To check and disable the `nmi_watchdog`:

```bash
# Check if NMI watchdog is enabled
cat /proc/sys/kernel/nmi_watchdog

# Disable it by editing the GRUB configuration
sudo nano /etc/default/grub
# Find the line starting with GRUB_CMDLINE_LINUX_DEFAULT and modify it as follows:
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash nmi_watchdog=0"

# Update GRUB to apply the changes
sudo update-grub
```


## Resources

Event code reference on Intel CPU: https://perfmon-events.intel.com/