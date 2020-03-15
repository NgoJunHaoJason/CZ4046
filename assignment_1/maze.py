import enum

from assignment_1.MDP import MarkovDecisionProcess


class MazeAction(enum.Enum):
    MOVE_UP = enum.auto()
    MOVE_DOWN = enum.auto()
    MOVE_LEFT = enum.auto()
    MOVE_RIGHT = enum.auto()


class Maze(MarkovDecisionProcess):
    def __init__(self, grid, reward_mapping, starting_point, discount_factor):
        self.grid = grid
        self.reward_mapping = reward_mapping
        self.current_state = starting_point
        self.discount_factor = discount_factor

        self.width = len(grid)
        self.height = len(grid[0])

        possible_states = {
            (x, y): {
                'x': x,  # repetition of value makes it easier later
                'y': y,  # repetition of value makes it easier later
                'reward': self.reward_mapping[self.grid[x][y]],
                'current_utility': 0,
                'previous_utility': 0,
                'optimal_action': None,
            }

            for x in range(self.width)
            for y in range(self.height)
            if self.grid[x][y] != 'w'
        }

        possible_actions = [
            MazeAction.MOVE_UP,
            MazeAction.MOVE_DOWN,
            MazeAction.MOVE_LEFT,
            MazeAction.MOVE_RIGHT,
        ]

        super().__init__(possible_states, possible_actions)

        for state_position in self.states:
            self.states[state_position]['action_next_state_map'] = \
                self._form_action_next_state_map(state_position)

    def _form_action_next_state_map(self, state):
        """
        state (tuple): x, y position

        returns:
        a dictionary that maps each action to the next possible states,
        along with the probability of each next possible state occuring,
        for the given state
        """
        return {
            action: self._get_next_states(state, action)
            for action in self.actions
        }

    def _get_next_states(self, state, action: MazeAction):
        """
        state (tuple): x, y position
        action (MazeAction): action to take at the given state

        returns:
        ((0.8, intended_state), (0.1, unintended_state_1), (0.1, unintended_state_2))
        """
        if action is MazeAction.MOVE_UP:

            above_state = (state[0], state[1] - 1)
            if above_state not in self.states:
                above_state = state

            left_state = (state[0] - 1, state[1])
            if left_state not in self.states:
                left_state = state

            right_state = (state[0] + 1, state[1])
            if right_state not in self.states:
                right_state = state

            next_states = ((0.8, above_state), (0.1, left_state), (0.1, right_state))

        elif action is MazeAction.MOVE_DOWN:

            below_state = (state[0], state[1] + 1)
            if below_state not in self.states:
                below_state = state

            left_state = (state[0] - 1, state[1])
            if left_state not in self.states:
                left_state = state

            right_state = (state[0] + 1, state[1])
            if right_state not in self.states:
                right_state = state

            next_states = ((0.8, below_state), (0.1, left_state), (0.1, right_state))

        elif action is MazeAction.MOVE_LEFT:

            left_state = (state[0] - 1, state[1])
            if left_state not in self.states:
                left_state = state

            above_state = (state[0], state[1] - 1)
            if above_state not in self.states:
                above_state = state

            below_state = (state[0], state[1] + 1)
            if below_state not in self.states:
                below_state = state

            next_states = ((0.8, left_state), (0.1, above_state), (0.1, below_state))

        else:  # action is MazeAction.MOVE_RIGHT

            right_state = (state[0] - 1, state[1])
            if right_state not in self.states:
                right_state = state

            above_state = (state[0], state[1] - 1)
            if above_state not in self.states:
                above_state = state

            below_state = (state[0], state[1] + 1)
            if below_state not in self.states:
                below_state = state

            next_states = ((0.8, right_state), (0.1, above_state), (0.1, below_state))

        return next_states

    def transition_model(self, state, action, next_state) -> float:
        """
        state (tuple): x, y position
        action (MazeAction): action to take at the given state
        next_state (tuple): x, y position

        return:
        probability which ranges from 0 to 1, inclusive (float)
        """
        action_next_state_map = self.states[state]['action_next_state_map']
        possible_next_states = action_next_state_map[action]

        for probability, possible_next_state in possible_next_states:
            if next_state == possible_next_state:
                return probability
        
        return 0

    def reward(self, state):
        """
        state (tuple): x, y position
        """
        colour = grid[state[0]][state[1]]
        return self.reward_mapping[colour]
