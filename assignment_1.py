import copy
from pprint import pprint

from assignment_1.algorithms import *
from assignment_1.config import *
from assignment_1.maze import *
from assignment_1.plot import *


def solve_MDP():
    """
    Main function.
    """
    # value iteration
    maze = Maze(
        grid=GRID,
        reward_mapping=REWARD_MAPPING,
        starting_point=STARTING_POINT,
        discount_factor=DISCOUNT_FACTOR
    )
    result = value_iteration(maze)

    _show_maze_result(maze, result, 'value_iteration_result.txt')

    plot_utility_vs_iteration(
        result['iteration_utilities'],
        save_file_name='value_iteration_utilities.png'
    )


    # For approximation of reference utilities given in instructions,
    # use discount factor of 0.95 and maximum error threshold of 1.4.
    # Values obtained through trial and error.
    maze = Maze(
        grid=GRID,
        reward_mapping=REWARD_MAPPING,
        starting_point=STARTING_POINT,
        discount_factor=0.95
    )
    result = value_iteration(maze, max_error=1.4)

    _show_maze_result(maze, result, 'approximate_reference_utilities_result.txt')

    plot_utility_vs_iteration(
        result['iteration_utilities'],
        save_file_name='approximate_reference_utilities.png'
    )


    # policy iteration
    maze = Maze(
        grid=GRID,
        reward_mapping=REWARD_MAPPING,
        starting_point=STARTING_POINT,
        discount_factor=DISCOUNT_FACTOR
    )
    result = policy_iteration(maze, num_policy_evaluation=11)
    
    _show_maze_result(maze, result, 'policy_iteration_result.txt')

    plot_utility_vs_iteration(
        result['iteration_utilities'],
        save_file_name='policy_iteration_utilities.png'
    )


def _show_maze_result(maze, result, save_file_name=None):
    """
    params:
    - maze (Maze)
    - result (dict): result of solving a maze
    - save_file_name (str): name of file to save plot as; defaults to None (not saved)
    """
    lines = []

    line = 'number of iterations required: ' + str(result['num_iterations'])
    print(line)
    lines.append(line)

    utilities, optimal_policy = result['utilities'], result['optimal_policy']

    optimal_policy_grid = copy.deepcopy(maze.grid)
    action_symbol_map = {
        MazeAction.MOVE_UP: '∧',
        MazeAction.MOVE_DOWN: 'v',
        MazeAction.MOVE_LEFT: '<',
        MazeAction.MOVE_RIGHT: '>',
    }

    line = '---utility for each state (row, column)---'
    print(line)
    lines.append(line)

    for state_position in maze.states:
        if state_position[1] == 0:
            print()

        line = str(state_position) + ' - utility: {:.3f}'.format(utilities[state_position])
        print(line)
        lines.append(line)

        action = optimal_policy[state_position]
        action_symbol = action_symbol_map[action]

        optimal_policy_grid[state_position[0]][state_position[1]] = action_symbol

    line = '---optimal policy grid (w = wall)---'
    print(line)
    lines.append(line)

    pprint(optimal_policy_grid)
    print()

    if save_file_name is not None:
        with open(RESULTS_DIR_PATH + save_file_name, 'w') as file:
            for line in lines:
                file.write(line + '\n')
            pprint(optimal_policy_grid, file)


if __name__ == '__main__':
    solve_MDP()
