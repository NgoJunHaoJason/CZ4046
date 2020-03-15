"""
Definition of reinforcement learning algorithms as functions in Python.

In this file:
- value iteration
- policy iteration
"""
from functools import reduce

from assignment_1.base import MarkovDecisionProcess


def _bellman_equation(
    mdp: MarkovDecisionProcess,
    state_position: tuple, 
    current_utilities: dict, 
):
    """
    Implementation of U′[s] ← R(s) + γ max a∈A(s) ∑s′P(s′|s, a)U[s′]

    params:
    - mdp (MarkovDecisionProcess): the MDP to solve
    - state_position (tuple): x, y
    - current_utilities (dict): maps any (x, y) to its current utility value

    return: (
        updated utility value of the state given (float),
        best action to take at the state given (MazeAction),
    )
    """
    max_expected_utility = float('-inf')
    best_action = None

    action_next_state_map = mdp.states[state_position]

    for action in action_next_state_map:
        expected_utility = 0

        for intended_next_state_position in action_next_state_map[action]:
            actual_next_state_position = \
                action_next_state_map[action][intended_next_state_position]['actual']
            next_state_utility = current_utilities[actual_next_state_position]

            probability = mdp.transition_model(
                state_position,
                action,
                intended_next_state_position
            )
            expected_utility += probability * next_state_utility

        if expected_utility > max_expected_utility:
            max_expected_utility = expected_utility
            best_action = action

    # U′[s]
    return (
        mdp.reward_function(state_position) + mdp.discount * max_expected_utility,
        best_action,
    )


# reference: value iteration algorithm,
# as shown in figure 17.4 of Artificial Intelligence: A Modern Approach
def value_iteration(
    mdp: MarkovDecisionProcess,
    max_error=1e-10,
):
    """
    params:
    - mdp (MarkovDecisionProcess): an MDP with 
        states S, 
        actions A(s), 
        transition model P(s′|s, a), 
        rewards R(s), 
        discount γ

    - max_error (float): the maximum error allowed in the utility of any state

    return: {
        'utilities': {
            (x, y): utility value (float)
        },
        'optimal_policy': {
            (x, y): best action to take at this state (MazeAction)
        },
        'num_iterations': num_iterations (int),
    }
    """
    # U,U′, vectors of utilities for states in S, initially zero
    current_utilities, new_utilities, optimal_policy = {}, {}, {}

    for state_position in mdp.states:
        current_utilities[state_position] = 0
        new_utilities[state_position] = 0
        optimal_policy[state_position] = None

    has_converged = False
    num_iterations = 0

    # repeat
    while not has_converged:
        for state_position in mdp.states:
            current_utilities[state_position] = new_utilities[state_position]  # U ← U′

        max_utility_change = 0  # δ ← 0

        # for each state s in S do 
        for state_position in mdp.states:
            # U′[s] ← R(s) + γ max a∈A(s) ∑s′P(s′|s, a)U[s′]
            new_utility, new_action = _bellman_equation(
                mdp,
                state_position,
                current_utilities, 
            )

            new_utilities[state_position] = new_utility
            optimal_policy[state_position] = new_action

            # if |U′[s]−U[s]| > δ then δ ← |U′[s]−U[s]|
            abs_utility_difference = abs(new_utilities[state_position] - \
                    current_utilities[state_position])

            if abs_utility_difference > max_utility_change:
                max_utility_change = abs_utility_difference

        num_iterations += 1

        print(
            'iteration:', num_iterations,
            '-maximum change in the utility of any state:', 
            '{:.6f}'.format(max_utility_change),
        )

        # until δ < ϵ(1−γ)/γ
        has_converged = max_utility_change < \
            max_error * (1 - mdp.discount) / mdp.discount

    # algorithm: return U
    #
    # in my implementation, I return the optimal policy and number of iterations
    # as well as they will come in useful later
    return {
        'utilities': current_utilities,
        'optimal_policy': optimal_policy,
        'num_iterations': num_iterations,
    }


def policy_iteration():
    pass  # TODO
