# Search algorithms definitions

# TODO: add minimization case in simulated annealing

from random import choice, uniform
from numpy import argmax, argmin
from math import exp

# ----------------------------- Hill Climbing ----------------------------- #
def hill_climb(search_space):
    """
     search_space = Population -> Population.individuals = list of Individuals
    """
    start = choice(search_space)

    position = start

    while True:
        n = position.get_neighbours() # list of neighbours

        n_fit = [i.get_fitness() for i in n] # fitness function for each neighbour


        if search_space.optim == 'max':

            best_n = n[argmax(n_fit)] # get the neighbour with highest fitness

            if position.get_fitness() >= best_n.get_fitness():
                break
            else:
                position = best_n
                print(f'Current best solution: {position.representation} Fitness: {position.get_fitness()}')
        else: 
            
            best_n = n[argmin(n_fit)] # get the neighbour with highest fitness

            if position.get_fitness() <= best_n.get_fitness():
                break
            else:
                position = best_n
                print(f'Current best solution: {position.representation} Fitness: {position.get_fitness()}')

    print(f'Best solution: {position.representation} Fitness: {position.get_fitness()}')
    return position

# -------------------------- Simmulated Annealing -------------------------- #
def sim_annealing(search_space, L = 20, c = 10, alpha = 0.95):
    """
        Simulated annealing implementation

        Args:
            search_space (Population): a Population object to search trough
            L (Int, optional): internal loop parameter
            c (Int, optional): temperature parameter
            alpha (float, optional): remperature decrease factor

        Returns:
            Individual: the best solution found by the algorithm
    """

    # 1. Initialize the current solution
    position = choice(search_space)

    # 2. Initialize L and C
    L = L
    c = c

    # 3. Repeat until termination condition
    while c >0.05:
        # 3.1. Repeat L times
        for _ in range(L):
            #3.1.1. Choose a random neighbor
            neigh = choice(position.get_neighbours())

            # if search_space.optim == 'max':

            # 3.1.2. If new solution better or equal than current, accept it
            if neigh.get_fitness() >= position.get_fitness():
                print(f'Better solution found: {position.representation} Fitness: {position.get_fitness()}')
                position = neigh

            else:
                # else: accept it with probability exp(-|new.get_fitness() - current.get_fitness|/c)
                p = uniform(0, 1)
                pc = exp(- abs(position.get_fitness() - neigh.get_fitness()) / c)

                if pc > p:
                    print(f'Worsening fitness. New position: {position.representation} Fitness: {position.get_fitness()}')
                    position = neigh


        # 3.2. Decrease c
        c = c * alpha

    # 4. Return best solution so far
    print(f'Best solution found: {position.representation}')
    print(f'Fitness:', position.get_fitness())
    return position

# ----------------------------- Genetic Algorithm ----------------------------- #
