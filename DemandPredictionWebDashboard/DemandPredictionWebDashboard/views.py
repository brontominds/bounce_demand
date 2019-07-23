"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, request
from DemandPredictionWebDashboard import app
import sys
import os
import string


import requests
import json
import pandas as pd

wff=sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'wf'))
#print(sys.path[-1])
from wff import weatherForecast

    
def holiday(df):
    flag=True
    if df['holiday'].isnull().values.any()==flag:
         return render_template('contact.html')
    else:
        holiday=df['holiday']
        return holiday


#TODO: Currently monsoon=4 is built. take care of other seasons. Ideally, Mayank should return an integer.
def ConvertSeason(stringSeason):
    stringSeason = (str(stringSeason).strip()).upper()

    if (stringSeason.find("MONSOON") !=-1):
        return 4;
    else:
        return 3;

def season(df):
    flag=True
    if df['season'].isnull().values.any()==flag:
         return render_template('contact.html')
    else:
        season=ConvertSeason(df['season'])
        return season
    
def workingday(df):
    flag=True
    if df['workingday'].isnull().values.any()==flag:
         return render_template('contact.html')
    else:
        workingday=df['workingday']
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
        weather=df['weather_code']
        return weather
    

def windspeed(df):
    flag=True
    if df['wind_spd'].isnull().values.any()==flag:
         return render_template('contact.html')
    else:
        windspeed=df['wind_spd']
        return windspeed
    
def year(df):
    flag=True
    if df['year'].isnull().values.any()==flag:
         return render_template('contact.html')
    else:
        year=df['year']
        return year
    
def day(df):
    flag=True
    if df['day'].isnull().values.any()==flag:
         return render_template('contact.html')
    else:
        year=df['day']
        return year
        
        
def month(df):
    flag=True
    if df['month'].isnull().values.any()==flag:
         return render_template('contact.html')
    else:
        month=df['month']
        return month

    
def dayofweek(df):
    flag=True
    if df['dayofweek'].isnull().values.any()==flag:
         return render_template('contact.html')
    else:
        dayofweek=df['dayofweek']
        return dayofweek

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
    

    
    df=weatherForecast()
    """Renders the contact page."""
    hour=int(request.form['hour'])
    date=request.form['date']
    location=request.form['location']
    
    df.inputData('latlon',[12.9304,77.6784] ,location)
    data=df.filterP(location,date,hour)
   

    
    params={
        'holiday':holiday(data),
        'workingDay':workingday(data),
        'temp':temp(data),
        'atemp':atemp(data),
        'humidity':humidity(data),
        'windspeed':windspeed(data),
        'season':season(data),
        'weather':weather(data),
        'year':year(data),
        'day':day(data),
        'hour':hour,
        'dayofweek':dayofweek(data),
        'month':month(data)
        }

    url='http://127.0.0.1:5000/predict'


    r = requests.post(url, data=params)
    print(r.text)
    
    data=r.json()
    
        

    
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
