#!/Users/hewgreen/anaconda/bin/python

from bokeh.charts import Scatter, output_file, show
from bokeh.plotting import figure, output_file, show
from bokeh.models import HoverTool, GlyphRenderer
import pandas as pd

df = pd.read_csv('sorted_out.csv')
df.index.name = 'index'


# some parsing to make data smaller if needed

parsed1_df = df.loc[df['Difference'] > 10000]
parsed2_df = df.loc[df['Difference'] < -5]
parsed_df = pd.concat([parsed1_df, parsed2_df])



# Making the Graph

# output to static HTML file
output_file("scatter.html")

hover = HoverTool(tooltips=[
    ("Facet A", "@{Key 1}"),
    ("Facet B", "@{Key 2}"),
    ("Expected", "@{Expected Frequency}"),
    ("Observed", "@{Observed Frequency}"),
    ("Difference", "@Difference"),
])



p =  Scatter(
	df,
	x='index',
	y='Difference',
	tools=[hover, 'pan', 'box_zoom', 'wheel_zoom', 'reset'],
	title="Attractive and repulsive facet pairs, beyond random concurrence.",
    xlabel="Facet Pairs (sorted)",
    ylabel="Significance of Concurrence (observed - expected)",
)

# Supposed to make it faster, but I dont think it helps
# p = figure(output_backend="webgl")
p.circle('index', 'Difference', size=5, source=df)

# show the results
show(p)












