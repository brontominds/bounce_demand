"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
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

@app.route('/predict')
def predict():
    """Renders the contact page."""
    params={
        'date':'24-july-2019',
        'location':'Bellandur',
        'season':'3',
        }
   # url='http://localhost:5050/predict'
    #r = requests.post(url, params=params)


    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Predicted Demand',
        demand='136'
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
