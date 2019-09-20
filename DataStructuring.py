#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 12:36:29 2019

@author: kojosarfo
"""

import numpy as np
import pandas as pd
import os
import pickle

def get_data():
    
    #Traffic data
    ToTraffic = pd.read_csv(os.getcwd() + '/cycped_vol.csv', low_memory = False);
    dateTimes = pd.to_datetime((ToTraffic['datetime_bin']), dayfirst = True);
    ToTraffic.insert(2,'DateTimes', dateTimes);
    
    # Weather data
    ToWeather = pd.read_csv(os.getcwd() + '/weather.csv', low_memory = False)
    weatherTimes = pd.to_datetime((ToWeather['date_time']), dayfirst = True);
    ToWeather['date_time'] = weatherTimes.dt.round('H');
    
    Intersections = np.unique(ToTraffic['intersection_uid']);
    
    Peds=[]; Cycs=[];
    for IntID in Intersections:
        print(IntID)
        
        CycsPeds = ToTraffic[ToTraffic['intersection_uid'] == IntID];
        
        # For pedestrians
        Pedestrians = CycsPeds[CycsPeds['classification_uid'] == 6] 
        #6 represents pedestrians
        
        #Aggregating traffic volume in all directions of travel 
        #and all legs for a given timestamp
        grouped = Pedestrians.groupby('DateTimes');
        groupA = grouped.sum();
        groupA = groupA['volume']; 
        groupB = grouped.first(); 
        groupB = groupB.iloc[:, 0:groupB.shape[1]-1];
        Pedestrians = pd.concat([groupB, groupA], axis=1, sort=False)
        
        #Aggregating volumes for 1 hour intervals; 
        #the weather data to be appended has a frequency of 1 hour.
        resampled = Pedestrians.resample('60Min');
        groupA = resampled.sum();
        groupA = groupA['volume'];
        groupB = resampled.first();
        groupB = groupB.iloc[:, 0:groupB.shape[1]-1]
        Pedestrians = pd.concat([groupB, groupA], axis=1, sort=False);
        
        #Extracting time information
        dateTimes = pd.to_datetime(Pedestrians['datetime_bin'], \
                                   dayfirst = True).dt.round('H');
        Pedestrians['datetime_bin'] = dateTimes;
        Pedestrians.insert(2, 'dateTimeIdx', groupB.index.get_level_values(0))
        Pedestrians.insert(3, 'Hour', dateTimes.dt.hour)
        Pedestrians.insert(4, 'Day', dateTimes.dt.day)
        Pedestrians.insert(5, 'DayOfWeek', dateTimes.dt.dayofweek)
        Pedestrians.insert(6, 'DayOfYear', dateTimes.dt.dayofyear)
        Pedestrians.insert(7, 'Month', dateTimes.dt.month)
        
        #Combining traffic data with pedestrian traffic data
        Pedestrians = Pedestrians.merge(ToWeather, how = 'inner',\
        left_on = 'dateTimeIdx', right_on = 'date_time')
        grouped = Pedestrians.groupby('date_time');
        Pedestrians = grouped.first();
        
        Peds.append(Pedestrians)
        
        
        # For Cyclists
        Cyclists = CycsPeds[CycsPeds['classification_uid'] == 2] 
        #2 represents cyclists
        
        #Aggregating traffic volume in all directions of travel 
        #and all legs for a given timestamp
        grouped = Cyclists.groupby('DateTimes');
        groupA = grouped.sum();
        groupA = groupA['volume']; 
        groupB = grouped.first(); 
        groupB = groupB.iloc[:, 0:groupB.shape[1]-1];
        Cyclists = pd.concat([groupB, groupA], axis=1, sort=False)
        
        #Aggregating volumes for 1 hour intervals; 
        #the weather data to be appended has a frequency of 1 hour.
        resampled = Cyclists.resample('60Min');
        groupA = resampled.sum();
        groupA = groupA['volume'];
        groupB = resampled.first();
        groupB = groupB.iloc[:, 0:groupB.shape[1]-1]
        Cyclists = pd.concat([groupB, groupA], axis=1, sort=False);
        
        #Extracting time information
        dateTimes = pd.to_datetime(Cyclists['datetime_bin'], \
                                   dayfirst = True).dt.round('H');
        Cyclists['datetime_bin'] = dateTimes;
        Cyclists.insert(2, 'dateTimeIdx', groupB.index.get_level_values(0))
        Cyclists.insert(3, 'Hour', dateTimes.dt.hour)
        Cyclists.insert(4, 'Day', dateTimes.dt.day)
        Cyclists.insert(5, 'DayOfWeek', dateTimes.dt.dayofweek)
        Cyclists.insert(6, 'DayOfYear', dateTimes.dt.dayofyear)
        Cyclists.insert(7, 'Month', dateTimes.dt.month)
        
        #Combining traffic data with pedestrian traffic data
        Cyclists = Pedestrians.merge(ToWeather, how = 'inner',\
        left_on = 'dateTimeIdx', right_on = 'date_time')
        grouped = Cyclists.groupby('date_time');
        Cyclists = grouped.first();
        
        Cycs.append(Pedestrians)
    
    filename = 'PedestriansData.sav'
    pickle.dump(Peds, open(filename, 'wb'))
    
    filename = 'CyclistsData.sav';
    pickle.dump(Cycs, open(filename, 'wb'))
    
    return Peds, Cycs





