from random import random, shuffle
from copy import deepcopy
import os
import sys
import time

# Add the parent folder to the sys.path
parent_folder = os.path.abspath(os.path.join(os.getcwd(), ".."))
sys.path.append(parent_folder)

# Import the variable from data.py
from data import relationships

# Access the variable
relationships_matrix = relationships.relationships_matrix


class Individual:
    """
      Possible solution to an optimization problem
    """
    # we always initialize
    def __init__(self, arrangement = None):

        representation = []

        # TODO: justificar isto
        if arrangement is not None:
            # it is a frozenset of frozensets
            if not isinstance(arrangement, list):
                # arragement is a frozenset with frozensets of guests
                # let's covert it into a list of sets
                arrangement = list(arrangement)
                representation = [set(table) for table in arrangement]
            # it is already a list of sets
            else:
                representation = arrangement

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
        for table_idx in range(len(self.representation)):
            fitness += self.get_table_fitness(table_idx)

        return fitness

    def get_table_fitness(self, table_idx):
        """
         Table fitness
        """
        table_fitness = 0

        table = deepcopy(self.representation[table_idx])

        while len(table) > 1:
            guest = table.pop()

            for other_guest in table:
                table_fitness += relationships_matrix[guest - 1][other_guest - 1]

        return table_fitness

    def get_guest_fitness(self, guest, table_idx):
        """
         Guest fitness
        """


        guest_fitness = 0

        table = self.representation[table_idx]
        
        if guest not in table:
            raise Exception('Guest not in table')

        for seated_guest in table:
            if seated_guest != guest:
                guest_fitness += relationships_matrix[guest - 1][seated_guest - 1]
        
        return guest_fitness
    
    def get_best_table_mate(self, guest, table_idx):
        """
        Get the guest with the best relationship with the guest
        """
        table_matrix = relationships_matrix[guest - 1,[other_guest - 1
                                                for other_guest in self.representation[table_idx] if other_guest != guest]]

        return max(table_matrix)
    
    
    def seat_guest(self, guest, table_idx):
        """
        Add guest to the table set
        """
        self.representation[table_idx].add(guest)

    def remove_guest(self, guest, table_idx):
        """
        Remove guest from the table set
        """
        self.representation[table_idx].remove(guest)

    def append_table(self, table):
        """
        Adds a table to the end of the list of tables
        """
        self.representation.append(table)

    def remove_table(self, table_idx):
        """
        Removes a table from the list of tables
        """
        self.representation.pop(table_idx)

    def __getitem__(self, table_idx):
        return self.representation[table_idx]
        
    def __setitem__(self, table_idx, table):
        """
        Add table set to list of tables
        """
        self.representation[table_idx] = table


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
            shuffle(guests)

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
        return self.pop_size

    def get_individuals(self):
        return self.individuals

    def best_individual(self):
        """
         Get the best individual of the population (Maximization Problem)
        """
        return deepcopy(sorted(self.individuals, key = lambda x: x.get_fitness(), reverse = True)[0])
    
    def evolve(self, n_generations, xo_prob, mut_prob, select, mutate, crossover, elitism):
        """
         Evolve the population: get generation after generation until the end of
         the evolutionary process
        """

        t0 = time.time()

        fitness_history = []

        for i in range(n_generations):

            new_pop = []

            if elitism:
                # keep the best individual
                elite = self.best_individual()

            while len(new_pop) < self.pop_size:
                p1, p2 = select(self), select(self)

                if random() < xo_prob:
                    offspring1, offspring2 = crossover(p1, p2)
                else:
                    # TODO Falar berfin: replication = copy of the parents
                    offspring1, offspring2 = deepcopy(p1), deepcopy(p2)

                assert(len(offspring1[0]) == 8)
                
                if offspring2 is not None:
                    assert(len(offspring2[0]) == 8)

                if random() < mut_prob:
                    offspring1 = mutate(offspring1)
                    assert(len(offspring1[0]) == 8)
                # Check if crossover produced two offsprings
                if offspring2 is not None and random() < mut_prob:
                    offspring2 = mutate(offspring2)
                    assert(len(offspring2[0]) == 8)

                new_pop.append(offspring1)
                
                # to check if we can insert both of the individuals or only one
                if offspring2 is not None and len(new_pop) < self.pop_size:
                    new_pop.append(offspring2)
                
            if elitism:
                worst_ind = min(new_pop, key = lambda x: x.get_fitness())
                
                # if elite is better than the worst individual in the population, replace it
                if elite.get_fitness() > worst_ind.get_fitness():
                    new_pop.pop(new_pop.index(worst_ind))
                    new_pop.append(elite)

            self.individuals = new_pop

            best_indiv = self.best_individual()
            print(f'Best individual in generation {i}: {best_indiv} Fitness: {best_indiv.get_fitness()}')

            fitness_history.append(best_indiv.get_fitness())


        t1 = time.time()

        print(f'Execution time: {t1 - t0} seconds')

        return fitness_history