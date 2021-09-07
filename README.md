# US-NG-Consumption-Market
Leveraging U.S. EIA open data, I investigated the United States Natural Gas (NG) consumption and prices dynamics and their correlation as well as compared NG prices between states.

## Project objectives

The repository is created as a final project for the SU Maxwell schools's PAI 789 "Advanced Policy Analysis" class. In this project, I investigated the United States' natural gas domestic consumption market. Particularly, I am interested in answering the following questions:

- How the number of consumers has changed over time by type of consumers and how this affected the total consumption?
- Did the consumption per capita increase over time?
- How the prices of different consumers categories vary in different States?
- Which states has the biggest gap between the Citygate and End prices?
- How significant (statistically) the price change's correlated with the consumption? 

## Limitations

Due to the limited open data, power plants prices and consumption were not included. Hence, the analysis focused only to three categories of consumers, namely, Residential, Commercial and Industrial. The main objective of this project is to understand the general economic market features utilizing some of the skills obtained in the course.

## Data Source

Data were sourced from reports downloaded from the U.S. Energy Information Administration’s (EIA) website https://www.eia.gov/energyexplained/natural-gas/.
For some reasons, wellhead prices and some consumption types in some states may not have been made available. Therefore, in some cases, States with incomplete or insufficient records were dropped manually or by Pandas and were not included in the analysis.

List of Data Used

1. The US Total Natural Gas number of consumers by type downloaded from this link https://www.eia.gov/dnav/ng/ng_cons_num_dcu_nus_a.htm. 
  a. Choose Area "U.S." and click "Download Series History". 
  b. Since it has long unclear name and we will need to download a bunch of other files, i renamed it Rename the file as "consumers_total_bytype.xls". 
2. Next, we need to download the Consumption data for each state from this link: https://www.eia.gov/dnav/ng/ng_cons_sum_dcu_nus_a.htm. 
  a. Choose "Annual" period and download each file in turn for every state. 
  b. Rename each report by using this naming convention:  state_con.xls, where * is a state name with lower cases divided by underscore. 
3. Do the same procedure in number (2) for prices data from this link https://www.eia.gov/dnav/ng/ng_pri_sum_dcu_SAL_a.htm and name each file as state _prices.xls. It is required to store Save all files in same repository to make scripts run properly.

## Scripts

There are 5 scripts each mainly uses Pandas module and reframe the data in the way for concrete objectives. I used Anaconda's Spyder with following modules: pandas, matplotlib.pyplot, os, seaborn, geopandas, statsmodels.api. For the final Panel data correaltion analysis I additionally use Stata to import the generated csv files. Finally, using QGIS I mapped average price differences on the US map.

### Script 1: 1_corr_cons.py

The data for the natural gas consumers were processed separately since they represent different market layers and serve different purposes. This script worked with consumption data and accomplished the following:

-	parse the total number of consumers for each category of market to appropriate DataFrame;
-	iterates through each states file to parse and distribute the consumption data for three Dataframes according to a type of consumer;
-	create new dataframe summarizing the consumption to analyze the consumption dynamics.

Results show fluctuations of the consumption for each category, but the most dramatic swing is for the industrial sector, which suggests that this category one class is the most sensitive. 

![NG_consumption.png](https://github.com/Nursultan77/US-NG-Consumption-Market/blob/main/NG_consumption.png) 

To see the reasons, I want to check whether the number of consumers changed significantly or not. This is hard to see from the cone graph since the consumers quantity differs significantly between the categories as the residential consumers are essentially households, while the relatively small number of industrial consumers such as factories each consumes much more NG. That is why, following three graphs (res_consum-number.png, com_consum-number.png, ind_consum-number.png) show correlation separately.

### Script 2: 2_ave_end_pr.py

This script is designed to visualize the end consumers price elasticity, and prepares the Dataframe of the average weighted end price for the script #3 where we will compare the difference between the citygate and final consumers prices differences in every state of the country. Since the prices from the source website contains the prices in real $ dollars ($), we don't need to correct adjust them by for inflation rate. To get the weighted price, we need to have the consumption data, which could be read from the previous script. Next, iterate through the .xls files to get the necessary columns that contain price for each category of consumers. For the next lines after erasing removing unnecessary symbols from state columns, pandas can multiply, summarize and divide each cell of the dataframes according to the headings and the indexes. final_pr_df is the final dataframe that contain average weihted weighted prices for each state and year. Doing similare procedure,  we get the av_pr and av_pr_long dataframes that contain average country's end prices.

Firstly, we can see, that the prices general tendencies over the years for all categories were the same with peak in late 2000's and further decline. 
![](https://github.com/Nursultan77/US-NG-Consumption-Market/blob/main/ave_prices_bysector.png) 

Next, we can look at the change in total consumption with change in consumers quantity.

As we can see, despite the increase number of residential consumers by 40%, te its total consumption did not change significantly. 
![](https://github.com/Nursultan77/US-NG-Consumption-Market/blob/main/res_number-consumption_pic.png) 

We also can see proportional growth with some fluctuations for commercial consumers quantity 
![](https://github.com/Nursultan77/US-NG-Consumption-Market/blob/main/com_number-consumption_pic.png) 

The most interesting is that for the industrial market, we can observe the dramatic drop of total consumption associated with decrease of consumers number since late 1990's till late 2000's and controversial increase of consumption after despite the decrease in total consumers number.
![](https://github.com/Nursultan77/US-NG-Consumption-Market/blob/main/ind_number-consumption_pic.png) 

Further, I illustrate the change of the prices and the consumption, which are represented in the attached presentation.
 
### Script 3: 3_prices_diff_by_state.py

Before we will get rid of the years and states fixed effects to check the more precise correlation between the consumption and prices, since we have weighted average end prices, we can examine the difference distribution between natural gas citygate and final prices. For this analysis I chose the year 2010 since this is the last year that contains data of prices for the vast majority of states. Later, we will visualize them on the GIS map. 

As we can see from the first graph, since the distribution of the citygate prices is quite narrow, the final prices are distributed more wider. the final prices are more widely dispersed than the citygate prices. Average citygate price in 2010 was $ 6.64 per Mcf, while average final price was $ 9.82 per Mcf.

![](https://github.com/Nursultan77/US-NG-Consumption-Market/blob/main/price_density.png) 

From the second figure, we can see observe that Delaware, Florida, Arizona, Georgia, New York, Washington, Missouri and Mariland Maryland has have the biggest difference between citygate and final prices and the price of natural gas in Hawaii differs from the rest of the country dramatically. Major Oil and Gas producing states such as Texas and Louisiana final prices are even lower than their citygate price.

![](https://github.com/Nursultan77/US-NG-Consumption-Market/blob/main/citygate_final_barplot.png) 

### Script 4: 4_fixed_eff and Stata regression

This script consolidates all previous data to final three dataframes of panel data according to consumer type to check the elasticities of the price. Then, save these dataframes to .csv files to import them in Stata.

Note: My Mac with Big Sur operational system seem like has some issues of supporting does not seem to support some modules such as 'linearmodels', so I ran this these regressions in Stata. To do that, we need to open Stata. Click Import from toolbar and choose Text data, choose sequentially each saved csv file and run the regression (check whether necessary variables have numeric values). As we can see, the consumption and prices are also highly correlated with national GDP, so I also control for GDP (Bureau of Economic Analysis data - https://www.bea.gov/data/gdp). The results of the regressions are saved in res-com-ind_reg.docx file.

### Script 5: 5_prices_geo and Mapping price differences

The final script is used in processing the data will be used top use the Data for mapping the average end prices on the map for each state, and represent the difference between consumers categories.

For plotting our analysis, we need to download shapefile from open source https://www.igismap.com/united-states-shapefile-download-free-map-boundary-states-and-county/. Save this file to the same folder of the final project and merge 2019 end prices data with the "shp" file. For concatenating the different styles of states to use them as a merge key, I used their states abbrevation abbreviation from this link https://gist.github.com/rogerallen/1583593 as merge key. And and added "US-" signs to all rows to match keys. as Igis folder we download has them.

In QGIS, I load the created by script#5 the 'states.gpkg' file created in script # 5. We need to create a copy of the layer to make stiped layer for mapping missing values of states. Set 'iso' label for states to mark them with obrevations observations. Drag the "FDiagonal" styled layer to the bottom and set black color. Then set "Graduated" style to initial prices layer with "Red" color ramp with 6 classes where more intensed color is for the higher quintiles of average end prices. That will show us the difference of end prices between states. Then add "Stacked bars with residential, commercial and industrial sectors respectively to see the gap between the category prices within a state.  

![](https://github.com/Nursultan77/US-NG-Consumption-Market/blob/main/prices_map.png)

### Conclusions:
- The quantity of residential consumers was risen even despite that its category's price is higher, so its equilibrium price is higher than the for the rest of market.
- For commercial market, although there is a positive correlation between the number of consumers, and total consumption, this market is pretty sensitive to price change. there is a same correalation for industrial market, although this market requires "long" investments, I assume, for this reason this part of the market was unable to manage the plant comissioning plans when the prices were risen in 2004-2008 years, after 2008, when prices get gown, the market could slightly recover that illustrates the increase in consumption. As we can see, when price dropped down after year 2008, even the number of industries declined, there was a persistent rise of consumption.
- For the most of the states, the residential prices are higher than for the rest share of the market.
- Top 5 States with the smallest gap between citygate end end prices gap are Louisiana, Texas, North Dakota, Wyoming, South Dakota. The general trend shows that states with lowest end prices have smallest gap between citygate and final prices. Top 5 States with biggest gap are Delaware, Florida, Arizona, Georgia, New York.

