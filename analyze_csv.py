#!/usr/bin/env python
# coding: utf-8

import os
import numpy as np
import matplotlib.pyplot as plt
import re
import datetime
import math

# Input callsign
station = 'W2NAF'

base_directory = './'
csv_dir        = os.path.join(base_directory,'output','csv',station)
output_dir     = os.path.join(base_directory,'output')

filename = 'ACF_FWL_data__15.0MHz_2024-05-10_0-24.csv'
filepath = os.path.join(csv_dir, filename)

# Pull frequency and date from filename
match = re.search(r'(\d+\.?\d*)MHz_(\d{4}-\d{2}-\d{2})_(\d+)-(\d+)', filename)
if match:
    frequency = f"{match.group(1)} MHz"
    date      = match.group(2)
    sHour     = f"{match.group(3)}:00"
    eHour     = f"{match.group(4)}:00"
else: 
    frequency = "Unknown frequency"
    date      = "Unknown date"

if not os.path.exists(filepath):
    raise FileNotFoundError(filepath)
else: 
    print(filepath)

# Read .csv data
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

# Convert decimal hours to UTC format
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

#Convert UTC format to decimal hours
def utc_to_decimal_hours(t):
   return t.hour + t.minute/60 + t.second/3600

# Input time window
start_time_utc = datetime.time(0,0,0)         # Edit inputs here
end_time_utc   = datetime.time(17,10,0)    

start_time_decimal = utc_to_decimal_hours(start_time_utc)
end_time_decimal   = utc_to_decimal_hours(end_time_utc)

# Set output directory to save plots in and name output .png
'''
plot_dir = os.path.join(output_dir,'plots',station)
os.makedirs(plot_dir,exist_ok=True
outfile  = os.path.join(
    plot_dir,
    f"{station}_Doppler_vs_time_{frequency.replace(' ','')}_{date}_{start_time_utc}-{end_time_utc}.png"
'''

# Separate dop shifts < 2 (low_fd) and dop shifts > 2 (large_fd) and find min/max of both lists

low_fd              = []
low_fd_timestamps   = []
large_fd            = []
large_fd_timestamps = []

doppler_mags = np.abs(doppler)
for i in range(len(doppler_mags)):
   magnitude = doppler_mags[i]
   timestamp = hour[i]
   if magnitude < 2.0:
      low_fd.append(magnitude)
      low_fd_timestamps.append(timestamp)
   if magnitude >= 2.0:
      large_fd.append(magnitude)
      large_fd_timestamps.append(timestamp)


timestamp_min = np.min(large_fd_timestamps)
timestamp_max = np.max(large_fd_timestamps)
timestamp_min_utc = decimal_hours_to_utc(timestamp_min)
timestamp_max_utc = decimal_hours_to_utc(timestamp_max)

print("Timestamp of min"+str(timestamp_min_utc))
print("Timestamp of max"+str(timestamp_max_utc))

total_timestamps = len(hour)
num_low_fd = len(low_fd)
num_large_fd = len(large_fd)

# Calculate what percent of the total data points are "low" and "large"
percent_low = (num_low_fd / total_timestamps) * 100
print(percent_low) 

percent_large = (num_large_fd / total_timestamps) * 100
print(percent_large)



# Plot whole 24-hour period
'''
plt.scatter(hour,doppler, s=3.5,c='black')
plt.title(f'Doppler Shift vs. Time\nFrequency: {frequency} | Date: {date} ')
plt.xlabel('Hour (UTC)')
plt.ylabel('Doppler Shift (Hz)')
plt.gcf().set_size_inches(8, 3, forward=True)
plt.tight_layout()
plt.savefig(outfile,dpi=300)
plt.show()
'''

# Time windows ==============================================================================================================================================
'''
mask = (hour >= start_time_decimal) & (hour <= end_time_decimal)

time_window = hour[mask]
doppler_window = doppler[mask]
spread_window = spread[mask]
level_window = level[mask]

doppler_window_min = np.min(doppler_window)
doppler_window_max = np.max(doppler_window)

index_min = np.argmin(doppler_window)
index_max = np.argmax(doppler_window)

t_min = time_window[index_min]
t_max = time_window[index_max]
t_min_utc = decimal_hours_to_utc(t_min)
t_max_utc = decimal_hours_to_utc(t_max)

print(f'Minimum doppler during this window: {doppler_window_min} at {t_min_utc}')
print(f'Maximum doppler during this window: {doppler_window_max} at {t_max_utc}')
'''

'''
plt.scatter(time_window, doppler_window, s=3.5, c='black')
plt.title(f'Doppler Shift vs. Time (UTC)\nFrequency: {frequency} | Date: {date}')
plt.xlabel('Hour (UTC)')
plt.ylabel('Doppler Shift (Hz)')
plt.gcf().set_size_inches(8, 3, forward=True)
plt.tight_layout()
plt.savefig(outfile,dpi=300)
plt.show()
'''