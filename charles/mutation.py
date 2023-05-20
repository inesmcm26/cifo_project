from random import sample, choice

def swap_mutation(individual):
    """
    Swap mutation for a GA individual

    Args: individual (Individual): A GA individual from charles.py

    Returns: Individual: Mutated Individual
    """

    table_idx = sample(range(len(individual)), 2)

    # Get two guests
    guest1 = individual[table_idx[0]].pop()
    guest2 = individual[table_idx[1]].pop()

    # Swap
    individual.seat_guest(table_idx[0], guest2)
    individual.seat_guest(table_idx[1], guest1)
    
    return individual

def merge_and_split(individual):
"""
    Merge and split mutation for a GA individual

    Args: individual (Individual): A GA individual from charles.py

    Returns: Individual: Mutated Individual
"""

    # Selects two random tables
    table_idx = sample(range(len(individual)), 2)

    # Merges the two tables
    mixed_tables= individual[table_idx[0]] | individual[table_idx[1]]

    # Splits the merged table into two new tables
    fst_table = sample(list(mixed_tables), len(individual[0]))
    snd_table = [person for person in mixed_tables if person not in fst_table]

    # Updates the individual
    individual[table_idx[0]]= set(fst_table)
    individual[table_idx[1]] = set(snd_table)

    return individual

def the_hop(individual):
    """
    The Hop operator, also known as the shift operator, shifts everyone in the tables one
    seat to the right.

    """

    # Create a list to keep track of persons that have been moved
    moved_persons = []

    # Iterate over each table
    for i in range(len(individual)):
        current_table = individual[i]

        # Filter out persons that have already been moved
        available_persons = list(current_table - set(moved_persons))

        # Choose a random person from the available persons in the current table
        random_person = choice(available_persons)

        # Remove the random person from the current table
        current_table.remove(random_person)

        # Add the random person to the moved_persons list
        moved_persons.append(random_person)

        # Move the random person to the next person
        next_table_index = (i + 1) % len(individual)
        next_table = individual[next_table_index]
        next_table.add(random_person)

    return individual

def dream_team(individual):
    """
    escolher as pessoas com maior relação nas duas mesas e mantê-las
    shuffle das outras
    """
    return


sets_list = [{1, 2, 3}, {4, 5, 6}, {7, 8, 9}]

muta = merge_and_split(sets_list)

print(muta)