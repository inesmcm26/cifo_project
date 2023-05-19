from collections import Counter
from copy import deepcopy
from charles.charles import Individual

def eager_breader_crossover(p1, p2):
    """
    Implementation of Eager Breader Crossover.

    Args:
        p1 (Individual): First parent for crossover.
        p2 (Individual): Second parent for crossover.

    Returns:
        Individual: One offspring resulting from the crossover.
        
    """
    
    p1_idx = 0
    p2_idx = 0

    offspring = Individual(arrangement = None)

    guests_per_table = len(p1[0])
    nr_guests = len(p1) * guests_per_table


    # Add tables until child has the correct number of tables
    while(len(offspring) < len(p1)):
        fit_table1 = p1.get_table_fitness(p1_idx)
        fit_table2 = p2.get_table_fitness(p2_idx)
        if fit_table1 >= fit_table2:
            offspring.append_table(deepcopy(p1[p1_idx]))
            p1_idx += 1
        else:
            offspring.append_table(deepcopy(p2[p2_idx]))
            p2_idx += 1
        
    # ----------------- Repair phase ----------------- #

    # Count the occurrences of each number in the sets
    guest_counts = Counter(guest for table in offspring for guest in table)

    # Get the numbers that occur more than once
    repeated_guests = {guest for guest, count in guest_counts.items() if count > 1}

    # Remove guest from table where he has lowest fitness
    for guest in repeated_guests:
        # Guest fitness in each table
        table_fitnesses = []
        tables_idx = []

        for table_idx, table in enumerate(offspring):
            if guest in table:

                # Get table without guest
                offspring.remove_guest(guest, table_idx)

                # Get fitness of the table without the guest
                table_fitnesses.append(offspring.get_table_fitness(table_idx))

                # Seat guest again
                offspring.seat_guest(guest, table_idx)

                # Save table index
                tables_idx.append(table_idx)

        # Remove guest from the table where it contributes the less to fitness
        # If the guest contributes less to table 0, remove it from table 0
        if table_fitnesses[0] >= table_fitnesses[1]:
            offspring[tables_idx[0]].remove(guest)
        # If the guest contributes less to table 1, remove it from table 1
        else:
            offspring[tables_idx[1]].remove(guest)

    
    # Fill the empty seats
    not_seated_guests = [guest for guest in range(1, nr_guests + 1) if guest not in guest_counts]

    for table_idx in range(len(offspring)):
        # Table with empty seats
        while len(offspring[table_idx]) < guests_per_table:
            max_fitness = -1
            guest_max_fitness = None
            for guest in not_seated_guests:
                # Seat guest at the table
                offspring.seat_guest(guest, table_idx)

                # Get table fitness
                table_fitness = offspring.get_table_fitness(table_idx)

                # Check if table has the highest fitness with the new guest
                if table_fitness > max_fitness:
                    max_fitness = table_fitness
                    guest_max_fitness = guest

                # Remove guest from the table
                offspring.remove_guest(guest, table_idx)

            # Seat the guest that has the highest fitness
            offspring.seat_guest(guest_max_fitness, table_idx)

            # Remove guest from the list of not seated guests
            not_seated_guests.remove(guest_max_fitness)

    return offspring

        
