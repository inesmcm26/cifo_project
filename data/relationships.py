import pandas as pd
import os

# Get the current directory of the script
script_directory = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the file within the same folder
file_path = os.path.join(script_directory, "seating_data.xlsx")

relationships = pd.read_excel(file_path)

relationships.drop('idx', axis = 1, inplace = True)

relationships_matrix = relationships.to_numpy()