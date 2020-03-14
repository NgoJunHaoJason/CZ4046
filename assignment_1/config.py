# let maze be a 2D array
GRID = [
    ['g', 'w', 'g', ' ', ' ', 'g'],
    [' ', 'b', ' ', 'g', 'w', 'b'],
    [' ', ' ', 'b', ' ', 'g', ' '],
    [' ', ' ', ' ', 'b', ' ', 'g'],
    [' ', 'w', 'w', 'w', 'b', ' '],
    [' ', ' ', ' ', ' ', ' ', ' '],
]

# mapping of squares to rewards
REWARD_MAPPING = {
    ' ': -0.04,  # white square
    'g': 1.0,  # green square
    'b': -1.0,  # brown square
}

STARTING_POINT = { 'x': 3, 'y': 2 }  # 4th row, 3rd column

DISCOUNT_FACTOR = 0.99
