#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 29 21:40:20 2019

@author: kojosarfo
"""

from __future__ import print_function
import warnings
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.close('all')
warnings.filterwarnings("ignore")

#%% Validation in terms of time: gap-filling

filename = 'gprPedsMdl.pickle'
gprPedsMdl = pickle.load(open(filename, 'rb'))

filename = 'gprCycsMdl.pickle'
gprCycsMdl = pickle.load(open(filename, 'rb'))

filename = 'PedestriansData.sav'
Pedestrians = pickle.load(open(filename, 'rb'))

filename = 'CyclistsData.sav'
Cyclists = pickle.load(open(filename, 'rb'))

filename = 'testInts.sav'
testInts = pickle.load(open(filename, 'rb')) # Hold-out intersection IDs

#Extracting the intersections used for training
allInts = list(np.arange(0,14)) #all intersections
trainInts = list(set(allInts) - set(testInts)) #trained intersections


RoadUser = ['Pedestrians', 'Cyclists']

trafficData = [Pedestrians, Cyclists]

gprMdls = [gprPedsMdl, gprCycsMdl] #Gaussian process regression models

for j in range(2):
    
    gprMdl = gprMdls[j] #Selecting Gaussian process regression model 
    #for pedestrian or cyclists
    
    testData = trafficData[j]    
    
    for k in trainInts:
        
        testTraffic = testData[k];
        
        IntersectionName = testTraffic['IntName'][0]
        
        #Evaluating the hold-out set on the month of June for which 
        #the intersections were not trained for gap-filling
        
        testStart = pd.to_datetime('2019-06-01 00:00:00');
        testEnd = pd.to_datetime('2019-06-30 23:00:00');
        
        testTraffic = testTraffic[testStart: testEnd]
            
        testTraffic = testTraffic.dropna()
        
        X_test = testTraffic[['Hour','DayOfWeek','isHoliday','lat','lng']];
        
        y_test = testTraffic['volume']
        
        yPred, yStd = gprMdl.predict(X_test, return_std = True)
        yPred = yPred.astype('int'); yPred[yPred<0]=0
        
        yPred = pd.DataFrame(yPred, columns =['forecast']); 
        yPred.index = y_test.index; yPred = yPred['forecast'];
        
        print('RMSE: '+str(np.sqrt(np.mean((yPred.values - y_test.values)**2))))
        print('R_Squared: '+str(gprMdl.score(X_test, y_test)))
        
        
        yLow = yPred - 3*yStd; yLow = yLow.astype('int'); yLow[yLow<0]=0
        yHigh = yPred + 3*yStd; yHigh = yHigh.astype('int');

        #Plotting for the month of June               
        plt.figure(j+k+1)
        ax = y_test.plot(label = 'Observed')
        yPred.plot(ax = ax, label = 'Predicted')
        ax.fill_between(y_test.index,
                            yLow,
                            yHigh, color='k', alpha=.2)
        ax.set_xlabel('Time')
        ax.set_ylabel(RoadUser[j]+ ' volume')
        ax.set_title(IntersectionName+ ' Intersection')
        plt.legend()
        plt.show()
