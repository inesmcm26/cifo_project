import random
from copy import deepcopy
from data.relationships import relationships_matrix

class Individual:
    """
      Possible solution to an optimization problem
    """
    # we always initialize
    def __init__(self, arrangement = None):

        representation = []
        
        # arragement is a frozenset with frozensets of guests
        # let's covert it into a list of sets
        arrangement = list(arrangement)
        representation = [set(table) for table in arrangement]

        self.representation = representation

    def __str__(self):
        """
         Solution string representation
        """
        return str(self.representation)
    
    def __len__(self):
        """
         Returns de number of tables
        """
        return len(self.representation)
    
    def get_fitness(self):
        """
         Solution fitness
        """
        fitness = 0
        for table_nr in range(len(self.representation)):
            fitness += self.get_table_fitness(table_nr)

        return fitness

    def get_table_fitness(self, table_nr):
        """
         Table fitness
        """
        table_fitness = 0

        table = self.representation[table_nr].copy()

        while len(table) > 1:
            guest = table.pop()

            for other_guest in table:
                table_fitness += relationships_matrix[guest - 1][other_guest - 1]

        return table_fitness

    def get_guest_fitness(self, guest, table_nr):
        """
         Guest fitness
        """

        guest_fitness = 0

        table = self.representation[table_nr]

        for seated_guest in table:
            if seated_guest != guest:
                guest_fitness += relationships_matrix[guest - 1][seated_guest - 1]
        
        return guest_fitness


class Population:
    """
      Search Space: set of individuals
    """
    def __init__(self, pop_size, nr_guests, nr_tables):

        self.nr_guests = nr_guests

        self.nr_tables = nr_tables

        self.guests_per_table = nr_guests // nr_tables

        self.pop_size = pop_size

        self.individuals = []

        guests = [i for i in range(1, nr_guests + 1)]

        pop = set()

        while len(pop) < pop_size:
            random.shuffle(guests)

            tables = frozenset(frozenset(guests[i:i + self.guests_per_table]) for i in range(0, len(guests), self.nr_tables))

            pop.add(tables)

        for arrangement in pop:
            self.individuals.append(Individual(arrangement))
    
    def __str__(self):
        """
         Population string representation
        """
        return '\n'.join([str(individual) for individual in self.individuals])

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

                new_pop.append(Individual(representation = offspring1))
                
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