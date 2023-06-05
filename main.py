import random
import time
from heuristics import BaseHeuristic, AdvanceHeuristic
from priorities import f_priority, h_priority, fw_priority
from search import search
from topspin import TopSpinState
import pandas as pd
from tqdm import trange

easy_problem = [1, 7, 10, 3, 6, 9, 5, 8, 2, 4, 11]  # easy instance
hard_problem = [1, 5, 11, 2, 6, 3, 9, 4, 10, 7, 8]  # hard instance

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


def random_walks(start_state: TopSpinState, number_of_potential_walks, number_of_instances_to_create=25) -> list:
    """
    To create a solvable solution, we will create random walks which will result in an instance which has a path to the goal.
    We will delete cycles if there any
    :param start_state: The start of the random walks
    :param number_of_potential_walks: integer: sample the path length from 0 to the value of the argument
    :param number_of_instances_to_create: how many instaces to create
    :return: list of np.array of solvable start states
    """
    problem_instances = []

    for _ in trange(number_of_instances_to_create, unit="instances"):
        permutation = start_state
        visited_states = {start_state}  # Will be used to prevent cycles
        number_of_walks = random.randint(1, number_of_potential_walks)

        for _ in range(number_of_walks):
            candidates = permutation.get_neighbors()
            action = random.randint(0, 2)  # Select an action at random
            next_permutation = candidates[action][0]
            if next_permutation in visited_states:
                # Cycle detected, choose a different action or backtrack
                continue
            permutation = next_permutation
            visited_states.add(permutation)

        # Add the final permutation to the list of instances
        problem_instances.append(permutation.state)

    return problem_instances


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
            result.to_csv("report.csv")


random.seed(42)  # Set a seed for reproducibility

# Run 50 random solvable instances
instances = []

# Create the list of 50 solvable instances.
print("Creating 50 solvable instances to solve")
instances += random_walks(TopSpinState(easy_problem, 4), number_of_potential_walks=1000)
instances += random_walks(TopSpinState(hard_problem, 4), number_of_potential_walks=1000)

for instance in instances:
    run_search(instance)
    print()  # Blank line

report = result.groupby(by=["method", "heuristic"]).mean()
print(report)
report.to_csv('report.csv')
