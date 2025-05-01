import re

count = 0
rr_better_than_emon = 0
elastic_better_than_rr = 0
diff = 0
# with open("merged.txt", "r") as f:
with open("results.txt", "r") as f:
    for line in f:
        count += 1
        seed = int(re.search(r'seed=([\-0-9.]+)', line).group(1))
        emon_value = float(re.search(r'emon=([\-0-9.]+)', line).group(1))
        rr_value = float(re.search(r'tintin_rr=([\-0-9.]+)', line).group(1))
        elastic_value = float(re.search(r'elastic_score=([\-0-9.]+)', line).group(1))
        nrmse_elastic_value = float(re.search(r'nrmse_elastic=([\-0-9.]+)', line).group(1))
        nrmse_rr_value = float(re.search(r'rr_nrmse=([\-0-9.]+)', line).group(1))
        elastic_weights = float(re.search(r'elastic_weights=([\-0-9.]+)', line).group(1))
        diff += elastic_value - emon_value
        if elastic_value >= emon_value:
            elastic_better_than_rr += 1

print(elastic_better_than_rr, count, diff/count)