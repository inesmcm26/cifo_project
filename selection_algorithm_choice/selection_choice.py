"""
This file contains a script used to assess the best selection algorithm.

Eigth combinations of other genetic operations are choosen to be used together
with each selection algorithm. Each combination is run 30 times and the median
fitness of each generation is saved.

The average best algorithm will be choosen as the selection method for later use.
"""

from charles.crossover import gbx_crossover, eager_breeder_crossover, twin_maker
from charles.mutation import swap_mutation, merge_and_split, the_hop, dream_team
from charles.selection import tournament_selection, fps, ranking_selection

from charles.charles import Population

from itertools import product
from random import sample
import pandas as pd
import numpy as np

# --------------- Hyperparameters to choose randomly ---------------- #
crossover = [eager_breeder_crossover, gbx_crossover, twin_maker]
mutation = [the_hop, merge_and_split, swap_mutation, dream_team]

# Randomly select 8 combinations of crossover and mutation
xo_mut_comb = sample(list(product(crossover, mutation)), 8)

# Add the selection methods to the combinations
tournament_combs = list(product([tournament_selection], xo_mut_comb))
fps_combs = list(product([fps], xo_mut_comb))
ranking_combs = list(product([ranking_selection], xo_mut_comb))

# Combinations of selection, crossover and mutation to be tested
selection_combs = tournament_combs + fps_combs + ranking_combs

# ---------------------- Fixed Hyperparameters ---------------------- #
# Genetic operators and elitism
xo_prob = 0.9
mut_prob = 0.1

# GA evolution
nr_runs = 30
n_generations = 100
pop_size = 50

# Problem specific
nr_guests = 64
nr_tables = 8

results = pd.DataFrame()


for (selection, (crossover, mutation)) in selection_combs:

    # Save the name of the combination
    combination_name = f'{selection.__name__}|{crossover.__name__}|{mutation.__name__}'

    # Save results of each run
    comb_results = []

    for run_nr in range(nr_runs):
        print(f'----------- Run_{run_nr + 1} of comb {combination_name}')

        # Create a population
        pop = Population(pop_size = pop_size, nr_guests = nr_guests, nr_tables = nr_tables)

        # Run the GA
        best_fitnesses = pop.evolve(n_generations = n_generations, xo_prob = xo_prob,
                                    mut_prob = mut_prob, select = selection,
                                    crossover = crossover, mutate = mutation)

        # Save the best fitnesses of each generation
        comb_results.append(best_fitnesses)

    results[combination_name] = np.median(np.transpose(comb_results), axis = 1)


results.to_csv('selection_results.csv')