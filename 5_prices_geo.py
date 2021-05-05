#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 21 21:06:04 2021

@author: nursultanyeshmukhan
"""
#%%Mapping
import pandas as pd
import geopandas

res_pr = pd.read_pickle("res_pr.pkl")
com_pr = pd.read_pickle("com_pr.pkl")
ind_pr = pd.read_pickle("ind_pr.pkl")
final_pr_df = pd.read_pickle("final_pr_df.pkl")
#%% from https://gist.github.com/rogerallen/1583593
us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'American Samoa': 'AS',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Guam': 'GU',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Northern Mariana Islands':'MP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'
}
#%%
us_state_abbrev = dict((k.lower(), v) for k,v in us_state_abbrev.items())

geoid = pd.read_csv("csvdata.csv")
geoid.rename(columns={'State': 'state'}, inplace=True)

price_cat = pd.DataFrame()

price_cat["residential"] = res_pr.loc['2019-06-30 00:00:00']
price_cat["commercial"] = com_pr.loc['2019-06-30 00:00:00']
price_cat["industrial"] = ind_pr.loc['2019-06-30 00:00:00']
price_cat["price_2016"] = final_pr_df.loc['2016-06-30 00:00:00']
price_cat = price_cat.reset_index()
price_cat.rename(columns={'index': 'state'}, inplace=True)
price_cat.sort_values("state")

price_cat['iso3166_2'] = price_cat['state'].map(us_state_abbrev )
price_cat["iso3166_2"] = "US-" + price_cat["iso3166_2"]
price_cat.to_csv("prices_by_category.csv", index = False)

#%%

geodata = geopandas.read_file("Igismap")
geodata = geodata.merge(price_cat, how = "left", on = "iso3166_2", indicator = True)

print(geodata["_merge"].value_counts())
geodata.drop('_merge',axis='columns',inplace=True)
geodata = geodata.dropna(axis=0, subset=['state'])
geodata["iso3166_2"] = geodata["iso3166_2"].map(lambda x: x.replace('US-',''))
geodata.to_file("states.gpkg", layer = "prices", driver = "GPKG")
