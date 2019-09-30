#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 29 12:40:38 2019

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

#%% Validation in terms of hold-out intersections

IntersectionNames = ['Richmond-Bay', 'Wellington-Blue_jays',
                     'Wellington-Bay', 'King-John'];
RoadUser = ['Pedestrians', 'Cyclists']

trafficData = [Pedestrians, Cyclists]

filename = 'gprPedsMdl.pickle'
gprPedsMdl = pickle.load(open(filename, 'rb'))

filename = 'gprCycsMdl.pickle'
gprCycsMdl = pickle.load(open(filename, 'rb'))

gprMdls = [gprPedsMdl, gprCycsMdl]

testStart = pd.to_datetime('2019-07-01 00:00:00');
testEnd = pd.to_datetime('2019-07-31 23:00:00');

for j in range(2):
    
    gprMdl = gprMdls[j]
    
    testData = trafficData[j]
    for k in range(4): #Intersection IDs: 10,11,12,13
        
        testIntersection = testData[k+10];
        
        testIntersection = testIntersection[testStart: testEnd]
            
        testIntersection = testIntersection.dropna()
        
        X = testIntersection[['Hour','DayOfWeek','isHoliday']];
        
        X['lat'] = np.ones([len(X),1])*Locations.iloc[k,0]
        X['lng'] = np.ones([len(X),1])*Locations.iloc[k,1]
        
        X_test = X
        
        X_test_scaled = scalerObj.transform(X_test)
        
        y_test = testIntersection['volume']
        
        yPred, yStd = gprMdl.predict(X_test_scaled, return_std=True)
        yPred = yPred.astype('int'); yPred[yPred<0]=0
        
        yPred = pd.DataFrame(yPred, columns =['forecast']); 
        yPred.index = y_test.index; yPred = yPred['forecast'];
        
        yLow = yPred - 3*yStd; yLow = yLow.astype('int'); yLow[yLow<0]=0
        yHigh = yPred + 3*yStd; yHigh = yHigh.astype('int');
        
        xIndex = np.arange(0,len(y_test))
               
        plt.figure(11+j+k)
        ax = y_test.plot(label = 'Observed')
        yPred.plot(ax = ax, label = 'Predicted')
        ax.fill_between(y_test.index,
                            yLow,
                            yHigh, color='k', alpha=.2)
        ax.set_xlabel('Time')
        ax.set_ylabel(RoadUser[j]+ ' volume')
        ax.set_title(IntersectionNames[k]+ ' Intersection')
        plt.legend()
        plt.show()
        
        print('RMSE: '+str(np.sqrt(np.mean((yPred.values - y_test.values)**2))))
        print('R_Squared: '+str(gprMdl.score(X_test, y_test)))
