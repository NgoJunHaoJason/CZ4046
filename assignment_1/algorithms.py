"""
Definition of reinforcement learning algorithms as functions in Python.

In this file:
- value iteration
- policy iteration
"""
from functools import reduce

from assignment_1.base import MarkovDecisionProcess
from assignment_1.maze import MazeAction


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
        'iteration_utilities': {
            (x, y): [utility for each iteration (float)]
        }
    }
    """
    # U,U′, vectors of utilities for states in S, initially zero
    current_utilities, new_utilities, optimal_policy = {}, {}, {}

    # for: Plot of utility estimates as a function of the number of iterations
    iteration_utilities = {}

    for state_position in mdp.states:
        current_utilities[state_position] = 0
        new_utilities[state_position] = 0
        optimal_policy[state_position] = None

        # utility start at index 1 (iteration number 1)
        iteration_utilities[state_position] = [None]

    has_converged = False
    num_iterations = 0

    # repeat
    while not has_converged:
        for state_position in mdp.states:
            current_utilities[state_position] = new_utilities[state_position]  # U ← U′
            iteration_utilities[state_position].append(current_utilities[state_position])

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
        'iteration_utilities': iteration_utilities,
    }


def policy_iteration(mdp: MarkovDecisionProcess):
    """
    params:
    - mdp (MarkovDecisionProcess): an MDP with 
        states S, 
        actions A(s), 
        transition model P(s′|s, a), 
        rewards R(s), 
        discount γ

    return: {
        'utilities': {
            (x, y): utility value (float)
        },
        'optimal_policy': {
            (x, y): best action to take at this state (MazeAction)
        },
        'num_iterations': num_iterations (int),
        'iteration_utilities': {
            (x, y): [utility for each iteration (float)]
        }
    }
    """
    # U , a vector of utilities for states in S , initially zero
    # π, a policy vector indexed by state, initially random
    utilities, policy = {}, {}

    # for: Plot of utility estimates as a function of the number of iterations
    iteration_utilities = {}

    for state_position in mdp.states:
        utilities[state_position] = 0
        policy[state_position] = MazeAction.MOVE_UP

        # utility start at index 1 (iteration number 1)
        iteration_utilities[state_position] = [None]

    unchanged = True
    num_iterations = 0

    # repeat
    while unchanged:
        for state_position in mdp.states:
            iteration_utilities[state_position].append(utilities[state_position])

        # U ← POLICY-EVALUATION (π, U , mdp)
        utilities = _policy_evaluation(policy, utilities, mdp)

        policy, unchanged = _policy_improvement(mdp, policy, utilities)

        num_iterations += 1

    # algorithm: return π
    #
    # in my implementation, I return the utilities and number of iterations
    # as well as they will come in useful later
    return {
        'utilities': utilities,
        'optimal_policy': policy,
        'num_iterations': num_iterations,
        'iteration_utilities': iteration_utilities,
    }


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
        expected_utility = _get_expected_utility(
            mdp,
            state_position,
            action,
            current_utilities
        )

        if expected_utility > max_expected_utility:
            max_expected_utility = expected_utility
            best_action = action

    # U′[s]
    return (
        mdp.reward_function(state_position) + mdp.discount * max_expected_utility,
        best_action,
    )


def _policy_evaluation(
    policy: dict, 
    utilities: dict, 
    mdp: MarkovDecisionProcess
) -> dict:
    """
    Based on Bellman equation.

    params:
    - policy: {
        (x, y): best action to take at this state (MazeAction)
    }
    - utilities: {
        (x, y): utility value (float)
    }
    - mdp (MarkovDecisionProcess): an MDP with 
        states S, 
        actions A(s), 
        transition model P(s′|s, a), 
        rewards R(s), 
        discount γ

    return: {
        (x, y): updated utility value (float)
    }
    """
    updated_utilities = {}

    # for each state s in S do
    for state_position in mdp.states:
        reward = mdp.reward_function(state_position)

        # ∑s′P (s'|s, π_i(s)) U_i(s')
        expected_utility = _get_expected_utility(
            mdp,
            state_position,
            policy[state_position],
            utilities
        )

        # U_i+1(s) ← R(s) + γ ∑s′P (s'|s, π_i(s)) U_i(s')
        updated_utilities[state_position] = reward + mdp.discount * expected_utility

    return updated_utilities


def _policy_improvement(
    mdp,
    policy,
    utilities, 
):
    """
    params:
    - mdp (MarkovDecisionProcess): the MDP to solve
    - policy: {
        (x, y): best action to take at this state (MazeAction)
    }
    - utilities: {
        (x, y): utility value (float)
    }

    return: (
        updated_policy (dict),
        unchanged (bool),
    )
    """
    updated_policy = {}
    unchanged = True  # unchanged? ← true

    # for each state s in S do
    for state_position in mdp.states:
        new_utility, new_action = _bellman_equation(
            mdp,
            state_position,
            utilities, 
        )

        utility = _get_expected_utility(
            mdp,
            state_position,
            policy[state_position],
            utilities
        )

        # if max a∈A(s) ∑s′ P (s'|s, a) U [s'] > ∑s′ P (s'|s, π[s]) U [s'] then do
        if new_utility > utility:
            updated_policy[state_position] = new_action
            unchanged = False
        else:
            updated_policy[state_position] = policy[state_position]

        return (updated_policy, unchanged)


def _get_expected_utility(
    mdp: MarkovDecisionProcess,
    state_position: tuple, 
    action: MazeAction,
    utilities: dict, 
) -> float:
    """
    Implementation of ∑s′P(s′|s, a)U[s′]

    params:
    - mdp (MarkovDecisionProcess): the MDP to solve
    - state_position (tuple): x, y
    - action (MazeAction): action to take at the given state
    - utilities: {
        (x, y): utility value (float)
    }

    return: utility value of the state given (float)
    """
    expected_utility = 0

    possible_next_states = mdp.get_next_states(state_position, action)

    for intended_next_state_position in possible_next_states:
        # The intended state to move into is used (even if it is invalid).
        # If there are more than 1 wall / border surrounding current state,
        # there will be an overlap in next states, since they will end up
        # remaining in the current state.
        # If next_state_1 == next_state_2, the transition model defined
        # will fail to calculate the correct probability, so intended state
        # is used instead of actual state
        probability = mdp.transition_model(
            state_position,
            action,
            intended_next_state_position
        )

        # actual state used to calculate utility,
        # since intended state may be invalid (wall / out of bounds)
        actual_next_state_position = \
            possible_next_states[intended_next_state_position]['actual']
        next_state_utility = utilities[actual_next_state_position]

        expected_utility += probability * next_state_utility

    return expected_utility
