from pprint import pprint

from assignment_1.algorithms import *
from assignment_1.config import *
from assignment_1.maze import Maze


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

    maze = Maze(
        grid=GRID,
        reward_mapping=REWARD_MAPPING,
        starting_point=STARTING_POINT,
        discount_factor=0.95
    )

    result = value_iteration(maze, 1.4)

    print('number of iterations required:', result['num_iterations'])

    utilities, optimal_policy = result['utilities'], result['optimal_policy']

    print('utility and optimal action for each state (row, column)')
    for state_position in utilities:
        if state_position[1] == 0:
            print()

        print(
            'at', state_position, 
            '-utility:', '{:.3f}'.format(utilities[state_position]),
            '-optimal action:', optimal_policy[state_position],
        )


if __name__ == '__main__':
    solve_MDP()
