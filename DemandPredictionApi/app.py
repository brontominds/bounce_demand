from flask import Flask, render_template,url_for,request,jsonify
import pandas as pd
import numpy as np
import pickle
from sklearn.externals import joblib
season=2
weather=3


def createDF():
    return (pd.read_csv('data_mean_std.csv', header=0))

def transform_temp(ini, temp):
    return ((temp-ini['mean_temp'][0])/ini['sd_temp'][0])

def transform_atemp(ini, atemp):
    return ((atemp-ini['mean_atemp'][0])/ini['sd_atemp'][0])

def transform_humidity(ini, humidity):
    return ((humidity-ini['mean_humidity'][0])/ini['sd_humidity'][0])

def transform_windspeed(ini, windspeed):
    return ((windspeed-ini['mean_windspeed'][0])/ini['sd_windspeed'][0])

def Season_1(s):
    if s==1:
        return (1)
    else:
        return (0)

def Season_2(s)
    if s==2:
        return (1)
    else:
        return (0)
    
def Weather_1(w)
    if w==1:
        return (1)
    else:
        return (0)

app = Flask(__name__)
#Machine Learning code goes here
if __name__ == '__main__':
    app.run(debug=True)
    #app.run(host='0.0.0.1', port=5005)
        


# In[ ]:


@app.route('/')
def home():
     return render_template('home.html')

@app.route('/predict' , methods = ['POST'])
def predict():
    ini = createDF()
    NN_model=joblib.load('NN_model.pkl')
    if request.method == 'POST':
        holiday=request.form['holiday']
        workingDay=request.form['workingDay']
        
        #In the code below, look for 1 and 0 related with seeason.
        #Replace them with corresponding calls to season function, like Season_1(season), Season_2(season) etc
        #Repeat for every on hot encoded variable
        predict_rest=[0,1, transform_temp(ini,22),transform_atemp(ini,22),transform_humidity(ini,71),transform_windspeed(ini,24),2012,6,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0 ]
        predict_rest=np.array(predict_rest)
        predict_rest=predict_rest.reshape((1, -1))
        prediction=NN_model.predict(predict_rest)
        a="Prediction:" + str(prediction)
        return a





