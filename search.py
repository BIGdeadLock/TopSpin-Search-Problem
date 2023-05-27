import heapq

# TODO: Delete tqdm
from tqdm import tqdm


def search(start, priority_function, heuristic_function):
    """
    This function implements the A* search algorithm.
    :param start: The start state as an instance of the TopSpinState class
    :param priority_function: Given g and h, returns the priority of a state
    :param heuristic_function: Given a state, returns the heuristic value of the state
    :return:
    """
    tq = tqdm()
    # Create a priority queue to store states
    priority_queue = []
    # Create a set to track visited states
    visited = set()
    # Initialize the number of expansions
    expansions = 0

    # Push the start state to the priority queue with priority based on the priority function
    heapq.heappush(priority_queue, (priority_function(start, heuristic_function(start)), [start]))

    # Start the search loop
    while priority_queue:
        # Pop the state with the highest priority from the priority queue
        _, path = heapq.heappop(priority_queue)
        current_state = path[-1]

        tq.update(1)

        # Check if the current state is the goal state
        if current_state.is_goal_state():
            return path, expansions

        # Check if the current state has been visited before
        if current_state in visited:
            continue

        # Mark the current state as visited
        visited.add(current_state)

        # Increment the number of expansions
        expansions += 1

        # Generate all possible successor states
        successors = current_state.generate_successors()

        # Add the successor states to the priority queue with priorities based on the priority function
        for successor in successors:
            successor_path = path + [successor]
            heapq.heappush(priority_queue,
                           (priority_function(successor, heuristic_function(successor)),
                            successor_path))

    # No path found
    return None, 0
