import pandas as pd
from sklearn.utils import shuffle
import matplotlib.pyplot as plt  # For plotting graphs 
from datetime import datetime    # To access datetime 

#Add date time specific columns to the dataframe
def datetime(df):
  from datetime import datetime
  df['datetime'] = pd.to_datetime(df['datetime'])
  df['year'] = df['datetime'].dt.year
  df['month']=df['datetime'].dt.month
  df['day'] = df['datetime'].dt.day 
  df['hour'] = df['datetime'].dt.hour
  df['dayofweek'] = df['datetime'].dt.dayofweek
  return df

#Normalize a column of dataframe and return mean and sd
def normalize(df,feature_name):
    result=df.copy()
    #for feature_name in columns :
    mean_value = df[feature_name].mean()
    std_value = df[feature_name].std()
    result[feature_name] = (df[feature_name] - mean_value) / std_value        
    return (result, mean_value, std_value)


#Read Training Data
data=pd.read_csv("data/train.csv")
data_original=data

data=datetime(data)
data=data.drop('datetime',axis=1)

data, mean_temp, sd_temp=normalize(data,["temp"])
data,mean_atemp,sd_atemp=normalize(data,["atemp"])
data,mean_humidity,sd_humidity=normalize(data,["humidity"])
data,mean_windspeed,sd_windspeed=normalize(data,["windspeed"])


#For debugging only
print(mean_temp, sd_temp, mean_atemp, sd_atemp, mean_humidity, sd_humidity, mean_windspeed, sd_windspeed)
#