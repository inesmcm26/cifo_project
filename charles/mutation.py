from random import sample, choice, shuffle

def swap_mutation(individual):
    """
    Swap mutation for a GGA individual

    The swap mutation operator swaps two guests from two different tables.

    Args: 
        individual (Individual): An individual from charles.py
    Returns:
        individual (Individual): Mutated Individual
    """

    # Get two random tables
    table_idx = sample(range(len(individual)), 2)

    # Get two guests from the tables
    guest1 = individual[table_idx[0]].pop()
    guest2 = individual[table_idx[1]].pop()

    # Swap
    individual.seat_guest(guest2, table_idx[0])
    individual.seat_guest(guest1, table_idx[1])
    
    return individual

def merge_and_split(individual):
    """
    Merge and split mutation for a GGA individual

    The merge and split mutation operator merges two tables and then randomly
    splits the merged table into two new tables.

    Args: 
        individual (Individual): An individual from charles.py
    Returns:
        individual (Individual): Mutated Individual
    """

    # Selects two random tables
    table_idx = sample(range(len(individual)), 2)

    # Merges the two tables
    mixed_tables = individual[table_idx[0]] | individual[table_idx[1]]

    # Splits the merged table into two new tables
    fst_table = sample(list(mixed_tables), len(individual[0]))
    snd_table = [person for person in mixed_tables if person not in fst_table]

    # Updates the individual
    individual[table_idx[0]]= set(fst_table)
    individual[table_idx[1]] = set(snd_table)

    return individual

def the_hop(individual):
    """
    The hop mutation for a GGA individual

    The Hop operator, also known as the Shift operator, shifts one guest
    from each table to the next table.

    Args: 
        individual (Individual): An individual from charles.py
    Returns:
        individual (Individual): Mutated Individual
    """

    # List to keep track of guests that have been moved
    moved_guests = []

    # Iterate over each table
    for i in range(len(individual)):
        current_table = individual[i]

        # Filter out guests that have already been moved
        available_guests = list(current_table - set(moved_guests))

        # Choose a random person from the available guests in the current table
        random_person = choice(available_guests)

        # Remove the random person from the current table
        current_table.remove(random_person)

        # Add the random person to the moved guests list
        moved_guests.append(random_person)

        # Move the random person to the next person
        next_table_index = (i + 1) % len(individual)
        next_table = individual[next_table_index]
        next_table.add(random_person)

    return individual

def dream_team(individual):
    """
    The dream team mutation for a GGA individual

    The dream team operator preserves guests with the strongest relationships
    at each table and randomly shuffles the remaining among tables.

    Args: 
        individual (Individual): An individual from charles.py
    Returns:
        individual (Individual): Mutated Individual
    """

    seats_per_table = len(individual[0])

    # List to save the guests to shuffle
    guests_to_shuffle = []

    for table_idx in range(len(individual)):

        # Dictionary to save the best relationship of each guest
        table_best_relationships = {}
    
        for guest in individual[table_idx]:
            table_best_relationships[guest] = individual.get_guest_max_relationship(guest, table_idx)

        # Get the highest relationship value of the table
        max_relationship = max(table_best_relationships.values())

        # Get all guests with worse highest relationship than max_relationship
        guests_to_remove = [guest for guest in individual[table_idx] if table_best_relationships[guest] != max_relationship]

        # Add those guests to be shuffled
        guests_to_shuffle = guests_to_shuffle + guests_to_remove

        # Remove those guests from the table
        for guest in guests_to_remove:
            individual.remove_guest(guest, table_idx)

    # Suffle guests
    shuffle(guests_to_shuffle)

    table_idx = 0

    # Seat guests in the suffled order
    while len(guests_to_shuffle) > 0:
        # Get the first guest left to seat
        guest_to_seat = guests_to_shuffle.pop(0)
        
        # Find the next table with available seats
        while len(individual[table_idx]) >= seats_per_table:
            table_idx += 1

        # Seat the guest
        individual.seat_guest(guest_to_seat, table_idx)

    return individual