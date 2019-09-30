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
#from datetime import datetime

def get_data():
    
    #Traffic data
    ToTraffic = pd.read_csv(os.getcwd() + '/cycped_vol.csv', low_memory = False);
    dateTimes = pd.to_datetime((ToTraffic['datetime_bin']), dayfirst = True);
    ToTraffic.insert(2,'DateTimes', dateTimes);
    
    ToLocations = pd.read_csv(os.getcwd() + '/miovision_intersections.csv', low_memory = False);
    Locations = ToLocations[['lat','lng']];
    
    # Weather data
    ToWeather = pd.read_csv(os.getcwd() + '/weather.csv', low_memory = False)
    weatherTimes = pd.to_datetime((ToWeather['date_time']), dayfirst = True);
    ToWeather['date_time'] = weatherTimes.dt.round('H');

    temp=['2019-01-01', '2019-02-14', '2019-02-18', '2019-03-17',
              '2019-04-19', '2019-04-22', '2019-05-12', '2019-05-20',
              '2019-06-16', '2019-07-01', '2019-08-05', '2019-09-02',
              '2019-10-14', '2019-10-31', '2019-12-25', '2019-12-26']
    
    HolidayCal = pd.DataFrame();
    HolidayCal['dates'] = pd.to_datetime(temp, dayfirst = True)
    
    Intersections = np.unique(ToTraffic['intersection_uid']);
    
    Peds=[]; Cycs=[];
    for IntID in Intersections:
        #print(IntID)
        
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
        dateTimes = Pedestrians.index        
        dateTimes = pd.to_datetime(Pedestrians['datetime_bin'], \
                                   dayfirst = True).dt.round('H');
        Pedestrians['datetime_bin'] = dateTimes;
        Pedestrians.insert(2, 'dateTimeIdx', groupB.index.get_level_values(0))
        temp = groupB.index.get_level_values(0)
        Pedestrians.insert(3, 'Hour', temp.hour)
        Pedestrians.insert(4, 'Day', temp.day)
        Pedestrians.insert(5, 'DayOfWeek', temp.dayofweek)
        Pedestrians.insert(6, 'DayOfYear', temp.dayofyear)
        Pedestrians.insert(7, 'Month', temp.month)
        
        dates = pd.DataFrame(temp.date, columns=['dates']);
        dates = dates['dates']
        Holidays = dates.isin(HolidayCal['dates'].dt.date)
        Holidays[Holidays== True]=1; Holidays[Holidays== False]=0;
        Pedestrians.insert(8, 'isHoliday', Holidays.values)
        
              
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
        temp = groupB.index.get_level_values(0)
        Cyclists.insert(3, 'Hour', temp.hour)
        Cyclists.insert(4, 'Day', temp.day)
        Cyclists.insert(5, 'DayOfWeek', temp.dayofweek)
        Cyclists.insert(6, 'DayOfYear', temp.dayofyear)
        Cyclists.insert(7, 'Month', temp.month)
        
        dates = pd.DataFrame(temp.date, columns=['dates']);
        dates = dates['dates']
        Holidays = dates.isin(HolidayCal['dates'].dt.date)
        Holidays[Holidays== True]=1; Holidays[Holidays== False]=0;
        Cyclists.insert(8, 'isHoliday', Holidays.values)
        
        #Combining traffic data with pedestrian traffic data
        Cyclists = Cyclists.merge(ToWeather, how = 'inner',\
        left_on = 'dateTimeIdx', right_on = 'date_time')
        grouped = Cyclists.groupby('date_time');
        Cyclists = grouped.first();
        
        Cycs.append(Cyclists)
        
    
    filename = 'PedestriansData.sav'
    with open(filename, 'wb') as handle:
        pickle.dump(Peds, handle)
    
    filename = 'CyclistsData.sav';
    with open(filename, 'wb') as handle:
        pickle.dump(Cycs, handle)
        
    filename = 'Locations.pickle';
    with open(filename, 'wb') as handle:
        pickle.dump(Locations, handle)
    
    return Peds, Cycs, Locations