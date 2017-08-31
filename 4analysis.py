#!/usr/bin/python

# Analysis script to find the probabilities of each key occurance

# Pseudo Code
# 1. read through the cooccur_df line by line in loop
# 2. store the two keys in memory
# 3. inner loop through keys_df re.search for key one match and store prob value then same foe second
# 4. maths (prob1 * prob2)*total samples= expected value
# 5. print whole line plus expected write out file
# 6. in a new module expected - obs and plot

# Done. Swap the printing if you want to see the individual probs. NB the BioSamplesKeys.csv is missing 202 values!


import pandas as pd
import numpy as np
import re
import sys
from decimal import Decimal
import csv

if __name__ == "__main__":

    with open('out.csv', 'w') as f:
    	
		writer = csv.writer(f)
		# writer.writerow(['Key 1', 'Key 2', 'Key 1 Probability', 'Key 2 Probability', 'Coocurance Probability', 'Expected Frequency', 'Observed Frequency', 'Difference'])
		writer.writerow(['Key 1', 'Key 2', 'Expected Frequency', 'Observed Frequency', 'Difference'])

		keys_df = pd.read_csv("cocoa_facets")
		keys_df["prob"] = keys_df["facets_count"] / 4698254
		dict = dict(zip(keys_df.facets_name, keys_df.prob))
		# print dict
		# print keys_df

		lines_skipped = 0

		cooccur_df = pd.read_csv("total_cooccurrence_matrix.csv", names = ["key1", "key2", "count"])
		# print cooccur_df

		for row in cooccur_df.itertuples():
			key1 = row[1].strip()
			key2 = row[2].strip()
			if key1 not in dict:
				lines_skipped = lines_skipped + 1
			else:
				prob1 = dict[key1]

			if key2 not in dict:
				lines_skipped = lines_skipped + 1
			else:
				prob2 = dict[key2]

			cooccur_prob = (prob1 * prob2)
			expected = cooccur_prob * 4698254
			observed = row[3]
			diff = observed - expected

			
			# writer.writerow([key1, key2, prob1, prob2, cooccur_prob, expected, observed, diff])
			writer.writerow([key1, key2, expected, observed, diff])










