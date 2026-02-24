# Script to create an average quiet day Doppler shift plot

import numpy as np

file_name = 'May_2024_quiet_days.csv'
data = np.genfromtxt(file_name, delimiter=',', skip_header=2)

timestamp = data[0,:]
avg_dop   = data[8,:]

print(len(timestamp))
