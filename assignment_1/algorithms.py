def bellman_equation(
    current_state, 
    successive_states, 
    actions,
    reward, 
    transition_model, 
    discount_factor,
):
    return reward(current_state)  # TODO


def value_iteration(states, actions, reward_function, transition_model, epsilon=1e-10):
    utilities = { 
        state: { 'current': 0, 'previous': 0 } 
        for state in states 
    }

    has_converged = False

    while not has_converged:
        for state in utilities:
            max_next_state_expected_utility = None

            for next_state in state['successive_states']:
                for action in actions:
                    next_state_expected_utility = transition_model(
                        next_state,
                        state,
                        action,
                    )

                    # TODO

            reward = reward_function(state)
            pass  # TODO


def policy_iteration():
    pass  # TODO
