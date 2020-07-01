import json
import plotly
import plotly.graph_objs as go
import numpy as np
import matplotlib
import matplotlib.colors as mc
matplotlib.use('agg')
import seaborn as sns
import colorsys
from  more_itertools import unique_everseen

def get_cmap_string(palette, domain):
    '''Function to get a graphing colour palette given the amount of variables to be plotted on the Sankey diagram.'''

    domain_unique = list(unique_everseen(domain))
    rgbmap = sns.color_palette(palette, len(domain_unique))
    color_dict = res = dict(zip(domain_unique, rgbmap))
    color_list = [color_dict.get(i) for i in domain]

    return color_list

def build_sankey(df, degree):
    '''Function to plot a Sankey diagram (flow diagram) of college major to career, given user's degree and a dataframe listing common career paths for each degree.'''

    # All nodes of the graph should be in a single list (all_nodes), with two additional lists containing the source and target flows for each node
    data = df.where(df['education_groups']==degree).dropna()
    all_nodes = data['identifier'].values.tolist() + data['top_jobs'].values.tolist()
    source_indices = [all_nodes.index(identifier) for identifier in data['identifier']]
    target_indices = [all_nodes.index(top_job) for top_job in data['top_jobs']]

    # Get unique colours from given palette in a list of strings as required by the plotly package
    cmap = get_cmap_string(palette='plasma_r', domain=all_nodes)

    # Plot plotly figure using graphing objects package
    fig = go.Figure(data=[go.Sankey
                          (node = dict(pad = 15,
                                       thickness = 20,
                                       line = dict(color = "black",
                                                   width = 0),
                                       label = all_nodes,
                                       color = ['rgb' + str(s).strip('[]') for s in cmap]
                                       ),
                           link = dict(source = source_indices,
                                       target = target_indices,
                                       value = data['job_percent']*100,
                                       ),
                          )
                         ]
                   )

    # Resize figure for display on the webpage
    fig.update_layout(
    autosize=False,
    width=800,
    height=800)

    # Return figure as html to be displayed on webpage
    div = fig.to_html()

    return div

