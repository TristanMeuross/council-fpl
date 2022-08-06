# -*- coding: utf-8 -*-
"""
Created on Fri Jul 22 16:40:01 2022

@author: Doug
"""

import requests
import pandas as pd
import numpy as np

from modules.my_modules import upload_gsheets, format_gsheets

url = 'https://fantasy.premierleague.com/api/entry/2969318/history/'
r = requests.get(url)
json = r.json()

#%%

current_df = pd.DataFrame(json['past'])
print(current_df.head())

#%%

points_df = pd.read_csv('data_files/council-fpl-tableau-data.csv')
points_df['cumulative_points'] = points_df.groupby(['team_name'])['points'].cumsum()
points_df['weekly_rank'] = points_df.groupby(
    ['gameweek']
    )['cumulative_points'].rank(
        method='first',
        ascending=False
        )


workbook_name = 'council-fpl-tableau-data'
upload_gsheets(
    workbook_name,
    [points_df],
    sheets=[0]
)

#%%
