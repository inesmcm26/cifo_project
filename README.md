# Wedding Seating Chart Problem

This project was developed to solve the Wedding Seating Chart Problem using Genetic Algorithms.

The ultimate goal of the project was to find an optimal seating arrangement of 64 guests across 8 tables aiming to maximize the relations among them. Nevertheless, this implementation supports any number of guests and tables, as long as a corresponding relationship matrix exists.

The problem is solved using a particular type of GA, the Group Genetic Algorithms, which is distinguished by group-based scheme used to encode solutions in the search space. 

## File organization

The files on this project are organized in the under structure:

- `charles` folder : Genetic Algorithms Library
    - `charles.py` : Contains the implementation of the Individual and Population classes for the Wedding Seating Chart problem
    - `crossover.py`: Contains the implementation of 3 crossover methods that operate at the group level to mix WSC Individuals
    - `mutation.py`: Contains the implementation of 4 mutation methods that operate at the group level on WSC Individuals
    - `selection.py`: Contains the implementation of 3 selection methods that choose a WSC Individual from the Population

    
- `data` folder : Contains the relationship matrix for a WSC problem with 64 guests and 8 tables, as well as a script to load that data into an appropiate numpy array


- `selection_algorithm_choice` folder : Contains files used to choose the selection method to use on the GA.

- `grid_search.py` : Script to perform a Grid Search over crossover, mutation and elitism operators. Analysis of the results is in the `results` folder.

- `results` folder : Contains the experimental results of the Grid Search, as well as a notebook with the analysis of those results.

- `WSC.py` : Runs the GA with the best combination of operators found in the Grid Search, for the Wedding Seating Chart Problem.
The population is initialized and evolved for 30 runs and the best individual found is printed.

## Data

An hypothetical dataset of relationships among 64 wedding guests was created, assumming the following values:

- 5000: Bride or Groom
- 2000: Spouse or Date
- 1000: Best Friend
- 900: Siblings
- 700: Parents or Child
- 500: Cousing
- 300: Aunt/Uncle or Niece/Nephew
- Strangers: 0
- Enimies: -1000

Relationships like, for example, Sister-in-Law and Great Uncle were set to 0 for simplicity, as we determined that their relevance was already somehow encoded in the other above mentioned relationships.

## Methodology

A Wedding Seating Chart (WSC) Individual and Population classes were implemented with the necessary and adequate methods. Several diferent genetic operators that work at the group level were also implemented.

After that, a selection method was choosen to be used through the rest of the project. The analysis and choice of the best selection algorithm can be found in the `selection_algorithm_choice` folder.

Later, some GA parameters were defined to the default widely used values, such as crossover probability of 0.9 and mutation probability of 0.1, and a population size of 50 Individuals was also fixed. In order to choose the best remaining GA hyperparameters, namely, crossover, mutation and elitism, a grid search was performed. This can be found in `grid_search.py` and the results and analysis in the `results` folder.

Finally, the best set of hyperparameters was retrieved and the final best GA was run to find an optimal seating arragement for the wedding.

## Outcomes

Through the course of this project we were able to identify the impact of selection, crossover, mutation and elitism in the success of our GA.

In the end, we were able to find an optimal seating arrangement with total fitness value of 81300.