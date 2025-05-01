from collections import OrderedDict
import random
from collections.abc import Sequence
from sklearn.ensemble import RandomForestRegressor
import numpy as np
import math
from pathlib import Path
from counts_parser import parse_emon_counts, parse_time_file, parse_tintin_counts
from sklearn.utils import shuffle
from counters import emon_events, tintin_events
from workload import Workload, WorkloadRun, WorkloadType, CountReading, calculate_slowdown
from count_transformer import cumulative_data_to_individual

def set_seed(seed: int) -> None:
    np.random.seed(seed)
    random.seed(seed)

def read_emon_data() -> dict[str, Workload]:
    emon_counter_data_path = Path("counter_data/emon")
    emon_counter_data: dict[str, Workload] = {}

    for workload_path in emon_counter_data_path.iterdir():
        if not workload_path.is_dir():
            continue
        
        workload = Workload(name=workload_path.name, runs=dict())
        l0_time = parse_time_file(workload_path.joinpath("L0-1.time"))
        l0_metrics = parse_emon_counts(workload_path.joinpath("L0-1-emon.dat"), emon_events)
        workload.runs[WorkloadType.L0] = WorkloadRun(WorkloadType.L0, l0_time, l0_metrics)
        l100_time = parse_time_file(workload_path.joinpath("L100-1.time"))
        #We don't use L100 metrics for anything. Skip loading to make it faster
        #l100_metrics = parse_emon_counts(workload_path.joinpath("L100-1-emon.dat"), emon_events)
        l100_metrics = OrderedDict()
        workload.runs[WorkloadType.L100] = WorkloadRun(WorkloadType.L100, l100_time, l100_metrics)
        emon_counter_data[workload_path.name] = workload
    return emon_counter_data

def read_tintin_data(folder: str) -> dict[str, Workload]:
    tintin_counter_data_path = Path("counter_data") / folder
    tintin_counter_data: dict[str, Workload] = {}

    for workload_path in tintin_counter_data_path.iterdir():
        if not workload_path.is_dir():
            continue
        
        workload = Workload(name=workload_path.name, runs=dict())
        l0_time = parse_time_file(workload_path.joinpath("L0-1.time"))
        l0_metrics = parse_tintin_counts(workload_path.joinpath("L0-1-tintin.dat"), tintin_events)
        workload.runs[WorkloadType.L0] = WorkloadRun(WorkloadType.L0, l0_time, l0_metrics)
        l100_time = parse_time_file(workload_path.joinpath("L100-1.time"))
        #We don't use L100 metrics for anything. Skip loading to make it faster        
        #l100_metrics = parse_tintin_counts(workload_path.joinpath("L100-1-tintin.dat"), tintin_events)
        l100_metrics = OrderedDict()
        workload.runs[WorkloadType.L100] = WorkloadRun(WorkloadType.L100, l100_time, l100_metrics)
        tintin_counter_data[workload_path.name] = workload
    return tintin_counter_data

def sample_test_workloads(workloads: list[str], test_size: float) -> list[str]:
    num_test_workloads = int(len(workloads) * test_size)
    return random.sample(workloads, k=num_test_workloads)

#nrmse = normalized root mean square error
def calculate_nrmse(readings: Sequence[CountReading]):
    s = [(reading.uncertainty/reading.count) ** 2 for reading in readings if reading.count != 0 and reading.uncertainty != 0]
    if not s:
        return 1
    return math.sqrt(sum(s))

'''
Splits counter data for multiple workloads into training and test datasets, as well as an NRMSE training set. 

HOW IS THE DATA ARRANGED?

Say we have n workloads, m events being measured, and k_i measurements for 1 <= i <= n. We have distinct k's because
each workload has a different running time, so each workload generates a distinct number of measurements. A
measurement is a vector of size m containing a value for each event.

The X datasets consist of measurement vectors. The Y dataset consist of scalars corresponding to the 
slowdown that the workload experienced. For example, if row 13 in the X dataset corresponds to 37th measurement for 
workload A. Then, item 37 in the Y dataset will be the slowdown of workload A.

The dimensions of the X dataset are (sum of k_i, m). The Y dataset will have dimension (sum of k_i). 
Values in the Y dataset will be repeated many times, as a workload has one unique slowdown but thousands of measurements. 
Datasets are shuffled, so row 13 might correspond to workload A, row 14 to workload B, row 15 to workload A, etc.

Splitting datasets: ALL the k_i measurements for a workload will either be in the training dataset, or the test dataset, 
but never both. This is to avoid overfitting. If the model is trained and tested on the same workload, it learns to 
fingerprint workloads instead of learning about the problem domain. 
These custom splitting requirements are what prevents us from using one of sklearn's built-in splitting functions

NRMSE: An NRMSE scalar value is obtained from a measurement vector. We return an NRMSE value for every measurement vector
in the training dataset. These values can then be used to inform the model's training.
'''
def arrange_data_concatenate_measurements(counter_data: dict[str, Workload], test_workloads: list[str]) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    X_train, Y_train, X_test, Y_test, NRMSE_train = [], [], [], [], []
    for name, workload in counter_data.items():
        if name in test_workloads:
            X, Y = X_test, Y_test
        else:
            X, Y = X_train, Y_train

        slowdown = calculate_slowdown(workload.runs[WorkloadType.L100], workload.runs[WorkloadType.L0])
        metrics = list(zip(*workload.runs[WorkloadType.L0].counts.values()))
        for readings in metrics:
            if name not in test_workloads:
                NRMSE_train.append(calculate_nrmse(readings))
            counts = list(map(lambda reading: reading.count, readings))
            X.append(counts)
            Y.append(slowdown)

    X_train, X_test, Y_train, Y_test, NRMSE_train = np.asarray(X_train), np.asarray(X_test), np.asarray(Y_train), np.asarray(Y_test), np.asarray(NRMSE_train)
    X_train, Y_train = shuffle(X_train, Y_train)
    X_test, Y_test = shuffle(X_test, Y_test)
    return X_train, X_test, Y_train, Y_test, NRMSE_train



# Reading data is really slow. Comment out what datasets you don't need. This could be parallelized for a speedup.
emon_counter_data = read_emon_data()
'''
Tintin measures cumulative event counts, whereas emon measures counts between measurements. We convert Tintin's data
to Emon's format as this format is more amenable to the analysis we perform.
'''
tintin_rr_data = {name:cumulative_data_to_individual(workload) for name, workload in read_tintin_data("rr_uncertainty").items()}
tintin_elastic_data = {name:cumulative_data_to_individual(workload) for name, workload in read_tintin_data("elastic_uncertainty").items()}
tintin_elastic_weights_data = {name:cumulative_data_to_individual(workload) for name, workload in read_tintin_data("elastic_weights").items()}

if not (emon_counter_data.keys() == tintin_rr_data.keys() == tintin_elastic_data.keys() == tintin_elastic_weights_data.keys()):
    raise RuntimeError("Expected all datasets to have the same workloads")

workloads = list(emon_counter_data.keys()) 
for seed in range(200):
    set_seed(seed)
    test_workloads = sample_test_workloads(workloads, test_size=0.3)

    emon_regressor = RandomForestRegressor(n_estimators=50, random_state=seed, n_jobs=6)
    tintin_rr_regressor = RandomForestRegressor(n_estimators=50, random_state=seed, n_jobs=4)
    tintin_rr_regressor_nrmse = RandomForestRegressor(n_estimators=50, random_state=seed, n_jobs=4)
    tintin_elastic_regressor = RandomForestRegressor(n_estimators=50, random_state=seed, n_jobs=4)
    tintin_elastic_weights_regressor = RandomForestRegressor(n_estimators=50, random_state=seed, n_jobs=4)
    
    X_train_emon, X_test_emon, Y_train_emon, Y_test_emon, _ = arrange_data_concatenate_measurements(emon_counter_data, test_workloads)
    X_train_rr, X_test_rr, Y_train_rr, Y_test_rr, NRMSE_train = arrange_data_concatenate_measurements(tintin_rr_data, test_workloads)
    X_train_elastic, X_test_elastic, Y_train_elastic, Y_test_elastic, _ = arrange_data_concatenate_measurements(tintin_elastic_data, test_workloads)
    X_train_weights, X_test_weights, Y_train_weights, Y_test_weights, _ = arrange_data_concatenate_measurements(tintin_elastic_weights_data, test_workloads)

    emon_regressor.fit(X_train_emon, Y_train_emon)
    tintin_rr_regressor.fit(X_train_rr, Y_train_rr)
    tintin_elastic_regressor.fit(X_train_elastic, Y_train_elastic)
    tintin_elastic_weights_regressor.fit(X_train_weights, Y_train_weights)
    tintin_rr_regressor_nrmse.fit(X_train_rr, Y_train_rr, sample_weight=list(map(lambda NRMSE: 1/NRMSE, NRMSE_train)))

    emon_score = emon_regressor.score(X_test_emon, Y_test_emon)
    tintin_rr_score = tintin_rr_regressor.score(X_test_rr, Y_test_rr)
    tintin_rr_nrmse_score = tintin_rr_regressor_nrmse.score(X_test_rr, Y_test_rr)
    tintin_elastic_score = tintin_elastic_regressor.score(X_test_elastic, Y_test_elastic)
    tintin_weights_score = tintin_elastic_weights_regressor.score(X_test_weights, Y_test_weights)

    # print(f"workloads={test_workloads} elastic={tintin_elastic_score} weights={tintin_weights_score} rr={tintin_rr_score} rr_nrmse={tintin_rr_nrmse_score}")
    with open("results.txt", "a") as results_file:
        results_file.write(f"seed={seed} elastic={tintin_elastic_score} weights={tintin_weights_score} rr={tintin_rr_score} rr_nrmse={tintin_rr_nrmse_score}\n")