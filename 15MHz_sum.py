# 15 MHz Observations Summary

# ===== SYM-H ====================================

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

sym_filename = '15MHz_GannonStorm_obs.csv'
sym_data = np.genfromtxt(sym_filename, delimiter=',', skip_header=2, dtype=str)

timestamp = np.array([datetime.strptime(t, '%Y-%m-%dT%H:%M:%S.%fZ') for t in sym_data[:, 0]])
SYM_H = sym_data[:, 1].astype(float)

#fig, ax = plt.subplots()
fig, ax = plt.subplots(figsize=(14, 5))
ax.plot(timestamp, SYM_H)
#ax.axvline(x=datetime(2024, 5, 10, 17, 10), color='red', linestyle='-', linewidth=0.5, label='SSC')
ax.axvline(x=datetime(2024, 5, 10, 17, 15), color='red', linestyle='--', linewidth=1.5, label='Start of main phase')
ax.axvline(x=datetime(2024, 5, 11, 2, 15), color='blue', linestyle='--', linewidth=1.5, label='Start of recovery phase')
ax.tick_params(axis='both', labelsize=20)
ax.legend(fontsize=16)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
fig.autofmt_xdate()
ax.set_xlabel('Time (UTC)', size=25.0, fontweight='bold')
ax.set_ylabel('SYM-H (nT)', size=25.0, fontweight='bold')
ax.set_title('SYM-H Index', size=30.0, fontweight='bold')
plt.tight_layout()
plt.show()

# ===== Load Data: Doppler Shift (Hz) & S+N (dB) ===========================================

May10_filename = 'ACF_FWL_data__15.0MHz_2024-05-10_0-24.csv'
May10_data = np.genfromtxt(May10_filename, delimiter=',', skip_header=3)
time = May10_data[:,0]
May10_dop = May10_data[:,1]
May10_level = May10_data[:,3]

May11_filename = 'ACF_FWL_data__15.0MHz_2024-05-11_0-24.csv'
May11_data = np.genfromtxt(May11_filename, delimiter=',', skip_header=3)
May11_dop = May11_data[:,1]
May11_level = May11_data[:,3]

May12_filename = 'ACF_FWL_data__15.0MHz_2024-05-12_0-24.csv'
May12_data = np.genfromtxt(May12_filename, delimiter=',', skip_header=3)
May12_dop = May12_data[:,1]
May12_level = May12_data[:,3]

May13_filename = 'ACF_FWL_data__15.0MHz_2024-05-13_0-24.csv'
May13_data = np.genfromtxt(May13_filename, delimiter=',', skip_header=3)
May13_dop = May13_data[:,1]
May13_level = May13_data[:,3]

May14_filename = 'ACF_FWL_data__15.0MHz_2024-05-14_0-24.csv'
May14_data = np.genfromtxt(May14_filename, delimiter=',', skip_header=3)
May14_dop = May14_data[:,1]
May14_level = May14_data[:,3]

# ===== Plot Doppler Shift Data for May 10 - May 14 ================================

# ===== Continuous Doppler Shift Plot: May 10 – May 14 ================================

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta

# Build continuous time axis — each day offsets by 24 hours
hours_per_day = 24
offsets = [0, 24, 48, 72, 96]  # May 10–14

day_data = [
    (May10_dop, May10_level),
    (May11_dop, May11_level),
    (May12_dop, May12_level),
    (May13_dop, May13_level),
    (May14_dop, May14_level),
]

day_labels = ['May 10', 'May 11', 'May 12', 'May 13', 'May 14']

# Concatenate with time offsets
cont_time  = np.concatenate([time + offset for offset in offsets])
cont_dop   = np.concatenate([d[0] for d in day_data])
cont_level = np.concatenate([d[1] for d in day_data])

# ===== Plot ================================

# Helper: convert a datetime to continuous hours from May 10 00:00 UTC
origin = datetime(2024, 5, 10, 0, 0)
def to_cont_hours(dt):
    return (dt - origin).total_seconds() / 3600

# Phase marker times
t_main_phase     = to_cont_hours(datetime(2024, 5, 10, 17, 15))
t_recovery_phase = to_cont_hours(datetime(2024, 5, 11,  2, 15))

fig, axes = plt.subplots(2, 1, figsize=(16, 7), sharex=True)
ax1, ax2 = axes

ax1.plot(cont_time, cont_dop,   color='#1f77b4', linewidth=0.7, alpha=0.9)
ax2.plot(cont_time, cont_level, color='#d62728', linewidth=0.7, alpha=0.9)

# Vertical day-boundary lines + labels
for i, offset in enumerate(offsets):
    for ax in axes:
        ax.axvline(offset, color='gray', linewidth=0.8, linestyle='--', alpha=0.5)
    ax1.text(offset + 0.5, ax1.get_ylim()[1], day_labels[i],
             fontsize=8, color='gray', va='top')

# Phase markers
for ax in axes:
    ax.axvline(t_main_phase,     color='red',  linestyle='--', linewidth=1.5)
    ax.axvline(t_recovery_phase, color='blue', linestyle='--', linewidth=1.5)

# Phase labels on top axes only
ax1.text(t_main_phase     + 0.3, ax1.get_ylim()[0], 'Main phase',     color='red',  fontsize=12, va='bottom')
ax1.text(t_recovery_phase + 0.3, ax1.get_ylim()[0], 'Recovery phase', color='blue', fontsize=12, va='bottom')

ax1.axhline(0, color='black', linewidth=0.6, linestyle=':')
ax1.set_ylabel('Doppler Shift (Hz)', fontsize=20)
ax1.set_title('15.0 MHz — Continuous Doppler Shift & Signal Level, May 10–14 2024', fontsize=26, weight='bold')
ax1.grid(True, linestyle='--', alpha=0.3)
ax1.legend(loc='upper right', fontsize=12)

ax2.set_ylabel('Signal + Noise (dB)', fontsize=16)
ax2.set_xlabel('Time (UTC)', fontsize=20)
ax2.grid(True, linestyle='--', alpha=0.3)

# X-axis ticks every 6 hours, labelled as day + HH:MM
tick_positions = np.arange(0, 5 * 24 + 1, 6)
tick_labels = []
for t in tick_positions:
    day_idx = int(t // 24)
    hour    = int(t % 24)
    if hour == 0:
        tick_labels.append(f"May {10 + day_idx}\n00:00")
    else:
        tick_labels.append(f"{hour:02d}:00")

ax2.set_xticks(tick_positions)
ax2.set_xticklabels(tick_labels, fontsize=7)
ax2.set_xlim(0, 5 * 24)
ax1.tick_params(axis='both', labelsize=14)
ax2.tick_params(axis='both', labelsize=14)
plt.tight_layout()
plt.savefig('doppler_may10_14_continuous.png', dpi=150, bbox_inches='tight')
plt.show()

# ===== Combined Figure: SYM-H + Doppler Shift + S+N Level ========================

origin = datetime(2024, 5, 10, 0, 0)
def to_cont_hours(dt):
    return (dt - origin).total_seconds() / 3600

# Convert SYM-H timestamps to continuous hours
symh_time = np.array([(t - origin).total_seconds() / 3600 for t in timestamp])

# Phase marker times
t_main_phase     = to_cont_hours(datetime(2024, 5, 10, 17, 15))
t_recovery_phase = to_cont_hours(datetime(2024, 5, 11,  2, 15))

fig, (ax_sym, ax1, ax2) = plt.subplots(3, 1, figsize=(16, 11), sharex=True)

# --- SYM-H ---
ax_sym.plot(symh_time, SYM_H, color='black', linewidth=0.8)
ax_sym.set_ylabel('SYM-H (nT)', fontsize=29, fontweight='bold')   # SYM-H label
ax_sym.set_title('15.0 MHz — May 10–14 2024', fontsize=28, fontweight='bold')  # Title label
ax_sym.grid(True, linestyle='--', alpha=0.3)
ax_sym.tick_params(axis='both', labelsize=20)   # Tick params

# --- Doppler Shift ---
ax1.plot(cont_time, cont_dop, color='#1f77b4', linewidth=0.7, alpha=0.9)
ax1.axhline(0, color='black', linewidth=0.6, linestyle=':')
ax1.set_ylabel('Doppler Shift (Hz)', fontsize=19, fontweight='bold')    # Doppler label
ax1.grid(True, linestyle='--', alpha=0.3)
ax1.tick_params(axis='both', labelsize=20)  # Tick params

# --- S+N Level ---
ax2.plot(cont_time, cont_level, color='#d62728', linewidth=0.7, alpha=0.9)
ax2.set_ylabel('Signal + Noise (dB)', fontsize=19, fontweight='bold')           # S+N label
ax2.set_xlabel('Time (UTC)', fontsize=22, fontweight='bold')
ax2.grid(True, linestyle='--', alpha=0.3)
ax2.tick_params(axis='both', labelsize=30)  # Tick params

# --- Phase markers + day boundaries on all three axes ---
for ax in (ax_sym, ax1, ax2):
    ax.axvline(t_main_phase,     color='red',  linestyle='--', linewidth=1.5)
    ax.axvline(t_recovery_phase, color='blue', linestyle='--', linewidth=1.5)
    for offset in offsets:
        ax.axvline(offset, color='gray', linewidth=0.8, linestyle='--', alpha=0.5)

# Day labels on top panel only
for i, offset in enumerate(offsets):
    ax_sym.text(offset + 0.5, ax_sym.get_ylim()[1], day_labels[i],
                fontsize=16, color='gray', va='top')          # Day labels

# Phase labels on SYM-H panel
ax_sym.text(t_main_phase     + 0.3, ax_sym.get_ylim()[0], 'Main phase',
            color='red',  fontsize=14, va='bottom')                              # main phase label
ax_sym.text(t_recovery_phase + 0.3, ax_sym.get_ylim()[0], 'Recovery phase',
            color='blue', fontsize=14, va='bottom')                              # recovery phase label

# --- Shared x-axis ticks ---
tick_positions = np.arange(0, 5 * 24 + 1, 6)
tick_labels = []
for t in tick_positions:
    day_idx = int(t // 24)
    hour    = int(t % 24)
    if hour == 0:
        tick_labels.append(f"May {10 + day_idx}\n00:00")
    else:
        tick_labels.append(f"{hour:02d}:00")

ax2.set_xticks(tick_positions)
ax2.set_xticklabels(tick_labels, fontsize=14)
ax2.set_xlim(0, 5 * 24)

plt.tight_layout()
plt.savefig('doppler_symh_may10_14.png', dpi=150, bbox_inches='tight')
plt.show()