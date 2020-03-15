import copy
from pprint import pprint

from assignment_1.algorithms import *
from assignment_1.config import *
from assignment_1.maze import *


def solve_MDP():
    # default

    # maze = Maze(
    #     grid=GRID,
    #     reward_mapping=REWARD_MAPPING,
    #     starting_point=STARTING_POINT,
    #     discount_factor=DISCOUNT_FACTOR
    # )

    # result = value_iteration(maze)

    # for approximation of reference utilities given in instructions
    # values obtained through trial and error

    maze = Maze(
        grid=GRID,
        reward_mapping=REWARD_MAPPING,
        starting_point=STARTING_POINT,
        discount_factor=0.95
    )

    result = value_iteration(maze, 1.4)

    print(
        'result for value iteration using discount factor of',
        0.95, 'and maximum error threshold of', 1.4
    )
    print('number of iterations required:', result['num_iterations'])

    utilities, optimal_policy = result['utilities'], result['optimal_policy']

    optimal_policy_grid = copy.deepcopy(maze.grid)
    action_text_map = {
        MazeAction.MOVE_UP: '^',
        MazeAction.MOVE_DOWN: 'v',
        MazeAction.MOVE_LEFT: '<',
        MazeAction.MOVE_RIGHT: '>',
    }

    print('utility for each state (row, column)')
    for state_position in utilities:
        if state_position[1] == 0:
            print()

        print(
            'at', state_position, 
            '- utility:', '{:.3f}'.format(utilities[state_position]),
        )

        optimal_policy_grid[state_position[0]][state_position[1]] = \
            action_text_map[optimal_policy[state_position]]

    pprint(optimal_policy_grid)


if __name__ == '__main__':
    solve_MDP()
