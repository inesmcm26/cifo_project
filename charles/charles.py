import os
import sys
# Add the parent folder to the sys.path to acess other files in the project
parent_folder = os.path.abspath(os.path.join(os.getcwd(), ".."))
sys.path.append(parent_folder)

from random import random, shuffle
from copy import deepcopy
from data import relationships

# Save data in a global variable
relationships_matrix = relationships.relationships_matrix

class Individual:
    """
    Possible solution to the optimization problem
    """
    def __init__(self, arrangement = None):
        """
        Initialize the individual and its representation (list of sets)

        Args:
            arrangement
                (list): List of sets, where each set represents a table
                (frozenset): Frozenset of frozensets, where each frozenset represents a table
                (None): Create an empty arrangement
        """
        representation = []

        # If some table arrangement is given, use it
        # Else, create an empty arrangement
        if arrangement is not None:
            # To handle population initialization, where the arrangement is a frozenset of frozensets
            if not isinstance(arrangement, list):
                arrangement = list(arrangement)
                representation = [set(table) for table in arrangement]
            # When a list of sets is given
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
         Solution fitness: sum of the fitness of each table
        """
        fitness = 0
        for table_idx in range(len(self.representation)):
            fitness += self.get_table_fitness(table_idx)

        return fitness

    def get_table_fitness(self, table_idx):
        """
         Table fitness: sum of pairwise relationships between guests in the table
        """
        table_fitness = 0

        table = deepcopy(self.representation[table_idx])

        while len(table) > 1:
            # Get a guest from the table and remove it to ensure that
            # each relationship is only counted once
            guest = table.pop()

            # Sum the relationships between the guest and the other guests in the table
            for other_guest in table:
                table_fitness += relationships_matrix[guest - 1][other_guest - 1]

        return table_fitness

    def get_guest_fitness(self, guest, table_idx):
        """
         Guest fitness: sum of relationships between guest and other guests in the table
        """
        guest_fitness = 0

        table = self.representation[table_idx]
        
        if guest not in table:
            raise Exception('Guest not in table')

        for seated_guest in table:
            if seated_guest != guest:
                guest_fitness += relationships_matrix[guest - 1][seated_guest - 1]
        
        return guest_fitness
    
    def get_guest_max_relationship(self, guest, table_idx):
        """
        Get the best pairwise relationship of a given guest in a table
        """

        if guest not in self.representation[table_idx]:
            raise Exception('Guest not in table')
        
        table_matrix = relationships_matrix[guest - 1,[other_guest - 1
                                                for other_guest in self.representation[table_idx]
                                                if other_guest != guest]]

        return max(table_matrix)
    
    def seat_guest(self, guest, table_idx):
        """
        Add guest to the table set
        """
        if guest in self.representation[table_idx]:
            raise Exception('Guest already in table')
        
        self.representation[table_idx].add(guest)

    def remove_guest(self, guest, table_idx):
        """
        Remove guest from a given table
        """
        if guest not in self.representation[table_idx]:
            raise Exception('Guest not in table')
        
        self.representation[table_idx].remove(guest)

    def append_table(self, table):
        """
        Appends a table to the end of the list of tables
        """
        self.representation.append(table)

    def remove_table(self, table_idx):
        """
        Removes a table from the list of tables
        """
        self.representation.pop(table_idx)

    def __getitem__(self, table_idx):
        """
        Get table set from list of tables
        """
        return self.representation[table_idx]
        
    def __setitem__(self, table_idx, table):
        """
        Add table set to list of tables
        """
        self.representation[table_idx] = table


class Population:
    """
      Search Space of possible solutions
    """
    def __init__(self, pop_size, nr_guests, nr_tables):

        self.nr_guests = nr_guests

        self.nr_tables = nr_tables

        self.guests_per_table = nr_guests // nr_tables

        self.pop_size = pop_size

        self.individuals = []

        # --------------------- Generate a random population --------------------- #

        guests = [i for i in range(1, nr_guests + 1)]
        
        # Population is a set of unique arrangements
        pop = set()

        while len(pop) < pop_size:
            # Shuffle guests
            shuffle(guests)

            # Create a set of tables, where each table is a set of guests
            tables = frozenset(frozenset(guests[i:i + self.guests_per_table]) for i in range(0, len(guests), self.nr_tables))

            # Add the arrangement to the population. If the arrangement is
            # already in the population, it will not be added because pop is a set
            # This prevents the generation of redundant arrangements
            pop.add(tables)

        # Convert the arrangements to Individuals
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

    def best_individuals(self, n = 5):
        """
        Get the best n individual of the population
        (Note: only works for maximization problems)
        """
        best_n = sorted(self.individuals, key = lambda x: x.get_fitness(), reverse = True)[:n]
        
        return [deepcopy(individual) for individual in best_n]

    def best_individual(self):
        """
        Get the best individual of the population
        (Note: only works for maximization problems)
        """
        return deepcopy(max(self.individuals, key = lambda x: x.get_fitness()))
    
    def evolve(self, n_generations, xo_prob, mut_prob, select, mutate, crossover, elitism = True, elite_size = 5):

        fitness_history = []

        for i in range(n_generations):

            new_pop = []

            if elitism:
                # Save the best individuals from previous generation
                elite = self.best_individuals(elite_size)

            while len(new_pop) < self.pop_size:
                # Select two parents
                p1, p2 = select(self), select(self)

                # Crossover
                if random() < xo_prob:
                    # Note: If crossover returns only one offspring, the second one is None
                    offspring1, offspring2 = crossover(p1, p2)
                else:
                    offspring1, offspring2 = deepcopy(p1), deepcopy(p2)

                # Mutation
                if random() < mut_prob:
                    offspring1 = mutate(offspring1)
                
                if offspring2 is not None and random() < mut_prob:
                    offspring2 = mutate(offspring2)

                new_pop.append(offspring1)
                
                # Check if there is still space in the population for the second offspring
                if offspring2 is not None and len(new_pop) < self.pop_size:
                    new_pop.append(offspring2)
            
            # Elitism
            if elitism:
                # Save the worst individuals from the current generation in a list of tuples
                # The second element of the tuple (True) indicates that the Individual belongs
                # to the new population
                worst_ind = [(ind, True) for ind in sorted(new_pop, key = lambda x: x.get_fitness())[:elite_size]]

                # Save the best individuals from the previous generation in a list of tuples
                # The second element of the tuple (False) indicates that the Individual belongs
                # to the previous population
                elite = [(ind, False) for ind in elite]

                # Join the best from the previous generation with the worst from the new onw and sort them
                elite_aux = sorted(elite + worst_ind, key = lambda x: x[0].get_fitness(), reverse = True)

                # Get best Individuals to keep
                individuals_to_keep = elite_aux[:elite_size]
                # Get worst Individuals to discard
                individuals_to_discard = elite_aux[elite_size:]
                
                # Remove necessary individuals from the new population
                for (individual, in_pop) in individuals_to_discard:
                    if in_pop:
                        new_pop.pop(new_pop.index(individual))
                
                # Add the new individuals from elite to the new population
                for (individual, in_pop) in individuals_to_keep:
                    if not in_pop:
                        new_pop.append(individual)

            # Replace the old population with the new one
            self.individuals = new_pop

            best_indiv = self.best_individual()
            print(f'Best individual in generation {i}: {best_indiv} Fitness: {best_indiv.get_fitness()}')

            # Save the best fitness of the generation
            fitness_history.append(best_indiv.get_fitness())

        return fitness_history, best_indiv