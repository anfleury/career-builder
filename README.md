# Uniquely Qualified

## An app for career discovery

<img src="notebooks/figures/app-landing2.png"></img>

Website: http://uniquely-qualified.live

### Introduction:

Uniquely qualified is an app for career discovery. The app is designed to be used by students who have recently graduated or are nearing graduation, in order to explore career paths outside of their major. The app uses data from the National Graduate Survey to chart common and uncommon paths for users. Uncommon paths are derived from topics common to the typical careers and to an optional chosen hobby.

### Setup and installation:

(<b>Note: this doesn't work yet, but it will.</b>)

After cloning this repository, run the following code:

`cd career-app/career-build`
`pip install -r requirements.txt`

App can then be run locally using:

`cd ..`
`python run.py`

### Usage

Enter your degree on the homepage to get a visualization of the most common jobs for your given degree.

<img src="notebooks/figures/app-sankey.png"></img>

The app will also load recommendations for uncommon jobs you may want to consider.

<img src="notebooks/figures/app-recs.png"></img>

Clicking on one of these 'uncommon' jobs will take you to a description of the job with a list of skills you may be missing given your educational background.

<img src="notebooks/figures/app-job-example.png"></img>
