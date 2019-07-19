import requests
import numpy as np
import pandas as pd
import datetime as dt


class weatherForecast:
    def __init__(self, hours = 48):
        self.PARAMS = {
        #DOCUMENTATION USED: https://www.weatherbit.io/api/weather-forecast-120-hour  

        #Get forecast by lat/lon 	lat,lon
            'lat':12.92735,
            'lon':77.67185,

        #Get forecast by city name  	city, state(optional), country (optional)

        #Get forecast by postal code 	postal_code, country (optional)
        #     'postal_code': 560102,
        #     'country': 'IN',

        #Get forecast by Station 	station

        #Get forecast by city id 	city_id

            'lang':'en',
            'hours':hours 
        }
        self.weather_forecast = pd.DataFrame()
        self.data = []
        
        seasons = pd.read_csv('seasons.csv')
        seasons['StartDate']= pd.to_datetime(seasons['StartDate']).dt.date
        seasons['EndDate']= pd.to_datetime(seasons['EndDate']).dt.date
        self.seasons = np.array(seasons.to_records(index = False))

        weather_codes = pd.read_csv("weather_codes.csv")
        weather_codes.drop(labels='Description ',axis = 1, inplace = True)
        self.weather_codes = dict(zip(weather_codes['Code '], weather_codes.Weather))
        
        holidays = pd.read_csv('Holidays 2019.csv')
        self.holidays = pd.to_datetime(holidays['Date']).dt.date.values

        
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
        r = requests.get("https://weatherbit-v1-mashape.p.rapidapi.com/forecast/hourly",
                         headers={
                             "X-RapidAPI-Host": "weatherbit-v1-mashape.p.rapidapi.com",
                             "X-RapidAPI-Key": "9760fa76cemsh3b3bc0cfd34ff97p14b793jsnacc85f71e316"
                         },
                         params = self.PARAMS
        )

        self.data = r.json()

        from pandas.io.json import json_normalize
        self.weather_forecast =  json_normalize(self.data['data'])
        

    def modifyDf(self):
        self.weather_forecast['datetime'] = pd.to_datetime(self.weather_forecast['datetime'], format = "%Y-%m-%d:%H")
        self.weather_forecast['timestamp_local'] = pd.to_datetime(self.weather_forecast['timestamp_local'])
        self.weather_forecast['city'] = self.data['city_name']
        self.weather_forecast['lon'] = self.data['lon']
        self.weather_forecast['lat'] = self.data['lat']
        self.weather_forecast['place'] = 'Bellandur'

        self.weather_forecast['weather_code'] = self.weather_forecast['weather.code'].apply(lambda x : int(self.weather_codes[x]))

    
        self.weather_forecast['season'], self.weather_forecast['season_code'] = zip(*self.weather_forecast['timestamp_local'].apply(self.getSeasonc))
        self.weather_forecast['dayofweek'] = self.weather_forecast['timestamp_local'].dt.dayofweek
        self.weather_forecast['workingday'] = self.weather_forecast['dayofweek']//5

        self.weather_forecast['holiday'] = self.weather_forecast['timestamp_local'].dt.date.apply(self.checkHolc)
        
        self.weather_forecast['year'] = self.weather_forecast['timestamp_local'].dt.year
        self.weather_forecast['month'] = self.weather_forecast['timestamp_local'].dt.month
        self.weather_forecast['day'] = self.weather_forecast['timestamp_local'].dt.hour
        self.weather_forecast['hour'] = self.weather_forecast['timestamp_local'].dt.hour


    def displayReq(self):
        print(self.weather_forecast[['place','lat', 'lon', 'city','app_temp', 'timestamp_local', 'temp', 'rh', 'wind_spd', 'weather_code','season', 'season_code','dayofweek', 'workingday','holiday', 'year', 'month', 'day', 'hour']])

