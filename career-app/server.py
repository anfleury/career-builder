from flask import Flask, session, render_template, request
import os
import pandas as pd
import numpy as np
from processing import build_sankey
from processing import uniqueness
from skills import convert_to_list
from skills import find_edu_skills
from skills import find_job_skills
from skills import get_description

# Create the application object
app = Flask(__name__)
app.secret_key = 'random'


@app.route('/',methods=["GET","POST"])
def home_page():
    return render_template('index.html')  # render a template

@app.route('/suggestions',methods=["GET","POST"])
def recommendation_output():
#
    # Pull input
    degree =request.args.get('user_input')

    # Case if empty
    if degree =="":
      return render_template("results.html",
                              my_input = degree,
                              my_form_result="Empty")
    else:
      session['degree'] = degree

      job_name_df = pd.read_csv('/Users/amanda/Documents/Projects/insight/data/processed/education-to-job.csv')
      df1 = pd.read_csv('/Users/amanda/Documents/Projects/insight/data/processed/model-1.csv')
      df2 = pd.read_csv('/Users/amanda/Documents/Projects/insight/data/processed/model-2.csv')

      fig = build_sankey(job_name_df, degree)
      results = uniqueness(df1,df2,degree)


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
                          my_form_result="NotEmpty")

@app.route('/job-details',methods=["GET","POST"])
def job_details():

    degree = session.get('degree', None)

    # Load appropriate dataframes for analysis
    data_path = '/Users/amanda/Documents/Projects/insight/data'

    skills = pd.read_csv(os.path.join(data_path,'processed','job-skills.csv'))
    job_name_df = pd.read_csv(os.path.join(data_path,'processed','education-to-job.csv'))

    skills_df = convert_to_list(skills,['expertise','skills','knowledge'])
    job_lookup = job_name_df[['top_jobs','link']].drop_duplicates()
    job_lookup['top_jobs'] = job_lookup['top_jobs'].str.lower()

    description_df = pd.read_csv(os.path.join(data_path,'processed','job-description.csv'))

    # Pull input
    if request.method == 'POST':

      alt_job = request.form.get('job')

      edu_skill_dict = find_edu_skills(job_name_df,skills_df,degree)
      job_skill_dict = find_job_skills(job_lookup,skills_df,alt_job)

      edu_skill_sort = sorted(list(edu_skill_dict.keys()))
      job_skill_sort = sorted(list(job_skill_dict.keys()))

      new_skills = set(job_skill_dict.keys()) - set(edu_skill_dict.keys())
      result = sorted(list(new_skills))

      description = get_description(job_lookup,description_df,alt_job)

      if alt_job is not None:
          return render_template("results.html",
                                 degree=degree,
                                 job_desc=description,
                                 interest_job=alt_job,
                                 edu_skills=edu_skill_sort,
                                 job_skills=job_skill_sort,
                                 new_skills=result,
                                 button_result="NotEmpty")


# start the server with the 'run()' method
if __name__ == "__main__":
    app.run(debug=True) #will run locally http://127.0.0.1:5000/

