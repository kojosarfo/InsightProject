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
    
    #Cyclist and pedestrian traffic data for 14 intersections at Downtown Toronto, 
    #collected at 1 to 2-minute intervals at Downtown Toronto, from May to August
    ToTraffic = pd.read_csv(os.getcwd() + '/cycped_vol.csv', low_memory = False);
    dateTimes = pd.to_datetime((ToTraffic['datetime_bin']), dayfirst = True);
    ToTraffic.insert(2,'DateTimes', dateTimes);
    
    # The csv file contains the intersection names and their geoographical co-ordinates
    ToLocations = pd.read_csv(os.getcwd() + '/miovision_intersections.csv', low_memory = False);
    
    # The spatial co-ordinates are extracted to be used as predictors of the traffic 
    #at different intersections
    Locations = ToLocations[['lat','lng']];
    
    # Weather data for the period from May to August, collected at hourly intervals
    ToWeather = pd.read_csv(os.getcwd() + '/weather.csv', low_memory = False)
    weatherTimes = pd.to_datetime((ToWeather['date_time']), dayfirst = True);
    ToWeather['date_time'] = weatherTimes.dt.round('H');

    # Major holidays in Ontario
    holidayDates=['2019-01-01', '2019-02-14', '2019-02-18', '2019-03-17',
              '2019-04-19', '2019-04-22', '2019-05-12', '2019-05-20',
              '2019-06-16', '2019-07-01', '2019-08-05', '2019-09-02',
              '2019-10-14', '2019-10-31', '2019-12-25', '2019-12-26']
    
    HolidayCal = pd.DataFrame();
    HolidayCal['dates'] = pd.to_datetime(holidayDates, dayfirst = True)
    
    #In the remaining lines, the traffic data for every intersection are collated 
    #in terms of pedestrians and cyclists
    
    Intersections = np.unique(ToTraffic['intersection_uid']);
    
    RoadUserIDs = [6, 2]; #6 represents pedestrians; 2 represents cyclists
    
    Peds=[]; Cycs=[]; RoadUserList = [Peds, Cycs]
    intCnt = 0;
    for IntID in Intersections:
        #print(IntID)
        
        CycsPeds = ToTraffic[ToTraffic['intersection_uid'] == IntID];
        userCnt = 0;
        for RoadUserID in RoadUserIDs:
        
            RoadUser = CycsPeds[CycsPeds['classification_uid'] == RoadUserID]
            
            #Aggregating traffic volume in all directions of travel
            #and all legs for a given timestamp
            grouped = RoadUser.groupby('DateTimes');
            groupA = grouped.sum();
            groupA = groupA['volume'];
            groupB = grouped.first();
            groupB = groupB.iloc[:, 0:groupB.shape[1]-1];
            RoadUser = pd.concat([groupB, groupA], axis=1, sort=False)
            
            #Aggregating traffic volumes in 1 hour intervals in order to reduce noise,
            #and also because the weather data to be appended has a frequency of 1 hour.
            resampled = RoadUser.resample('60Min');
            groupA = resampled.sum();
            groupA = groupA['volume'];
            groupB = resampled.first();
            groupB = groupB.iloc[:, 0:groupB.shape[1]-1]
            RoadUser = pd.concat([groupB, groupA], axis=1, sort=False);
            
            
            #Extracting time information: day of week, hour, holiday, etc. 
            #These information are not explicit in the timestamps, but might possibly
            #influence pedestrian/cyclist traffic volumes
            dateTimes = RoadUser.index
            dateTimes = pd.to_datetime(RoadUser['datetime_bin'], \
                                       dayfirst = True).dt.round('H');
            RoadUser['datetime_bin'] = dateTimes;
            RoadUser.insert(2, 'dateTimeIdx', groupB.index.get_level_values(0))
            temp = groupB.index.get_level_values(0)
            RoadUser.insert(3, 'Hour', temp.hour)
            RoadUser.insert(4, 'Day', temp.day)
            RoadUser.insert(5, 'DayOfWeek', temp.dayofweek)
            RoadUser.insert(6, 'DayOfYear', temp.dayofyear)
            RoadUser.insert(7, 'Month', temp.month)
            
            dates = pd.DataFrame(temp.date, columns=['dates']);
            dates = dates['dates']
            Holidays = dates.isin(HolidayCal['dates'].dt.date)
            Holidays[Holidays== True]=1; Holidays[Holidays== False]=0;
            RoadUser.insert(8, 'isHoliday', Holidays.values)
            
                  
            #Combining traffic data with pedestrian traffic data
            RoadUser = RoadUser.merge(ToWeather, how = 'inner',\
            left_on = 'dateTimeIdx', right_on = 'date_time')
            grouped = RoadUser.groupby('date_time');
            RoadUser = grouped.first();
            
            #Appending the geographical co-ordinates to the traffic/weather data
            RoadUser['lat'] = np.ones([len(RoadUser),1])*Locations.iloc[intCnt,0]
            RoadUser['lng'] = np.ones([len(RoadUser),1])*Locations.iloc[intCnt,1]
            
            #Appedning intersection names
            RoadUser['IntName'] = [ToLocations['intersection_name']\
                     [intCnt] for i in range(len(RoadUser))]
            
            RoadUserList[userCnt].append(RoadUser)
            userCnt = userCnt + 1
        intCnt = intCnt + 1    
    Peds = RoadUserList[0]; Cycs = RoadUserList[1];
    
    #Saving the resulting list of dataframes with Pickle
    
    filename = 'PedestriansData.sav'
    with open(filename, 'wb') as handle:
        pickle.dump(Peds, handle)
    
    filename = 'CyclistsData.sav';
    with open(filename, 'wb') as handle:
        pickle.dump(Cycs, handle)
        
    filename = 'Locations.sav';
    with open(filename, 'wb') as handle:
        pickle.dump(Locations, handle)
    
    return Peds, Cycs, Locations
