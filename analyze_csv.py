#!/usr/bin/env python
# coding: utf-8

import os
import numpy as np

station = 'W2NAF'

base_directory = './'
data_dir = os.path.join(base_directory,'output','csv',station)

filename = 'ACF_FWL_data__15.0MHz_2024-05-10.csv'
filepath = os.path.join(data_dir, filename)
print(filepath)
print(os.path.exists(filepath))

data = np.genfromtxt(
    filepath,
    delimiter=',',
    skip_header=3,
    invalid_raise=False
)

hour    = data[:,0]
doppler = data[:,1]
spread  = data[:,2]
level   = data[:,3]

doppler_min = np.min(doppler)
doppler_max = np.max(doppler)

index_min = np.argmin(doppler)
index_max = np.argmax(doppler)

t_min = hour[index_min]
t_max = hour[index_max]


print(f'Minimum doppler: {doppler_min} at {t_min}')
print(f'Maximum doppler: {doppler_max} at {t_max}')

