from random import sample, random
import itertools
from collections import Counter
from copy import deepcopy

from charles.charles import Individual


def get_best_combination(guests_to_seat, nr_guests_to_fill, table_to_fill, offspring):
    """
    Get the best combination of guests to fill the table, based on the fitness of the table.
    Input:  guests_to_set (set of integers)
            nr_guests_to_fill (integer)
            table_to_fill (list of integers)
            offspring (Individual)
    Returns:
        best_comb: The best combination of guests used to fill the table.
        offspring: The offspring with the best table added.
    """

    # Possible combinations of people to fill the table
    guests_combinations = list(itertools.combinations(guests_to_seat, nr_guests_to_fill))
    print('Guests combinations ', guests_combinations)

    best_fitness = 0
    best_table = None
    best_comb = None

    print('Offspring', offspring)

    for comb in guests_combinations:
        # Add guests to the table to fill
        table_aux = table_to_fill | set(comb)

        # Add table to offspring
        offspring.append_table(table_aux)

        # Calculate table fitness
        table_fitness = offspring.get_table_fitness(-1)
        print('Combination ', comb)
        print('Table fitness ', table_fitness)
        
        if table_fitness >= best_fitness:
            best_fitness = table_fitness
            best_table = table_aux
            best_comb = comb
        
        # Remove table from offspring
        offspring.remove_table(-1)
    
    print('Offspring should be equal', offspring)
    
    # Add table with highest fitness to offspring
    offspring.append_table(best_table)

    print('Offspring after inserting guests', offspring)
    print('Best comb ', best_comb)

    return best_comb, offspring


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


def gbx_crossover(p1, p2):
    """
    Applies group based crossover to two ps to create an offspring.

    Args:
        p1 (Individual): An Individual object representing the first parent.
        p2 (Individual): An Individual object representing the second parent.

    Returns:
        offspring (Individual): An Individual object representing the offspring.
    """
    # Nr of seats per table
    seats_per_table = len(p1[0])

    # Get the crossover point
    crossover_point = get_crossover_point()

    # Get the number of tables to keep from the first p
    num_tables_to_keep = int(crossover_point * len(p1))

    # Get the tables to keep from the first p and add them to the offspring
    # offspring = sample(deepcopy(p1).representation, num_tables_to_keep)
    offspring = Individual(sample(deepcopy(p1).representation, num_tables_to_keep))

    # Get the people of the tables already selected
    seated_guests = {guest for table in offspring for guest in table}
    
    # Get people yet to be seated
    guests_to_seat = set(range(1, len(p1) * seats_per_table + 1)) - seated_guests

    # Remove the people in the selected tables from the second p
    p2_copy = [table.difference(seated_guests) for table in deepcopy(p2)]

    print("p1 selected tables")
    print(offspring)
    print("p2_copy")
    print(p2_copy)
    print('guests_to_seat')
    print(guests_to_seat)

    # While there are guests left to seat
    while len(guests_to_seat) > 0:

        # Sort the tables of the second p by size in descending order
        p2_copy.sort(key=len, reverse=True)

        print('\n')
        print("p2_copy")
        print(p2_copy)

        table_to_fill = p2_copy[0]

        # Exclude people seated in the table from the people to seat
        guests_to_seat = guests_to_seat.difference(table_to_fill)

        print('table to fill ', table_to_fill)

        print('offspring ', offspring)

        # If table if full, remove it from the second p copy and add it to the offspring
        if len(table_to_fill) == seats_per_table:
            # Add table to offspring
            offspring.append_table(table_to_fill)


            # Remove table from the second p copy
            p2_copy.remove(table_to_fill)

            print('offspring ', offspring)
            print('p2_copy ', p2_copy)

        # If table is not full, it needs to be filled with people from other tables
        else:
            # Number of empty seats in the table
            nr_guests_to_fill = seats_per_table - len(table_to_fill)

            print("guests_to_seat")
            print(guests_to_seat)

            # Get the best combination of guests to fill the table and add it to the offspring
            # Also return the best combination of guests so they can be removed from the people to seat
            best_comb, offspring = get_best_combination(guests_to_seat, nr_guests_to_fill, table_to_fill, offspring)
            
            # Remove the people of the combination from the people not selected
            guests_to_seat -= set(best_comb)

            print('Guests to seat after removing best comb ', guests_to_seat)

            # Remove the guests added to table_to_fill from the other tables of p2
            p2_copy = [table - set(best_comb) for table in p2_copy]

            print('p2_copy after removing best comb ', p2_copy)

            # Remove table from the second p
            p2_copy.pop(0)

            print('p2_copy after removing table to fill ', p2_copy)

    return offspring

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

    print('Offspring', offspring)
        
    # ----------------- Repair phase ----------------- #

    # Count the occurrences of each number in the sets
    guest_counts = Counter(guest for table in offspring for guest in table)

    # Get the numbers that occur more than once
    repeated_guests = {guest for guest, count in guest_counts.items() if count > 1}

    # Remove guest from table where he has lowest fitness
    for guest in repeated_guests:
        # Guest fitness in each table
        guest_fitnesses = []
        tables_idx = []

        print('Guest ', guest)

        for table_idx, table in enumerate(offspring):
            if guest in table:

                # Get fitness of the table without the guest
                guest_fitnesses.append(offspring.get_guest_fitness(guest, table_idx))

                # Save table index
                tables_idx.append(table_idx)

        print('table fitnesses ', guest_fitnesses)
        print('tables_idx ', tables_idx)

        # Remove guest from the table where it contributes the less to fitness
        if guest_fitnesses[0] >= guest_fitnesses[1]:
            offspring[tables_idx[1]].remove(guest)
        else:
            offspring[tables_idx[0]].remove(guest)

    print('Offspring after removing ', offspring)
    
    # Fill the empty seats
    not_seated_guests = [guest for guest in range(1, nr_guests + 1) if guest not in guest_counts]

    print('not seated guests ', not_seated_guests)

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

                print('guest ', guest)
                print('table fitness ', table_fitness)

                # Check if table has the highest fitness with the new guest
                if table_fitness > max_fitness:
                    max_fitness = table_fitness
                    guest_max_fitness = guest

                # Remove guest from the table
                offspring.remove_guest(guest, table_idx)

            # Seat the guest that has the highest fitness
            offspring.seat_guest(guest_max_fitness, table_idx)
            
            print('Offspring after seating ', offspring)
            # Remove guest from the list of not seated guests
            not_seated_guests.remove(guest_max_fitness)

    return offspring

def my_custom_crossover (p1, p2):

    # Initialize offspring1 and offspring2
    offspring1 = [set() for _ in range(len(p1))]
    offspring2 = [set() for _ in range(len(p2))]

    nr_guests = len(p1) * len(p1[0])

    # Loop through p1 and p2, and then p2 and p1
    for p1, p2, offspring in [(p1, p2, offspring1), (p2, p1, offspring2)]:
        guests_to_keep = random.sample(range(1, nr_guests),
                                       random.randint(round(nr_guests / 3),
                                                      round(nr_guests / 2)))  # get guests to keep on the same seat

        print('Guests to keep from ', p1, ':', guests_to_keep)
        # Add guests to offspring based on p1
        for guest in guests_to_keep:
            for idx, table in enumerate(p1):
                if guest in table:
                    offspring[idx].add(guest)

        print('Offspring after adding guests:', offspring)

        offspring_idx = 0

        # Add guests to offspring based on p2
        for table in p2:
            print('P2 table:', table)
            for guest in table:
                if guest not in guests_to_keep:
                    print('Guest to add:', guest)
                    if len(offspring[offspring_idx]) < len(table) or offspring_idx == (len(p2) - 1):
                        offspring[offspring_idx].add(guest)
                        print('Offspring after adding guest:', offspring)
                    else:
                        offspring_idx += 1
                        offspring[offspring_idx].add(guest)
                        print('Offspring after adding guest on next table:', offspring)
                        
    return Individual(offspring1), Individual(offspring2)

