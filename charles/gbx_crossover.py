from random import sample, random
import itertools
from data.relationships import relationships_matrix
from charles.charles import Individual, Population
from copy import deepcopy

def get_the_best_combination(guests_to_seat, nr_guests_to_fill, table_to_fill, offspring):
    """
    Get the best combination of guests to fill the table, based on the fitness of the table.
    Input:  guests_to_set (set of integers)
            nr_guests_to_fill (integer)
            table_to_fill (list of integers)
            offspring (Individual)
    Returns:
        best_comb: The best combination of guests used to fill the table.
        offspring: The offspring with the best table added.
    """

    # Possible combinations of people to fill the table
    guests_combinations = list(itertools.combinations(guests_to_seat, nr_guests_to_fill))
    print('Guests combinations ', guests_combinations)

    best_fitness = 0
    best_table = None
    best_comb = None

    print('Offspring', offspring)

    for comb in guests_combinations:
        # Add guests to the table to fill
        table_aux = table_to_fill | set(comb)

        # Add table to offspring
        offspring.append_table(table_aux)

        # Calculate table fitness
        table_fitness = offspring.get_table_fitness(-1)
        print('Combination ', comb)
        print('Table fitness ', table_fitness)
        
        if table_fitness >= best_fitness:
            best_fitness = table_fitness
            best_table = table_aux
            best_comb = comb
        
        # Remove table from offspring
        offspring.remove_table(-1)
    
    print('Offspring should be equal', offspring)
    
    # Add table with highest fitness to offspring
    offspring.append_table(best_table)

    print('Offspring after inserting guests', offspring)
    print('Best comb ', best_comb)

    return best_comb, offspring


def get_crossover_point():
    """
    Get the crossover point.
    Returns:
        float: The crossover point.
    """
    # Define constants
    LOWER_BOUND = 1 / 3
    UPPER_BOUND = 2 / 3

    # Generate a random float between 0 and 1
    crossover_point = random()

    # Scale the random number to the desired range
    crossover_point = LOWER_BOUND + (UPPER_BOUND - LOWER_BOUND) * crossover_point

    return crossover_point


def gbx_crossover(parent1, parent2):
    """
    Applies group based crossover to two parents to create an offspring.

    Args:
        parent1 (Individual): An Individual object representing the first parent.
        parent2 (Individual): An Individual object representing the second parent.

    Returns:
        offspring (Individual): An Individual object representing the offspring.
    """
    # Nr of seats per table
    seats_per_table = len(parent1[0])

    # Get the crossover point
    crossover_point = get_crossover_point()

    # Get the number of tables to keep from the first parent
    num_tables_to_keep = int(crossover_point * len(parent1))

    # Get the tables to keep from the first parent and add them to the offspring
    # offspring = sample(deepcopy(parent1).representation, num_tables_to_keep)
    offspring = Individual(sample(deepcopy(parent1).representation, num_tables_to_keep))

    # Get the people of the tables already selected
    seated_guests = {guest for table in offspring for guest in table}
    
    # Get people yet to be seated
    guests_to_seat = set(range(1, len(parent1) * seats_per_table + 1)) - seated_guests

    # Remove the people in the selected tables from the second parent
    parent2_copy = [table.difference(seated_guests) for table in deepcopy(parent2)]

    print("parent1 selected tables")
    print(offspring)
    print("parent2_copy")
    print(parent2_copy)
    print('guests_to_seat')
    print(guests_to_seat)

    # While there are guests left to seat
    while len(guests_to_seat) > 0:

        # Sort the tables of the second parent by size in descending order
        parent2_copy.sort(key=len, reverse=True)

        print('\n')
        print("parent2_copy")
        print(parent2_copy)

        table_to_fill = parent2_copy[0]

        print('table to fill ', table_to_fill)

        print('offspring ', offspring)

        # If table if full, remove it from the second parent copy and add it to the offspring
        if len(table_to_fill) == seats_per_table:
            # Add table to offspring
            offspring.append_table(table_to_fill)

            # Exclude people seated in the table from the people to seat
            guests_to_seat = guests_to_seat.difference(table_to_fill)

            # Remove table from the second parent copy
            parent2_copy.remove(table_to_fill)

            print('offspring ', offspring)
            print('parent2_copy ', parent2_copy)

        # If table is not full, it needs to be filled with people from other tables
        else:
            # Number of empty seats in the table
            nr_guests_to_fill = seats_per_table - len(table_to_fill)
            
            # Exclude people seated in the new table from the people to seat
            guests_to_seat = guests_to_seat.difference(table_to_fill)

            print("guests_to_seat")
            print(guests_to_seat)

            # Get the best combination of guests to fill the table and add it to the offspring
            # Also return the best combination of guests so they can be removed from the people to seat
            best_comb, offspring = get_the_best_combination(guests_to_seat, nr_guests_to_fill, table_to_fill, offspring)
            
            # Remove the people of the combination from the people not selected
            guests_to_seat -= set(best_comb)

            print('Guests to seat after removing best comb ', guests_to_seat)

            # Remove the guests added to table_to_fill from the other tables of parent2
            parent2_copy = [table - set(best_comb) for table in parent2_copy]

            print('parent2_copy after removing best comb ', parent2_copy)

            # Remove table from the second parent
            parent2_copy.pop(0)

            print('parent2_copy after removing table to fill ', parent2_copy)

    return offspring


#ind1 = Individual(frozenset({frozenset({1, 7, 5}), frozenset({6, 3, 8}), frozenset({2, 4, 9}), frozenset({10, 11, 12})}))
#ind2 = Individual(frozenset({frozenset({4, 6, 9}), frozenset({12, 7, 8}), frozenset({10, 3, 5}), frozenset({1, 2, 11})}))

# pop=Population(2,64,8)

# ind1, ind2 = pop.get_individuals()

# a = group_based_crossover(ind1, ind2)
