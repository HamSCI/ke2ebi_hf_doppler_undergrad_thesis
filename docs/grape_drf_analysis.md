# GRAPE DigitalRF Doppler plotting and analysis (G3ZIL)

These general-purpose tools for reading and analysing GRAPE / PSWS HF Doppler recordings in
[Digital RF](https://github.com/MITHaystack/digital_rf) format were developed by Gwyn Griffiths
(G3ZIL). They are not specific to the thesis, but the thesis uses
`grape_acf_doppler_spread.py` to produce the per-day reduced Doppler / signal-to-noise figures
(see [../FIGURES.md](../FIGURES.md)). For the thesis workflow as a whole, see the
[top-level README](../README.md).

## Data layout

The examples below assume one-day Grape DigitalRF data files in directories
`./data/psws_grapeDRF/ch0_*` where `*` is a PSWS reporting station callsign. Multi-day stations are
stored as one directory per day with a date suffix (for example `ch0_W2NAF_2024-04-08`); single-day
stations omit the suffix (for example `ch0_G4HZX`, `ch0_N8GA`). This repository does not bundle the
raw data; obtain station recordings from the HamSCI PSWS data portal (or the companion Zenodo
dataset linked from the README) and place them under `data/psws_grapeDRF/` to reproduce the example
commands. Example channel names referenced below: `ch0_G4HZX`, `ch0_N8GA`, `ch0_W2NAF_2024-04-08`.

Plots are written to `./output/plots/<callsign>/` and CSV data files to `./output/csv/<callsign>/`.

## Listing metadata

To list the available metadata for a station the data channel name is the single command line
argument, run:
```
python3 grape_digital_RF_metadata.py ch0_G4HZX
```

## Plotting a simple spectrogram

The script requires four command line arguments: channel name, frequency index (from the metadata),
and start and end times in hours UTC. For example, with frequency index 6 for 15 MHz between 8 and
13 UTC, run:
```
python3 grape_fft_spectrogram.py ch0_G4HZX 6 8 13
```
An optional fifth command line argument `DB` produces a second plot combining the as-received
spectrogram with a synthetic spectrogram derived from ray tracing — see
[Part 4 of the synthetic spectrograms doc](synthetic_spectrograms.md#part-4-overlaying-as-received-and-synthetic-spectrograms).

## Time domain Doppler analysis using complex autocorrelation

The script plots time series of signal+noise (S+N) level, Doppler shift and frequency spread. The
Doppler shift and spread estimates are only applicable where the spectrum is unimodal. The same four
command line arguments are required, run:
```
python3 grape_acf_doppler_spread.py ch0_G4HZX 6 8 14
```
This is the script the thesis uses for the per-day 15 MHz reduced Doppler / S+N figures; see
[../FIGURES.md](../FIGURES.md) for the exact thesis commands.

## Plot single interval spectrum, identifying N peaks

The script calculates a spectrum and fits Ricker wavelets with a Continuous Wavelet Transform (CWT)
to identify peaks. The four command line arguments are channel name, frequency index, time of the
spectrum in decimal hours, and N, the number of peaks to find, run:
```
python3 grape_fft_CWT_single_plot.py ch0_W2NAF_2024-04-08 8 14.5 2
```

## Experimental multiple Doppler tracking

This script is under development and may fail with data-dependent errors. Two (July 2025) Doppler
spectrum peaks in each time interval are identified from CWT fits. A small training set, where each
peak is correctly assigned to one of the N propagation modes, is used with a forecasting tool to
predict the next value for set A. Whichever data value is closest to the prediction in the next
interval is assigned to set A et seq. The script needs four command line arguments: channel name,
frequency index, time of the spectrum in decimal hours, and duration in minutes:
```
python3 grape_fft_CWT_tracking_prophet.py ch0_W2NAF_2024-04-08 8 14.4 80
```
Here are the example plots, first the raw data and second the assigned-to-mode:

![Figure 9 traces raw and tracked](https://github.com/user-attachments/assets/ae258af9-0bc6-40ac-8c47-98eaaf18a03b)
