# Uniquely Qualified

## An app for career discovery

<img src="notebooks/figures/app-landing.png"></img>

Website: tbd

### Introduction:

Uniquely Qualified is a web-based app designed to enable career exploration for graduates or soon-to-be graduates of post-secondary programs.

### Setup and installation:

(<b>Note: this doesn't work yet, but it will.</b>)

After cloning this repository, run the following code:

`cd career-build`
`pip install -r requirements.txt`

App can then be run locally using:

`cd ../career-app`
`python server.py`

### Usage

Enter your degree on the homepage to get a visualization of the most common jobs for your given degree.

<img src="notebooks/figures/app-sankey.png"></img>

The app will also load recommendations for uncommon jobs you may want to consider.

<img src="notebooks/figures/app-recs.png"></img>

Clicking on one of these 'uncommon' jobs will take you to a description of the job with a list of skills you may be missing given your educational background.

<img src="notebooks/figures/app-job-example.png"></img>
