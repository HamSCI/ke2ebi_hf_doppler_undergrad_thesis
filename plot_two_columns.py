# Two columns

#!/bin/env python
# This scripts contains edits from original plotting code
#  1) Defined inputs outside of main "if" indent
#  2) Side-by-side date comparison: two dates plotted in parallel columns,
#     one column per date, one row per frequency

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
mpl.rcParams['font.weight']     = 'bold'
mpl.rcParams['axes.grid']       = True
mpl.rcParams['axes.titlesize']  = 45
mpl.rcParams['grid.linestyle']  = ':'
mpl.rcParams['figure.figsize']  = np.array([15, 8])
mpl.rcParams['axes.xmargin']    = 0
mpl.rcParams['legend.fontsize'] = 'xx-large'

mpl.rcParams['xtick.labelsize'] = 40   # x-axis tick labels
mpl.rcParams['ytick.labelsize'] = 40   # y-axis tick labels
mpl.rcParams['axes.labelsize']  = 40   # x and y axis titles (e.g. 'UTC')

mpl.rcParams['axes.titlepad']  = 20   # space between axes title and the axes
mpl.rcParams['xtick.major.pad'] = 20   # space between x tick marks and tick labels
mpl.rcParams['ytick.major.pad'] = 20   # space between y tick marks and tick labels


data_source = 'w2naf_grape1'                    # Data directory {callsign}_{instrument}
callsign    = data_source.split('_')[0]         # Extract callsign from directory name
instrument  = data_source.split('_')[1]         # Extract instrument type from directory name

# ── Two dates to compare side by side ────────────────────────────────────────
sDate1      = datetime.datetime(2024, 5, 8)
eDate1      = datetime.datetime(2024, 5, 9)
sDate2      = datetime.datetime(2024, 5, 10)
eDate2      = datetime.datetime(2024, 5, 11)

date_pairs  = [(sDate1, eDate1), (sDate2, eDate2)]

# Use the earlier start / later end for file-naming and suptitle fallback
sDate       = sDate1
eDate       = eDate2
num_days    = 1                                 # controls title date format per column

lat         =  41.335116    # W2NAF
lon         = -75.600692    # W2NAF
frequencies = [5.0, 10.0, 15.0]
# ─────────────────────────────────────────────────────────────────────────────

station_dct = {}
sdct        = station_dct[callsign] = {}

if __name__ == '__main__':
    sDate_str  = sDate.strftime('%Y%m%d')
    eDate_str  = eDate.strftime('%Y%m%d')
    output_dir = os.path.join('output', data_source,
                              f'{data_source}_{sDate_str}-{eDate_str}')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    station = callsign

    # Base figure dict (per-column xlim will be set inside the loop)
    figd = {}
    figd['solar_lat']               = lat
    figd['solar_lon']               = lon
    figd['overlaySolarElevation']   = True

    cfreqs      = frequencies
    plot_list   = ['WDgrape']

    # ── Build output filename ─────────────────────────────────────────────────
    png_ = []
    for sd, ed in date_pairs:
        png_.append(sd.strftime('%Y%m%d.%H%M'))
        png_.append(ed.strftime('%Y%m%d.%H%M'))
    png_.append(station)
    for pll in plot_list:
        png_.append(pll)
        if pll == 'WDgrape':
            png_ += ['{!s}'.format(x) for x in cfreqs]

    png_fname = '_'.join(png_) + '.png'
    png_fpath = os.path.join(output_dir, png_fname)

    # ── Grid dimensions ───────────────────────────────────────────────────────
    nrows = len(cfreqs)         # one row per frequency
    ncols = len(date_pairs)     # one column per date

    fig   = plt.figure(figsize=(28 * ncols, nrows * 7))         # increase overall figure size
    letter_fdict     = {'size': 32}
    col_title_fdict  = {'size': 60, 'weight': 'bold'}           # Column title

    axs = []   # stored in row-major order: [row0col0, row0col1, row1col0, ...]

    # ── Grape plots ───────────────────────────────────────────────────────────
    if 'WDgrape' in plot_list:
        for col_inx, (sd, ed) in enumerate(date_pairs):
            print(f'\n=== Date column {col_inx + 1}: {sd.strftime("%Y-%m-%d")} ===')
            gDRF   = grapeDRF.GrapeDRF(sd, ed, data_source)
            g_figd = figd.copy()
            g_figd['xlim'] = (sd, ed)

            for row_inx, cfreq in enumerate(cfreqs):
                print('   {!s} MHz...'.format(cfreq))

                # Matplotlib subplot index is 1-based, row-major
                ax_inx = row_inx * ncols + col_inx + 1
                ax     = fig.add_subplot(nrows, ncols, ax_inx)

                # Store in row-major order so the finalize loop stays simple
                # Extend list on first column pass; replace placeholder on later passes
                if col_inx == 0:
                    axs.append([ax])
                else:
                    axs[row_inx].append(ax)

                gDRF.plot_ax(cfreq, ax, **g_figd)
                ax.yaxis.get_offset_text().set_fontsize(30)
                ax.yaxis.get_offset_text().set_fontweight('bold')
                #yticks = ax.get_yticks()
                #ax.set_yticks(yticks)

                ax.set_ylabel(ax.get_ylabel(), fontsize=40, fontweight='normal')
                ax.set_xlabel(ax.get_xlabel(), fontsize=40, fontweight='normal')

                # Increase solar elevation angle label size
                for twin_ax in ax.figure.axes:
                    if twin_ax != ax and twin_ax.bbox.bounds == ax.bbox.bounds:
                        twin_ax.set_ylabel(twin_ax.get_ylabel(), fontsize=40, fontweight='normal', labelpad=20)

                # Panel letter  (a, b, c …)  — unique across the whole figure
                letter = letters[row_inx * ncols + col_inx]
                ax.set_title('({!s})'.format(letter), loc='left', fontdict=letter_fdict)
                '''
                # Frequency label on the right side of the left column only
                if col_inx == 0:
                    ax.set_title('{!s} MHz Receiver'.format(cfreq), loc='right')
                '''
                ax.set_title('{!s} MHz Receiver'.format(cfreq), loc='right')

                # Date column header on the top row only
                if row_inx == 0:
                    ax.set_title(sd.strftime('%d %b %Y'), fontdict=col_title_fdict)

    # ── Finalize axes (tick labels, x-limits) ─────────────────────────────────
    for row_inx, row_axs in enumerate(axs):
        for col_inx, ax in enumerate(row_axs):
            sd, ed = date_pairs[col_inx]
            ax.set_xlim(sd, ed)

            xticks = ax.get_xticks()
            ax.set_xticks(xticks)

            is_bottom_row = (row_inx == nrows - 1)

            if not is_bottom_row:
                ax.set_xlabel('')
                ax.set_xticklabels(['' for _ in xticks])
            else:
                ax.set_xlabel('UTC', fontsize=40, fontweight='normal', labelpad=20)
                xtkls = [mpl.dates.num2date(xtk).strftime('%H:%M') for xtk in xticks]
                ax.set_xticklabels(xtkls)

    # ── Super-title ───────────────────────────────────────────────────────────
    sdct = station_dct.get(station, {})
    stxt = '{!s} ({!s})'.format(station.upper(), instrument.upper())

    txt = [stxt]
    if 'QTH' in sdct:
        txt.append(sdct['QTH'])
    # Show combined date range in the suptitle
    #txt.append('{} and {}'.format(sDate1.strftime('%d %b %Y'), sDate2.strftime('%d %b %Y')))

    fontdict = {'size': 70, 'weight': 'bold'}
    fig.text(0.5, 1., '\n'.join(txt), fontdict=fontdict, ha='center', va='bottom')

    fig.tight_layout(w_pad=4, h_pad=6)
    fig.savefig(png_fpath, bbox_inches='tight')
    print(png_fpath)
