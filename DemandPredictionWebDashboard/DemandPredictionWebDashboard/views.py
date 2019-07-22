"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, request
from DemandPredictionWebDashboard import app
import importlib 
module_name = "WeatherFrecast"
from WeatherFrecast import weatherForecast
import requests
import json
import pandas as pd
import os





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
    #df=pd.read_csv(FILE_PATH)

    
    df=weatherForecast()
    """Renders the contact page."""
    hour=request.form['hour']
    date=request.form['date']
    location=request.form['location']

    data=df.filterP(location,date,hour)
    

    holiday=df.checkHolc(date)

    season=getSeasonc(date)    
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
  
  
    
    
    
    
    params={
        'holiday':holiday,
        'workingDay':workingday(data),
        'temp':temp(data),
        'atemp':atemp(data),
        'humidity':humidity(data),
        'windspeed':windspeed(data),
        'season':season,
        'weather':weather(data),
        'year':year(data),
        'day':day(data),
        'hour':hour(data),
        'dayofweek':dayofweek(data),
        'month':month(data)
        
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
