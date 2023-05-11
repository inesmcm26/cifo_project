from random import shuffle, sample, choice, random
from copy import deepcopy

class Individual:
    """
      Possible solution to an optimization problem
    """
    # we always initialize
    def __init__(self, representation = None, size = None, valid_set = None, replacement = True):
        # valid set is a list of possible values on the representation
        # size is the size of the binary number for example

        if representation is None:
            # individual will be chosen from the valid_set with a specific size

            if replacement:
                self.representation = [choice(valid_set) for _ in range(size)]
            else:
                self.representation = sample(valid_set, size)

        # if we pass an argument like Individual(my_path)
        else:
            self.representation = representation

    def __repr__(self):
        """
         Solution representation
        """
        return self.representation

    def __str__(self):
        """
         Solution string representation
        """
        return str(self.representation)
    
    def __len__(self):
        return len(self.representation)

    def __setitem__(self, position, value):
        self.representation[position] = value
    
    def __getitem__(self, position):
        return self.representation[position]
    
    def index(self, value):
        return self.representation.index(value)
    
    def get_neighbours():
        raise Exception('You need to implement this method')
    
    def get_fitness():
        """
         Solution fitness
        """
        raise Exception('You need to implement this method')

class Population:
    """
      Search Space: set of individuals
    """
    def __init__(self, size, optim, type_of_individ,  **kwargs):

        self.type_of_individ = type_of_individ

        # population size
        self.size = size

        # defining the optimization problem as a minimization or maximization problem
        self.optim = optim

        self.individuals = []

        # appending the population with all possible individuals (all possible solutions)
        for _ in range(size):
            self.individuals.append(
                type_of_individ(
                    size = kwargs['sol_size'],
                    valid_set = kwargs['valid_set'],
                    replacement = kwargs['replacement']
                )
            )

    def __len__(self):
        return len(self.individuals)

    def __getitem__(self, position):
        return self.individuals[position]

    def get_type_of_individ(self):
        return self.type_of_individ
    
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