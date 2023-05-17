import pandas as pd

relationships = pd.read_excel('data/seating_data.xlsx')

relationships_matrix = relationships.to_numpy()