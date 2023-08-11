import pandas as pd

# create a sample DataFrame
df = pd.DataFrame({'values': [1, 3, 5, 7, 9]})

# find the first index where values > i
i = 0
mask = df['values'] > i
if mask.any():
    index = df.loc[mask, 'values'].idxmin()
print(index)