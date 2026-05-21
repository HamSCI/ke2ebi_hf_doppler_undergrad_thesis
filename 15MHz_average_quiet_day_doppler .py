# Script to create an average quiet day Doppler shift plot

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.ticker as ticker
import datetime

# Load data from .csv ================================================================================================================================

file_name = 'data/W2NAF_May_2024_quiet_days(15MHz).csv'
data = np.genfromtxt(file_name, delimiter=',', skip_header=5)

timestamp   = data[:,0]
avg_dop     = data[:,8]
lower_error = data[:,10]    # average + stdev
upper_error = data[:,11]    # average - stdev

# Datetime conversions ====================================================================================================================================

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


# Plot entire spectrogram =========================================================================================================================================

def format_time(x, pos=None):
    hours = int(x) % 24
    minutes = int((x % 1) * 60)
    return f"{hours:02d}:{minutes:02d}"


# Create custom legend handles
legend_elements = [
    Line2D([0], [0], color='black', linewidth=1, label='Average'),
    Line2D([0], [0], color='red',   linewidth=1, label='-STDEV'),
    Line2D([0], [0], color='blue',  linewidth=1, label='+STDEV'),
]

plt.scatter(timestamp, avg_dop, color='black', s=1.5, label='Average')
plt.scatter(timestamp, lower_error, color='red', s=0.25, label='-STDEV')
plt.scatter(timestamp, upper_error, color='blue', s=0.25, label='+STDEV')
plt.title('May 2024 Quiet Time Average | W2NAF at 15.0 MHz', weight='bold', size=18)
#plt.suptitle('W2NAF at 15.0 MHz', fontsize=12)
plt.xlabel('Time (UTC)', size=14)
plt.ylabel('Doppler shift (Hz)', size=14)
#plt.ylim(-5,5)
plt.gcf().set_size_inches(8, 3, forward=True)

ax = plt.gca()
ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_time))
# Set x-axis range and ticks
ax.set_xlim(0, 23 + 59/60)
ax.set_xticks([0, 3, 6, 9, 12, 15, 18, 21, 23 + 59/60])  # last tick = 23:59
ax.tick_params(axis='both', labelsize=12)  # Set whatever size you want

plt.legend(handles=legend_elements)
plt.tight_layout()
plt.savefig("./output/W2NAF_May_2024_15MHz_quiet_time_avg.png", dpi=600)
plt.show()


# Plot a portion of the spectrogram ==============================================================================================================================================

# Input time window
start_time_utc = datetime.time(8,0,0)         # Edit inputs here
end_time_utc   = datetime.time(13,0,0)    

start_time_decimal = utc_to_decimal_hours(start_time_utc)
end_time_decimal   = utc_to_decimal_hours(end_time_utc)

print(start_time_decimal)

time_window = []
doppler_window = []
upper_error_window = []
lower_error_window = []

for i in range(len(timestamp)):
   stamp = timestamp[i]
   dop_shift = avg_dop[i]
   pos_stdev = upper_error[i]
   neg_stdev = lower_error[i]
   if stamp >= start_time_decimal and stamp <= end_time_decimal:
      time_window.append(stamp)
      doppler_window.append(dop_shift)
      upper_error_window.append(pos_stdev)
      lower_error_window.append(neg_stdev)
'''
# Find max & min Dop shift in that time window
max_idx  = np.argmax(doppler_window)
max_time = time_window[max_idx]
max_val  = doppler_window[max_idx]
min_idx  = np.argmin(doppler_window)
min_time = time_window[min_idx]
min_val  = doppler_window[min_idx]


# Find max positive STDEV
max_stdev_idx  = np.argmax(pos_stdev_window)
max_stdev_time = pos_stdev_window[max_stdev_idx]
max_stdev_val  = pos_stdev_window[max_stdev_idx]

min_stdev_idx  = np.argmin(neg_stdev_window)
min_stdev_time = time_window[min_stdev_idx]
min_stdev_val  = neg_stdev_window[min_stdev_idx]


hours_max   = int(max_time)
minutes_max = int((max_time % 1) * 60)
hours_min   = int(min_time)
minutes_min = int((min_time % 1) * 60)
print(f'Max Dop shift: {max_val:.2f} Hz at {hours_max:02d}:{minutes_max:02d} UTC')
print(f'Min Dop shift: {min_val:.2f} Hz at {hours_min:02d}:{minutes_min:02d} UTC')
'''

# Create custom legend handles
legend_elements = [
    Line2D([0], [0], color='black', linewidth=1, label='Average'),
    Line2D([0], [0], color='red',   linewidth=1, label='-STDEV'),
    Line2D([0], [0], color='blue',  linewidth=1, label='+STDEV'),
]

plt.scatter(time_window, doppler_window, color='black', s=1.5, label='Average')
plt.scatter(time_window, lower_error_window, color='red', s=1.0, label='-STDEV')
plt.scatter(time_window, upper_error_window, color='blue', s=1.0, label='+STDEV')
#plt.ylim(-4,4)
plt.title(f'May 2024 Quiet Time Average | W2NAF at 15.0 MHz', weight='bold', size=15)
plt.xlabel('Time (UTC)', size=14)
plt.ylabel('Doppler shift (Hz)', size=14)
plt.legend(handles=legend_elements)
ax.tick_params(axis='both', labelsize=13)  # Set whatever size you want
plt.savefig("output/15_MHz_quiet_time_avg_window.png", dpi=600)
plt.show()
