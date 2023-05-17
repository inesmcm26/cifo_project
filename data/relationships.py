import pandas as pd

relationships = pd.read_excel('data/seating_data.xlsx')

relationships.drop('idx', axis = 1, inplace = True)

relationships_matrix = relationships.to_numpy()