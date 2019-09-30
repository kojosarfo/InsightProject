#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 12:23:02 2019

@author: kojosarfo
"""

from __future__ import print_function
import pickle
import numpy as np
import pandas as pd
    
filename = 'PedestriansData.sav'
Pedestrians = pickle.load(open(filename, 'rb'))

filename = 'CyclistsData.sav'
Cyclists = pickle.load(open(filename, 'rb'))

filename = 'Locations.sav'
Locations = pickle.load(open(filename, 'rb'))

# Training/validation data ranges from 1 July to 31st July

trainStart = pd.to_datetime('2019-07-01 00:00:00');
trainEnd = pd.to_datetime('2019-07-31 23:00:00');

allPeds = pd.DataFrame(columns=Pedestrians[0].columns)
allCycs = pd.DataFrame(columns=Cyclists[0].columns)
  
for i in range(10): #Training on first 10 intersections
    Peds = Pedestrians[i]
    T = Peds[trainStart:trainEnd]
    T['lat'] = np.ones([len(T),1])*Locations.iloc[i,0]
    T['lng'] = np.ones([len(T),1])*Locations.iloc[i,1]
    
    allPeds = pd.concat([allPeds, T])
    
    Cycs = Cyclists[i]
    T = Cycs[trainStart:trainEnd]
    T['lat'] = np.ones([len(T),1])*Locations.iloc[i,0]
    T['lng'] = np.ones([len(T),1])*Locations.iloc[i,1]
    
    allCycs = pd.concat([allCycs, T])

filename = 'stackedPeds.pickle'
with open(filename, 'wb') as handle:
    pickle.dump(allPeds, handle)
    
filename = 'stackedCycs.pickle'
with open(filename, 'wb') as handle:
    pickle.dump(allCycs, handle)