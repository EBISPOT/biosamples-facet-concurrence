#!/usr/bin/python

import pandas as pd

df = pd.read_csv("out.csv")
# df.plot.scatter(['Key 1'], ['Difference'])

sorted_df = df.sort_values(['Fold_Difference'])
sorted_df.to_csv('sorted_out.csv', header = True, mode = 'w', )