from flask import Flask, render_template,url_for,request,jsonify
import pandas as pd
import numpy as np
import pickle
from sklearn.externals import joblib

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
        temp=request.form['temp']
        atemp=request.form['atemp']
	humidity=request.form['humidity']
	windspeed=request.form['windspeed']
	year=request.form['year']
	

            json_ = request.json
            query = pd.get_dummies(pd.DataFrame(json_))
            query = query.reindex(columns=model_columns, fill_value=0)

        
        predict_rest=[holiday,workingDay, transform_temp(ini,temp),transform_atemp(ini,atemp),transform_humidity(ini,humidity),transform_windspeed(ini,windspeed),2012,6,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0 ]
        predict_rest=np.array(predict_rest)
        predict_rest=predict_rest.reshape((1, -1))
        prediction=NN_model.predict(predict_rest)
        return jsonify({'prediction': list(prediction)})
        





