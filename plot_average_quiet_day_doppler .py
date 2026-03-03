# Script to create an average quiet day Doppler shift plot

import numpy as np
from matplotlib import pyplot as plt
import datetime

# Load data from .csv ================================================================================================================================

file_name = 'W2NAF_May_2024_quiet_days(15MHz).csv'
data = np.genfromtxt(file_name, delimiter=',', skip_header=5)

timestamp   = data[:,0]
avg_dop     = data[:,8]
lower_error = data[:,10]    # average + stdev
upper_error = data[:,11]    # average - stdev

# Plot entire spectrogram =========================================================================================================================================

plt.scatter(timestamp, avg_dop, color='black', label='May 2024 Quiet Time Average', s=1.5)
plt.scatter(timestamp, lower_error, color='red', label='STDEV', s=0.25)
plt.scatter(timestamp, upper_error, color='blue', s=0.25)
plt.title('May 2024 Quiet Time Average')
plt.suptitle('W2NAF at 15.0 MHz', fontsize=12)
plt.xlabel('Time (UTC)')
plt.ylabel('Doppler shift (Hz)')
plt.ylim(-5,5)
plt.gcf().set_size_inches(8, 3, forward=True)
plt.tight_layout()
plt.savefig("W2NAF_May_2024_15MHz_quiet_time_avg.png", dpi=600)
plt.show()
'''
#print("Min: " + str(np.min(avg_dop)))
#print("Max: " + str(np.max(avg_dop)))

# Datetime Conversions =======================================================================================================================================

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

# =============================================================================================================================================================

# Input time window
start_time_utc = datetime.time(12,0,0)         # Edit inputs here
end_time_utc   = datetime.time(23,59,0)    

start_time_decimal = utc_to_decimal_hours(start_time_utc)
end_time_decimal   = utc_to_decimal_hours(end_time_utc)

time_window = []
doppler_window = []

for i in range(len(timestamp)):
   stamp = timestamp[i]
   dop_shift = avg_dop[i]
   if stamp >= start_time_decimal and stamp <= end_time_decimal:
      time_window.append(stamp)
      doppler_window.append(dop_shift)

print("Min: " + str(np.min(doppler_window)))
print("Max: " + str(np.max(doppler_window)))


plt.scatter(time_window, doppler_window, color='black', s=1.5)
plt.title('May 2024 Quiet Time Average')
plt.suptitle('W2NAF at 15.0 MHz', fontsize=12)
plt.xlabel('Time (UTC)')
plt.ylabel('Doppler shift (Hz)')
plt.savefig("recent.png", dpi=600)
plt.show()

'''