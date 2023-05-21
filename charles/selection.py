from random import choice, uniform, choices

def fps(population):
    """
    Fitness proportionate selection implementation.

    Args:
        population (Population): The population we want to select from.

    Returns:
        Individual: selected individual.
    """
    # sum total fitness
    total_fitness = sum([i.get_fitness() for i in population])

    # get a random number between 0 and total fitness (mark on the line)
    mark = uniform(0, total_fitness)

    position = 0

    # find individual that has mark
    for i in population:
        position += i.get_fitness()
        if position >= mark:
            return i
    
def rank_selection(population):
    sorted_population = sorted(population, key = lambda ind: ind.get_fitness(), reverse = True)

    ranks = range(1, len(sorted_population) + 1)

    selection_probs = [1 - (rank / sum(ranks)) for rank in ranks]

    selected_individual = choices(sorted_population, weights = selection_probs, k = 1)[0]

    return selected_individual

def tournament_selection(population, tournament_size = 4):
    """
    Tournament selection implementation.

    Args:
        population (Population): The population we want to select from.
        tournament_size (int, optional): Size of the tournament.

    Returns:
        Individual: selected individual.
    """
    
    # Select 'size' random individuals with repetition
    tournament = [choice(population.get_individuals()) for _ in range(tournament_size)]

    return max(tournament, key = lambda x: x.get_fitness())