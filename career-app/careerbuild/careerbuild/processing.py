import pandas as pd
import numpy as np
from scipy import spatial
from fuzzywuzzy import process

def uniqueness(df1,df2,group,hobby_df,hobby):

    '''Function takes in two dataframes containing information about education and common career paths, and information about user hobbies. The output is a list of uncommon careers that share topic similarity with comon careers and hobbies.'''

    # How much should the hobby affect the results?
    hobby_multiplier = 6

    # Find common jobs for given education group
    group_jobs = df1.where(df1['education_groups']==group).dropna().drop_duplicates(['top_jobs'])

    # Construct a dataframe to hold the common jobs, and a separate dataframe to hold uncommon jobs
    is_job = df2[df2.noc.isin(group_jobs['noc'])]
    job_scores = is_job.iloc[:,-28:-3] #based on 25 topics
    not_job = df2[~df2.noc.isin(group_jobs['noc'].values)]

    # Compute an average vector of topic scores for the common jobs and optional hobby
    if hobby:
        hobby_topics = hobby_df.where(hobby_df['hobby']==hobby).dropna()
        hobby_scores = hobby_topics.iloc[:,-25:] * hobby_multiplier
        unique_mean = pd.concat([job_scores, hobby_scores], axis=0).mean(axis=0, skipna=True)
    else:
        unique_mean = list((is_job.iloc[:,-28:-3]).mean(axis=0, skipna=True))

    # All topic vectors are normalized
    unique_mean = unique_mean/np.sum(unique_mean)

    # Compute the cosine similarity between the 'common' vector computed above and the vectors for every career in the 'uncommon' dataframe
    results = []
    similarity = []
    for i in range(len(not_job)):
        b = not_job.iloc[i,-28:-3] #based on 25 topics
        c_sim = 1 - spatial.distance.cosine(unique_mean, b)
        similarity.append(c_sim)

    # Sort similarities to find the most similar and return the top 10
    not_job['similarity'] = similarity
    sorted_df = not_job.sort_values(by=['similarity'],ascending=False)
    results = sorted_df['job_group'][0:10]

    return list(results)

def find_closest_match(usr_input,name_list):
    '''Takes in a string from the user and outputs the closest matches in a list of strings using fuzzy word matching.'''

    # Use fuzzywuzzy to find top fuzzy word matches for given input
    highest = process.extract(usr_input,name_list)[0:5]
    topmatches = [x[0] for x in highest]

    return topmatches

