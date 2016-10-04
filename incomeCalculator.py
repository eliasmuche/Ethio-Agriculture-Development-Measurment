# Authors: Elias Muche & Ahmed Moalim
# Calculates daily income for two combnations of years based on inputs from the Social_Survey_Ethiopia data set
# To get data sets for different years change the path in data2011 and data2013

import pandas as pd 
import os
import math

data2011 = pd.read_csv('Social_Survey_Ethiopia_2011/sect4_hh_w1.csv') # Change to location of sec4_hh_w1.csv
data2013 = pd.read_csv('Social_Survey_Ethiopia_2013/sect4_hh_w2.csv') # Change to location of sec4_hh_w2.csv

divideBy={"nan":1,"Hour":(1/14),"Day":1,"Week":7,"Fortnight":14,"Month":30,"Quarter":(365/4),"1/2 Year":(365/2),"Year":365}

def getDailyIncome ( row ):
    
    # Change index names to calculate data for various columns  
    firstJob = row['hh_s4q16'] / divideBy[str(row['hh_s4q17'])] if not math.isnan(row['hh_s4q16']) else 0   
    secondJob = row['hh_s4q27'] / divideBy[str(row['hh_s4q28'])] if not math.isnan(row['hh_s4q27']) else 0
    firstAllowance = row['hh_s4q18'] / divideBy[str(row['hh_s4q19'])] if not math.isnan(row['hh_s4q18']) else 0
    secondAllowance = row['hh_s4q29'] / divideBy[str(row['hh_s4q30'])] if not math.isnan(row['hh_s4q29']) else 0
    
    return firstJob + secondJob + firstAllowance + secondAllowance

def getincome (year):
    if year == 2013:
        data2013["Daily_Income"] = data2013.apply(lambda row: getDailyIncome (row), axis = 1)
    else :
        data2011["Daily_Income"] = data2011.apply(lambda row: getDailyIncome (row), axis = 1)

def nullIincome(row):
    inc_fields = ['hh_s4q16','hh_s4q27','hh_s4q18','hh_s4q29']
    count = 0
    for f in inc_fields:
        if pd.isnull(row[f]):
            count += 1
        else:
            continue
    if count == 4:
        return None
    else:
        return row.Daily_Income
getincome(2013)
getincome(2011)
data2011['Daily_Income'] = data2011.apply(lambda row: nullIincome(row), axis=1)
data2013['Daily_Income'] = data2013.apply(lambda row: nullIincome(row), axis=1)

data2013.head()
data2013.to_csv('output2013.csv')
data2011.to_csv('output2011.csv')