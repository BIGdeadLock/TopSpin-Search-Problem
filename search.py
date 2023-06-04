import heapq

from topspin import TopSpinState


def build_path(goal: TopSpinState):
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


class OpenList:
    def __init__(self):
        self.items = {}
        self.heap = []

    def insert(self, state: TopSpinState, priority: int):
        key = str(state)  # Use the string representation of the state as a dict key
        self.items[key] = [priority, state]
        heapq.heappush(self.heap, self.items[key])

    def is_in_queue(self, state: TopSpinState):
        return str(state) in self.items

    def update(self, state: TopSpinState, new_priority: int):
        key = str(state)
        if key in self.items:
            item = self.items[key]  # position 0 is the priority and index 1 is the state
            if new_priority < item[0]:
                print(f"Update: {state}, old: {item[0]}, new: {new_priority}")
                item[0] = new_priority
                item[1].priority = new_priority
                # Sort the heap again
                heapq.heapify(self.heap)

    def pop_min(self):
        if self.heap:
            priority, state = heapq.heappop(self.heap)
            return priority, state
        else:
            return None, None


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
    priority_queue = OpenList()
    # Create a set to track visited states
    visited = set()
    # Initialize the number of expansions
    expansions = 0

    # Push the start state to the priority queue with priority based on the priority function
    # The cost of the start state is 0
    priority_queue.insert(start, start.priority)

    while priority_queue:
        # Pop the state with the highest priority from the priority queue
        _, current_state = priority_queue.pop_min()  # heapq.heappop(priority_queue)

        if current_state.is_goal():
            return build_path(current_state), expansions

        # Check if the current state has been visited before
        if current_state in visited:
            continue
        # Mark the current state as visited
        visited.add(current_state)

        expansions += 1
        # Generate all possible successor states
        successors = current_state.get_neighbors()

        # Add the successor states to the priority queue with priorities based on the priority function
        for successor, cost in successors:
            priority = priority_function(current_state.priority + cost, heuristic_function(successor))
            successor.priority = priority
            if priority_queue.is_in_queue(successor):
                priority_queue.update(successor, priority)
            else:
                priority_queue.insert(successor, priority)

    # No path found
    return None, 0
