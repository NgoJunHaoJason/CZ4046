"""
Implementation of a maze environment,
which is also a Markov decision process.
"""
import enum

from assignment_1.base import MarkovDecisionProcess


class MazeAction(enum.Enum):
    MOVE_UP = enum.auto()
    MOVE_DOWN = enum.auto()
    MOVE_LEFT = enum.auto()
    MOVE_RIGHT = enum.auto()


class Maze(MarkovDecisionProcess):
    """
    Maze is a 2D array where squares of different colour have different rewards.

    colours / types of squares:
    - ' ': white
    - 'g': green
    - 'b': brown
    - 'w': wall (obstacle; no accessible)
    """
    # order matters
    def __init__(self, grid, reward_mapping, starting_point, discount_factor):
        """
        Initialises:
        - states: {
            (x, y): {
                action_1 (MazeAction): {
                    next_state_1 (tuple): probability,
                    ...,
                    next_state_k (tuple): probability,
                },
                ...,
                action_n: {
                    next_state_1 (tuple): probability,
                    ...,
                    next_state_k (tuple): probability,
                },
            }
        }
        - actions: list of MazeAction
        - discount (for future states): float
        """
        self.grid = grid
        self.reward_mapping = reward_mapping
        self.starting_point = starting_point  # not used for this assignment

        self.width = len(grid)
        self.height = len(grid[0])

        possible_states = {
            (x, y): {}
            for x in range(self.width)
            for y in range(self.height)
            if grid[x][y] != 'w'
        }

        possible_actions = [
            MazeAction.MOVE_UP,
            MazeAction.MOVE_DOWN,
            MazeAction.MOVE_LEFT,
            MazeAction.MOVE_RIGHT,
        ]

        super().__init__(possible_states, possible_actions, discount_factor)

        for state_position in possible_states:
            possible_states[state_position] = \
                self._form_action_next_state_map(state_position, possible_actions)

    def transition_model(self, state, action, next_state) -> float:
        """
        params
        - state (tuple): x, y position
        - action (MazeAction): action to take at the given state
        - next_state (tuple): intended x, y position (may be invalid)

        return:
        probability which ranges from 0 to 1, inclusive (float)
        """
        # if state and action not present, should throw and error
        next_state_probability_map = self.states[state][action]           
        return next_state_probability_map.get(next_state, 0)['probability']

    def reward_function(self, state):
        """
        params:
        - state (tuple): x, y position

        return: reward value (float)
        """
        colour = self.grid[state[0]][state[1]]
        return self.reward_mapping[colour]

    # helper function - to be called during instantiation
    def _form_action_next_state_map(self, state, actions):
        """
        params:
        - state (tuple): x, y position
        - actions (list): possible actions to take at the state given

        return: {
            MazeAction.MOVE_UP: {
                intended_next_state (tuple): {
                    'actual': actual_next_state (tuple),
                    'probability': 0.8 (float)
                },
                unintended_next_state_1 (tuple): {
                    'actual': actual_next_state (tuple),
                    'probability': 0.1 (float)
                },
                unintended_next_state_2 (tuple): {
                    'actual': actual_next_state (tuple),
                    'probability': 0.1 (float)
                },
            }
            MazeAction.MOVE_DOWN: { ...like in MazeAction.MOVE_UP... },
            MazeAction.MOVE_LEFT: { ...like in MazeAction.MOVE_UP... },
            MazeAction.MOVE_RIGHT: { ...like in MazeAction.MOVE_UP... },
        }
        """
        return {
            action: self._get_next_states(state, action)
            for action in actions
        }

    # helper function - to be called during instantiation
    def _get_next_states(self, state, action: MazeAction):
        """
        params:
        - state (tuple): x, y position
        - action (MazeAction): action to take at the given state

        return: {
            intended_next_state (tuple): {
                'actual': actual_next_state (tuple),
                'probability': 0.8 (float)
            },
            unintended_next_state_1 (tuple): {
                'actual': actual_next_state (tuple),
                'probability': 0.1 (float)
            },
            unintended_next_state_2 (tuple): {
                'actual': actual_next_state (tuple),
                'probability': 0.1 (float)
            },
        }
        """
        if action is MazeAction.MOVE_UP:

            above_state = (state[0], state[1] - 1)

            if above_state in self.states:
                actual_above_state = above_state 
            else:
                actual_above_state = state  # invalid state -> remain same spot

            left_state = (state[0] - 1, state[1])

            if left_state in self.states:
                actual_left_state = left_state 
            else:
                actual_left_state = state  # invalid state -> remain same spot

            right_state = (state[0] + 1, state[1])

            if right_state in self.states:
                actual_right_state = right_state 
            else:
                actual_right_state = state  # invalid state -> remain same spot

            next_states = { 
                above_state: {
                    'actual': actual_above_state,
                    'probability': 0.8,
                }, 
                left_state: {
                    'actual': actual_left_state,
                    'probability': 0.1,
                }, 
                right_state: {
                    'actual': actual_right_state,
                    'probability': 0.1,
                }, 
            }

        elif action is MazeAction.MOVE_DOWN:

            below_state = (state[0], state[1] + 1)
            
            if below_state in self.states:
                actual_below_state = below_state 
            else:
                actual_below_state = state  # invalid state -> remain same spot

            left_state = (state[0] - 1, state[1])
            
            if left_state in self.states:
                actual_left_state = left_state 
            else:
                actual_left_state = state  # invalid state -> remain same spot

            right_state = (state[0] + 1, state[1])

            if right_state in self.states:
                actual_right_state = right_state 
            else:
                actual_right_state = state  # invalid state -> remain same spot

            next_states = {
                below_state: {
                    'actual': actual_below_state,
                    'probability': 0.8,
                }, 
                left_state: {
                    'actual': actual_left_state,
                    'probability': 0.1,
                }, 
                right_state: {
                    'actual': actual_right_state,
                    'probability': 0.1,
                },
            }

        elif action is MazeAction.MOVE_LEFT:

            left_state = (state[0] - 1, state[1])
            
            if left_state in self.states:
                actual_left_state = left_state 
            else:
                actual_left_state = state  # invalid state -> remain same spot

            above_state = (state[0], state[1] - 1)

            if above_state in self.states:
                actual_above_state = above_state 
            else:
                actual_above_state = state  # invalid state -> remain same spot

            below_state = (state[0], state[1] + 1)

            if below_state in self.states:
                actual_below_state = below_state 
            else:
                actual_below_state = state  # invalid state -> remain same spot

            next_states = {
                left_state: {
                    'actual': actual_left_state,
                    'probability': 0.8,
                },
                above_state: {
                    'actual': actual_above_state,
                    'probability': 0.1,
                }, 
                below_state: {
                    'actual': actual_below_state,
                    'probability': 0.1,
                }, 
            }

        else:  # action is MazeAction.MOVE_RIGHT

            right_state = (state[0] + 1, state[1])

            if right_state in self.states:
                actual_right_state = right_state 
            else:
                actual_right_state = state  # invalid state -> remain same spot

            above_state = (state[0], state[1] - 1)

            if above_state in self.states:
                actual_above_state = above_state 
            else:
                actual_above_state = state  # invalid state -> remain same spot

            below_state = (state[0], state[1] + 1)

            if below_state in self.states:
                actual_below_state = below_state 
            else:
                actual_below_state = state  # invalid state -> remain same spot

            next_states = {
                right_state: {
                    'actual': actual_right_state,
                    'probability': 0.8,
                },
                above_state: {
                    'actual': actual_above_state,
                    'probability': 0.1,
                }, 
                below_state: {
                    'actual': actual_below_state,
                    'probability': 0.1,
                },
            }

        return next_states
