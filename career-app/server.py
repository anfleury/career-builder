from flask import Flask, render_template, request
import pandas as pd
import numpy as np
from processing import build_sankey
from processing import uniqueness

# Create the application object
app = Flask(__name__)

@app.route('/',methods=["GET","POST"]) #we are now using these methods to get user input
def home_page():
    return render_template('career-app.html')  # render a template

@app.route('/output')
def recommendation_output():
#
       # Pull input
       degree =request.args.get('user_input')

       # Case if empty
       if degree =="":
          return render_template("career-app.html",
                                  my_input = degree,
                                  my_form_result="Empty")
       else:
          job_name_df = pd.read_csv('/Users/amanda/Documents/Projects/insight/data/processed/education-to-job.csv')
          df1 = pd.read_csv('/Users/amanda/Documents/Projects/insight/data/processed/model-1.csv')
          df2 = pd.read_csv('/Users/amanda/Documents/Projects/insight/data/processed/model-2.csv')

          filename = build_sankey(job_name_df, degree)
          results = uniqueness(df1,df2,degree)


          return render_template("career-app.html",
                              my_input=degree,
                              my_output=filename,
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


# start the server with the 'run()' method
if __name__ == "__main__":
    app.run(debug=True) #will run locally http://127.0.0.1:5000/

