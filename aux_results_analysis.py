import ast
import pandas as pd
import numpy as np

results = pd.read_csv('results.csv')

print(results.head())

results = results.applymap(eval)

for col in results.columns:
    results[f'{col}_Avg'] = results[col].apply(np.mean)

print(results.head())