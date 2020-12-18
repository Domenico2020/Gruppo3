# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 10:32:03 2020

@author: Domenico
"""

import pandas as pd

df = pd.read_csv (r'./data/yellow_tripdata_2020-03.csv')

#Date in numero per date un significato temporale DateTime to TimeStamp


#Ordino per Distanza percorsa cosi da clearare valori che comportano nulli
sorted_df = df.sort_values(by='trip_distance', ascending=False)
sorted_df = sorted_df[sorted_df.trip_distance < 1000]

sorted_df = sorted_df.sort_values(by='passenger_count')
sorted_df = sorted_df.sort_values(by='passenger_count', ascending=False)

sorted_df = sorted_df.sort_values(by='tpep_pickup_datetime')
sorted_df = sorted_df[sorted_df.tpep_pickup_datetime > "2020-03-01 00:00:00"]
sorted_df = sorted_df[sorted_df.tpep_pickup_datetime < "2020-04-01 00:00:00"]

