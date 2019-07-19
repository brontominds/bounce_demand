"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, request
from DemandPredictionWebDashboard import app
import requests
import json


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
    """Renders the contact page."""
    holiday=request.form['holiday']
    workingday=request.form['workingDay']
    temp=request.form['temp']
    atemp=request.form['atemp']
    humidity=request.form['humidity']
    windspeed=request.form['windspeed']
    season=request.form['season']
    weather=request.form['weather']
    year=request.form['year']
    day=request.form['day']
    hour=request.form['hour']
    dayofweek=request.form['dayofweek']
    month=request.form['month']
    date=request.form['date']
    location=request.form['location']

    params={
        'holiday':holiday,
        'workingDay':workingday,
        'temp':temp,
        'atemp':atemp,
        'humidity':humidity,
        'windspeed':windspeed,
        'season':season,
        'weather':weather,
        'year':year,
        'day':day,
        'hour':hour,
        'dayofweek':dayofweek,
        'month':month
        
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
