import random
from charles.charles import Individual

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