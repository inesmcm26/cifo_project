from random import sample, random, randint
import itertools
from collections import Counter
from copy import deepcopy

from charles.charles import Individual


def get_best_combination(guests_to_seat, nr_guests_to_fill, table_to_fill, offspring):
    """
    Auxiliary function for GBX crossover.

    Given a table with empty seats, it finds the best combination of guests to fill the table
    by finding the combination that maximizes the fitness of the table. In the end, the best
    combination is added to the table and the table is added to the offspring.

    Input:  guests_to_set (set of int)
            nr_guests_to_fill (int)
            table_to_fill (list of int)
            offspring (Individual)
    Returns:
        best_comb (list of int): The best combination of guests used to fill the table.
        offspring (Individual): The offspring after the table is filled with the best combination.
    """

    # Possible combinations of people to fill the table
    guests_combinations = list(itertools.combinations(guests_to_seat, nr_guests_to_fill))

    best_fitness = -100000
    best_table = None
    best_comb = None

    for comb in guests_combinations:
        # Add guests to the table to fill
        table_aux = table_to_fill | set(comb)

        # Append table to offspring
        offspring.append_table(table_aux)

        # Calculate table fitness
        table_fitness = offspring.get_table_fitness(-1)
        
        if table_fitness >= best_fitness:
            best_fitness = table_fitness
            best_table = table_aux
            best_comb = comb
        
        # Remove table from offspring
        offspring.remove_table(-1)
    
    # Add table with highest fitness to offspring
    offspring.append_table(best_table)

    return best_comb, offspring

def gbx_crossover(p1, p2):
    """
    Group based crossover (GBX) implementation.

    The GBX starts by selecting between 1/3 and 2/3 of the tables from the
    first parent and sets them in the offspring. The guests seated in this
    step are removed from the second parent. Then, it fills the remaining
    tables with the guests from the second parent in a greedy way.

    At each iteration, the tables of the second parent are sorted by number
    of empty seats. The first table is filled with the best combination of
    guests remaining in other tables. Once the table is filled, it is passed
    to the offspring.

    Args:
        p1 (Individual): First parent for crossover.
        p2 (Individual): Second parent for crossover.

    Returns:
        offspring (Individual): One offspring resulting from the crossover.
    """
    seats_per_table = len(p1[0])

    # ----------------------- Selection of tables from p1 ----------------------- #
    # Define constants
    LOWER_BOUND = 1 / 3
    UPPER_BOUND = 2 / 3

    # Generate a random float between 0 and 1
    tables_pct = random()

    # Scale the random number to the desired range
    tables_pct = LOWER_BOUND + (UPPER_BOUND - LOWER_BOUND) * tables_pct

    # Get the number of tables to keep from the first p
    num_tables_to_keep = int(tables_pct * len(p1))

    # Get the tables to keep from the first parent and add them to the offspring
    offspring = Individual(sample(deepcopy(p1).representation, num_tables_to_keep))

    # Save the guests seated guests and the guests yet to seat
    seated_guests = {guest for table in offspring for guest in table}
    guests_to_seat = set(range(1, len(p1) * seats_per_table + 1)) - seated_guests

    # Remove seated guests from the second parent
    p2_remaining = [table.difference(seated_guests) for table in deepcopy(p2)]

    # ----------------------- Filling of tables from p2 ----------------------- #

    # While there are still guests left to seat
    while len(guests_to_seat) > 0:

        # Sort the tables of the second parent by number of empty seats
        p2_remaining.sort(key=len, reverse=True)

        # Get the first table to be filled
        table_to_fill = p2_remaining[0]

        # Remove guests seated in that table from the guests yet to be seated
        guests_to_seat = guests_to_seat.difference(table_to_fill)

        # If table if full, remove it from the second parent and add it to the offspring
        if len(table_to_fill) == seats_per_table:
            offspring.append_table(table_to_fill)
            p2_remaining.remove(table_to_fill)

        # If table is not full, it needs to be filled with guests from other tables
        else:
            # Number of empty seats in the table
            nr_guests_to_fill = seats_per_table - len(table_to_fill)

            # Get the best combination of guests to fill the table and add it to the offspring
            # Also return the best combination of guests so they can be removed from the guests to seat
            best_comb, offspring = get_best_combination(guests_to_seat, nr_guests_to_fill, table_to_fill, offspring)

            # Remove the seated guests from the guests to seat
            guests_to_seat -= set(best_comb)

            # Remove the seated guests from the other tables of p2
            p2_remaining = [table - set(best_comb) for table in p2_remaining]

            # Remove table from the p2
            p2_remaining.pop(0)

    return offspring, None

def eager_breeder_crossover(p1, p2):
    """
    Eager Breeder Crossover (EBC) implementation.

    The Eager Breeder Crossover (EBC) starts by sorting the tables of each parent
    by fitness. Then, it iteratively adds the table with the highest fitness to
    the offspring until the offspring has the same number of tables as the parents.

    In the end of this phase, each guest may be seated in more than one table, one
    table or no table. A repair phase is then applied to the offspring to remove
    repeated guests from the tables where they contribute the least to fitness and
    replace them with guests that are not seated yet.

    Args:
        p1 (Individual): First parent for crossover.
        p2 (Individual): Second parent for crossover.

    Returns:
        offspring (Individual): One offspring resulting from the crossover.
    """
    
    # Initialize pointers
    p1_idx = 0
    p2_idx = 0

    # Sort parents by table fitness
    p1.representation = sorted(p1, key=lambda table: p1.get_table_fitness(p1.representation.index(table)), reverse=True)
    p2.representation = sorted(p2, key=lambda table: p2.get_table_fitness(p2.representation.index(table)), reverse=True)

    # Initialize offspring
    offspring = Individual(arrangement = None)

    guests_per_table = len(p1[0])
    nr_guests = len(p1) * guests_per_table

    # ------------------------- Collection phase ------------------------- #

    # Add tables with best fitness until child has the correct number of tables
    while(len(offspring) < len(p1)):
        fit_table1 = p1.get_table_fitness(p1_idx)
        fit_table2 = p2.get_table_fitness(p2_idx)
        if fit_table1 >= fit_table2:
            offspring.append_table(deepcopy(p1[p1_idx]))
            p1_idx += 1
        else:
            offspring.append_table(deepcopy(p2[p2_idx]))
            p2_idx += 1

        
    # --------------------------- Repair phase --------------------------- #

    # Count the occurrences of each guest in the tables
    guest_counts = Counter(guest for table in offspring for guest in table)

    # Get the guests that are seated more than once
    repeated_guests = {guest for guest, count in guest_counts.items() if count > 1}

    # Remove guest from table where he contributed the least to fitness
    for guest in repeated_guests:
        # To save guest fitness in each table
        guest_fitnesses = []
        tables_idx = []

        for table_idx, table in enumerate(offspring):
            if guest in table:
                # Get contribution of guest to table fitness
                guest_fitnesses.append(offspring.get_guest_fitness(guest, table_idx))

                # Save table index
                tables_idx.append(table_idx)


        # Remove guest from the table where it contributes the less to fitness
        if guest_fitnesses[0] >= guest_fitnesses[1]:
            offspring[tables_idx[1]].remove(guest)
        else:
            offspring[tables_idx[0]].remove(guest)

    
    # Fill the empty seats with guests that are not seated yet
    not_seated_guests = [guest for guest in range(1, nr_guests + 1) if guest not in guest_counts]

    for table_idx in range(len(offspring)):
        
        while len(offspring[table_idx]) < guests_per_table:
            max_fitness = -100000
            guest_max_fitness = None

            for guest in not_seated_guests:
                # Seat guest at the table
                offspring.seat_guest(guest, table_idx)

                # Get table fitness
                table_fitness = offspring.get_table_fitness(table_idx)

                if table_fitness > max_fitness:
                    max_fitness = table_fitness
                    guest_max_fitness = guest

                # Remove guest from the table
                offspring.remove_guest(guest, table_idx)

            # Seat the guest that has the highest fitness
            offspring.seat_guest(guest_max_fitness, table_idx)
            
            # Remove guest from the list of not seated guests
            not_seated_guests.remove(guest_max_fitness)

    return offspring, None

def twin_maker(p1, p2):
    """
    Twin Maker crossover implementation.

    The Twin Maker crossover starts by selecting a random number of guests
    between 1/3 and 2/3 of the total number of guests from the first parent
    and seats them in the same tables in the offspring. Then, it fills the
    remaining tables with the guests from the second parent, while keeping
    their relative order in the tables.

    The process is repeated with the second parent, resulting in two offspring.

    Args:
        p1 (Individual): First parent for crossover.
        p2 (Individual): Second parent for crossover.
    
    Returns:
        offspring1 (Individual): First offspring resulting from the crossover.
        offspring2 (Individual): Second offspring resulting from the crossover.
    """

    # Initialize offspring1 and offspring2
    offspring1 = [set() for _ in range(len(p1))]
    offspring2 = [set() for _ in range(len(p2))]

    nr_guests = len(p1) * len(p1[0])
    seats_per_table = len(p1[0])

    # Get random guests to keep
    guests_to_keep = sample(range(1, nr_guests),
                                    randint(round(nr_guests / 3),
                                                    round(nr_guests / 2)))
    
    # Loop through p1 and p2, and then p2 and p1
    for p1, p2, offspring in [(p1, p2, offspring1), (p2, p1, offspring2)]:
        
        # Add guests to offspring on the same table as p1
        for guest in guests_to_keep:
            for table_idx, table in enumerate(p1):
                if guest in table:
                    offspring[table_idx].add(guest)

        offspring_idx = 0

        # Seat remaining guests by the order they appear in p2
        for table in p2:
            for guest in table:
                # Check if guest is already seated
                if guest not in guests_to_keep:
                    # Find the first table with available seats
                    while len(offspring[offspring_idx]) >= seats_per_table:
                        offspring_idx += 1
                    
                    # Seat guest in the table
                    offspring[offspring_idx].add(guest)
                        
    return Individual(offspring1), Individual(offspring2)

