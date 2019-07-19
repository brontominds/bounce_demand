from flask import Flask, render_template,url_for,request,jsonify, Response
import pandas as pd
import numpy as np
import pickle
from sklearn.externals import joblib


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
    
    NN_model=joblib.load('BounceDemandPrediction_without_weather.pkl')
    if request.method == 'POST':
        holiday=request.form['holiday']
        workingday=request.form['workingDay']
        year=request.form['year']
        day=request.form['day']
        season=request.form['season']
        hour=request.form['hour']
        dayofweek=request.form['dayofweek']
        month=request.form['month']
        data=(np.zeros((59,), dtype=int))
    
    df=pd.DataFrame([data],columns=['holiday', 'workingday', 
           'year', 'day', 'season_1', 'season_2', 'season_3', 'season_4',
            'hour_0', 'hour_1',
           'hour_2', 'hour_3', 'hour_4', 'hour_5', 'hour_6', 'hour_7', 'hour_8',
           'hour_9', 'hour_10', 'hour_11', 'hour_12', 'hour_13', 'hour_14',
           'hour_15', 'hour_16', 'hour_17', 'hour_18', 'hour_19', 'hour_20',
           'hour_21', 'hour_22', 'hour_23', 'dayofweek_0', 'dayofweek_1',
           'dayofweek_2', 'dayofweek_3', 'dayofweek_4', 'dayofweek_5',
           'dayofweek_6', 'month_1', 'month_2', 'month_3', 'month_4', 'month_5',
           'month_6', 'month_7', 'month_8', 'month_9', 'month_10', 'month_11',
           'month_12'])
  
  

    df['holiday'][0] = int(holiday)
    df['workingday'][0] = int(workingday)
    
    df["hour_" + str(hour)][0]=1
    df["dayofweek_" + str(dayofweek)][0]=1
    df["month_" + str(month)][0]=1

  
    predict_rest=np.array(df.values.tolist())
    predict_rest=predict_rest.reshape((1, -1))
    prediction=NN_model.predict(predict_rest)
    a=str(prediction[0][0])
    #print(jsonify(prediction=a))
    return jsonify(prediction=a)
        





