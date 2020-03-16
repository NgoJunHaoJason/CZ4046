"""
Base classes are defined here.

abstract classes:
- MarkovDecisionProcess
"""


class MarkovDecisionProcess:
    """
    Has the Markov property - the likelihood of future states of the process
    depends only on the present state, not the sequence of states that preceeds it.
    """
    def __init__(self, states, actions, discount):
        """
        Initialise states, actions and discount.
        """
        self.states = states
        self.actions = actions
        self.discount = discount

    def transition_model(self, state, action, next_state) -> float:
        """
        returns: the probability of transitioning into the next state,
            given the current state and action taken at current state
        """
        pass

    def reward_function(self, state):
        """
        returns: the reward obtained at the current state
        """
        pass

    def get_next_states(self, state, action):
        """
        params:
        - state (tuple): x, y position
        - action (MazeAction): action to take at the given state

        return: possible next states
        """
        pass
