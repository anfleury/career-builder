import pandas as pd
import numpy as np
from scipy import spatial
from fuzzywuzzy import process

def uniqueness(df1,df2,group,hobby_df,hobby):

    hobby_multiplier = 6

    group_jobs = df1.where(df1['education_groups']==group).dropna().drop_duplicates(['top_jobs'])

    is_job = df2[df2.noc.isin(group_jobs['noc'])]
    job_scores = is_job.iloc[:,-28:-3]
    not_job = df2[~df2.noc.isin(group_jobs['noc'].values)]

    if hobby:
        hobby_topics = hobby_df.where(hobby_df['hobby']==hobby).dropna()
        hobby_scores = hobby_topics.iloc[:,-25:] * hobby_multiplier
        unique_mean = pd.concat([job_scores, hobby_scores], axis=0).mean(axis=0, skipna=True)
    else:
        unique_mean = list((is_job.iloc[:,-28:-3]).mean(axis=0, skipna=True))

    unique_mean = unique_mean/np.sum(unique_mean)

    results = []
    similarity = []
    for i in range(len(not_job)):
        b = not_job.iloc[i,-28:-3]
        c_sim = 1 - spatial.distance.cosine(unique_mean, b)
        similarity.append(c_sim)

    not_job['similarity'] = similarity

    sorted_df = not_job.sort_values(by=['similarity'],ascending=False)

    results = sorted_df['job_group'][0:10]

    return list(results)

def find_closest_match(usr_input,name_list):

    highest = process.extract(usr_input,name_list)[0:5]
    topmatches = [x[0] for x in highest]

    return topmatches

