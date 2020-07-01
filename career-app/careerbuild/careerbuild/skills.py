import pandas as pd
import numpy as np
import os, re, ast


def convert_to_list(df,columns):
    '''When saving as a .csv, a column of lists gets flattened into a single string. This function uses literal_eval to turn the string back into a list.'''

    df.fillna('', inplace=True)

    for col in columns:
        if isinstance(df[col][0], str):
            df[col] = [ast.literal_eval(s) for s in df[col]]

    return df

def find_edu_skills(job_df,skills_df,education):
    '''Given a database of skills for each career, find the skills associated with the top 10 careers for a given degree.'''

    # Use merge to find the skills associated with only the given degree and output a single dataframe with only those skills
    education_jobs = job_df.loc[job_df['education_groups'] == education]
    merged_df = pd.merge(left=education_jobs,
                         right=skills_df,
                         how='left',
                         left_on='noc',
                         right_on='noc')

    merged_df_unique = merged_df.drop_duplicates(subset=['noc'])

    # Explode dataframe to have unique records for every job and skill
    skills_expanded = merged_df_unique[['noc',
                                        'edu_level',
                                        'education_groups',
                                        'top_jobs',
                                        'job_percent',
                                        'skills']].explode('skills')

    # Count how many times each skill is mentioned and remove skills from the list where the count is less than 2 as they're probably not strongly associated with the education
    skills_dict = skills_expanded['skills'].value_counts().to_dict()
    skill_values = {key:val for key, val in skills_dict.items() if val > 2}

    return skill_values

def find_job_skills(job_lookup,skills_df,job):
    '''Given a database of skills for each career, find the skills associated with each unique job.'''

    # Find noc code associated with the given job and use this code to find skills in skills table
    job_link = job_lookup.loc[job_lookup['job_group'] == job.lower()]
    merged_df = pd.merge(left=job_link,
                         right=skills_df,
                         how='left',
                         left_on='noc',
                         right_on='noc')

    merged_df_unique = merged_df.drop_duplicates(subset=['noc'])

    # Explode dataframe to have unique records for every skill
    skills_expanded = merged_df_unique[['noc',
                                        'job_group',
                                        'skills']].explode('skills')

    job_skill_values = skills_expanded['skills'].value_counts().to_dict()

    return job_skill_values

def get_description(job_lookup,df,job):
    '''Lookup job description from a table given the job title.'''

    job_link = job_lookup['noc'].loc[job_lookup['job_group'] == job.lower()]
    merged_df = pd.merge(left=job_link,
                         right=df,
                         how='left',
                         left_on='noc',
                         right_on='noc')

    description = merged_df['description'][0]

    return description
