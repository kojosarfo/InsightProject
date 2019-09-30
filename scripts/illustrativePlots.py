#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 29 00:27:19 2019

@author: kojosarfo
"""

from __future__ import print_function
import pickle
#import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

filename = 'PedestriansData.sav'
Pedestrians = pickle.load(open(filename, 'rb'))

filename = 'CyclistsData.sav'
Cyclists = pickle.load(open(filename, 'rb'))


#Typical pedestrian traffic in a day
Peds = Pedestrians[0]
startTime = pd.to_datetime('2019-08-31 00:00:00');
endTime = pd.to_datetime('2019-08-31 23:00:00');

X = Peds[startTime: endTime]
X = X.dropna()
y = X['volume']
x = y.index
plt.plot(x.hour, y, 'r')
plt.grid('True'); plt.title('Pedestrian traffic at Adelaide - Bay intersection')
plt.xlabel('31 August 2019'); plt.ylabel('Pedestrian volume')
plt.show()


#Typical cyclist traffic in a day
Cycs = Cyclists[0]
startTime = pd.to_datetime('2019-08-31 00:00:00');
endTime = pd.to_datetime('2019-08-31 23:00:00');

X = Cycs[startTime: endTime]
X = X.dropna()
y = X['volume']
x = y.index
plt.plot(x.hour, y, 'r')
plt.grid('True'); plt.title('Cyclist traffic at King - Peter intersection')
plt.xlabel('31 August 2019'); plt.ylabel('Cyclist volume')
plt.show()

#Illustration of missing data: gap-filling

#Intersection number 13:
Cycs = Cyclists[13]
startTime = pd.to_datetime('2019-05-01 00:00:00');
endTime = pd.to_datetime('2019-05-31 23:00:00');
X = Cycs[startTime: endTime]
X = X.dropna()
y = X['volume']
x = y.index
plt.plot(x.day, y, 'ro')
plt.grid('True'); plt.title('Cyclist traffic at King - John intersection')
plt.xlabel('May 2019'); plt.ylabel('Cyclist volume')
plt.show()

Cycs = Cyclists[9]
startTime = pd.to_datetime('2019-05-01 00:00:00');
endTime = pd.to_datetime('2019-05-31 23:00:00');
X = Cycs[startTime: endTime]
X = X.dropna()
y = X['volume']
x = y.index
plt.plot(x.day, y, 'ro')
plt.grid('True'); plt.title('Cyclist traffic at Richmond - Spadina intersection')
plt.xlabel('May 2019'); plt.ylabel('Cyclist volume')
plt.show()
