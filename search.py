import heapq

# TODO: Delete tqdm
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

import heapq

class OpenList:
    def __init__(self):
        self.items = {}
        self.heap = []
        self.counter = 0

    def insert(self, key, value):
        self.items[key] = (value, self.counter)
        heapq.heappush(self.heap, (value, self.counter, key))
        self.counter += 1

    def update(self, key, new_value):
        if key in self.items:
            old_value, counter = self.items[key]
            if new_value < old_value:
                self.items[key] = (new_value, counter)
                self._rebuild_heap()

    def get_min(self):
        if self.heap:
            min_value, _, min_key = self.heap[0]
            return min_key, min_value
        else:
            return None

    def _rebuild_heap(self):
        self.heap = [(value, counter, key) for value, counter, key in self.heap if key in self.items]

    def find(self, key):
        if key in self.items:
            value, _ = self.items[key]
            return value
        else:
            return None


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

    while priority_queue:
        # Pop the state with the highest priority from the priority queue
        _, current_state = heapq.heappop(priority_queue)

        if current_state.is_goal():
            return build_path(current_state), expansions

        # Check if the current state has been visited before
        if current_state in visited:
            continue

        # TODO: Delete
        tq.update(1)

        # Mark the current state as visited
        visited.add(current_state)

        expansions += 1

        # Generate all possible successor states
        successors = current_state.get_neighbors()

        # Add the successor states to the priority queue with priorities based on the priority function
        for successor, cost in successors:
            priority = priority_function(current_state.priority + cost, heuristic_function(successor))
            # TODO: Use a data structure with O(1) search of an item and O(1) to get the minimum
            # Check if the successor state is already in the open list
            # if it is, update it's priority based on the min from the current priority and the old priority
            old = list(filter(lambda x: x[1] == successor, priority_queue))
            if old:
                priority = min(priority, old[0][1].priority)
            successor.priority = priority

            heapq.heappush(priority_queue, (successor.priority, successor))

    # No path found
    return None, 0
