import pandas as pd
import numpy as np
import os, re


data_path = '/Users/amanda/Documents/Projects/insight/data'

# Load education and occupation details

overview_df = pd.read_csv(os.path.join(data_path,
                                       'processed',
                                       'job-overview.csv'))
description_df = pd.read_csv(os.path.join(data_path,
                                          'processed',
                                          'job-description.csv'))
regulation_df = pd.read_csv(os.path.join(data_path,
                                         'processed',
                                         'job-regulation.csv'))
skills_df = pd.read_csv(os.path.join(data_path,
                                     'processed',
                                     'job-skills.csv'))


