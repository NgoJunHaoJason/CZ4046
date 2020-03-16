"""
Contains function for plotting.
"""
import matplotlib.pyplot as plt

from assignment_1.config import RESULTS_DIR_PATH


def plot_utility_vs_iteration(iteration_utilities, save_file_name=None):
    """
    params:
    - iteration_utilities: {
        (x, y): [utility for each iteration (float)]
    }
    - save_file_name (str): name of file to save plot as; defaults to None (not saved)
    """
    plt.figure(figsize=(16, 8))

    for state_position in iteration_utilities:
        plt.plot(iteration_utilities[state_position])

    plt.legend(iteration_utilities, loc='center left', bbox_to_anchor=(1, 0.5))

    plt.title('utility of each state at each iteration')
    plt.xlabel('iteration')
    plt.ylabel('utility estimate')

    if save_file_name is not None:
        plt.savefig(RESULTS_DIR_PATH + save_file_name)

    plt.show()
