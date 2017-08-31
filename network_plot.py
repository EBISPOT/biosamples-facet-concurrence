#!//Users/hewgreen/anaconda/bin/python

# script to plot a networkx graph and save out graphs compatible with Gephi and Cytoscape
# this may work but loading and viewing the whole graph is very demanding.

import numpy as np
import networkx as nx
from matplotlib import pylab
import matplotlib.pyplot as plt
import pandas as pd

G=nx.Graph()

df = pd.read_csv('sorted_out.csv', header=0)
# source,target,weight
G = nx.from_pandas_dataframe(df,source='Key 1', target='Key 2', edge_attr='Fold_Difference')

# # for cytoscape save
# nx.write_gml(G,'network.gml')
# for gephi save
nx.write_gexf(G,'fold_diff_weighted_network.gexf')
