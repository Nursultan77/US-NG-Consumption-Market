#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  7 20:03:23 2021

@author: nursultanyeshmukhan
"""

#This script summarize the data of the Natural Gas consumption in the United States,
# also provides the sumarize information of the number of consumers, and finally,
# shows the correlation between theNatural Gas consumption and number of consumbers
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
# Open the US total consumers number by type of consumers

res_xls = pd.read_excel("consumers_total_bytype.xls", 
                           sheet_name= "Data 1", 
                           header = 2, index_col="Date", 
                           usecols = ["Date", "U.S. Natural Gas Number of Residential Consumers (Count)"], 
                           dtype = str)


com_xls = pd.read_excel("consumers_total_bytype.xls", 
                                sheet_name= "Data 2", 
                                header = 2, index_col="Date", 
                                usecols = ["Date", "U.S. Natural Gas Number of Commercial Consumers (Count)"],
                                dtype = str)

ind_xls = pd.read_excel("consumers_total_bytype.xls", 
                            sheet_name= "Data 3", 
                            header = 2, index_col="Date", 
                            usecols = ["Date", "U.S. Natural Gas Number of Industrial Consumers (Count)"],
                            dtype = str)


#%%
# Get the number of consumers to its Dataframe by type 
res_count = pd.DataFrame()
com_count = pd.DataFrame()
ind_count = pd.DataFrame()
for col in res_xls.columns:
    res_c = res_xls[col]
    res_count['number'] = res_c
    res_count["sector"] = "residential"
    
for col in com_xls.columns:
    com_c = com_xls[col]
    com_count["number"] = com_c
    com_count["sector"] = "commercial"
        
for col in ind_xls.columns:
    ind_c = ind_xls[col]
    ind_count["number"] = ind_c
    ind_count["sector"] = "industrial"



#%%

# Get the total consumption by type: Iterate through consumption by state files
# to concatenate the consumption quantity by type of consumers
path = os.getcwd()
consumption = os.listdir("/Users/nursultanyeshmukhan/Desktop/PAI789/US-NG-Consumption-Market/consumption/")

con_xls = [f for f in consumption if f[-7:] == 'con.xls']

# DataFrames of residential, commercial and industrial consumption respectively data
res_con = pd.DataFrame()
com_con = pd.DataFrame()
ind_con = pd.DataFrame()

for f in con_xls:
    data = pd.read_excel(f, sheet_name = 'Data 1', header = 2, index_col = "Date")
    for col in data.columns:
        if "Residential" in col:
            res_c = data[col]
            res_con[f] = res_c         
        elif "Commercial" in col:
            com_c = data[col]
            com_con[f] = com_c 
        elif "Industrial" in col:
            ind_c = data[col]
            ind_con[f] = ind_c

            
res_con = res_con.dropna(axis = 0)
com_con = com_con.dropna(axis = 0)
ind_con = ind_con.dropna(axis = 0)   
 

# Remove "_con.xls" part from each column
res_con.columns = res_con.columns.map(lambda x: str(x)[:-8])
com_con.columns = com_con.columns.map(lambda x: str(x)[:-8])
ind_con.columns = ind_con.columns.map(lambda x: str(x)[:-8])  
 
       
#%%
# Summarize total country's consumption through iter
res_con_tot = pd.DataFrame()
com_con_tot = pd.DataFrame()
ind_con_tot = pd.DataFrame()

res_con_tot["consumption, MMcf"] = res_con.sum(axis = "columns")
res_con_tot["sector"] = "residential"
com_con_tot["consumption, MMcf"] = com_con.sum(axis = "columns")
com_con_tot["sector"] = "commercial"
ind_con_tot["consumption, MMcf"] = ind_con.sum(axis = "columns")
ind_con_tot["sector"] = "industrial"


#%%
# Merge dataframes of consumption and number of consumers by each type of consumers
# Along the way, calculate consumption per capita dividing appropriate columns values
res_merge = res_count.merge(res_con_tot["consumption, MMcf"], left_index=True, right_index=True)
res_merge["number"] = res_merge["number"].astype(float)
res_merge["per capita, MMcf"] = res_merge["consumption, MMcf"]/res_merge["number"]

com_merge = com_count.merge(com_con_tot["consumption, MMcf"], left_index=True, right_index=True)
com_merge["number"] = com_merge["number"].astype(float)
com_merge["per capita, MMcf"] = com_merge["consumption, MMcf"]/com_merge["number"]

ind_merge = ind_count.merge(ind_con_tot["consumption, MMcf"], left_index=True, right_index=True)
ind_merge["number"] = ind_merge["number"].astype(float)
ind_merge["per capita, MMcf"] = ind_merge["consumption, MMcf"]/ind_merge["number"]


frames = [res_merge, com_merge, ind_merge]
conc_df = pd.concat(frames)
conc_df["number"] = conc_df["number"].astype(float)


#%% Visualize:
    # consumption by year and type
jg = sns.relplot(data=conc_df, x='Date', y='consumption, MMcf',col='sector',kind='line')
jg.savefig('NG_consumption.png')
    # consumers by year and type
jg = sns.relplot(data=conc_df, x='Date', y='number',col='sector',kind='line')

#%% # consumption by number and type (quantity of consumers elasticity
# Residential consumption is kinda elastic (almost no corrrelation)
jg = sns.lmplot(data=res_merge, x='number', y='consumption, MMcf')
ax = plt.gca()
ax.set_title("Quantity Elasticiy of number (Residential)")
jg.savefig('res_consum-number.png')
#%%
jg = sns.lmplot(data=com_merge, x='number', y='consumption, MMcf')
ax = plt.gca()
ax.set_title("Quantity Elasticiy of number (Commercial)")
jg.savefig('com_consum-number.png')
#%%
jg = sns.lmplot(data=ind_merge, x='number', y='consumption, MMcf')
ax = plt.gca()
ax.set_title("Quantity Elasticiy of number (Industrial)")
jg.savefig('ind_consum-number.png')
#%%

# Indeed, per capita cpnsumption decreased. Later we will analyze the price elasticity to check vulnerability to price 
jg = sns.relplot(data=res_merge, x='Date', y='per capita, MMcf',kind='line')
ax = plt.gca()
ax.set_title("US NG consumption per capita (Residential)")
jg.savefig('res_consum-capita.png')
#For commercial did not change significantly
jg = sns.relplot(data=com_merge, x='Date', y='per capita, MMcf',kind='line')
ax = plt.gca()
ax.set_title("US NG consumption per capita (Commercial)")
jg.savefig('com_consum-capita.png')
# For industrial, there is a fall till 2008, and then dramatic rise
jg = sns.relplot(data=ind_merge, x='Date', y='per capita, MMcf',kind='line')
ax = plt.gca()
ax.set_title("US NG consumption per capita (Industrial)")
jg.savefig('ind_consum-capita.png')
#We see the fluctuation of the consumption
#%%

# Regression


# Note the difference in argument order
model_res = sm.OLS(res_merge['consumption, MMcf'], res_merge['number']).fit()
print(model_res.summary())

model_com = sm.OLS(com_merge['consumption, MMcf'], com_merge['number'], missing = "drop").fit()
print(model_com.summary())

model_ind = sm.OLS(ind_merge['consumption, MMcf'], ind_merge['number']).fit()
print(model_ind.summary())


res_con.to_pickle("res_con.pkl")
com_con.to_pickle("com_con.pkl")
ind_con.to_pickle("ind_con.pkl")
conc_df.to_pickle("conc_df.pkl")

res_merge.to_pickle("res_merge.pkl")
com_merge.to_pickle("com_merge.pkl")
ind_merge.to_pickle("ind_merge.pkl")


