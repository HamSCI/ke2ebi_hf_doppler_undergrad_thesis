#!/usr/bin/env python
# coding: utf-8

import os
import numpy as np
import matplotlib.pyplot as plt
import re
import datetime
import math

station = 'W2NAF'

base_directory = './'
data_dir       = os.path.join(base_directory,'output','csv',station)
output_dir     = os.path.join(base_directory,'output')

filename = 'ACF_FWL_data__15.0MHz_2024-05-10.csv'
filepath = os.path.join(data_dir, filename)

# Pull frequency and date from filename
match = re.search(r'(\d+\.?\d*)MHz_(\d{4}-\d{2}-\d{2})', filename)
if match:
    frequency = f"{match.group(1)} MHz"
    date      = match.group(2)
else: 
    frequency = "Unknown frequency"
    date      = "Unknown date"

if not os.path.exists(filepath):
    raise FileNotFoundError(filepath)
else: 
    print(filepath)

# Set output directory to save plots in and name output .png
plot_dir = os.path.join(output_dir,'plots',station)
os.makedirs(plot_dir,exist_ok=True)
outfile  = os.path.join(
    plot_dir,
    f"{station}_Doppler_vs_time_{frequency.replace(' ','')}_{date}.png"
)

# Read .csv
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

plt.scatter(hour,doppler, s=3.5,c='black')
plt.title(f'Doppler Shift vs. Time\nFrequency: {frequency} | Date: {date} ')
plt.xlabel('Hour (UTC)')
plt.ylabel('Doppler Shift (Hz)')
plt.gcf().set_size_inches(8, 3, forward=True)
plt.tight_layout()
plt.savefig(outfile,dpi=300)
plt.show()

# Convert decimal hours to an actual UTC time
def decimal_hours_to_utc(h):
   hours = int(h)
   minutes = int((h-hours)*60)
   seconds = round((((h-hours)*60)-minutes)*60)
   if seconds == 60:
    seconds = 0
    minutes += 1
   if minutes == 60:
      minutes = 0
      hours += 1
   if hours == 24:
      hours = 0

   return datetime.time(hour=hours,minute=minutes,second=seconds)

for t in hour:
    print(decimal_hours_to_utc(t))


