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
    individual[table_idx[0]].add(guest2)
    individual[table_idx[1]].add(guest1)
    
    return individual

def merge_and_split(individual):
    # TODO
    """
    The Merge and Split, also known as Division and Combination operator,
    works in two phases. In the first stage, it selects two groups and transforms
    them into a single one. Then, in the second stage, it picks a group to distribute
    its items between two distinct groups.
    """
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
