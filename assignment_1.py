from pprint import pprint

from assignment_1.algorithms import value_iteration, policy_iteration
from assignment_1.config import *
from assignment_1.maze import Maze


def solve_MDP():
    maze = Maze(
        grid=GRID,
        reward_mapping=REWARD_MAPPING,
        starting_point=STARTING_POINT,
        discount_factor=DISCOUNT_FACTOR
    )

    # states = value_iteration(
    #     maze.states,
    #     maze.discount_factor,
    # )

    # for approximation of example results given in instructions
    states = value_iteration(
        maze.states,
        0.95,
        epsilon=0.08
    )

    print('utility and optimal action for each state (row, column)')
    for state_position in states:
        print(
            state_position, 
            'utility:', '{:.3f}'.format(states[state_position]['current_utility']),
            'optimal action:', states[state_position]['optimal_action'],
        )


if __name__ == '__main__':
    solve_MDP()
