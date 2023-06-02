import numpy as np

class TopSpinState:

    def __init__(self, state, k=4, priority=0, parent=None):
        self.state = np.array(state)
        self.k = k
        self.priority = priority
        self.parent = parent

    def __lt__(self, other):
        return self.priority < other.priority

    def __gt__(self, other):
        return self.priority > other.priority

    def __str__(self):
        return str(self.state)

    def __hash__(self):
        return hash(str(self.state))

    def __eq__(self, other):
        return np.array_equal(self.state, other.state)

    def is_goal(self):
        goal_state = np.arange(1, len(self.state) + 1)
        return np.array_equal(self.state, goal_state)

    def get_state_as_list(self):
        return self.state.tolist()

    def get_neighbors(self):
        neighbors = []

        # Move tiles clockwise
        clockwise_state = np.roll(self.state, -1)
        neighbors.append((TopSpinState(clockwise_state, self.k, parent=self), 1))

        # Move tiles counterclockwise
        counterclockwise_state = np.roll(self.state, 1)
        neighbors.append((TopSpinState(counterclockwise_state, self.k, parent=self), 1))

        # Reverse the order of the first k elements
        reverse_state = np.copy(self.state)
        reverse_state[:self.k] = np.flip(reverse_state[:self.k])
        neighbors.append((TopSpinState(reverse_state, self.k, parent=self), 1))

        return neighbors
