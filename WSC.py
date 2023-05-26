"""
This file runs the GA with the best combination of operators found in the Grid Search,
for the Wedding Seating Chart Problem.

We know from the analysis on results/experimental_results.ipynb that the best
combination of operators is:
    - Crossover: eager_breeder_crossover
    - Mutation: dream_team
    - Elitism: True

The algorithm is run 30 times with the same selection method, population size, number of
generations, crossover and mutation probabilities, and elite size as in the Grid Search.

The best individual found in the last generation across all runs is printed,
as well as detailed information.

"""

from charles.charles import Population
from charles.selection import tournament_selection
from charles.crossover import eager_breeder_crossover
from charles.mutation import dream_team

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
        

# -------- Run the GA with the best hyperparameters found in the Grid Search -------- #

best_individual = run_GA(tournament_selection, eager_breeder_crossover, dream_team, True)