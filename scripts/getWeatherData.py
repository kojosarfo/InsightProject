#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 11:51:28 2019

@author: kojosarfo
"""

#This script scrapes weather data from World Weather Online (WWO) API.
#An account on WWO needs to be created to get the api_key.

from wwo_hist import retrieve_hist_data
import os

os.getcwd()

frequency = 1 #Frequency of one hour. This is the minimum frequency available.

start_date = '01-MAY-2019'

end_date = '31-AUG-2019'

api_key = 'a88c6df82fcc4b91908160057191609' #Replace this with your own API key

location_list = ['toronto']

hist_weather_data = retrieve_hist_data(api_key,
                                location_list,
                                start_date,
                                end_date,
                                frequency,
                                location_label = False,
                                export_csv = True,
                                store_df = True)
