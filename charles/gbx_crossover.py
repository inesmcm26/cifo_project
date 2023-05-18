from random import sample, random
import itertools
from relationships import relationships_matrix
from charles import Individual, Population


def get_the_best_combination(persons_not_in_selected_tables, nr_persons_to_fill, table_to_fill):
    """
    Get the best combination of persons to fill the table, based on the fitness of the table.
    Returns:
        tuple: The best combination of persons to fill the table.
    """

    # Possible combinations of persons to fill the table
    persons_combinations = list(itertools.combinations(persons_not_in_selected_tables, nr_persons_to_fill))

    # Fitness history of the combinations
    fitness_history = {}

    # Test the fitness of persons from other tables
    for comb in persons_combinations:
        # Test the fitness of updated table
        table_fitness = sum(
            [relationships_matrix[guest - 1][other_guest - 1] for guest in comb for other_guest in comb if
             guest != other_guest])
        # Save the fitness of the combinations
        fitness_history[comb] = table_fitness

    # Get the combination with the best fitness
    best_comb = max(fitness_history, key=fitness_history.get)

    return best_comb


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


def group_based_crossover(parent1, parent2):
    """
    Applies group based crossover to two parents to create an offspring.

    Args:
        parent1 (Individual): An Individual object representing the first parent.
        parent2 (Individual): An Individual object representing the second parent.

    Returns:
        offspring (Individual): An Individual object representing the offspring.
    """

    # Get the crossover point
    crossover_point = get_crossover_point()

    # Get the number of tables to keep from the first parent
    num_tables_to_keep = int(crossover_point * len(parent1))

    # Get the tables to keep from the first parent
    tables_to_keep = sample(parent1.representation, num_tables_to_keep)

    # Get the persons of the tables already selected
    persons_in_selected_tables = {person for table in tables_to_keep for person in table}

    # Get the persons not in the selected tables
    persons_not_in_selected_tables = {person for table in parent1.representation for person in table if
                               person not in persons_in_selected_tables}

    # Remove the persons in the selected tables from the second parent
    parent2_copy = [table.difference(persons_in_selected_tables) for table in parent2.representation]

    # Create a new offspring
    offspring = list(tables_to_keep)

    # Full table size
    full_table_size = len(parent1.representation[0])

    print("parent1 selected tables")
    print(tables_to_keep)
    print("parent2")
    print(parent2)

    # While there are persons not selected to fill the offspring
    while len(persons_not_in_selected_tables) > 0:

        # Sort the tables of the second parent by size
        parent2_copy.sort(key=len)

        print('\n')
        print("parent2_copy")
        print(parent2_copy)

        # Get the next table to fill
        table_to_fill = next((t for t in parent2_copy if len(t) < full_table_size and len(t) > 0), None)

        print("table_to_fill")
        print(table_to_fill)

        # If there is no table available to fill, break the loop
        if not table_to_fill:
            break

        # Necessary persons to fill the table
        nr_persons_to_fill = full_table_size - len(table_to_fill)

        # Exclude from the not selected persons the persons in the table to fill
        persons_not_in_selected_tables = persons_not_in_selected_tables.difference(table_to_fill)

        print("persons_not_in_selected_tables")
        print(persons_not_in_selected_tables)

        # Get the best combination of persons to fill the table
        best_comb = get_the_best_combination(persons_not_in_selected_tables, nr_persons_to_fill, table_to_fill)

        # Create the new table
        new_table = set(best_comb) | table_to_fill

        print("new_table")
        print(new_table)

        # Remove the persons of the combination from the persons not selected
        persons_not_in_selected_tables -= set(best_comb)

        # Remove the persons of the combination from the old table of second parent copy
        parent2_copy = [p - set(best_comb) for p in parent2_copy]

        # Add the persons of the combination to the new table of the second parent copy
        parent2_copy[parent2_copy.index(table_to_fill)] = new_table

        print("parent2_copy")
        print(parent2_copy)

        # Add the new table to the offspring
        offspring.append(new_table)
        print("offspring")
        print(offspring)

    return Individual(offspring)


#ind1 = Individual(frozenset({frozenset({1, 7, 5}), frozenset({6, 3, 8}), frozenset({2, 4, 9}), frozenset({10, 11, 12})}))
#ind2 = Individual(frozenset({frozenset({4, 6, 9}), frozenset({12, 7, 8}), frozenset({10, 3, 5}), frozenset({1, 2, 11})}))

pop=Population(2,64,8)

ind1, ind2 = pop.get_individuals()

a = group_based_crossover(ind1, ind2)
