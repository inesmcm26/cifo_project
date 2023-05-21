from charles.charles import Population
from charles.selection import tournament_selection, rank_selection, fps
from charles.crossover import gbx_crossover, eager_breader_crossover, twin_maker
from charles.mutation import swap_mutation, merge_and_split, the_hop, dream_team

from itertools import product
import pandas as pd

selection = [tournament_selection, rank_selection, fps]
crossover = [gbx_crossover, eager_breader_crossover, twin_maker]
mutation = [swap_mutation, merge_and_split, the_hop, dream_team]
elitism = [True, False]

nr_runs = 30
n_generations = 70
pop_size = 100

hyperparameters_search = list(product(selection, crossover, mutation, elitism))

results = pd.DataFrame()

for (selection, crossover, mutation, elitism) in hyperparameters_search:

    comb_results = pd.DataFrame()

    for run_nr in range(nr_runs):

        pop = Population(pop_size = pop_size, nr_guests = 64, nr_tables = 8)

        fitness_history = pop.evolve(n_generations = n_generations, xo_prob = 0.9, mut_prob = 0.1, select = selection,
                                    mutate = mutation, crossover = crossover, elitism = elitism)
    
        comb_results[f'Run_{run_nr}'] = fitness_history

    combination_name = f'{selection.__name__}_{crossover.__name__}_{mutation.__name__}_Elitism:{elitism}'

    results[combination_name] = comb_results.mean(axis = 1)

results.to_csv('results.csv')