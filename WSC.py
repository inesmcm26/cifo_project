from charles.charles import Population
from charles.selection import tournament_selection, rank_selection, fps
from charles.crossover import gbx_crossover, eager_breader_crossover, twin_maker
from charles.mutation import swap_mutation, merge_and_split, the_hop, dream_team

from itertools import product
import pandas as pd
import numpy as np
import csv
import json
import time

selection = [tournament_selection, fps, rank_selection]
crossover = [eager_breader_crossover, gbx_crossover, twin_maker]
mutation = [the_hop, merge_and_split, swap_mutation, dream_team]
elitism = [True, False]

nr_runs = 30
n_generations = 100
pop_size = 50

nr_guests = 64
nr_tables = 8

hyperparameters_search = list(product(selection, crossover, mutation, elitism))

t0 = time.time()

# This dataframe will save the best fitness of each generation, for each combination
# and for each run. Each cell is a list of the best fitnesses on the n runs
# for a specific combination and a generation
results = pd.DataFrame()

for (selection, crossover, mutation, elitism) in hyperparameters_search:

    combination_name = f'{selection.__name__}|{crossover.__name__}|{mutation.__name__}|elitism_{elitism}'
    
    comb_results = []

    for run_nr in range(nr_runs):
        print(f'----------- Run_{run_nr + 1} of comb {combination_name}')

        pop = Population(pop_size = pop_size, nr_guests = nr_guests, nr_tables = nr_tables)

        fitness_history = pop.evolve(n_generations = n_generations, xo_prob = 0.9, mut_prob = 0.1, select = selection,
                                    mutate = mutation, crossover = crossover, elitism = elitism)
    
        comb_results.append(fitness_history)
    
    results[combination_name] = list(np.transpose(comb_results))


# Formatting
results = results.applymap(lambda x: json.dumps(x.tolist()) if isinstance(x, np.ndarray) else x)

# Saves results to file
results.to_csv('results.csv', quoting=csv.QUOTE_NONNUMERIC, index=False)


t1 = time.time()

print(f'Execution time: {t1 - t0} seconds')