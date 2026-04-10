# Time rate of change

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.ticker as ticker
import datetime
import os
import re
import math

# Load Data ==============================================================================================================

station = 'W2NAF'

base_directory = './'
csv_dir        = os.path.join(base_directory,'output','csv',station)
output_dir     = os.path.join(base_directory,'output')

filename = 'ACF_FWL_data__15.0MHz_2024-05-10_0-24.csv'                  # Input data file name here
filepath = os.path.join(csv_dir, filename)

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

#============================================================================================================================

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

# Covert between decimal hours and UTC format ====================================================================

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

utc = datetime.time(17,10,0)
decimal_result = utc_to_decimal_hours(utc)
print(f'Decimal result: {decimal_result}')

# Plot figure =====================================================================================================

plt.scatter(hour,doppler, s=3.5,c='black')
plt.title(f'Doppler Shift vs. Time\nFrequency: {frequency} | Date: {date} ')
plt.xlabel('Hour (UTC)')
plt.ylabel('Doppler Shift (Hz)')
plt.gcf().set_size_inches(8, 3, forward=True)
plt.tight_layout()
#plt.savefig(outfile,dpi=300)
#plt.show()

# Find Rate of Change ==============================================================================================

# Input time window
#start_time_utc = datetime.time(17,10,0)                              # Edit inputs here
#end_time_utc   = datetime.time(23,59,59)    

#start_time_decimal = utc_to_decimal_hours(start_time_utc)
#end_time_decimal   = utc_to_decimal_hours(end_time_utc)

start_time_decimal = decimal_result
end_time_decimal = 23.96667

time_window = []
dop_window = []
spread_window = []
level_window = []

for i in range(len(hour)):
   time = hour[i]
   dop = doppler[i]
   freq_spread = spread[i]
   sn_level = level[i]

   if time >= start_time_decimal and time <= end_time_decimal:
      time_window.append(time)
      dop_window.append(dop)
      spread_window.append(freq_spread)
      level_window.append(sn_level)



if len(level_window) > 0:
    max_idx = np.argmax(level_window)
    min_idx = np.argmin(level_window)

    max_level = level_window[max_idx]
    min_level = level_window[min_idx]
    max_time  = decimal_hours_to_utc(time_window[max_idx])
    min_time  = decimal_hours_to_utc(time_window[min_idx])

    print(f"Max S/N level: {max_level:.2f} dB at {max_time}")
    print(f"Min S/N level: {min_level:.2f} dB at {min_time}")
else:
    print("No data in time window.")





#===========================================================================================================
