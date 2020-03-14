"""
Definition of reinforcement learning algorithms as functions.

In this file:
- Bellman equation
- value iteration
- policy iteration
"""

from functools import reduce


def bellman_equation(
    state, 
    actions,
    reward: function, 
    transition_model: function, 
    discount_factor: float,
):
    """
    U(s) = R(s) + gamma * max( sum( P(s'|s,a) * U(s') ) ) for a in A(s)

    state: s
    actions: A(s)
    reward: R
    transition_model: P(s'|s,a)
    discount_factor: gamma

    return: U(s)
    """
    max_expected_utility = float('-inf')

    for action in actions:
        expected_utility = reduce(
            lambda utility, next_state: utility + transition_model(
                state, 
                action, 
                next_state
            ) * next_state['previous_utility'],
            action[state],
            0,
        )

        max_expected_utility = max(max_expected_utility, expected_utility)

    # U(s)
    return reward(state) + discount_factor * max_expected_utility


def value_iteration(
    states,
    actions,
    reward_function,
    transition_model,
    discount_factor,
    epsilon=1e-10,
):
    # start off with every U(s) = 0
    for state in states:
        state['current_utility'] = 0
        state['previous_utility'] = 0  # required for Bellman equation

    has_converged = False
    num_iterations = 0

    while not has_converged:
        has_converged = True
        num_iterations += 1

        for state in states:
            state['previous_utility'] = state['current_utility']

        for state in states:
            state['current_utility'] = bellman_equation(
                state,
                actions,
                reward_function,
                transition_model,
                discount_factor,
            )

            if abs(state['current_utility'] - state['previous_utility']) > epsilon:
                has_converged = False

    optimal_policy = {}

    for state in states:
        pass

    return optimal_policy


def policy_iteration():
    pass  # TODO
