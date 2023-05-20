import random

def swap_mutation(individual):
    """
    Swap mutation for a GA individual

    Args: individual (Individual): A GA individual from charles.py

    Returns: Individual: Mutated Individual
    """

    table_idx = random.sample(range(len(individual)), 2)

    # Get two guests
    guest1 = individual[table_idx[0]].pop()
    guest2 = individual[table_idx[1]].pop()

    # Swap
    individual.seat_guest(table_idx[0], guest2)
    individual.seat_guest(table_idx[1], guest1)
    
    return individual

def merge_and_split(individual):

    table_idx = random.sample(range(len(individual)), 2) #selects two random tables
    mixed_tables= individual[table_idx[0]] + individual[table_idx[1]]

    fst_table = random.sample(mixed_tables, len(individual[0]))
    snd_table = [person for person in mixed_tables if person not in fst_table]

    individual[table_idx[0]]= fst_table
    individual[table_idx[1]] = snd_table

    return individual

def the_hop(individual):
    # TODO
    """
    The Chega Pra Lá operator, also known as the shift operator, shifts everyone in the tables one
    seat to the left or to the right.
    
    """
    return individual

def dream_team(individual):
    """
    escolher as pessoas com maior relação nas duas mesas e mantê-las
    shuffle das outras
    """
    return
