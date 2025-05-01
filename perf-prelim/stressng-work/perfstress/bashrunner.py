import os

NUM_TRIALS = 100

def main():
    for i in range(NUM_TRIALS):
        os.system("./systemperf.sh " + str(i))

    for i in range(NUM_TRIALS):
        os.system("sudo perf_5.10 stat -e LLC-load-misses -x, -o ./results/task-wide/" + str(i) + " stress-ng --cpu 1 --quiet --cache-ops 300")

if __name__ == "__main__":
    main()