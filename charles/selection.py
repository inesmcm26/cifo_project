from random import choice, uniform

def fitness_proportionate_selection(population):
    """
    Fitness proportionate selection implementation.

    Args:
        population (Population): The population we want to select from.

    Returns:
        Individual: selected individual.
    """
    if population.optim == 'max':
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
            
    elif population.optim == "min":
        raise NotImplementedError

    else:
        raise Exception("No optimization specified (min or max).")
    
def rank_selection(population):
    """
    Rank selection implementation.
    """

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

    if population.get_optim() == 'max':
        return max(tournament, key = lambda x: x.get_fitness())
    else:
        return min(tournament, key = lambda x: x.get_fitness())