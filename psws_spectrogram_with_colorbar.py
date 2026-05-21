# Plot PSWS spectrograms with color bars

#!/bin/env python

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

mpl.rcParams['xtick.labelsize'] = 30   # x-axis tick labels
mpl.rcParams['ytick.labelsize'] = 30   # y-axis tick labels
mpl.rcParams['axes.labelsize']  = 40   # x and y axis titles (e.g. 'UTC')


data_source = 'w2naf_rx888'                     # Data directory {callsign}_{instrument}
callsign    = data_source.split('_')[0]         # Extract callsign from directory name
instrument  = data_source.split('_')[1]         # Extract instrument type from directory name
sDate       = datetime.datetime(2024,5,8)       # Specify start date
eDate       = datetime.datetime(2024,5,9)       # Specify end date
num_days    = 1                                 # Specify number of days to be plotted
lat         =  41.335116 # W2NAF                # latitude coordinate
lon         =  -75.600692 # W2NAF               # longitude coordinate
frequencies = [5.0,10.0,15.0]                   # frequencies to be plotted


station_dct = {}
sdct        = station_dct[callsign] = {}

if __name__ == '__main__':
    sDate_str = sDate.strftime('%Y%m%d')
    eDate_str = eDate.strftime('%Y%m%d')
    output_dir = os.path.join('output', data_source, f'{data_source}_{sDate_str}-{eDate_str}')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    station     = callsign                        
    figd = {}
    figd['solar_lat']               = lat
    figd['solar_lon']               = lon
    figd['overlaySolarElevation']   = True
    figd['xlim']                    = (sDate,eDate)

    # 'center_frequencies': array([ 2.5 ,  3.33,  5.  ,  7.85, 10.  , 14.67, 15.  , 20.  , 25.  ])
    cfreqs          = frequencies
    plot_list   = []
    plot_list.append('WDgrape')

    str_sDate   = sDate.strftime('%Y%m%d.%H%M')
    str_eDate   = eDate.strftime('%Y%m%d.%H%M')
    png_ = []
    png_.append(str_sDate)
    png_.append(str_eDate)
    png_.append(station)
    for pll in plot_list:
        png_.append(pll)
        if pll == 'WDgrape':
            png_ = png_ +  ['{!s}'.format(x) for x in cfreqs]

    png_fname   = '_'.join(png_)+'.png'
    png_fpath   = os.path.join(output_dir,png_fname)


    nrows       = len(plot_list)
    if 'WDgrape' in plot_list:
        nrows += len(cfreqs) - 1
    ncols       = 1
    ax_inx      = 0
    axs         = []

    fig         = plt.figure(figsize=(22,nrows*5))
    letter_fdict = {'size':32}
    # Grape Plots ##########################
    if 'WDgrape' in plot_list:
        gDRF                        = grapeDRF.GrapeDRF(sDate,eDate,data_source)
        g_figd                      = figd.copy()
        for cfreq in cfreqs:
            print('   {!s} MHz...'.format(cfreq))
            ax_inx      += 1
            ax          = fig.add_subplot(nrows,ncols,ax_inx)
            axs.append(ax)
            gDRF.plot_ax(cfreq,ax,**g_figd)
            ax.set_title('({!s})'.format(letters[ax_inx-1]),loc='left',fontdict=letter_fdict)
            ax.set_title('{!s} MHz Receiver'.format(cfreq))

    # Finalize Figure ######################
    for ax_inx,ax in enumerate(axs):
        ax.set_xlim(sDate,eDate)
        ax.set_ylabel('')
        for twin_ax in ax.get_shared_x_axes().get_siblings(ax):
            if twin_ax is not ax:
                twin_ax.set_ylabel('')
        xticks  = ax.get_xticks()
        ax.set_xticks(xticks)
        if ax_inx != len(axs)-1:
            ax.set_xlabel('')
            xtkls = ['']*len(xticks)
        else:
            ax.set_xlabel('UTC', labelpad=15)
            ax.tick_params(axis='x', pad=15)  # increase to move timestamps down
            xtkls   = []
            for xtk in xticks:
                dt      = mpl.dates.num2date(xtk)
                xtkl    = dt.strftime('%H:%M')
                xtkls.append(xtkl)
        ax.set_xticklabels(xtkls)

    sdct    = station_dct.get(station,{})
    stxt = '{!s} ({!s})'.format(station.upper(),instrument.upper())

    txt = []
    txt.append(stxt)
    if 'QTH' in sdct:
        txt.append(sdct['QTH'])
    if num_days == 1:
        txt.append(sDate.strftime('%d %b %Y'))
    else:
        txt.append('{} - {}'.format(sDate.strftime('%d %b %Y'), eDate.strftime('%d %b %Y')))
    fontdict    = {'size':50,'weight':'bold'}  #title size?
    fig.text(0.5,1.,'\n'.join(txt),fontdict=fontdict,ha='center',va='bottom')

    # Single shared y-labels
    fig.supylabel('Doppler Shift (Hz)', fontsize=40, x=0.065)
    fig.tight_layout(rect=[0.05, 0, 0.88, 1])          # leave room for label + colorbar

    # Shared colorbar on the right side
    mappable = None
    for ax in axs:
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
        cbar.set_label('Relative Signal Strength (dB)', fontsize=40, labelpad=40, rotation=270)
        cbar.ax.tick_params(labelsize=30)

    fig.savefig(png_fpath, bbox_inches='tight')
    print(png_fpath)