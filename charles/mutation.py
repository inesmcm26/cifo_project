from random import randint, sample


def non_adjacent_swap_mutation(individual):
    """
    Swap mutation for a GA individual

    Args: individual (Individual): A GA individual from charles.py

    Returns: Individual: Mutated Individual
    """
    # TODO
    # Select two random tables
    # Select n random individuals -> swap them
    mutation_idxs = sample(range(len(individual)), 2)

    individual[mutation_idxs[0]], individual[mutation_idxs[1]] = individual[mutation_idxs[1]], individual[mutation_idxs[0]]

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

def chega_pra_la(individual):
    # TODO
    """
    The Chega Pra Lá operator, also known as the shift operator, shifts everyone in the tables one
    seat to the left or to the right.
    
    """
    return individual


def thrors(individual):
    """
    Thrors Mutation
    Three genes are chosen randomly which shall take the different positions not
    necessarily successive i < j < l. the gene of the position i becomes in the position j
    and the one who was at this position will take the position l and the gene that has
    held this position takes the position i.

    Tipo 1 2 3 4 5 6

    Seleciona 1 2 4 e 6 e troca a ordem deles

    6 4 FIXO(3) 2 FIXO(5) 1

    Kinda swap mutation de dentro para fora
    """
