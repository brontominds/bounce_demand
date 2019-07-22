import requests
import numpy as np
import pandas as pd
import datetime as dt

class weatherForecast:
    def __init__(self, hours = 48):
        self.ready = False
        self.PARAMS = {
            'lang':'en',
            'hours':hours 
        }
        
        self.temp = pd.DataFrame()
        self.weather_forecast = pd.DataFrame()
        
        self.data = []
        
        self.input_data = pd.DataFrame(columns = ['Type', 'Location', 'Status', 'City', 'Name'])
        
        seasons = pd.read_csv('seasons.csv')
        seasons['StartDate']= pd.to_datetime(seasons['StartDate']).dt.date
        seasons['EndDate']= pd.to_datetime(seasons['EndDate']).dt.date
        self.seasons = np.array(seasons.to_records(index = False))

        weather_codes = pd.read_csv("weather_codes.csv")
        weather_codes.drop(labels='Description ',axis = 1, inplace = True)
        self.weather_codes = dict(zip(weather_codes['Code '], weather_codes.Weather))
        
        holidays = pd.read_csv('Holidays 2019.csv')
        self.holidays = pd.to_datetime(holidays['Date']).dt.date.values
        
    def filterP(self, place, date, hr):
        if not place in list(self.input_data['Name']):
            print("Not in input data yet, please add first")
            print(list(self.input_data['Place']))
            return
        
        date = dt.datetime.strptime(date, '%Y-%m-%d').date()
        dattim = dt.datetime.combine(date, dt.time(hr, 30))
        
        ans = self.weather_forecast[(self.weather_forecast['place'] == place) & (self.weather_forecast['timestamp_local'] == dattim)]
        
        if(ans.shape[0] == 0):
            print("No results found")
            return -1
        if ans.shape[0] > 1:
            print("Too many results(?)")
            print(ans)
            return -2
        
        return ans
    
        
        
    def inputData(self, typeloc, loc, nameofPlace='NA',hours = 48):
        if not typeloc in ['latlon']:
            return 
        
        if(typeloc == 'latlon'):
            self.PARAMS = {
                'lat':loc[0],
                'lon':loc[1],
                
                'lang':'en',
                'hours':hours 
            }
            
            self.ready = True
            x = self.callAPI()
            self.ready = False

            if not x.status_code == 200:
                print("Invalid response",x.status_code)
                return
            self.data = x.json()

            from pandas.io.json import json_normalize
            self.temp =  json_normalize(self.data['data'])
            
            loc = [typeloc,loc,1, self.data['city_name'], nameofPlace]
            self.input_data = self.input_data.append(pd.DataFrame([loc], columns = ['Type', 'Location', 'Status', 'City', 'Name']))
            self.modifyDf(nameofPlace)
            self.addDf()
            
            
    def addDf(self):
        if self.weather_forecast.empty:
            self.weather_forecast = self.temp.copy()
        else:
            self.weather_forecast = self.weather_forecast.append(self.temp, ignore_index = True)
            
        self.temp = pd.DataFrame()
        
        
    def getSeasonc(self, dateGive):
        Y = 2000
        if isinstance(dateGive, dt.datetime):
            dateGive = dateGive.date()
        else:
            raise TypeError("wrong Type Given")
        dateGive = dateGive.replace(year=Y)
        return next((season,code) for start, end,season, fancy,code in self.seasons
                    if start <= dateGive <= end)


    def checkHolc(self, dateGive):
        if isinstance(dateGive, dt.datetime):
            dateGive = dateGive.date()

        if not isinstance(dateGive, dt.date):
            raise TypeError("wrong Type Given")

        if dateGive in self.holidays:
            return 1
        return 0

    
    def callAPI(self):
        if not self.ready:
            print("Not Reayd")
            return
        
        r = requests.get("https://weatherbit-v1-mashape.p.rapidapi.com/forecast/hourly",
                         headers={
                             "X-RapidAPI-Host": "weatherbit-v1-mashape.p.rapidapi.com",
                             "X-RapidAPI-Key": "9760fa76cemsh3b3bc0cfd34ff97p14b793jsnacc85f71e316"
                         },
                         params = self.PARAMS
        )
        return r
        

    def modifyDf(self, place):
        self.temp['datetime'] = pd.to_datetime(self.temp['datetime'], format = "%Y-%m-%d:%H")
        self.temp['timestamp_local'] = pd.to_datetime(self.temp['timestamp_local'])
        self.temp['city'] = self.data['city_name']
        self.temp['lon'] = self.data['lon']
        self.temp['lat'] = self.data['lat']
        self.temp['place'] = place

        self.temp['weather_code'] = self.temp['weather.code'].apply(lambda x : int(self.weather_codes[x]))

    
        self.temp['season'], self.temp['season_code'] = zip(*self.temp['timestamp_local'].apply(self.getSeasonc))
        self.temp['dayofweek'] = self.temp['timestamp_local'].dt.dayofweek
        self.temp['workingday'] = self.temp['dayofweek']//5

        self.temp['holiday'] = self.temp['timestamp_local'].dt.date.apply(self.checkHolc)
        
        self.temp['year'] = self.temp['timestamp_local'].dt.year
        self.temp['month'] = self.temp['timestamp_local'].dt.month
        self.temp['day'] = self.temp['timestamp_local'].dt.hour
        self.temp['hour'] = self.temp['timestamp_local'].dt.hour


    def displayReq(self):
        print(self.temp[['place','lat', 'lon', 'city','app_temp', 'timestamp_local', 'temp', 'rh', 'wind_spd', 'weather_code','season', 'season_code','dayofweek', 'workingday','holiday', 'year', 'month', 'day', 'hour']])

