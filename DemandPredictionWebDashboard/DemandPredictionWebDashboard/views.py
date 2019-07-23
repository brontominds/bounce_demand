"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, request
from DemandPredictionWebDashboard import app
import sys
import os



import requests
import json
import pandas as pd

wff=sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'wf'))
#print(sys.path[-1])
from wff import weatherForecast

    
def Checking_Null_values(df,column_name):
    flag=True
    if df['column_name'].isnull().values.any()==flag:
         return render_template('contact.html')
    else:
        column_name=df['column_name']
        return column_name

    
def validate(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
        
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")
        
def validate_hour(hour):
    try:
        if (int(hour)<0)&(int(hour)>23):
    except ValueError:
        raise ValueError("Invalid value")

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
    date=validate(request.form['date'])
    location=request.form['location']
 
    
    df.inputData('latlon',[12.9304,77.6784] ,location)
    data=df.filterP(location,date,hour)
   
   

    
    params={
        'holiday':Checking_Null_values(data,holiday),
        'workingDay':Checking_Null_values(data,workingday),
        'temp':Checking_Null_values(data,temp),
        'atemp':Checking_Null_values(data,app_temp),
        'humidity':Checking_Null_values(data,rh),
        'windspeed':Checking_Null_values(data,wind_spd),
        'season':Checking_Null_values(data,season_code),
        'weather':Checking_Null_values(data,weather_code),
        'year':Checking_Null_values(data,year),
        'day':Checking_Null_values(data,day),
        'hour':hour,
        'dayofweek':Checking_Null_values(data,dayofweek),
        'month':Checking_Null_values(data,month)
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
