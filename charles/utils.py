import seaborn as sns
import matplotlib.pyplot as plt
from int_bin import IntBinIndividual

def fitness_landscape(search_space):
    """
     Plots the fitness landscape given a search space and a fitness function
    """

    print([i.get_fitness() for i in search_space])

    sns.lineplot(data = [i.get_fitness() for i in search_space])

    plt.show()

search_space = [IntBinIndividual(representation = i) for i in [[0, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0],
                                                                 [0, 0, 1, 1], [0, 1, 0, 0], [0, 1, 0, 1],
                                                                 [0, 1, 1, 0], [0, 1, 1, 1], [1, 0, 0, 0],
                                                                 [1, 0, 0, 1], [1, 0, 1, 0], [1, 0, 1, 1],
                                                                 [1, 1, 0, 0], [1, 1, 0, 1], [1, 1, 1, 0], [1, 1, 1, 1]]]

def plot_c(c, alpha, threshold):
    c_list = [c]

    while c > threshold:
        c = c * alpha
        c_list.append(c)

    plt.plot(c_list)
    plt.show()

plot_c(10, 0.95, 0.05)