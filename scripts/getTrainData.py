#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 12:23:02 2019

@author: kojosarfo
"""

from __future__ import print_function
import pickle
import warnings
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.close('all')
warnings.filterwarnings("ignore")

#Reading saved pedestrians and cyclist traffic data; these include weather data appended.

filename = 'PedestriansData.sav'
Pedestrians = pickle.load(open(filename, 'rb'))

filename = 'CyclistsData.sav'
Cyclists = pickle.load(open(filename, 'rb'))

# Training/validation set comprises a month's worth of data 
#randomly selected from 1 May to 31st May, and from 1 July to 31st July. 
#This is so that we can forecast and test on the month of August, 
#as well as gap-fill and test on the month of June
#Out of the month's data, 80% would be used for training, 
#and the model validated on the remaining fraction.
#Larger amounts of training data is computationally burdensome 
#for the Gaussian process regression (GPR) method that is used.

trainStart1 = pd.to_datetime('2019-05-01 00:00:00');
trainEnd1 = pd.to_datetime('2019-05-31 23:00:00');

trainStart2 = pd.to_datetime('2019-07-01 00:00:00');
trainEnd2 = pd.to_datetime('2019-07-31 23:00:00');

trainStarts =[trainStart1, trainStart2]
trainEnds =[trainEnd1, trainEnd2]

allPeds = pd.DataFrame(columns=Pedestrians[0].columns)
allCycs = pd.DataFrame(columns=Cyclists[0].columns)

#In the following lines, we loop through 10 intersections that are randomly selected, 
#and stack up their traffic data for the same date range -- to be used for 
#training/validation. The remaining intersections will be used for 
#testing how accurately Gaussian process regression is at estimating 
#intersections without monitoring stations.

randInts = random.sample(list(np.arange(0,14)),10) #Random intersections

for i in randInts:
    
    for j in range(2):
        trainStart = trainStarts[j]; trainEnd = trainEnds[j];
        
        Peds = Pedestrians[i]
        trainPeds = Peds[trainStart:trainEnd]
        allPeds = pd.concat([allPeds, trainPeds])
        
        Cycs = Cyclists[i]
        trainCycs = Cycs[trainStart:trainEnd]
        allCycs = pd.concat([allCycs, trainCycs])

allPeds = allPeds.dropna()        
allPeds = allPeds.sample(n = 7200, random_state = 0) 
#720 is approximately a month's worth of data at 1 hour intervals.
# times 10 intersections gives 7200

allCycs = allCycs.dropna()
allCycs = allCycs.sample(n = 7200, random_state = 0) 
 
filename = 'stackedPeds.sav'
with open(filename, 'wb') as handle:
    pickle.dump(allPeds, handle)
    
filename = 'stackedCycs.sav'
with open(filename, 'wb') as handle:
    pickle.dump(allCycs, handle)
    

#Plotting a snapshot of the training/validation instances for a random intersection
xIndex = np.arange(0,7200)

plt.figure(1)
plt.plot(xIndex, allPeds['volume'].values, 'ro')
plt.ylabel('Pedestrian volume')
plt.xlabel('Random time instances')
plt.title(allPeds['IntName'][i]+ ' intersection')
plt.grid('True')
plt.show()

plt.figure(2)
plt.plot(xIndex, allCycs['volume'].values, 'bo')
plt.ylabel('Cyclist volume')
plt.xlabel('Random time instances')
plt.title(allCycs['IntName'][i]+ ' intersection')
plt.grid('True')
plt.show()

#Saving the intersections not used for training
allInts = list(np.arange(0,14)) #all intersections
testInts = list(set(allInts) - set(randInts)) #test intersections

filename = 'testInts.sav'
with open(filename, 'wb') as handle:
    pickle.dump(testInts, handle)
    