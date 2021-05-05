# US-NG-Consumption-Market
Leveraging U.S. EIA open data I investigate the United States Natural Gas consumption and prices dynamics and their correlation as well as compare NG prices between states 

## Project aim

The repository is created as a final project of the Maxwell PAI 789 "Advanced Policy Analysis" class. In this project I investigate the United States natural gas domestic consumption market. Particularly, I am interested in answering questions:

How the number of consumers has changed over time by type of consumers and how this affected the total consumption?
Did the consumption per capita increase over time?
How the prices of different consumers categories varies in different States?
Which states has the biggest gap between the Citygate and End prices?
How significant (statistically) the price change over time affects the consumption? 

## Limitations

Due to the limitations of open data, I was not able to get the Power plants prices and consumption so my work is limited only by three categories of consumers such as Residential, Commercial and Industrial sectors. However, the main aim of this project is to understang the market features, and finally to consolidate some skills obtained during the course.

## Data Source

The source of data are excel sheets from the The U.S. Energy Information Administration (EIA)https://www.eia.gov/energyexplained/natural-gas/. Perhaps, since the Natural Gas market is strategic and highly related to National Security, theres is a scarcity of the data of wellhead prices and some consumption types in some states, we will drop the states information with the insufficient data or Pandas will do it for us.
Getting and preparing the Data

The first file we need is The US Total Natural Gas number of consumers by type which is the excell file can be downloaded from this link https://www.eia.gov/dnav/ng/ng_cons_num_dcu_nus_a.htm. Choose Area "U.S." and click "Download Series History". Since it has long unclear name and we will need to download a bunch of other files, i renamed it as "consumers_total_bytype.xls".
Next, we need to download the consumption data for each state from this link: https://www.eia.gov/dnav/ng/ng_cons_sum_dcu_nus_a.htm. Choose "Annual" period and download each file in turn for every state. Rename them by *_con.xls, where * is a state name with lower cases divided by underscore. Do same procedure for prices from this link https://www.eia.gov/dnav/ng/ng_pri_sum_dcu_SAL_a.htm and name each file as *_prices.xls. It is required to store all files in same repository to make scripts run properly.

## Scripts

There are 5 scripts each mainly uses Pandas module and reframe the data in the way for concrete objectives. I use Spyder Anaconda with following modules: pandas, matplotlib.pyplot, os, seaborn, geopandas, statsmodels.api. For the final Panel data correaltion analysis I additionally use Stata from the generated csv files. Finally, using I map average price differences on the US map

### Script 1: 1_corr_cons.py

Since the natural gas consumers are basically divided by three categories, each of them has its own purposes of usage and incomparable with each other as represent the different market layers, it makes sence to work with each category separately to execute necessary commands for each of them and do not mix with each other. This script essentially works with consumption data, doing the following:

- iterates through each consumers files to get three Dataframes with number of consumers of each consumption category and three Dataframes with consumption data parsing the data from each of file of the state;
- since the consumption dataframes contains has a prosperity of data by each state which we will need later, create new dataframe summarizing the consumption to analyze the consumption dynamics.

From the first graph NG_consumption.png, we can see the fluctuations of the consumption for each category, but the most dramatic swing is for the industrial sector, which makes me presume that this category one is the most sensitive.
![NG_consumption.png](https://github.com/Nursultan77/US-NG-Consumption-Market/blob/main/NG_consumption.png) 

To see the reasons, I want to check whether the number of consumers changed significantly or no. This is hard to see from the cone graph since the consumers quantity differs significantly between the categories which makes sense since the residential consumers are essentially households, while the relatively small number of industrial consumers such as factories each consumes much more NG. That is why, following three graphs shows the the correlation separetely.

### Script 2: 2_ave_end_pr.py

This script is designed to visualize the end consumers price elasticity, and prepares the dataframe of the average weighted end price for the script #3 where we will compare the difference between the citygate and final consumers prices differences in every state of the country. Since the prices from the source website contains the prices in real $ dollars, we don't need to correct them by inflation rate. To get the weighted price, we need to have the consumption data, which could be read from the previous script. Next, iterate through the .xls files to get the necessary columns that contain price for each category of consumers. For the next lines after erasing unnecessary symbols from state columns, pandas can multiply, summarize and divide each cell of the dataframes according to the headings and the indexes. final_pr_df is the final dataframe that contain average weihted prices for each state and year. Doing similare procedure we get the av_pr and av_pr_long dataframes that contain average country's end prices.

Firstly, we can see, that the prices general tendencies over the years for all categories were the same with peak in late 2000's and further decline. 
![](https://github.com/Nursultan77/US-NG-Consumption-Market/blob/main/ave_prices_bysector.png) 

Next, we can look at the change in total consumption with change in consumers quantity.

As we can see, despite the increase number of residential consumers by 40%, te its total consumption did not change significantly. 
![](https://github.com/Nursultan77/US-NG-Consumption-Market/blob/main/res_number-consumption_pic.png) 

We also can see proportional growth with some fluctuations  for commercial consumers quantity 
![](https://github.com/Nursultan77/US-NG-Consumption-Market/blob/main/com_number-consumption_pic.png) 

The most interesting is that for the industrial market, we can observe the dramatic drop of total consumption despite of the rapid growth of consumer's number 
![](https://github.com/Nursultan77/US-NG-Consumption-Market/blob/main/com_number-consumption_pic.png) 

### Script 3: 3_prices_diff_by_state.py

Before we will get rid of the years and states fixed effects to check the more precise correlation between the consumption and prices, since we have weighted average end prices, we can examine the difference distribution between natural gas citygate and final prices. For this analysis I chose the year 2010 since as this is the last year contains that contains data of prices for the vast majority of states. Later, we will visualize them on the GIS map. 

As we can see from the first graph, since the distribution of the citygate prices is quite narrow, the final prices are distributed more wider. Average citygate price in 2010 was $ 6.64 per Mcf, average final price was $ 9.82 per Mcf.
![](https://github.com/Nursultan77/US-NG-Consumption-Market/blob/main/price_density.png) 

From the second picture we can see that Delaware, Florida, Arizona, Georgia, New York, Washington, Missouri and Mariland has the biggest difference between citygate and final prices and the price of natural gas in Hawaii differs from the rest of the country dramatically. Oil and Gas procution states Texas and Louisiana final prices are even lower than their citygate price.
![](https://github.com/Nursultan77/US-NG-Consumption-Market/blob/main/citygate_final_barplot.png) 

### Script 4: 4_fixed_eff and Stata regression

This scrypt consolidates all previous data to final three dataframes of panel data according to consumers type to check the elasticities of the price. Then, save these dataframes to .csv files to import them in Stata. Note: My Mac with Big Sur operational system seem like has some issues of supporting some modules such as linearmodels, so I run this regressions in Stata. To do that, we need to open Stata. Click Import from toolbar and choose Text data, choose sequentially each saved csv file and run the regrression (check whether necessary variables have numeric values).  As we can see, the consumptiona and prices are also highly correlated with national GDP, so I also control for GDP (Bureau of Economic Analysis data - https://www.bea.gov/data/gdp).

### Script 5: 5_prices_geo and Mapping price differences

The final script will be used top use the Data for mapping the average end prices on the map for each state, and represent the difference between consumers categories.

For plotting our analysis, we need to download shapefile from open source https://www.igismap.com/united-states-shapefile-download-free-map-boundary-states-and-county/. Save this file to the same folder of the final project and merge 2019 end prices data with "shp" file. For concatenating the different styles of states to use them as a merge key, I use states abbrevation from this link https://gist.github.com/rogerallen/1583593. And add "US-" signs to all rows. as Igis folder we download has them.

In QGIS, I load the created by script#5 'states.gpkg' file. We need to create a copy of the layer to make stiped layer for mapping missing values of states. Set 'iso' label for states to mark them with obrevations. Drag the "FDiagonal" styled layer to the bottom and set black color. Then set "Graduated" style to initial prices layer with "Red" color ramp with 6 classes where more intensed color is for the higher quintiles of average end prices. That will show us the difference of end prices between states. Then add "Stacked bars with residential, commercial and industrial sectors respectively to see the gap between the category prices within a state. 
![](https://github.com/Nursultan77/US-NG-Consumption-Market/blob/main/prices_map.png)
