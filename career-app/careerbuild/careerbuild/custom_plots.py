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

def adjust_lightness(color, amount=1.5):
    c = color
    c = colorsys.rgb_to_hls(*mc.to_rgb(c))
    rgb = colorsys.hls_to_rgb(c[0], max(0, min(1, amount * c[1])), c[2])
    return rgb

def get_cmap_string(palette, domain):

    domain_unique = list(unique_everseen(domain ))
    rgbmap = sns.color_palette(palette, len(domain_unique))
    color_dict = res = dict(zip(domain_unique, rgbmap))
    color_list = [color_dict.get(i) for i in domain]

    return color_list

def build_sankey(df, degree):

    data = df.where(df['education_groups']==degree).dropna()

    data['identifier'] = data['identifier'].str.replace(" : ","- ")

    all_nodes = data['identifier'].values.tolist() + data['top_jobs'].values.tolist()
    source_indices = [all_nodes.index(identifier) for identifier in data['identifier']]
    target_indices = [all_nodes.index(top_job) for top_job in data['top_jobs']]

    cmap = get_cmap_string(palette='plasma_r', domain=all_nodes)
    cmap2 = list(map(adjust_lightness, cmap))

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
                                       color = ['rgb' + str(s).strip('[]') for s in cmap2]
                                       ),
                          )
                         ]
                   )

    filename = 'static/{}.png'.format(degree)

    fig.update_layout(
    autosize=False,
    width=800,
    height=800)

    div = fig.to_html()

    return div

