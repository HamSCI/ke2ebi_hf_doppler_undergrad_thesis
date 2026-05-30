# Custom SYM-H plot

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime


filename = 'data/SYMH_GannonStorm.csv'
data = np.genfromtxt(filename, delimiter=',', skip_header=69, dtype=str)

time = np.array([datetime.strptime(t, '%Y-%m-%dT%H:%M:%S.%fZ') for t in data[:, 0]])
SYM_H = data[:, 1].astype(float)

SYM_H[SYM_H > 9000] = np.nan

target = datetime(2024, 5, 11, 2, 15)
idx = np.argmin(np.abs(time - target))
print(f"SYM-H at {time[idx]}: {SYM_H[idx]} nT")

#fig, ax = plt.subplots()
fig, ax = plt.subplots(figsize=(14, 5))
ax.plot(time, SYM_H)
#ax.axvline(x=datetime(2024, 5, 10, 17, 10), color='red', linestyle='-', linewidth=0.5, label='SSC')
ax.axvline(x=datetime(2024, 5, 10, 17, 15), color='red', linestyle='--', linewidth=1.5, label='Start of main phase')
ax.axvline(x=datetime(2024, 5, 11, 2, 15), color='blue', linestyle='--', linewidth=1.5, label='Start of recovery phase')
ax.tick_params(axis='both', labelsize=20)
ax.legend(fontsize=16)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
ax.xaxis.set_major_locator(mdates.HourLocator(interval=12))   # ticks every 12 h
ax.set_xlim(datetime(2024, 5, 10), datetime(2024, 5, 14))     # crop to the storm window
fig.autofmt_xdate()
ax.set_xlabel('Time (UTC)', size=25.0, fontweight='bold')
ax.set_ylabel('SYM-H (nT)', size=25.0, fontweight='bold')
ax.set_title('SYM-H Index', size=30.0, fontweight='bold')
plt.tight_layout()
plt.savefig("output/Gannon_SYM-H_Plot.png", dpi=600)
plt.show()