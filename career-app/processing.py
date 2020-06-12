import json
import plotly
import plotly.graph_objs as go
from scipy import spatial


def build_sankey(df, degree):

    data = df.where(df['education_groups']==degree).dropna()

    all_nodes = data['identifier'].values.tolist() + data['top_jobs'].values.tolist()
    source_indices = [all_nodes.index(identifier) for identifier in data['identifier']]
    target_indices = [all_nodes.index(top_job) for top_job in data['top_jobs']]

    fig = go.Figure(data=[go.Sankey
                          (node = dict(pad = 15,
                                       thickness = 20,
                                       line = dict(color = "black",
                                                   width = 0),
                                       label = all_nodes,
                           ),
                           link = dict(source = source_indices,
                                       target = target_indices,
                                       value = data['job_percent']*100)
                          )
                         ]
                   )

    filename = 'static/{}.png'.format(degree)

    div = fig.to_html()

    return div

def uniqueness(df1,df2,group):

    group_jobs = df1.where(df1['education_groups']==group).dropna().drop_duplicates(['top_jobs'])

    is_job = df2[df2.link.isin(group_jobs['link'])]

    not_job = df2[~df2.link.isin(group_jobs['link'].values)]
    not_job = not_job.dropna(subset=['top_jobs'])

    job_mean = (is_job.iloc[:,-23:-3]).mean(axis = 0, skipna = True)

    results = []
    similarity = []
    for i in range(len(not_job)):
        b = not_job.iloc[i,-23:-3]
        c_sim = 1 - spatial.distance.cosine(job_mean, b)
        similarity.append(c_sim)

    not_job['similarity'] = similarity

    sorted_df = not_job.sort_values(by=['similarity'],ascending=False)

    results = sorted_df['top_jobs'][0:10]

    return list(results)
