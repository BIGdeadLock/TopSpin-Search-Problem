import heapq

# TODO: Delete tqdm
import time

from tqdm import tqdm

tq = tqdm()


def build_path(goal):
    """
    Get the goal state and build the path from the start state to the goal state
    :param goal: TopSpinState object
    :return: list of TopSpinState objects
    """
    print("#" * 10, "Building path", "#" * 10)
    path = []
    current = goal
    while current is not None:
        path.append(current)
        current = current.parent
    return path[::-1]

def search(start, priority_function, heuristic_function):
    """
    This function implements the A* search algorithm.
    :param start: The start state as an instance of the TopSpinState class
    :param priority_function: Given g and h, returns the priority of a state
    :param heuristic_function: Given a state, returns the heuristic value of the state
    :return:
    """
    print("#" * 10, "Starting BFS search", "#" * 10)
    # Create a priority queue to store states
    priority_queue = []
    # Create a set to track visited states
    visited = set()
    # Initialize the number of expansions
    expansions = 0

    # Push the start state to the priority queue with priority based on the priority function
    # The cost of the start state is 0
    heapq.heappush(priority_queue, (start.priority, start))

    # Start the search loop
    while priority_queue:
        # Pop the state with the highest priority from the priority queue
        _, current_state = heapq.heappop(priority_queue)

        # Check if the current state is the goal state
        if current_state.is_goal():
            return build_path(current_state), expansions

        # Check if the current state has been visited before
        if current_state in visited:
            continue

        tq.update(1)

        # Mark the current state as visited
        visited.add(current_state)

        # Increment the number of expansions
        expansions += 1

        # Generate all possible successor states
        successors = current_state.get_neighbors()

        # Add the successor states to the priority queue with priorities based on the priority function
        for successor, cost in successors:
            successor.priority = priority_function(current_state.priority + cost, heuristic_function(successor))
            heapq.heappush(priority_queue, (successor.priority, successor))

    # No path found
    return None, 0
