# Combined: SYM-H + PSWS Spectrogram + Doppler Shift + S+N Level
# Panels (top to bottom): SYM-H | Spectrogram | Doppler Shift | S+N Level

import os
import datetime
import logging
logger = logging.getLogger(__name__)

import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
import grapeDRF

data         = os.path.join(os.getcwd(), 'data')

letters = 'abcdefghijklmnopqrtuvwxyz'

mpl.rcParams['font.size']       = 12
mpl.rcParams['font.weight']     = 'normal'
mpl.rcParams['axes.grid']       = True
mpl.rcParams['axes.titlesize']  = 30
mpl.rcParams['grid.linestyle']  = ':'
mpl.rcParams['figure.figsize']  = np.array([15, 8])
mpl.rcParams['axes.xmargin']    = 0
mpl.rcParams['legend.fontsize'] = 'xx-large'
mpl.rcParams['axes.labelsize']  = 28
mpl.rcParams['xtick.labelsize'] = 30
mpl.rcParams['ytick.labelsize'] = 20

# --- Shared config ---
data_source = 'w2naf_rx888'                            # Input data directory ("callsign_instrument")
callsign    = data_source.split('_')[0]
instrument  = data_source.split('_')[1]
sDate       = datetime.datetime(2024, 5, 10)           # Input start date
eDate       = datetime.datetime(2024, 5, 15)           # Input end date
lat         =  41.335116                               # Input station latitude
lon         =  -75.600692                              # Input station longitude
frequencies = [15.0]                                   # Specify frequency you want to plot

station_dct = {}
sdct        = station_dct[callsign] = {}

if __name__ == '__main__':
    sDate_str  = sDate.strftime('%Y%m%d')
    eDate_str  = eDate.strftime('%Y%m%d')
    output_dir = os.path.join('output', data_source, f'{data_source}_{sDate_str}-{eDate_str}')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    station  = callsign
    cfreqs   = frequencies

    png_fname = f"{sDate.strftime('%Y%m%d.%H%M')}_{eDate.strftime('%Y%m%d.%H%M')}_{station}_combined_symh_spect_doppler.png"
    png_fpath = os.path.join(output_dir, png_fname)

    # ------------------------------------------------------------------ #
    # 1. Load SYM-H
    # ------------------------------------------------------------------ #
    sym_filename = 'SYMH_GannonStorm.csv'
    sym_data     = np.genfromtxt(os.path.join(data, sym_filename), delimiter=',', skip_header=2, dtype=str)
    timestamp    = np.array([datetime.datetime.strptime(t, '%Y-%m-%dT%H:%M:%S.%fZ')
                             for t in sym_data[:, 0]])
    SYM_H        = sym_data[:, 1].astype(float)

    # ------------------------------------------------------------------ #
    # 2. Load Doppler / S+N CSVs and build datetime arrays
    # ------------------------------------------------------------------ #
    csv_dir   = os.path.join(os.getcwd(), 'output', 'csv', 'W2NAF')
    day_files = [
        os.path.join(csv_dir, 'ACF_FWL_data__15.0MHz_2024-05-10_0-24.csv'),
        os.path.join(csv_dir, 'ACF_FWL_data__15.0MHz_2024-05-11_0-24.csv'),
        os.path.join(csv_dir, 'ACF_FWL_data__15.0MHz_2024-05-12_0-24.csv'),
        os.path.join(csv_dir, 'ACF_FWL_data__15.0MHz_2024-05-13_0-24.csv'),
        os.path.join(csv_dir, 'ACF_FWL_data__15.0MHz_2024-05-14_0-24.csv'),
    ]
    day_origins = [datetime.datetime(2024, 5, 10 + i) for i in range(5)]

    dop_times, dop_vals, level_vals = [], [], []
    for fname, origin in zip(day_files, day_origins):
        d = np.genfromtxt(fname, delimiter=',', skip_header=3)
        hours = d[:, 0]
        dop_times.append(np.array([origin + datetime.timedelta(hours=float(h)) for h in hours]))
        dop_vals.append(d[:, 1])
        level_vals.append(d[:, 3])

    dop_time   = np.concatenate(dop_times)
    cont_dop   = np.concatenate(dop_vals)
    cont_level = np.concatenate(level_vals)

    # ------------------------------------------------------------------ #
    # 3. Phase marker datetimes
    # ------------------------------------------------------------------ #
    t_main_phase     = datetime.datetime(2024, 5, 10, 17, 15)
    t_recovery_phase = datetime.datetime(2024, 5, 11,  2, 15)
    day_boundaries   = day_origins

    # ------------------------------------------------------------------ #
    # 4. Build figure
    # ------------------------------------------------------------------ #
    fig = plt.figure(figsize=(22, 20))
    gs  = fig.add_gridspec(4, 1, height_ratios=[1, 1, 1, 1],
                           hspace=0.2, left=0.10, right=0.88, top=0.88, bottom=0.07)

    ax_sym   = fig.add_subplot(gs[0])
    ax_spect = fig.add_subplot(gs[1], sharex=ax_sym)
    ax_dop   = fig.add_subplot(gs[2], sharex=ax_sym)
    ax_level = fig.add_subplot(gs[3], sharex=ax_sym)

    letter_fdict = {'size': 32}

    # ------------------------------------------------------------------ #
    # 5. Panel (a): SYM-H
    # ------------------------------------------------------------------ #
    ax_sym.plot(timestamp, SYM_H, color='black', linewidth=0.8)
    ax_sym.set_ylabel('SYM-H (nT)', fontsize=25, fontweight='bold', rotation=270)
    ax_sym.tick_params(axis='both', labelsize=20)
    ax_sym.set_title('(a)', loc='left', fontdict=letter_fdict)
    #ax_sym.set_title('SYM-H Index')

    # ------------------------------------------------------------------ #
    # 6. Panel (b): PSWS spectrogram via grapeDRF
    # ------------------------------------------------------------------ #
    figd = {
        'solar_lat':             lat,
        'solar_lon':             lon,
        'overlaySolarElevation': True,
        'xlim':                  (sDate, eDate),
    }
    gDRF = grapeDRF.GrapeDRF(sDate, eDate, data_source)
    for cfreq in cfreqs:
        print('   {!s} MHz...'.format(cfreq))
        gDRF.plot_ax(cfreq, ax_spect, **figd)
        for twin_ax in ax_spect.get_shared_x_axes().get_siblings(ax_spect):
            if twin_ax is not ax_spect:
                twin_ax.yaxis.label.set_rotation(90)
                twin_ax.yaxis.label.set_ha('center')
                twin_ax.yaxis.labelpad = 3
    ax_spect.set_title('(b)', loc='left', fontdict=letter_fdict)
    ax_spect.set_title('{!s} MHz Receiver'.format(cfreqs[0]))
    ax_spect.set_ylabel('Doppler Shift (Hz)', fontsize=25, fontweight='bold')
    ax_spect.set_xlabel('')

    # ------------------------------------------------------------------ #
    # 7. Panel (c): Doppler shift line plot
    # ------------------------------------------------------------------ #
    ax_dop.plot(dop_time, cont_dop, color='#1f77b4', linewidth=0.7, alpha=0.9)
    ax_dop.axhline(0, color='black', linewidth=0.6, linestyle=':')
    ax_dop.set_ylabel('Doppler Shift (Hz)', fontsize=25, fontweight='bold')
    ax_dop.tick_params(axis='both', labelsize=20)
    ax_dop.set_title('(c)', loc='left', fontdict=letter_fdict)

    # ------------------------------------------------------------------ #
    # 8. Panel (d): S+N level
    # ------------------------------------------------------------------ #
    ax_level.plot(dop_time, cont_level, color='#d62728', linewidth=0.7, alpha=0.9)
    ax_level.set_ylabel('Signal + Noise (dB)', fontsize=25, fontweight='bold')
    ax_level.set_xlabel('Time (UTC)', fontsize=28, fontweight='bold')
    ax_level.tick_params(axis='both', labelsize=20)
    ax_level.set_title('(d)', loc='left', fontdict=letter_fdict)

    # ------------------------------------------------------------------ #
    # 9. Phase markers + day boundaries on all panels
    # ------------------------------------------------------------------ #
    for ax in (ax_sym, ax_spect, ax_dop, ax_level):
        ax.axvline(t_main_phase,     color='red',  linestyle='--', linewidth=1.5, label="Start of main phase")
        ax.axvline(t_recovery_phase, color='blue', linestyle='--', linewidth=1.5, label="Start of recovery phase")
        for bd in day_boundaries:
            ax.axvline(bd, color='gray', linewidth=0.8, linestyle='--', alpha=0.5)
        ax_sym.legend(fontsize=20, loc='lower right')

    # Phase + day labels on SYM-H panel only
    ylim_sym = ax_sym.get_ylim()
    day_labels = [f'May {10 + i}' for i in range(5)]
    for i, bd in enumerate(day_boundaries):
        ax_sym.text(bd + datetime.timedelta(minutes=30), ylim_sym[1],
                    day_labels[i], fontsize=25, color='gray', va='top')

    # ------------------------------------------------------------------ #
    # 10. X-axis ticks — only show on bottom panel
    # ------------------------------------------------------------------ #
    for ax in (ax_sym, ax_spect, ax_dop):
        plt.setp(ax.get_xticklabels(), visible=False)
        ax.set_xlabel('')

    def xtick_fmt(x, pos):
        dt = mdates.num2date(x)
        if dt.hour == 0 and dt.minute == 0:
            return dt.strftime('%d %b\n%Y')
        elif dt.hour == 12:
            return '12:00'
        return ''

    ax_level.xaxis.set_major_locator(mdates.HourLocator(byhour=[0, 12]))
    ax_level.xaxis.set_major_formatter(mpl.ticker.FuncFormatter(xtick_fmt))
    ax_level.set_xlim(sDate, eDate)
    ax_level.tick_params(axis='x', labelsize=25, pad=8)

    # ------------------------------------------------------------------ #
    # 11. Supertitle
    # ------------------------------------------------------------------ #
    sdct  = station_dct.get(station, {})
    stxt  = '{!s} ({!s})'.format(station.upper(), instrument.upper())
    txt   = [stxt]
    if 'QTH' in sdct:
        txt.append(sdct['QTH'])
    txt.append('{} - {}'.format(sDate.strftime('%d %b %Y'), eDate.strftime('%d %b %Y')))
    fontdict = {'size': 42, 'weight': 'bold'}
    fig.text(0.5, 0.97, '\n'.join(txt), fontdict=fontdict, ha='center', va='top')

    # ------------------------------------------------------------------ #
    # 12. Shared colorbar for the spectrogram
    # ------------------------------------------------------------------ #
    mappable = None
    for child in ax_spect.get_children():
        if hasattr(child, 'get_array') and child.get_array() is not None:
            mappable = child
            break

    if mappable is not None:
        #fig.text(0.89, 0.5, 'Solar Elevation Angle',
                 #fontsize=25, ha='left', va='center', rotation=270,
                 #transform=fig.transFigure)
        cbar_ax = fig.add_axes([0.95, 0.07, 0.018, 0.84])
        cbar    = fig.colorbar(mappable, cax=cbar_ax)
        cbar.set_label('Relative Signal Strength (dB)', fontsize=25,
                       labelpad=50, rotation=270)
        cbar.ax.tick_params(labelsize=20)

    fig.align_ylabels([ax_sym, ax_spect, ax_dop, ax_level])
    fig.savefig(png_fpath, bbox_inches='tight')
    print(png_fpath)