# Script to create an average quiet day Doppler shift plot

import numpy as np
from matplotlib import pyplot as plt

file_name = 'May_2024_quiet_days.csv'
data = np.genfromtxt(file_name, delimiter=',', skip_header=2)

timestamp = data[:,0]
avg_dop   = data[:,8]

plt.scatter(timestamp, avg_dop, color='black', label='May 2024 Quiet Time Average', s=1.0)
plt.title('May 2024 Quiet Time Average')
plt.suptitle('W2NAF at 15.0 MHz', fontsize=12)
plt.xlabel('Time (UTC)')
plt.ylabel('Doppler shift (Hz)')
#plt.ylim(-5,5)
plt.gcf().set_size_inches(8, 3, forward=True)
plt.tight_layout()
plt.savefig("W2NAF_May_2024_15MHz_quiet_time_avg.png", dpi=600)
plt.show()

