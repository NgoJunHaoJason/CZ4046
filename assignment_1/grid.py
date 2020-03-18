import random
import pprint


# Based on maze given, ~0.5 (16 out of 36 squares) of the maze is not white space.
# Among non-white spaces (16 squares), roughly 
# ~1/3 are walls (5 walls), 
# ~1/3 are brown squares (5 brown),
# ~1/3 are green squares (6 green)
# Therefore, try to generate maze with roughly same distribution.
def generate_maze(grid_length: int):
    """
    Generates a maze as a square grid that has size of (grid_length x grid_length).

    params:
    - grid_length (int): length of the grid

    return:
    - 2D array (list of list): [
        [' ', ..., ' '],
        ...,
        [' ', ..., ' '],
    ]
    """
    random.seed()
    grid = []

    for row in range(grid_length):
        grid.append([])
        
        for _ in range(grid_length):  # _ is column; column value not used
            colour_number = random.random()

            if colour_number < 0.5 / 3:
                grid[row].append('w')  # wall
            elif colour_number < 0.5 * 2 / 3:
                grid[row].append('b')  # brown
            elif colour_number < 0.5:
                grid[row].append('g')  # green
            else:
                grid[row].append(' ')  # white

    return grid
