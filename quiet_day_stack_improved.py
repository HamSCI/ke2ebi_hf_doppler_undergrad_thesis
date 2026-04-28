#!/bin/env python
# This script contains edits from original plotting code
#  1) Defined inputs outside of main "if" indent
#  2) Plot seven different dates stacked on top of each other

import os
import datetime
import logging
logger  = logging.getLogger(__name__)

import numpy as np
import pandas as pd

import matplotlib as mpl
from matplotlib import pyplot as plt

import grapeDRF

letters = 'abcdefghijklmnopqrtuvwxyz'

mpl.rcParams['font.size']       = 12
mpl.rcParams['font.weight']     = 'normal'
mpl.rcParams['axes.grid']       = True
mpl.rcParams['axes.titlesize']  = 45
mpl.rcParams['grid.linestyle']  = ':'
mpl.rcParams['figure.figsize']  = np.array([15, 8])
mpl.rcParams['axes.xmargin']    = 0
mpl.rcParams['legend.fontsize'] = 'xx-large'

mpl.rcParams['xtick.labelsize'] = 30
mpl.rcParams['ytick.labelsize'] = 27.0
mpl.rcParams['axes.labelsize']  = 40

data_source = 'w2naf_grape1'
callsign    = data_source.split('_')[0]
instrument  = data_source.split('_')[1]
lat         =  41.335116  # W2NAF
lon         =  -75.600692 # W2NAF
frequencies = [15.0]

# --- Seven dates to stack ---
date_pairs = [
    (datetime.datetime(2024, 5, 8), datetime.datetime(2024, 5, 9)),
    (datetime.datetime(2024, 5, 9), datetime.datetime(2024, 5, 10)),
    (datetime.datetime(2024, 5, 14), datetime.datetime(2024, 5, 15)),
    (datetime.datetime(2024, 5, 20), datetime.datetime(2024, 5, 21)),
    (datetime.datetime(2024, 5, 25), datetime.datetime(2024, 5,  26)),
    (datetime.datetime(2024, 5, 28), datetime.datetime(2024, 5,  29)),
    (datetime.datetime(2024, 5, 29), datetime.datetime(2024, 5, 30)),
]

station_dct = {}
sdct        = station_dct[callsign] = {}

if __name__ == '__main__':
    # Use the overall span for the output filename
    sDate_all = date_pairs[0][0]
    eDate_all = date_pairs[-1][1]
    sDate_str = sDate_all.strftime('%Y%m%d')
    eDate_str = eDate_all.strftime('%Y%m%d')
    output_dir = os.path.join('output', data_source, f'{data_source}_{sDate_str}-{eDate_str}')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    station     = callsign
    plot_list   = ['WDgrape']
    cfreqs      = frequencies

    # Build output filename
    str_sDate   = sDate_all.strftime('%Y%m%d.%H%M')
    str_eDate   = eDate_all.strftime('%Y%m%d.%H%M')
    png_ = [str_sDate, str_eDate, station]
    for pll in plot_list:
        png_.append(pll)
        if pll == 'WDgrape':
            png_ += ['{!s}'.format(x) for x in cfreqs]
    png_fname = '_'.join(png_) + '.png'
    png_fpath = os.path.join(output_dir, png_fname)

    # --- Layout: rows = dates × frequencies ---
    rows_per_date = len(cfreqs)   # one row per frequency
    nrows   = len(date_pairs) * rows_per_date
    ncols   = 1
    ax_inx  = 0
    axs     = []            # flat list of (ax, sDate, eDate) tuples

    fig = plt.figure(figsize=(22, nrows * 5))
    letter_fdict = {'size': 32}

    for date_idx, (sDate, eDate) in enumerate(date_pairs):
        figd = {}
        figd['solar_lat']             = lat
        figd['solar_lon']             = lon
        figd['overlaySolarElevation'] = True
        figd['xlim']                  = (sDate, eDate)

        if 'WDgrape' in plot_list:
            gDRF = grapeDRF.GrapeDRF(sDate, eDate, data_source)
            for cfreq in cfreqs:
                print('   Date {} — {!s} MHz...'.format(sDate.strftime('%Y-%m-%d'), cfreq))
                ax_inx += 1
                ax = fig.add_subplot(nrows, ncols, ax_inx)
                axs.append((ax, sDate, eDate))
                gDRF.plot_ax(cfreq, ax, **figd)
                ax.set_title('({!s})'.format(letters[ax_inx - 1]),
                             loc='left', fontdict=letter_fdict)
                # ~~~ CHANGE 1: date only, no frequency label ~~~
                ax.set_title(sDate.strftime('%B %d, %Y'))

    # --- Finalize axes ---
    for i, (ax, sDate, eDate) in enumerate(axs):
        ax.set_xlim(sDate, eDate)
        ax.set_ylabel('')
        for twin_ax in ax.get_shared_x_axes().get_siblings(ax):
            if twin_ax is not ax:
                twin_ax.set_ylabel('')

        xticks = ax.get_xticks()
        ax.set_xticks(xticks)

        is_last_in_date_block = ((i + 1) % rows_per_date == 0)
        is_very_last = (i == len(axs) - 1)

        # ~~~ CHANGE 2: "UTC" label and tick marks only on the very last plot ~~~
        if is_very_last:
            ax.set_xlabel('UTC', labelpad=15)
            ax.tick_params(axis='x', pad=15)
            xtkls = []
            for xtk in xticks:
                dt = mpl.dates.num2date(xtk)
                xtkls.append(dt.strftime('%H:%M'))
        else:
            ax.set_xlabel('')
            xtkls = [''] * len(xticks)

        ax.set_xticklabels(xtkls)

    # --- Figure title ---
    sdct = station_dct.get(station, {})
    stxt = '{!s} ({!s})'.format(station.upper(), instrument.upper())
    txt = [stxt]
    if 'QTH' in sdct:
        txt.append(sdct['QTH'])
    # ~~~ CHANGE 1 (cont.): add frequency to supertitle ~~~
    freq_str = ', '.join('{!s} MHz'.format(f) for f in cfreqs)
    txt.append('{} Receiver'.format(freq_str))
    fontdict = {'size': 50, 'weight': 'bold'}
    fig.text(0.5, 1., '\n'.join(txt), fontdict=fontdict, ha='center', va='bottom')

    # --- Shared axis labels ---
    fig.supylabel('Doppler Shift (Hz)', fontsize=40, x=0.065)
    fig.tight_layout(rect=[0.05, 0, 0.88, 1])

    # Shared colorbar on the right side
    mappable = None
    for ax, sDate, eDate in axs:
        for child in ax.get_children():
            if hasattr(child, 'get_array') and child.get_array() is not None:
                mappable = child
                break
        if mappable is not None:
            break

    if mappable is not None:
        # Solar Elevation label between plots and colorbar
        fig.text(0.89, 0.5, 'Solar Elevation Angle',
                 fontsize=40, ha='left', va='center', rotation=270,
                 transform=fig.transFigure)

        # Colorbar to the right of that label
        cbar_ax = fig.add_axes([0.93, 0.05, 0.018, 0.88])
        cbar    = fig.colorbar(mappable, cax=cbar_ax)
        cbar.set_label('Relative Signal Strength (dB)', fontsize=40,
                       labelpad=60, rotation=270)
        cbar.ax.tick_params(labelsize=30)

    fig.savefig(png_fpath, bbox_inches='tight')
    print(png_fpath)