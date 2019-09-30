#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 21:21:14 2019

@author: kojosarfo
"""

##This script implements pedestrian traffic forecast 
#using Facebook's Prophet.

#Inputs: date, hour, intersection ID, frecast horizon

#Requirements: 'PedestriansData.sav' or ('cycped_vol.csv' and 'weather.csv')
#In the case that the csv files are available, 
#uncomment Line 44: Pedestrians, Cyclists = get_data()

import warnings
import pickle
from fbprophet import Prophet
#import numpy as np
import matplotlib.pyplot as plt
warnings.filterwarnings("ignore")
plt.style.use('fivethirtyeight')
import pandas as pd
#import statsmodels.api as sm
import matplotlib
from DataStructuring import get_data

matplotlib.rcParams['axes.labelsize'] = 14
matplotlib.rcParams['xtick.labelsize'] = 12
matplotlib.rcParams['ytick.labelsize'] = 12
matplotlib.rcParams['text.color'] = 'k'
plt.close('all')
pd.plotting.register_matplotlib_converters()

filename = 'PedestriansData.sav'
Pedestrians = pickle.load(open(filename, 'rb'))

filename = 'PedestriansData.sav'
Cyclists = pickle.load(open(filename, 'rb'))


#Pedestrians, Cyclists = get_data()

#Splitting the data into days

IntID = int(input('For what intersection do you want to obtain forecasts?\n'))
#Example: 0; Set={0:13}

FirstDate = input('From what date do you want forecasts? Use the form: YYYY-MM-DD\n')
#Example: 2019-06-26

FirstTime = input('From what hour do you want to begin your forecast? Use the form: HH\n')
#Example: 00

Horizon = int(input('How long is your forecast horizon in hours?\n'))
#Example: 24*7, i.e., one week

startDate = FirstDate +' '+ FirstTime + ':00:00';
testStart = pd.to_datetime(startDate);
testEnd = testStart + pd.Timedelta(hours=Horizon-1);

TrainSize = 24*7*4;
trainStart = testStart - pd.Timedelta(hours = TrainSize)
trainEnd = testStart - pd.Timedelta(hours = 1)

Peds = Pedestrians[IntID];
trainVolume = Peds[trainStart: trainEnd]['volume']

testVolume = Peds[testStart: testEnd]['volume'];
weatherForecast = Peds[trainStart: testEnd][['tempC','humidity']];

pInput = Peds[trainStart: trainEnd][['dateTimeIdx','volume',
             'tempC','humidity']]
pInput = pInput.rename(columns={"dateTimeIdx": "ds", "volume": "y"})

#Using Prophet
m = Prophet(yearly_seasonality=False, weekly_seasonality=True, daily_seasonality=True);
m.add_regressor('tempC')
m.add_regressor('humidity')
m.fit(pInput)
future = m.make_future_dataframe(periods = Horizon, freq = 'h');
future['tempC'] = weatherForecast['tempC'].values
future['humidity'] = weatherForecast['humidity'].values
forecast = m.predict(future)
#m.plot(forecast)

forecast_mean = forecast['yhat'][-Horizon:];
forecast_mean = round(forecast_mean); forecast_mean[forecast_mean<0] = 0;
forecastVolume = pd.DataFrame(forecast_mean);
#forecastVolume.rename(columns={'yhat': 'Predicted'})
forecastVolume.index = testVolume.index
forecastVolume=forecastVolume['yhat']

forecast_ci= forecast[['yhat_lower','yhat_upper']][-Horizon:];
forecast_ci = round(forecast_ci); forecast_ci[forecast_ci<0] = 0;
pred_ci= pd.DataFrame(forecast_ci);
pred_ci.index=testVolume.index

## Loading ARIMA model from disk
#filename = 'finalized_model.sav'
#results = pickle.load(open(filename, 'rb'))
#
#pred = results.get_prediction(start = testStart, end = testEnd)
#pred_ci = pred.conf_int();
#forecastVolume = pred.predicted_mean;
#forecastVolume = round(forecastVolume); forecastVolume[forecastVolume<0] = 0;

ax = trainVolume[386:].plot(label='Historical')
testVolume.plot(ax=ax, label='Observed')
forecastVolume.plot(ax=ax, label='Forecast')
ax.fill_between(pred_ci.index,
                pred_ci['yhat_lower'],
                pred_ci['yhat_upper'], color='k', alpha=.2)
ax.set_xlabel('Date')
ax.set_ylabel('Pedestrian volume')
plt.legend()
plt.show()
