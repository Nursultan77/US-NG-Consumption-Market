#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 11 22:21:41 2021

@author: nursultanyeshmukhan
"""
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# DataFrames of citygate and final price respectively data
prices = os.listdir("/Users/nursultanyeshmukhan/Desktop/PAI789/ny_final_project/")

pri_xls = [f for f in prices if f[-10:] == 'prices.xls']
cityg_pr_df = pd.DataFrame()
final_pr_df = pd.read_pickle("final_pr_df.pkl")
for f in pri_xls:
    data = pd.read_excel(f, sheet_name = 'Data 1', header = 2, index_col = "Date")
    for col in data.columns:          
        if "Citygate" in col:
            gate_p = data[col]
            cityg_pr_df[f] = gate_p
        

#%%
#take only 2010 year, add category column for each dataframe respectively

cityg_pr_ndf = cityg_pr_df.query("Date == '2010-06-30 00:00:00'").copy()

cityg_pr_ndf.columns = cityg_pr_ndf.columns.map(lambda x: str(x)[:-11])

cityg_pr_ndf["category"] = "citygate"
cols = cityg_pr_ndf.columns.tolist()
cols = cols[-1:] + cols[:-1]
cityg_pr_ndf = cityg_pr_ndf[cols]

final_pr_ndf =final_pr_df.query("Date == '2010-06-30 00:00:00'").copy()

final_pr_ndf["category"] = "final"
cols = final_pr_ndf.columns.tolist()
cols = cols[-1:] + cols[:-1]
final_pr_ndf = final_pr_ndf[cols]



#%%
# Combine data to united Dataframe that contains density of prices 
frames = [cityg_pr_ndf, final_pr_ndf]
pr_df = pd.concat(frames)
#pr_df.reset_index(drop=True, inplace=True)
pr_df = pr_df.dropna(axis = "columns", how = "any")

#%%
pr_df = pr_df.T


new_header = pr_df.iloc[0] #grab the first row for the header
pr_df = pr_df[1:] #take the data less the header row
pr_df.columns = new_header #set the header row as the df header


#pr_df["wellhead"] = pr_df["wellhead"].astype(float)
pr_df["citygate"] = pr_df["citygate"].astype(float)
pr_df["final"] = pr_df["final"].astype(float)
pr_df["difference"] = pr_df["final"]/pr_df["citygate"]
#pr_df.sortby(pr_df["difference"])

#%%
pr_df1 = pr_df.stack().reset_index()
pr_df1.columns = ["state", "category", "price",]

#%%
pr_df_kde = pr_df.drop("difference", axis = "columns")
fig, ax1 = plt.subplots()
#sns.histplot(pr_df, stat = "density", ax = ax1)
sns.kdeplot(data = pr_df_kde, shade = True, ax = ax1)
ax1.set_title("US Natural Gas citygate & Final price density, 2010")
ax1.set_xlabel("natural gas prices. $ per Mcf")
# how to set title
fig.tight_layout()
fig.savefig("price_density.png")
#%%
print("Number of states having the data for prices in 2010:\n")
pr_df.info()
#%%

print("Average citygate price in 2010:", pr_df["citygate"].mean())
print("Average final price in 2010:", pr_df["final"].mean())
#%%
pr_df = pr_df.sort_values("difference", ascending=False)
fig, ax = plt.subplots(figsize=(10, 15))
sns.set_color_codes("pastel")
sns.barplot(x="final", y=pr_df.index, data=pr_df, label="Final price", color="b").set_title("Citygate and Final prices difference in the United States, 2010")
sns.set_color_codes("muted")
sns.barplot(x="citygate", y=pr_df.index, data=pr_df,label="Citygate price", color="b")

# Add a legend and informative axis label
ax.legend(ncol=2, loc="lower right", frameon=True)
ax.set(xlim=(0, 24), ylabel="",
       xlabel="Natural gas prices")
sns.despine(left=True, bottom=True)
fig.savefig("citygate_final_barplot.png")


