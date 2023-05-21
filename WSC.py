from charles.charles import Population
from charles.selection import tournament_selection, rank_selection, fps
from charles.crossover import gbx_crossover, eager_breader_crossover, twin_maker
from charles.mutation import swap_mutation, merge_and_split, the_hop, dream_team

from itertools import product
import pandas as pd
import numpy as np
import csv
import json

selection = [tournament_selection, fps, rank_selection]
crossover = [eager_breader_crossover, gbx_crossover, twin_maker]
mutation = [the_hop, merge_and_split, swap_mutation, dream_team]
elitism = [True, False]

nr_runs = 10
n_generations = 5
pop_size = 100

hyperparameters_search = list(product(selection, crossover, mutation, elitism))

# This dataframe will save the best fitness of each generation, for each combination
# and for each run. Each cell is a list of the best fitnesses on the n runs
# for a specific combination and a generation

results = pd.DataFrame()

for (selection, crossover, mutation, elitism) in hyperparameters_search[:4]:

    combination_name = f'{selection.__name__}|{crossover.__name__}|{mutation.__name__}|elitism_{elitism}'
    
    comb_results = []

    for run_nr in range(nr_runs):
        print(f'----------- Run_{run_nr + 1} of comb {combination_name}')

        pop = Population(pop_size = pop_size, nr_guests = 64, nr_tables = 8)

        fitness_history = pop.evolve(n_generations = n_generations, xo_prob = 0.9, mut_prob = 0.1, select = selection,
                                    mutate = mutation, crossover = crossover, elitism = elitism)
    
        comb_results.append(fitness_history)
    
    results[combination_name] = list(np.transpose(comb_results))


# Formatting
results = results.applymap(lambda x: json.dumps(x.tolist()) if isinstance(x, np.ndarray) else x)

# Saves results to file
results.to_csv('results.csv', quoting=csv.QUOTE_NONNUMERIC, index=False)