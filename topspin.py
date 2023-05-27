import numpy as np

class TopSpinState:

    def __init__(self, state, k=4):
        self.state = np.array(state)
        self.k = k

    def is_goal(self):
        goal_state = np.arange(1, len(self.state) + 1)
        return np.array_equal(self.state, goal_state)

    def get_state_as_list(self):
        return self.state.tolist()

    def get_neighbors(self):
        neighbors = []

        # Move tiles clockwise
        clockwise_state = np.roll(self.state, -1)
        neighbors.append((TopSpinState(clockwise_state, self.k), 1))

        # Move tiles counterclockwise
        counterclockwise_state = np.roll(self.state, 1)
        neighbors.append((TopSpinState(counterclockwise_state, self.k), 1))

        # Shift tiles k positions to the left
        shifted_state = np.roll(self.state, -self.k)
        neighbors.append((TopSpinState(shifted_state, self.k), 2))

        # Shift tiles k positions to the right
        shifted_state = np.roll(self.state, self.k)
        neighbors.append((TopSpinState(shifted_state, self.k), 2))

        return neighbors
