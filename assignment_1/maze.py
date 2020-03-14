from enum import Enum

from assignment_1.MDP import MarkovDecisionProcess


class MazeAction(Enum):
    MOVE_UP = enum.auto()
    MOVE_DOWN = enum.auto()
    MOVE_LEFT = enum.auto()
    MOVE_RIGHT = enum.auto()


class Maze(MarkovDecisionProcess):
    def __init__(self, grid, reward_mapping, starting_point, discount_factor):
        self.grid = grid
        self.reward_mapping = reward_mapping
        self.current_state = starting_point
        self.discount_factor

        self.width = len(grid)
        self.height = len(grid[0])

        possible_states = [
            { 'x': x, 'y': y }
            for x in range(self.width)
            for y in range(self.height)
            if self.grid[x][y] != 'w'
        ]

        possible_actions = [
            MazeAction.MOVE_UP,
            MazeAction.MOVE_DOWN,
            MazeAction.MOVE_LEFT,
            MazeAction.MOVE_RIGHT,
        ]

        super().__init__(possible_states, possible_actions)

    def transition_model(self, state, action, next_state) -> float:
        if action is MazeAction.MOVE_UP:
            if state['x'] == next_state['x'] and state['y'] == next_state['y'] - 1:
                return 0.8  # move up

            elif state['x'] == next_state['x'] - 1 and state['y'] == next_state['y']:
                return 0.1  # move left

            elif state['x'] == next_state['x'] + 1 and state['y'] == next_state['y']:
                return 0.1  # move right

            else:
                return 0

        elif action is MazeAction.MOVE_DOWN:
            if state['x'] == next_state['x'] and state['y'] == next_state['y'] + 1:
                return 0.8  # move down

            elif state['x'] == next_state['x'] - 1 and state['y'] == next_state['y']:
                return 0.1  # move left

            elif state['x'] == next_state['x'] + 1 and state['y'] == next_state['y']:
                return 0.1  # move right

            else:
                return 0

        elif action is MazeAction.MOVE_LEFT:
            if state['x'] == next_state['x'] - 1 and state['y'] == next_state['y']:
                return 0.8  # move left

            if state['x'] == next_state['x'] and state['y'] == next_state['y'] - 1:
                return 0.1  # move up

            if state['x'] == next_state['x'] and state['y'] == next_state['y'] + 1:
                return 0.1  # move down

            else:
                return 0

        else:  # action is MazeAction.MOVE_RIGHT
            if state['x'] == next_state['x'] + 1 and state['y'] == next_state['y']:
                return 0.8  # move right

            if state['x'] == next_state['x'] and state['y'] == next_state['y'] - 1:
                return 0.1  # move up

            if state['x'] == next_state['x'] and state['y'] == next_state['y'] + 1:
                return 0.1  # move down

            else:
                return 0

    def reward(self, state):
        square_colour = grid[state['x']][state['y']]
        return self.reward_mapping(square_colour)

    def get_next_squares(self, square, action: MazeAction):
        if action is MazeAction.MOVE_UP:  # up, left or right
            return self._get_next_action_valid_squares(
                square, 
                invalid_move_direction=MazeAction.MOVE_DOWN,
            )

        elif action is MazeAction.MOVE_DOWN:  # down, left or right
            return self._get_next_action_valid_squares(
                square, 
                invalid_move_direction=MazeAction.MOVE_UP,
            )

        elif action is MazeAction.MOVE_LEFT:  # left, up or down
            return self._get_next_action_valid_squares(
                square, 
                invalid_move_direction=MazeAction.MOVE_RIGHT,
            )

        else:  # action is MazeAction.MOVE_RIGHT - right, up or down
            return self._get_next_action_valid_squares(
                square, 
                invalid_move_direction=MazeAction.MOVE_LEFT,
            )


    def _get_next_action_valid_squares(
        self, 
        square, 
        invalid_move_direction: MazeAction,
    ):
        possible_squares = []

        if invalid_move_direction is not MazeAction.MOVE_UP:
            cannot_move_up = square['y'] == 0 or \
                self.grid[square['x']][square['y'] - 1] == 'w'

            if cannot_move_up:  # stay in the same spot
                possible_squares.append(square)

            else:  # can move to square above
                possible_squares.append({ 
                    'x': square['x'],
                    'y': square['y'] - 1,
                })

        if invalid_move_direction is not MazeAction.MOVE_DOWN:
            cannot_move_down = square['y'] == self.height - 1 or \
                self.grid[square['x']][square['y'] + 1] == 'w'

            if cannot_move_down:  # stay in the same spot
                possible_squares.append(square)

            else:  # can move to square below
                possible_squares.append({ 
                    'x': square['x'],
                    'y': square['y'] + 1,
                })

        if invalid_move_direction is not MazeAction.MOVE_LEFT:
            cannot_move_left = square['x'] == 0 or \
                self.grid[square['x'] - 1][square['y']] == 'w'

            if cannot_move_left:  # stay in the same spot
                possible_squares.append(square)

            else:  # can move to square to the left
                possible_squares.append({ 
                    'x': square['x'] - 1,
                    'y': square['y'],
                })

        if invalid_move_direction is not MazeAction.MOVE_RIGHT:
            cannot_move_right = square['x'] == self.width - 1 or \
                self.grid[square['x'] + 1][square['y']] == 'w'

            if cannot_move_right:  # stay in the same spot
                possible_squares.append(square)

            else:  # can move to square to the right
                possible_squares.append({ 
                    'x': square['x'] + 1,
                    'y': square['y'],
                })

        return possible_squares
