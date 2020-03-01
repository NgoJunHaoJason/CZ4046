# mapping of squares to rewards
REWARDS = {
    'w': -0.04,  # white square
    'g': 1.0,  # green square
    'b': -1.0,  # brown square
}

# let maze be a 2D array
MAZE = [
    ['g', 'x', 'g', 'w', 'w', 'g'],
    ['w', 'b', 'w', 'g', 'x', 'b'],
    ['w', 'w', 'b', 'w', 'g', 'w'],
    ['w', 'w', 'w', 'b', 'w', 'g'],
    ['w', 'x', 'x', 'x', 'b', 'w'],
    ['w', 'w', 'w', 'w', 'w', 'w'],
]

STARTING_POINT = (3, 2)  # 4th row, 3rd column
