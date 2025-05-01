
This case study is adapted from the repository of the DMon OSDI'21 paper (https://github.com/efeslab/DMon-AE). It includes a complete end-to-end example demonstrating how selective profiling can be used to monitor in-production data locality issues.

## Set up

We need to compile Tintin's LLVM passes:

```bash
$ cd  llvm-passes
$ mkdir build
$ cd build
$ cmake ../DmonPass
$ make
```


- Linux running on an Intel Processor (perferrably Skylake)
- Linux perf
- [pmu-tools](https://github.com/andikleen/pmu-tools) that implements [Intel's Top-Down Microarchitecure Analysis Method](https://ieeexplore.ieee.org/document/6844459).
- LLVM


## Reproduce results in Tintin paper




### Origianl DMon profiling

```bash
$ cd ~/tintin-user/case-studies/DMon/test-case
$ ./dmon-run.sh
```

The above commands will generate profiling log files, producing results similar to those shown in Figure 11(a).

### Tintin Profiling

```bash
$ ./tintin-run.sh
```

The above commands will display logs directly in the terminal, similar to the output shown in Figure 11(b).