<h1>AccPerf Preliminary Experiments Source Code</h1>

<h2><code>perfspec.py</code></h2>

This script invokes perf tool repeatedly on combinations of events and SPEC CPU2017 workloads.

<h3>Script Invocation:</h3>
<code>python3 perfspec.py -e <event-input-file> -w <workload-input-file> [options]</code>

NOTE: Event of interest should be the first event in event-input-file if --simple is turned on.



<h2><code>perflist.py</code></h2>

This script generates a formatted list of perf events using the user's system's perf list command to ensure compatability.

<h3>Script Invocation:</h3>
<code>python3 perflist.py</code>


``[-p, --perfversion]``
Option to specify perf version to invoke. Intended for embedded users. Default: "perf"

``-o, --output``
Output file location.





<h2>SPEC CPU 2017 instrumentation notes</h2>
cpu2017/benchspec/CPU/502.gcc_r/src/toplev.c is instrumented with <code>perf_event_open()</code> calls
