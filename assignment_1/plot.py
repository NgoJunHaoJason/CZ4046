import matplotlib.pyplot as plt


def plot_utility_vs_iteration(iteration_utilities):
    """
    params:
    - iteration_utilities: {
        (x, y): [utility for each iteration (float)]
    }
    """
    for state_position in iteration_utilities:
        plt.plot(iteration_utilities[state_position])

    plt.legend(iteration_utilities, loc='center left', bbox_to_anchor=(1, 0.5))
    plt.title('utility of each state at each iteration')
    plt.xlabel('iteration')
    plt.ylabel('utility estimate')

    plt.show()
