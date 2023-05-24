"""
This file contains a script to perform a Grid Search over crossover,
mutation and elitism operators of group genetic algorithm for the
Wedding Seating Chart Problem. The results of the Grid Search are
analyzed in the notebook results/experimental_analysis.ipynb.

It also contains a function that runs the GA with the best combination
of operators found in the Grid Search.
"""

from charles.charles import Population
from charles.selection import tournament_selection
from charles.crossover import gbx_crossover, eager_breeder_crossover, twin_maker
from charles.mutation import swap_mutation, merge_and_split, the_hop, dream_team

from itertools import product
import pandas as pd
import numpy as np
import csv
import json


# --------------------- Hyperparameters to tune -------------------- #
selection = [tournament_selection]
crossover = [eager_breeder_crossover, gbx_crossover, twin_maker]
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

def grid_search(selection, crossover, mutation, elitism):
    """
    This function performs a Grid Search over crossover, mutation and elitism

    Each algorithm is run 30 times and the fitness of each generation is saved.

    The algorithms with average best fitness on the last generation will be
    later analysed and compared.

    """

    # Generate all combinations of GO and Elite Hyperparameters
    hyperparameters_search = list(product(selection, crossover, mutation, elitism))

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
            fitness_history, _ = pop.evolve(n_generations = n_generations, xo_prob = xo_prob,
                                        mut_prob = mut_prob, select = selection, mutate = mutation,
                                        crossover = crossover, elitism = elitism, elite_size = elite_size)
        
            comb_results.append(fitness_history)
        
        # Save results of the combination in the N runs
        results[combination_name] = list(np.transpose(comb_results))

    # Formatting
    results = results.applymap(lambda x: json.dumps(x.tolist()) if isinstance(x, np.ndarray) else x)

    # Save results to file
    results.to_csv('results/results.csv', quoting=csv.QUOTE_NONNUMERIC, index=False)


def run_GA(selection_method, crossover_method, mutation_method, elitism):
    """
    Runs the GA with the given hyperparameters for 30 runs and saves the best
    individual found in the last generation among the runs.
    """

    best_fitness = 0
    best_individual = None

    for _ in range(nr_runs):

        pop = Population(pop_size = pop_size, nr_guests = nr_guests, nr_tables = nr_tables)

        _, ind = pop.evolve(n_generations = n_generations, xo_prob = xo_prob,
                                            mut_prob = mut_prob, select = selection_method,
                                            mutate = mutation_method, crossover = crossover_method,
                                            elitism = elitism, elite_size = elite_size)
        
        if ind.get_fitness() > best_fitness:
            best_fitness = ind.get_fitness()
            best_individual = ind
    
    # Print the best individual found across all runs
    print('Best individual found by the algorithm in the last generation: ', best_individual,
          '\nFitness: ', best_fitness)
    
    # Detailed information about the best individual
    for table_idx in range(len(best_individual)):
        print('Table: ', best_individual[table_idx],
              ' with fitness: ', best_individual.get_table_fitness(table_idx))
        
        

#  ------------------ Run the Grid Search (NOTE: Uncomment to run) ------------------ #

# grid_search(selection, crossover, mutation, elitism)



# -------- Run the GA with the best hyperparameters found in the Grid Search -------- #

# We know from the analysis on results/experimental_results.ipynb that the best
# combination of operators is:
# Selection: tournament_selection
# Crossover: eager_breeder_crossover
# Mutation: dream_team
# Elitism: True

# Run the GA with the best combination of operators found in the Grid Search
best_individual = run_GA(tournament_selection, eager_breeder_crossover, dream_team, True)