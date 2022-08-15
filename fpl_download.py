# -*- coding: utf-8 -*-
"""
Created on Fri Jul 22 16:40:01 2022

@author: Tristan
"""

import requests
import pandas as pd
from pandas.api.types import CategoricalDtype

from modules.my_modules import upload_gsheets


team_id = [
    '2969318',
    '440350',
    '4056362',
    '5521906',
    '1881171',
    '5380567',
    '2927478',
    '441995',
    '453402',
    '4763326',
    '3504906',
    '3662726',
    '2828384',
    '6093864'
]


current_df = pd.DataFrame(columns=[
    'event',
    'points',
    'total_points',
    'rank',
    'rank_sort',
    'overall_rank',
    'bank',
    'value',
    'event_transfers',
    'event_transfers_cost',
    'points_on_bench',
    'team_id'
])


for i in team_id:
    URL = (
        'https://fantasy.premierleague.com/api/entry/'
        + i
        + '/history/'
    )
    r = requests.get(URL)
    json = r.json()
    df = pd.DataFrame(json['current'])
    df['team_id'] = i
    current_df = pd.concat([current_df, df])

current_df.rename(
    columns={'event': 'gameweek'},
    inplace=True
)

current_df = current_df.astype({
    'gameweek': 'int32',
    'event_transfers': 'int32',
    'event_transfers_cost': 'int32'
})


current_df['weekly_rank'] = current_df.groupby(['gameweek'])['total_points'].rank(
    method='first',
    ascending=False
)

current_df['total_transfers'] = current_df.groupby(
    ['team_id'])['event_transfers'].cumsum()
current_df['total_transfers_cost'] = current_df.groupby(
    ['team_id'])['event_transfers_cost'].cumsum()

# Sets up the team_id order as a custom list
cat_size_order = CategoricalDtype(
    team_id,
    ordered=True
)

# Sets the order of the team_id column to the team_id list
current_df['team_id'] = current_df['team_id'].astype(cat_size_order)

# Sorts by team_id list then gameweek
current_df.sort_values(by=['gameweek', 'team_id'], inplace=True)

weekly_points_df = current_df[[
    'team_id',
    'gameweek',
    'points',
    'total_points',
    'weekly_rank',
    'points_on_bench'
]]

transfers_df = current_df[[
    'team_id',
    'gameweek',
    'bank',
    'value',
    'event_transfers',
    'total_transfers',
    'event_transfers_cost',
    'total_transfers_cost'
]]

print(current_df)
print(weekly_points_df)
print(transfers_df)


WORKBOOK_NAME = 'council-fpl-tableau-data-22-23'
upload_gsheets(
    WORKBOOK_NAME,
    [weekly_points_df, transfers_df],
    sheets=[0, 1]
)
