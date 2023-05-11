from random import randint, sample, uniform

def single_point_crossover(parent1, parent2):
    """
    Implementation of single point crossover.

    Args:
        p1 (Individual): First parent for crossover.
        p2 (Individual): Second parent for crossover.

    Returns:
        Individuals: Two offspring, resulting from the crossover.
        
    """
    xo_point = randint(1, len(parent1) - 1)

    offspring1 = parent1[:xo_point] + parent2[xo_point:]
    offspring2 = parent2[:xo_point] + parent1[xo_point:]

    return offspring1, offspring2

def cycle_crossover(parent1, parent2):

    offspring1 = [None] * len(parent1)
    offspring2 = [None] * len(parent1)

    while None in offspring1:
        idx = offspring1.index(None)

        val1 = parent1[idx]
        val2 = parent2[idx]

        while val1 != val2:
            # set values on the offspring
            offspring1[idx] = parent1[idx]
            offspring2[idx] = parent2[idx]

            # update val2 to the value on the new index
            val2 = parent2[idx]

            # get new position on parent 1 that correspond to the value on parent 2
            idx = parent1.index(val2)


        for element in offspring1:
            if element is None:
                idx = offspring1.index(element)
                if offspring1[idx] is None:
                    offspring1[idx] = parent2[idx]
                    offspring2[idx] = parent1[idx]

    return offspring1, offspring2


def partially_matched_crossover(parent1, parent2):

    xo_points = sample(range(len(parent1)), 2)
    xo_points.sort()


    def pmx_offspring(parent1, parent2):
        offspring = [None for _ in range(len(parent1))]

        # get the segment from the first parent
        offspring[xo_points[0]:xo_points[1]] = parent1[xo_points[0]:xo_points[1]]
        
        # get the numbers that do not belong to the segments of both parents
        # numbers of the segment that are unique for parent2
        z = set(parent2[xo_points[0]:xo_points[1]]) - set(parent1[xo_points[0]:xo_points[1]])

        for num in z:
            temp = num

            # get the index of the mirror number on the other parent
            idx = parent2.index(parent1[parent2.index(temp)])
            while offspring[idx] is not None:
                temp = idx
                idx = parent2.index(parent1[temp])
            offspring[idx] = num
        
        while None in offspring:
            idx = offspring.index(None)
            offspring[idx] = parent2[idx]
        
        return offspring

    
    return pmx_offspring(parent1, parent2), pmx_offspring(parent2, parent1)

def arithmetic_crossover(parent1, parent2):
    """
    Arithmetic crossover for real-valued individuals.

    Args:
        p1 (Individual): First parent for crossover.
        p2 (Individual): Second parent for crossover.

    Returns:
        Individuals: Two offspring, resulting from the crossover.
        
    """
    offspring1 = [None] * len(parent1)
    offspring2 = [None] * len(parent1)

    alpha = uniform(0, 1)

    for i in range(len(parent1)):
        offspring1[i] = alpha * parent1[i] + (1 - alpha) * parent2[i]
        offspring2[i] = alpha * parent2[i] + (1 - alpha) * parent1[i]

    return offspring1, offspring2


if __name__ == '__main__':
    # p1 = [0, 0, 0, 0]
    # p2 = [1, 1, 1, 1]
    # print(single_point_crossover(p1, p2))

    # p1 = [9, 8, 4, 5, 6, 7, 1, 3, 2, 10]
    # p2 = [8, 7, 1, 2, 3, 10, 9, 5, 4, 6]
    # print(partially_matched_crossover(p1, p2))

    p1, p2 = [0.1, 0.3, 0.1], [0.5, 0.2, 0.5]
    print(arithmetic_crossover(p1, p2))

