# Analyze signal to noise level

import os
import numpy as np
from matplotlib import pyplot as plt
import datetime

station = 'W2NAF'

base_directory = './'
csv_dir        = os.path.join(base_directory,'output','csv',station)
output_dir     = os.path.join(base_directory,'output')

file_name = 'ACF_FWL_data__15.0MHz_2024-05-11_0-24.csv'
filepath = os.path.join(csv_dir, file_name)

parts = file_name.split('_')
freq = [p for p in parts if 'MHz' in p][0]
date_str = [p for p in parts if p.count('-') == 2 and p[:2] == '20'][0]   # YYYY-MM-DD token

data = np.genfromtxt(filepath, delimiter=',', skip_header=3)

timestamp = data[:,0]
level     = data[:,3]

# Functions ==========================================================================================================================

#Convert UTC format to decimal hours
def utc_to_decimal_hours(t):
   return t.hour + t.minute/60 + t.second/3600

#=====================================================================================================================================

# Input time window
start_time_utc = datetime.time(18,0,0)     # input start of time window here
end_time_utc   = datetime.time(22,0,0)    # input end of time window here

# Convert to decimal hours
start_time_decimal = utc_to_decimal_hours(start_time_utc)
end_time_decimal   = utc_to_decimal_hours(end_time_utc)


time_window = []
sn_window   = []

# Pull data points only inside the desired time window
for i in range(len(timestamp)):
   time = timestamp[i]
   sn   = level[i]
   if time >= start_time_decimal and time <= end_time_decimal:
      time_window.append(time)
      sn_window.append(sn)

# Find maximum S+N Level in that time window
max_idx  = np.argmax(sn_window)
max_time = time_window[max_idx]
max_val  = sn_window[max_idx]

hours1   = int(max_time)
minutes1 = int((max_time % 1) * 60)
print(f'Max S+N: {max_val:.2f} dB at {hours1:02d}:{minutes1:02d} UTC')

# Find minimum S+N Level in that time window
min_idx  = np.argmin(sn_window)
min_time = time_window[min_idx]
min_val  = sn_window[min_idx]

hours2   = int(min_time)
minutes2 = int((min_time % 1) * 60)
print(f'Min S+N: {min_val:.2f} dB at {hours2:02d}:{minutes2:02d} UTC')

# Create figure
plt.scatter(time_window, sn_window, color='black', s=2.0)
plt.gcf().set_size_inches(8, 3, forward=True)
plt.suptitle(f'S+N Level {station} at {freq}')
plt.title(f'{date_str}')
plt.xlabel('Hour (UTC)')
plt.ylabel('Signal + Noise Level (dB)')
plt.tight_layout()
plt.savefig('./output/sn_level_analysis.png')
plt.show()
