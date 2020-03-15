"""
Definition of reinforcement learning algorithms as functions in Python.

In this file:
- Bellman equation
- value iteration
- policy iteration
"""
from functools import reduce


def bellman_equation(
    state, 
    discount_factor: float,
    all_states,
):
    """
    U(s) = R(s) + gamma * max( sum( P(s'|s,a) * U(s') ) ) for a in A(s)

    state: {
        'x': x (int),
        'y': y (int),
        'reward': reward (float)
        'current_utility': current utility (float),
        'previous_utility': previous utility (float),
        'optimal_action': optimal action (MazeAction),
        'action_next_state_map': { 
            action: (
                (0.8, intended_state), 
                (0.1, unintended_state_1), 
                (0.1, unintended_state_2)
            )
        }
    }
    discount_factor: gamma

    return: U(s) - updated utility of the given state
    """
    max_expected_utility = float('-inf')

    action_next_state_map = state['action_next_state_map']

    for action in action_next_state_map:
        expected_utility = 0

        for probability, next_state_position in action_next_state_map[action]:
            next_state_utility = all_states[next_state_position]['previous_utility']
            expected_utility += probability * next_state_utility

        if expected_utility > max_expected_utility:
            max_expected_utility = expected_utility
            state['optimal_action'] = action

    # U(s)
    return state['reward'] + discount_factor * max_expected_utility


def value_iteration(
    states,
    discount_factor: float,
    epsilon=1e-10,
):
    """
    states (MDP.states): all states in an environment
    discount_factor (float): discount factor for future states
    epsilon (float): threshold for difference between current utility and previous utility,
        below which solution can be considered to have been converged upon
    """
    # start off with every U(s) = 0
    for state_position in states:
        states[state_position]['current_utility'] = 0
        states[state_position]['previous_utility'] = 0  # required for Bellman equation
        states[state_position]['optimal_action'] = None

    has_converged = False
    num_iterations = 0

    while not has_converged:
        total_utility_difference = 0
        has_converged = True
        num_iterations += 1

        print('doing iteration', num_iterations)

        for state_position in states:
            states[state_position]['previous_utility'] = states[state_position]['current_utility']

        for state_position in states:
            states[state_position]['current_utility'] = bellman_equation(
                states[state_position],
                discount_factor,
                states
            )

            utility_difference = abs(states[state_position]['current_utility'] - \
                    states[state_position]['previous_utility'])

            if utility_difference > epsilon:
                has_converged = False

            total_utility_difference += utility_difference

        print(
            'total difference between previous and current utility values:',
            total_utility_difference,
        )

    return states


def policy_iteration():
    pass  # TODO
