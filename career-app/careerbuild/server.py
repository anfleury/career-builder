from flask import Flask, session, render_template, request, jsonify
import os
import pickle
import pandas as pd
import numpy as np
from careerbuild.careerbuild.processing import uniqueness
from careerbuild.careerbuild.processing import find_closest_match
from careerbuild.careerbuild.custom_plots import build_sankey
from careerbuild.careerbuild.skills import convert_to_list
from careerbuild.careerbuild.skills import find_edu_skills
from careerbuild.careerbuild.skills import find_job_skills
from careerbuild.careerbuild.skills import get_description

from careerbuild import app

# Create the application object
# app = Flask(__name__)
app.secret_key = 'random'

# Load education and occupation details
overview_df = pd.read_csv('./careerbuild/static/noc-overview.csv')
description_df = pd.read_csv('./careerbuild/static/job-description.csv')
#regulation = pd.read_csv('./static/job-regulation.csv')
skills_df = pd.read_csv('./careerbuild/static/job-skills.csv')
job_name_df = pd.read_csv('./careerbuild/static/education-to-job.csv')
df1 = pd.read_csv('./careerbuild/static/model-1.csv')
df2 = pd.read_csv('./careerbuild/static/model-2.csv')
hobby_df = pd.read_pickle('./careerbuild/static/hobby-topics.pkl')

f = open('./careerbuild/static/hobbies.pkl', 'rb')
hobbies_dict = pickle.load(f)
f.close()


@app.route('/',methods=["GET","POST"])
def home_page():
    hobbies = sorted(list(hobbies_dict.keys()))
    return render_template('index.html',hobbies=hobbies)  # render a template

@app.route('/about',methods=["GET","POST"])
def about_page():
    return render_template('about.html')  # render a template

@app.route('/contact',methods=["GET","POST"])
def contact_page():
    return render_template('contact.html')  # render a template


@app.route('/suggestions',methods=["GET","POST"])
def recommendation_output():

    education_match = ['']
#
    # Pull input
    if request.method == 'GET':
      edu_input =request.args.get('usr_degree')
      hobby =request.args.get('usr_hobby')
      session['hobby'] = hobby
      edu_names = list(job_name_df['education_groups'].unique())
      education_match = sorted([s for s in edu_names if edu_input.lower() in s.lower()])
    elif request.method == 'POST':
      edu_input = request.form.get('user_input')
      education_match[0] = edu_input
      hobby = session.get('hobby', None)
    else:
      edu_input = ''

    # Case if empty
    if not edu_input:
      return render_template('results.html',
                              my_input = edu_input,
                              my_form_result=1)

    # No match found for user input, use fuzzy matching
    elif len(education_match) == 0:
      close_match = find_closest_match(edu_input,edu_names)
      return render_template('results.html',
                              my_input = edu_input,
                              matches = close_match,
                              my_form_result=2)

    # Only one match found for user input, return job details
    elif len(education_match) == 1:
      degree = education_match[0]
      session['degree'] = degree

      fig = build_sankey(job_name_df, degree)
      hobby_mult = 4
      results = uniqueness(df1, df2, degree, hobby_df, hobby, hobby_multiplier=hobby_mult)
      results2 = uniqueness(df1, df2, degree, hobby_df, False)
      overlap = len(list(set(results) & set(results2))) / len(results)
      print('Hobby multiplier {} gives {:.0f}% new job recommendations.'.format(hobby_mult, (1 - overlap)*100))

      return render_template("results.html",
                          my_input=degree,
                          sankey=fig,
                          job1=results[0],
                          job2=results[1],
                          job3=results[2],
                          job4=results[3],
                          job5=results[4],
                          job6=results[5],
                          job7=results[6],
                          job8=results[7],
                          job9=results[8],
                          job10=results[9],
                          hobby=hobby,
                          my_form_result=4)

    # More than one match found, return all matches and allow the user to choose the open that makes the most sense
    else:
      return render_template("results.html",
                          my_input=edu_input,
                          matches=education_match,
                          my_form_result=3)

@app.route('/job-details',methods=["GET","POST"])
def job_details():

    degree = session.get('degree', None)

    job_skills_df = convert_to_list(skills_df,
                                    ['expertise',
                                    'skills',
                                    'knowledge'])
    job_lookup = overview_df[['job_group','noc']].drop_duplicates()
    job_lookup['job_group'] = job_lookup['job_group'].str.lower().str.strip()

    # Pull input
    if request.method == 'POST':

      alt_job = request.form.get('job')

      edu_skill_dict = find_edu_skills(job_name_df,job_skills_df,degree)
      job_skill_dict = find_job_skills(job_lookup,job_skills_df,alt_job)

      edu_skill_sort = sorted(list(edu_skill_dict.keys()))
      job_skill_sort = sorted(list(job_skill_dict.keys()))

      new_skills = set(job_skill_dict.keys()) - set(edu_skill_dict.keys())
      result = sorted(list(new_skills))

      job_description = get_description(job_lookup,description_df,alt_job)

      if alt_job is not None:
          return render_template("results.html",
                                 degree=degree,
                                 job_desc=job_description,
                                 interest_job=alt_job,
                                 edu_skills=edu_skill_sort,
                                 job_skills=job_skill_sort,
                                 new_skills=result,
                                 button_result="NotEmpty")

# app.run(host='0.0.0.0', debug = True)

# start the server with the 'run()' method
#if __name__ == "__main__":
#    app.run(host='0.0.0.0', debug=True) #will run locally http://127.0.0.1:5000/

