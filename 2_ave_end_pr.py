#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 21:57:55 2021

@author: nursultanyeshmukhan
"""
# Next, I want to check the price difference: wellhead-citygate-final price 
# Since the end consumers prices varies, for comparing the difference between
# citygate price and final price, we need to get weghted average price of the natural gas.

import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
#%%
#Read consumption by state and type
res_con = pd.read_pickle("res_con.pkl")
com_con = pd.read_pickle("com_con.pkl")
ind_con = pd.read_pickle("ind_con.pkl")

# Read summarized consumption dataframe
conc_df = pd.read_pickle("conc_df.pkl")
# Read dataframe of consumption by type
res_merge = pd.read_pickle("res_merge.pkl")
com_merge = pd.read_pickle("com_merge.pkl")
ind_merge = pd.read_pickle("ind_merge.pkl")


#%%       

# Get the prices by type: Iterate through price by state files
# to concatenate the priceby type of consumers
path = os.getcwd()

files = os.listdir("/Users/nursultanyeshmukhan/Desktop/PAI789/ny_final_project/")

pri_xls = [f for f in files if f[-10:] == 'prices.xls']
res_pr = pd.DataFrame()
com_pr = pd.DataFrame()
ind_pr = pd.DataFrame()


for f in pri_xls:
    data = pd.read_excel(f, sheet_name = 'Data 1', header = 2, index_col = "Date")
    for col in data.columns:
        if "Price of Natural Gas Delivered to Residential Consumers" in col:
            res_p = data[col]
            res_pr[f] = res_p
            
        elif "Price of Natural Gas Sold to Commercial Consumers" in col:
            com_p = data[col]
            com_pr[f] = com_p
        
        elif "Natural Gas Industrial Price" in col:
            ind_c = data[col]
            ind_pr[f] = ind_c
        
            
#%%
# Remove "_prices.xls" part from each column heading
res_pr.columns = res_pr.columns.map(lambda x: str(x)[:-11])
com_pr.columns = com_pr.columns.map(lambda x: str(x)[:-11])
ind_pr.columns = ind_pr.columns.map(lambda x: str(x)[:-11])

# Time to get weighted average price of each state
# Numerator: consumption times price
res_rev = res_con.mul(res_pr)
com_rev = com_con.mul(com_pr)
ind_rev = ind_con.mul(ind_pr)


#Denominator: consumption sum
sum_con = res_con + com_con + ind_con

#Weighted average: numerator over denominator
final_pr_df = (res_rev + com_rev + ind_rev)/sum_con

final_pr_df.to_pickle("final_pr_df.pkl")

#%%
# Calculate average total country's end price by type
av_pr = pd.DataFrame()
av_pr["residential"] = (res_pr*res_con).sum(axis = "columns")/res_con.sum(axis = "columns")
av_pr["commercial"] = (com_pr*com_con).sum(axis = "columns")/com_con.sum(axis = "columns")
av_pr["industrial"] = (ind_pr*ind_con).sum(axis = "columns")/ind_con.sum(axis = "columns")

av_pr_long = av_pr.stack().reset_index()
av_pr_long = av_pr_long.rename(columns = {"level_1" : "sector", 0 : "average price, $ per Mcf"})
av_pr_long = av_pr_long.set_index("Date")

#%%
jg = sns.relplot(data=av_pr_long, x='Date', y='average price, $ per Mcf',col='sector',kind='line')
jg.savefig('ave_prices_bysector.png')

#%%
res_pr.to_pickle("res_pr.pkl")
com_pr.to_pickle("com_pr.pkl")
ind_pr.to_pickle("ind_pr.pkl")


#%%
# Get merged number of consumers , price and consumption dataframes for each category to plot the elasticity of price
grouped_pr = av_pr_long.groupby(av_pr_long.sector)

resid_df = grouped_pr.get_group("residential")
comme_df = grouped_pr.get_group("commercial")
indus_df = grouped_pr.get_group("industrial")

res_merge = res_merge.drop("sector", axis = "columns")
res_merge1 = res_merge.merge(resid_df, on = "Date", how = "left")

com_merge = com_merge.drop("sector", axis = "columns")
com_merge1 = com_merge.merge(comme_df, on = "Date", how = "left")

ind_merge = ind_merge.drop("sector", axis = "columns")
ind_merge1 = ind_merge.merge(indus_df, on = "Date", how = "left")



#%%

#residential number-consumption relationship
fig,ax = plt.subplots()
ax.plot(res_merge1['consumption, MMcf']/1000, color="orangered")
ax.set_xlabel("year",fontsize=12)
ax.set_ylabel("consumption, Bcf",color="orangered",fontsize=12)

ax2=ax.twinx()
ax2.plot(res_merge1['number']/1e6,color="deepskyblue")
ax2.set_ylabel("number of consumers, millions",color="deepskyblue",fontsize=12)
ax.set_title("Consumption and number of consumers in the United States (Residential)", fontsize = 7)
fig.tight_layout()
plt.show()
fig.savefig('res_number-consumption_pic.png',
            dpi=500, bbox_inches='tight')
#%%
#commercial number-consumption relationship
fig,ax = plt.subplots()
ax.plot(com_merge1['consumption, MMcf']/1000, color="orangered")
ax.set_xlabel("year",fontsize=12)
ax.set_ylabel("consumption, Bcf",color="orangered",fontsize=12)

ax2=ax.twinx()
ax2.plot(com_merge1['number']/1e6,color="deepskyblue")
ax2.set_ylabel("number of consumers, millions",color="deepskyblue",fontsize=12)
ax.set_title("Consumption and number of consumers in the United States (Commercial)", fontsize = 7)
fig.tight_layout()
plt.show()
fig.savefig('com_number-consumption_pic.png',
            dpi=500, bbox_inches='tight')

#%%
#industrial number-consumption relationship
fig,ax = plt.subplots()
ax.plot(ind_merge1['consumption, MMcf']/1000, color="orangered")
ax.set_xlabel("year",fontsize=12)
ax.set_ylabel("consumption, Bcf",color="orangered",fontsize=12)

ax2=ax.twinx()
ax2.plot(ind_merge1['number']/1000,color="deepskyblue")
ax2.set_ylabel("number of consumers, thousands",color="deepskyblue",fontsize=12)
ax.set_title("Consumption and number of consumers in the United States (Industrial)", fontsize = 7)
fig.tight_layout()
plt.show()
fig.savefig('ind_number-consumption_pic.png',
            dpi=500, bbox_inches='tight')


#%%
#Plotting the consumption per capita and average price
# create figure and axis objects with subplots()
fig,ax = plt.subplots()
# make a plot
ax.plot(res_merge1['per capita, MMcf'], color="orangered", marker="o")
# set x-axis label
ax.set_xlabel("year",fontsize=12)
# set y-axis label
ax.set_ylabel("consumption per capita, MMcf",color="orangered",fontsize=12)

#Next we use twinx() function to create the second axis object “ax2”. 
# twin object for two different y-axis on the sample plot
ax2=ax.twinx()
# make a plot with different y-axis using second axis object
ax2.plot(res_merge1['average price, $ per Mcf'],color="deepskyblue",marker="o")
ax2.set_ylabel("average price, $ per Mcf",color="deepskyblue",fontsize=12)
ax.set_title("Price-consumption dynamics in the United States (Residential)", fontsize = 8)
plt.show()
fig.savefig('res_price-consumption_pic.png',
            dpi=500, bbox_inches='tight')
#%%
#Do same procedure for commercial and industrial consumers
fig,ax = plt.subplots()
ax.plot(com_merge1['per capita, MMcf'], color="orangered", marker="o")
ax.set_xlabel("year",fontsize=12)
ax.set_ylabel("consumption per capita, MMcf",color="orangered",fontsize=12)

ax2=ax.twinx()
ax2.plot(com_merge1['average price, $ per Mcf'],color="deepskyblue",marker="o")
ax2.set_ylabel("average price, $ per Mcf",color="deepskyblue",fontsize=12)
ax.set_title("Price-consumption dynamics in the United States (Commercial)", fontsize = 8)
plt.show()
fig.savefig('com_price-consumption_pic.png',
            dpi=500, bbox_inches='tight')
#%%
fig,ax = plt.subplots()
ax.plot(ind_merge1['per capita, MMcf'], color="orangered", marker="o")
ax.set_xlabel("year",fontsize=12)
ax.set_ylabel("consumption per capita, MMcf",color="orangered",fontsize=12)

ax2=ax.twinx()
ax2.plot(ind_merge1['average price, $ per Mcf'],color="deepskyblue",marker="o")
ax2.set_ylabel("average price, $ per Mcf",color="deepskyblue",fontsize=12)
ax.set_title("Price-consumption dynamics in the United States (Industrial)",  fontsize = 8)
plt.show()
fig.savefig('ind_price-consumption_pic.png',
            dpi=500, bbox_inches='tight')



#%%


jg = sns.lmplot(data = res_merge1, x="average price, $ per Mcf", y="per capita, MMcf")
ax = plt.gca()
ax.set_title("Residential consumption elasticity of price")
jg.savefig("resid_price_elasticity")

jg = sns.lmplot(data = com_merge1, x="average price, $ per Mcf", y="per capita, MMcf")
ax = plt.gca()
ax.set_title("Commercial consumption elasticity of price")
jg.savefig("com_price_elasticity")

jg = sns.lmplot(data = ind_merge1, x="average price, $ per Mcf", y="per capita, MMcf")
ax = plt.gca()
ax.set_title("Industial consumption elasticity of price")
jg.savefig("ind_price_elasticity")























