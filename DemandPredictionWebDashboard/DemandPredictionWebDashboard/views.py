"""
Routes and views for the flask application.
"""

import datetime
from flask import render_template, request
from DemandPredictionWebDashboard import app
import sys
import os



import requests
import json
import pandas as pd
try:
    wf=sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__))))
    #print(sys.path[-1])
    from wf import weatherForecast, AppError


    def Checking_Null_values(df,column_name):
        flag=True
        if df[column_name].isnull().values.any()==flag:
             return render_template('contact.html')
        else:
            column_name=df[column_name]
            return column_name
    def validate_date(dt):
        from dateutil import parser
        dt=parser.parse(dt)
        
        date=dt.strftime('%Y-%m-%d')
        return date
    def validate_hour(hr):
        if hr==['^a-zA-Z']:
            return render_template('contact.html')
        elif hr==['"!@#$%^&*()[]{};:,./<>?\|`~-=_+", " "']:
            return render_template('contact.html')
        elif int(hr)>23:
            return render_template('contact.html')
        else:
            return int(hr)



    @app.route('/')
    @app.route('/home')
    def home():
        """Renders the home page."""
        return render_template(
            'index.html',
            title='Home Page',
            year=datetime.datetime.now().year,
        )

    @app.route('/predict', methods = ['POST'])
    def predict():


        print("started")

        df=weatherForecast()
        
        """Renders the contact page."""
        
           
        hour=validate_hour(request.form['hour'])
        date= validate_date(request.form['date'])
        date_1=datetime.datetime.strptime(date,'%Y-%m-%d').date()
        hour_1=str(validate_hour(hour))
        hour_1=datetime.datetime.strptime(hour_1, '%H').time()
        combine_date_time=datetime.datetime.combine(date_1,hour_1)
        present = datetime.datetime.now()
               
        if combine_date_time<present:
               raise AppError(2,"DateError: " + str(combine_date_time) + ", outside range of weather prediction.")

        
        location=(request.form['location'])


        df.inputData('latlon',[12.9304,77.6784] ,location)
        
        data=df.filterP(location,date,hour)
       


        print("df success")

        params={
            'holiday':Checking_Null_values(data,'holiday'),
            'workingDay':Checking_Null_values(data,'workingday'),
            'temp':Checking_Null_values(data,'temp'),
            'atemp':Checking_Null_values(data,'app_temp'),
            'humidity':Checking_Null_values(data,'rh'),
            'windspeed':Checking_Null_values(data,'wind_spd'),
            'season':Checking_Null_values(data,'season_code'),
            'weather':Checking_Null_values(data,'weather_code'),
            'year':Checking_Null_values(data,'year'),
            'day':Checking_Null_values(data,'day'),
            'hour':hour,
            'dayofweek':Checking_Null_values(data,'dayofweek'),
            'month':Checking_Null_values(data,'month')
            }

        url='http://127.0.0.1:5000/predict'

        print("post start")
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
except AppError as ae:
    print (ae)
    #WriteToLog(Date, Time, ae.err_code, ae)
except ValueError as ve:
    pass
except Exception as e:
    pass