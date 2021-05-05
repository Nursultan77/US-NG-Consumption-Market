#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 20 19:24:12 2021

@author: nursultanyeshmukhan
"""

import pandas as pd

#%%
res_con = pd.read_pickle("res_con.pkl")
com_con = pd.read_pickle("com_con.pkl")
ind_con = pd.read_pickle("ind_con.pkl")

res_pr = pd.read_pickle("res_pr.pkl")
com_pr = pd.read_pickle("com_pr.pkl")
ind_pr = pd.read_pickle("ind_pr.pkl")

final_pr_df = pd.read_pickle("final_pr_df.pkl")

#%%
gdp = pd.read_csv("united-states-gdp-growth-rate.csv", header = 9)
gdp["year"] = gdp["date"].map(lambda x: x.replace("-12-31",''))
gdp = gdp.drop("date", axis = "columns")
gdp = gdp.dropna(axis = "columns")

#%%
gdp = pd.read_excel("historical-gdp.xlsx", sheet_name = 'Sheet0', header = 5)
gdp = gdp.loc[1].to_frame().reset_index()
gdp = gdp.loc[2:]
gdp.rename(columns={'State': 'state'}, inplace=True)
gdp.columns = ["year", "GDP, bln of dollars"]

#%%
res_con_l = res_con.unstack().reset_index()
res_con_l.columns = ["state", "Date", "consumption"]
res_con_l.set_index(["Date", "state"], inplace=True)

res_pr_l = res_pr.unstack().reset_index()
res_pr_l.columns = ["state", "Date", "price"]
res_pr_l.set_index(["Date", "state"], inplace=True)


com_con_l = com_con.unstack().reset_index()
com_con_l.columns = ["state", "Date", "consumption"]
com_con_l.set_index(["Date", "state"], inplace=True)

com_pr_l = res_pr.unstack().reset_index()
com_pr_l.columns = ["state", "Date", "price"]
com_pr_l.set_index(["Date", "state"], inplace=True)


ind_con_l = ind_con.unstack().reset_index()
ind_con_l.columns = ["state", "Date", "consumption"]
ind_con_l.set_index(["Date", "state"], inplace=True)

ind_pr_l = res_pr.unstack().reset_index()
ind_pr_l.columns = ["state", "Date", "price"]
ind_pr_l.set_index(["Date", "state"], inplace=True)


fixed_res = res_con_l.merge(res_pr_l["price"], left_index=True, right_index=True)
fixed_res = fixed_res.reset_index()
fixed_res['year'] = fixed_res['Date'].dt.strftime('%G')
fixed_res = fixed_res.drop("Date", axis = "columns")
fixed_res = fixed_res.merge(gdp, on = "year", validate = "m:1")
fixed_res.to_csv("fixed_res.csv")

fixed_com = com_con_l.merge(com_pr_l["price"], left_index=True, right_index=True)
fixed_com = fixed_com.reset_index()
fixed_com['year'] = fixed_com['Date'].dt.strftime('%G')
fixed_com = fixed_com.merge(gdp, on = "year", validate = "m:1")
fixed_com.to_csv("fixed_com.csv")

fixed_ind = ind_con_l.merge(ind_pr_l["price"], left_index=True, right_index=True)
fixed_ind = fixed_ind.reset_index()
fixed_ind['year'] = fixed_ind['Date'].dt.strftime('%G')
fixed_ind = fixed_ind.merge(gdp, on = "year", validate = "m:1")
fixed_ind.to_csv("fixed_ind.csv")

# Export files to Stata to make regression from the dofile



