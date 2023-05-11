from random import shuffle, sample, choice, random
from copy import deepcopy
import itertools

class Individual:
    """
      Possible solution to an optimization problem
    """
    # we always initialize
    def __init__(self, arrangement = None):

        representation = []
        
        for table in arrangement:
            representation.append(set(table))

        self.representation = representation

    def __str__(self):
        """
         Solution string representation
        """
        # TODO
        return str(self.representation)
    
    def __len__(self):
        # TODO
        return len(self.representation)
    
    def get_fitness():
        """
         Solution fitness
        """
        # TODO
        raise Exception('You need to implement this method')

class Population:
    """
      Search Space: set of individuals
    """
    def __init__(self, pop_size, nr_guests, nr_tables):


        # population size
        self.nr_guests = nr_guests

        # defining the optimization problem as a minimization or maximization problem
        self.nr_tables = nr_tables

        self.individuals = []

        nrs = [i for i in range(1, nr_guests + 1)]

        possible_tables = list(itertools.combinations(nrs, nr_guests // nr_tables))

        table_distributions = list(itertools.combinations(possible_tables, nr_tables))

        valid_arrangements = []

        for combination in table_distributions:
            unique_values = set(num for group in combination for num in group)
            
            if len(unique_values) == len(nrs): # confirm that there are no redundant solutions
                        valid_arrangements.append(combination)

        
        selected_arrangements = sample(valid_arrangements, pop_size)


        for arrangement in selected_arrangements:
            self.individuals.append(Individual(arrangement))
    
    def __str__(self):
        """
         Population string representation
        """
        # TODO
        for individual in self.individuals:
            print(individual)
        # return str(self.individuals)

    def __len__(self):
        return len(self.individuals)

    def __getitem__(self, position):
        return self.individuals[position]
    
    def get_size(self):
        return self.size

    def get_optim(self):
        return self.optim

    def get_individuals(self):
        return self.individuals

    def best_individual(self):
        """
         Get the best individual of the population
        """
        return deepcopy(sorted(self.individuals, key = lambda x: x.get_fitness(), reverse = (self.optim == 'max'))[0])
    
    def evolve(self, n_generations, xo_prob, mut_prob, select, mutate, crossover, elitism):
        """
         Evolve the population: get generation after generation until the end of
         the evolutionary process
        """

        for i in range(n_generations):

            new_pop = []

            if elitism:
                # keep the best individual
                elite = self.best_individual()

            while len(new_pop) < self.size:
                p1, p2 = select(self), select(self) # selection method is passed as argument

                if random() < xo_prob:
                    # crossover method is passed as argument
                    offspring1, offspring2 = crossover(p1, p2)
                else:
                    offspring1, offspring2 = p1, p2

                if random() < mut_prob:
                    offspring1 = mutate(offspring1) # mutation method is passed as argument
                if random() < mut_prob:
                    offspring2 = mutate(offspring2) # mutation method is passed as argument

                new_pop.append(self.get_type_of_individ()(representation = offspring1))
                
                # to check if we can insert both of the individuals or only one
                if len(new_pop) < self.size:
                    new_pop.append(self.get_type_of_individ()(representation = offspring2))
                
            
            if elitism:
                if self.get_optim() == 'max':
                    worst_ind = min(new_pop, key = lambda x: x.get_fitness())
                    # if elite is better than the worst individual in the population, replace it
                    if elite.get_fitness() > worst_ind.get_fitness():
                        new_pop.pop(new_pop.index(worst_ind))
                        new_pop.append(elite)
                else:
                    worst_ind = max(new_pop, key = lambda x: x.get_fitness())
                    # if elite is better than the worst individual in the population, replace it
                    if elite.get_fitness() < worst_ind.get_fitness():
                        new_pop.pop(new_pop.index(worst_ind))
                        new_pop.append(elite)

            self.individuals = new_pop

            best_indiv = self.best_individual()
            print(f'Best individual in generation {i}: {best_indiv} Fitness: {best_indiv.get_fitness()}')




pop = Population(10, 64, 8)

print(pop)