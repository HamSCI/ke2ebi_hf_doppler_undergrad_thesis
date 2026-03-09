# Stack a Gannon Storm Date and the average quiet time plot

# Imports ==============================================================================================

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.ticker as ticker
import datetime
import os
import re
import math

# Load Quiet day data =================================================================================

# Quiet days data
file_name = 'W2NAF_May_2024_quiet_days(15MHz).csv'
data = np.genfromtxt(file_name, delimiter=',', skip_header=5)

timestamp   = data[:,0]
avg_dop     = data[:,8]
lower_error = data[:,10]    # average + stdev
upper_error = data[:,11]    # average - stdev

# Load Gannon Storm Day data ==========================================================================

station = 'W2NAF'

base_directory = './'
csv_dir        = os.path.join(base_directory,'output','csv',station)
output_dir     = os.path.join(base_directory,'output')

filename = 'ACF_FWL_data__15.0MHz_2024-05-10_0-24.csv'                  # Input data file name here
filepath = os.path.join(csv_dir, filename)

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

# Input time window =================================================================================================

start_time_utc = datetime.time(0,0,0)                              # Edit inputs here
end_time_utc   = datetime.time(17,10,0)    

start_time_decimal = utc_to_decimal_hours(start_time_utc)
end_time_decimal   = utc_to_decimal_hours(end_time_utc)

# Plot quiet time average ===========================================================================================

def format_time(x, pos=None):
    hours = int(x) % 24
    minutes = int((x % 1) * 60)
    return f"{hours:02d}:{minutes:02d}"


# Create custom legend handles
legend_elements = [
    Line2D([0], [0], color='black', linewidth=1, label='Average'),
    Line2D([0], [0], color='red',   linewidth=1, label='STDEV'),
    Line2D([0], [0], color='blue',  linewidth=1, label='STDEV'),
]

plt.scatter(timestamp, avg_dop, color='black', s=1.5, label='Average')
plt.scatter(timestamp, lower_error, color='red', s=0.25, label='STDEV')
plt.scatter(timestamp, upper_error, color='blue', s=0.25, label='STDEV')
plt.title('May 2024 Quiet Time Average | W2NAF at 15.0 MHz', weight='bold')
#plt.suptitle('W2NAF at 15.0 MHz', fontsize=12)
plt.xlabel('Time (UTC)')
plt.ylabel('Doppler shift (Hz)')
plt.ylim(-5,5)
plt.gcf().set_size_inches(8, 3, forward=True)

ax = plt.gca()
ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_time))
# Set x-axis range and ticks
ax.set_xlim(0, 23 + 59/60)
ax.set_xticks([0, 3, 6, 9, 12, 15, 18, 21, 23 + 59/60])  # last tick = 23:59

plt.legend(handles=legend_elements)
plt.tight_layout()
#plt.savefig("W2NAF_May_2024_15MHz_quiet_time_avg.png", dpi=600)
plt.show()

# Plot whole day (Gannon storm) ======================================================================================

plt.scatter(hour,doppler, s=3.5,c='black')
plt.title(f'Doppler Shift vs. Time\nFrequency: {frequency} | Date: {date} ')
plt.xlabel('Hour (UTC)')
plt.ylabel('Doppler Shift (Hz)')
plt.gcf().set_size_inches(8, 3, forward=True)
plt.tight_layout()
#plt.savefig(outfile,dpi=300)
plt.show()
