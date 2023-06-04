import random
import time
from heuristics import BaseHeuristic, AdvanceHeuristic
from priorities import f_priority, h_priority, fw_priority
from search import search
from topspin import TopSpinState
import pandas as pd

result = pd.DataFrame(columns=['method', "heuristic", "runtime", "path_length", "expansions"])
method_names = {
    "A*": f_priority,
    "WA*": fw_priority(w=0.5),
    "GBFS": h_priority
}
heuristic_names = {
    "basic": BaseHeuristic,
    "advanced": AdvanceHeuristic
}


def is_solvable(instance):
    """
     function to check if an instance is solvable based on the parity of inversions.
     The goal state has 0 inversions since it is sorted in an ascending order meaning that the parity is even.
     Therefore the instance given shold has a even parity as well to be considered solvable.
    :param instance: List of numbers
    :return: True - solvable, false - not solvable
    """
    # Count the number of inversions
    inversions = 0
    for i in range(len(instance) - 1):
        for j in range(i + 1, len(instance)):
            if instance[i] > instance[j]:
                inversions += 1

    # Check if the number of inversions has the same parity as the goal state
    return inversions % 2 == 0


def run_search(instance):
    global result
    start = TopSpinState(instance, 4)
    for algo_name, search_algo in method_names.items():
        for heuristic_name, heuristic in heuristic_names.items():
            print(f"Using: \n heuristic: {heuristic_name}\n  algorithm: {algo_name}\n on problem: {instance}")
            start_time = time.time()
            path, expansions = search(start, search_algo, heuristic(11, 4).get_h_value)
            end_time = time.time()

            runtime = end_time - start_time
            path_length = len(path) if path else 0
            result = pd.concat([result,
                                pd.DataFrame({
                                    "method": [algo_name],
                                    "heuristic": [heuristic_name],
                                    "runtime": [runtime],
                                    "path_length": [path_length],
                                    "expansions": [expansions]
                                })])
            print(f"Runtime for problem:{instance} is: {runtime}")


random.seed(42)  # Set a seed for reproducibility


# Run 50 random solvable instances
instances = []

# Create the list of 50 solvable instances.
while len(instances) < 50:
    instance = random.sample(range(1, 12), 11)
    if is_solvable(instance=instance):
        instances.append(instance)
    else:
        print(f"Instance: {instance} is not solvable")

for instance in instances:
    run_search(instance)
    print() # Blank line

report = result.groupby(by=["method", "heuristic"]).mean()
print(report)
report.to_csv('report.csv')
