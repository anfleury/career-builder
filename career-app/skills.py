import pandas as pd
import numpy as np
import os, re, ast


def convert_to_list(df,columns):

    df.fillna('', inplace=True)

    for col in columns:
        if isinstance(df[col][0], str):
            df[col] = [ast.literal_eval(s) for s in df[col]]

    return df

def find_edu_skills(job_df,skills_df,education):

    education_jobs = job_df.loc[job_df['education_groups'] == education]
    merged_df = pd.merge(left=education_jobs,
                         right=skills_df,
                         how='left',
                         left_on='link',
                         right_on='link')

    merged_df_unique = merged_df.drop_duplicates(subset=['link'])

    skills_expanded = merged_df_unique[['link',
                                        'degree',
                                        'education_groups',
                                        'top_jobs',
                                        'job_percent',
                                        'skills']].explode('skills')

    skills_dict = skills_expanded['skills'].value_counts().to_dict()

    # Remove skills from the list where the count is less than 2 as they're probably not strongly associated with the educaiton
    skill_values = {key:val for key, val in skills_dict.items() if val > 2}

    return skill_values

def find_job_skills(job_lookup,skills_df,job):

    job_link = job_lookup.loc[job_lookup['top_jobs'] == job]

    merged_df = pd.merge(left=job_link,
                         right=skills_df,
                         how='left',
                         left_on='link',
                         right_on='link')


    merged_df_unique = merged_df.drop_duplicates(subset=['link'])

    skills_expanded = merged_df_unique[['link',
                                        'top_jobs',
                                        'skills']].explode('skills')

    job_skill_values = skills_expanded['skills'].value_counts().to_dict()

    return job_skill_values

