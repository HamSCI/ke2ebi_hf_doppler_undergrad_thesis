# Custom SYM-H plot

'''
import math
from matplotlib import pyplot as plt
import numpy as np

filename = 'OMNI_HRO_1MIN_2496091.csv'
data = np.genfromtxt(filename, delimiter=',', skip_header = 69)

time = data[:,0]
SYM_H = data[:,1]

SYM_H[SYM_H > 9000] = np.nan
plt.plot(time, SYM_H)
plt.show()

with open(filename) as f:
    lines = f.readlines()
print(lines[68])  # the header row (0-indexed, so row 69 = index 68)

print(data[:5, :5])   # should show numbers, not nan
print(data.shape)     # should be (rows, columns) with reasonable counts
'''

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

filename = 'OMNI_HRO_1MIN_2496091.csv'

data = np.genfromtxt(filename, delimiter=',', skip_header=69, dtype=str)

time = np.array([datetime.strptime(t, '%Y-%m-%dT%H:%M:%S.%fZ') for t in data[:, 0]])
SYM_H = data[:, 1].astype(float)

SYM_H[SYM_H > 9000] = np.nan

#fig, ax = plt.subplots()
fig, ax = plt.subplots(figsize=(14, 5))
ax.plot(time, SYM_H)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
fig.autofmt_xdate()
ax.set_xlabel('Time (UTC)')
ax.set_ylabel('SYM-H (nT)')
ax.set_title('SYM-H Index')
plt.tight_layout()
plt.show()
plt.savefig("Custom SYM-H Plot")