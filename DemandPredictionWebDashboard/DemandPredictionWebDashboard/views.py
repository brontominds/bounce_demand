"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, request
from DemandPredictionWebDashboard import app
import requests
import json
import pandas as pd
import os


APP_ROOT=os.path.dirname(os.path.abspath(__file__))
FILE_PATH=os.path.join(APP_ROOT,'output.csv')



@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/predict', methods = ['POST'])
def predict():
    df=pd.read_csv(FILE_PATH)
    """Renders the contact page."""
    hour=request.form['hour']
    date=request.form['date']
    location=request.form['location']
    
def filtering_the_data(df,location,date,hour):

if df['place'].str.contains(location).any():
    df=df[df['datetime'].dt.date.astype(str) == date]
    df=df[df['hour']==(hour)]
    return df
else:
    print('Location not present')
    
def length_of_dataframe(df):
    if len(df)==0:
    return render_template(
        'contact.html')
elif len(df)>1:
    return render_template(
        'contact.html')
else:
    return df

def holiday(df):
    flag=True
    if df['holiday'].isnull().values.any()==flag:
         return render_template('contact.html')
    else:
        holiday=df['holiday'].astype(int)
        return holiday
    
def workingday(df):
    flag=True
    if df['workingday'].isnull().values.any()==flag:
         return render_template('contact.html')
    else:
        workingday=df['workingday'].astype(int)
        return workingday
    
def temp(df):
    flag=True
    if df['temp'].isnull().values.any()==flag:
         return render_template('contact.html')
    else:
        temp=df['temp'].astype(float)
        return temp
    
def atemp(df):
    flag=True
    if df['app_temp'].isnull().values.any()==flag:
         return render_template('contact.html')
    else:
        atemp=df['app_temp'].astype(float)
        return atemp
    
def humidity(df):
    flag=True
    if df['rh'].isnull().values.any()==flag:
         return render_template('contact.html')
    else:
        humidity=df['rh'].astype(float)
        return humidity
    
def weather(df):
    flag=True
    if df['weather_code'].isnull().values.any()==flag:
         return render_template('contact.html')
    else:
        weather=df['weather_code'].astype(int)
        return weather
    
def season(df):
    flag=True
    if df['season_code'].isnull().values.any()==flag:
         return render_template('contact.html')
    else:
        season=df['season_code'].astype(int)
        return season
    
def windspeed(df):
    flag=True
    if df['windspeed'].isnull().values.any()==flag:
         return render_template('contact.html')
    else:
        windspeed=df['windspeed'].astype(int)
        return windspeed
    
def year(df):
    flag=True
    if df['year'].isnull().values.any()==flag:
         return render_template('contact.html')
    else:
        year=df['year'].astype(int)
        return year
    
def day(df):
    flag=True
    if df['day'].isnull().values.any()==flag:
         return render_template('contact.html')
    else:
        year=df['day'].astype(int)
        return year

def hour(df):
    flag=True
    if df['hour'].isnull().values.any()==flag:
         return render_template('contact.html')
    else:
        hour=df['hour'].astype(int)
        return hour
        
        
def month(df):
    flag=True
    if df['month'].isnull().values.any()==flag:
         return render_template('contact.html')
    else:
        month=df['month'].astype(int)
        return month
  
  df= filtering_the_data(df,location,date,hour)
     df=length_of_dataframe(df)
  
    
    
    
    
    params={
        'holiday':holiday(df),
        'workingDay':workingday(df),
        'temp':temp(df),
        'atemp':atemp(df),
        'humidity':humidity(df),
        'windspeed':windspeed(df),
        'season':season(df)
        'weather':weather(df),
        'year':year(df),
        'day':day(df),
        'hour':hour(df),
        'dayofweek':dayofweek(df),
        'month':month(df)
        
        }

    url='http://127.0.0.1:5000/predict'


    r = requests.post(url, data=params)
    data = r.json()
    a = data['prediction']

    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Predicted Demand',
        demand=a
    )



@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )
