#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 12:21:31 2019

@author: kojosarfo
"""

from __future__ import print_function
from sklearn.model_selection import train_test_split
from sklearn.gaussian_process import GaussianProcessRegressor as gpr
from sklearn.gaussian_process.kernels import RBF
import warnings
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.close('all')
warnings.filterwarnings("ignore")

#%%
filename = 'stackedPeds.sav'
trainPeds = pickle.load(open(filename, 'rb'))

filename = 'stackedCycs.sav'
trainCycs = pickle.load(open(filename, 'rb'))

#%%
filenames = ['gprPedsMdl.pickle', 'gprCycsMdl.pickle']
yLabels = ['Pedestrian volume','Cyclist volume']

#%% Training on both pedestrians and cyclists
trainData = [trainPeds, trainCycs]
for i in range(2):
    
    print(i)
    
    trafficData = trainData[i]
    
    trafficData = trafficData.dropna()
    
    #X = trafficData[['Hour','DayOfWeek','isHoliday','lat','lng']]; 
    #Feature selection showed these features to be most predictive of 
    #the traffic volumes. Perhaps no weather parameter significantly 
    #influences pedestrian/cyclist traffic because the weather doesn't 
    #vary much between May and August.
    
    X = trafficData[['Hour','DayOfWeek','isHoliday','lat','lng',]];
    
    Y = trafficData['volume']
    
    #Random split into training and validation sets
    X_train, X_test, y_train, y_test = \
    train_test_split(X, Y, test_size=0.2, random_state=0)
    
    #Training with Gaussian process regression. The kernel used is a 
    #radial basis function (squared exponential) kernel whose 
    #length_scale is initialised to a vector of all ones: [1,1,1,1,1], 
    #the size of which is equal to the number of features (5);
    
    kernel = RBF(length_scale=np.ones([5,]))
    gprMdl = gpr(kernel=kernel, random_state=0, normalize_y=True, 
                 n_restarts_optimizer = 0).fit(X_train, y_train)
    
    filename = filenames[i]
    with open(filename, 'wb') as handle:
        pickle.dump(gprMdl, handle, protocol=pickle.HIGHEST_PROTOCOL)
               
    # Validation
    yPred, yStd = gprMdl.predict(X_test, return_std=True) 
    #Gaussian process regression returns the standard devition 
    #of the prediction
    yPred = yPred.astype('int'); yPred[yPred<0]=0 
    #Since we are forecasting pedestrian traffic, we round of all 
    #floats and trim negative values to zero.
    
    yPred = pd.DataFrame(yPred, columns = ['forecast']); 
    yPred.index = y_test.index; yPred = yPred['forecast'];
    
    # +/- 3 times the standard deviation is used, representing a 99.7% 
    #confidence bound
    yLow = yPred - 3*yStd; yLow = yLow.astype('int'); yLow[yLow<0]=0
    yHigh = yPred + 3*yStd; yHigh = yHigh.astype('int');
    
    xIndex = np.arange(0,len(y_test))
    
    plt.figure(i+1)
    plt.plot(xIndex, y_test.values, 'ro', label = 'Observed')
    plt.plot(xIndex, yPred.values, 'bo', label ='Predicted')
    plt.ylabel(yLabels[i])
    plt.xlabel('Random time instances')
    plt.show()
    
    print('RMSE: '+str(np.sqrt(np.mean((yPred.values - y_test.values)**2))))
    print('R_Squared: '+str(gprMdl.score(X_test, y_test)))
