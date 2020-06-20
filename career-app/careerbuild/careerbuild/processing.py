from scipy import spatial
from fuzzywuzzy import process

def uniqueness(df1,df2,group):

    group_jobs = df1.where(df1['education_groups']==group).dropna().drop_duplicates(['top_jobs'])

    is_job = df2[df2.noc.isin(group_jobs['noc'])]

    not_job = df2[~df2.noc.isin(group_jobs['noc'].values)]
    #not_job = not_job.dropna(subset=['top_jobs'])

    job_mean = (is_job.iloc[:,-23:-3]).mean(axis = 0, skipna = True)

    results = []
    similarity = []
    for i in range(len(not_job)):
        b = not_job.iloc[i,-23:-3]
        c_sim = 1 - spatial.distance.cosine(job_mean, b)
        similarity.append(c_sim)

    not_job['similarity'] = similarity

    sorted_df = not_job.sort_values(by=['similarity'],ascending=False)

    results = sorted_df['job_group'][0:10]

    return list(results)

def find_closest_match(usr_input,name_list):

    highest = process.extract(usr_input,name_list)[0:5]
    topmatches = [x[0] for x in highest]

    return topmatches

