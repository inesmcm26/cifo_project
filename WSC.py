from charles.charles import Population
from charles.selection import tournament_selection
from charles.crossover import gbx_crossover, eager_breader_crossover, twin_maker
from charles.mutation import swap_mutation, merge_and_split, the_hop, dream_team

from itertools import product
import pandas as pd
import numpy as np
import csv
import json
import time

# --------------------- Hyperparameters to tune -------------------- #
selection = [tournament_selection]
crossover = [eager_breader_crossover, gbx_crossover, twin_maker]
mutation = [the_hop, merge_and_split, swap_mutation, dream_team]
elitism = [True, False]


# ---------------------- Fixed Hyperparameters ---------------------- #
# Genetic operators and elitism
elite_size = 5
xo_prob = 0.9
mut_prob = 0.1

# GA evolution
nr_runs = 30
n_generations = 100
pop_size = 50

# Problem specific
nr_guests = 64
nr_tables = 8


# Generate all combinations of GO and Elite Hyperparameters
hyperparameters_search = list(product(selection, crossover, mutation, elitism))

t0 = time.time()

# This dataframe will save the best fitness of each generation, for every combination
# of hyperparameters at each run. The columns are the combinations of hyperparameters
# and the rows are the generations. Each cell is a list of the best fitnesses of the
# corresponding combination and generation.
results = pd.DataFrame()

# For each combination of hyperparameters
for (selection, crossover, mutation, elitism) in hyperparameters_search:
    
    # Save the name of the combination
    combination_name = f'{selection.__name__}|{crossover.__name__}|{mutation.__name__}|elitism_{elitism}'
    
    # Save results of each run
    comb_results = []

    for run_nr in range(nr_runs):
        print(f'----------- Run_{run_nr + 1} of comb {combination_name}')

        # Create a population
        pop = Population(pop_size = pop_size, nr_guests = nr_guests, nr_tables = nr_tables)

        # Evolve the population
        fitness_history = pop.evolve(n_generations = n_generations, xo_prob = xo_prob,
                                     mut_prob = mut_prob, select = selection, mutate = mutation,
                                     crossover = crossover, elitism = elitism, elite_size = elite_size)
    
        comb_results.append(fitness_history)
    
    # Save results of the combination in the N runs
    results[combination_name] = list(np.transpose(comb_results))

# Formatting
results = results.applymap(lambda x: json.dumps(x.tolist()) if isinstance(x, np.ndarray) else x)

# Save results to file
results.to_csv('results/results.csv', quoting=csv.QUOTE_NONNUMERIC, index=False)

t1 = time.time()

print(f'Execution time: {t1 - t0} seconds')