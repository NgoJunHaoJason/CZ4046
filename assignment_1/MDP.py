class MarkovDecisionProcess:
    def __init__(self, states, actions):
        self.states = states
        self.actions = actions

    def transition_model(self, state, action, next_state) -> float:
        pass

    def reward(self, state):
        pass
