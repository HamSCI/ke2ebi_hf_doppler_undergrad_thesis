# grapeDRF Doppler Model — Documentation

**Repository:** [Rebecca-FP/grapeDRF_doppler_model](https://github.com/Rebecca-FP/grapeDRF_doppler_model)
**Upstream:** [g3zil/grapeDRF_doppler_model](https://github.com/g3zil/grapeDRF_doppler_model)
**License:** GPL-3.0
**Language:** Python 97.5%, Shell 2.5%

---

## Table of Contents

1. [Overview](#overview)
2. [Background Concepts](#background-concepts)
3. [Installation](#installation)
4. [Repository Structure](#repository-structure)
5. [Configuration Files](#configuration-files)
6. [Module Reference](#module-reference)
   - [Core Library: grapeDRF.py](#core-library-grapedrfpy)
   - [load_metadata.py](#load_metadatapy)
   - [calcSun.py](#calcsunpy)
7. [Script Reference](#script-reference)
   - [Eclipse Plotting](#eclipse-plotting)
   - [Spectrogram and Doppler Analysis](#spectrogram-and-doppler-analysis)
   - [Synthetic Spectrogram Pipeline](#synthetic-spectrogram-pipeline)
   - [Sidescatter Computation](#sidescatter-computation)
   - [Multi-day and Summary Scripts](#multi-day-and-summary-scripts)
8. [Workflow Guides](#workflow-guides)
   - [Quick Start: Eclipse Plot](#quick-start-eclipse-plot)
   - [Analysing a GRAPE Station Recording](#analysing-a-grape-station-recording)
   - [Full Synthetic Spectrogram Pipeline](#full-synthetic-spectrogram-pipeline)
   - [Sidescatter Animation](#sidescatter-animation)
9. [Data Layout](#data-layout)
10. [Output Layout](#output-layout)
11. [Dependencies](#dependencies)
12. [Acknowledgements](#acknowledgements)

---

## Overview

This toolkit processes HF (high-frequency) radio Doppler data recorded by [GRAPE](https://hamsci.org/grape) citizen-science receivers and stored in [DigitalRF](https://github.com/MITHaystack/digital_rf) format. It provides:

- **Doppler spectrogram plotting** from raw IQ data
- **Time-domain Doppler and spread analysis** via complex autocorrelation
- **CWT-based peak identification** for resolving multiple propagation modes
- **Synthetic spectrogram generation** by ray tracing through the ionosphere (requires [PyLap](https://github.com/HamSCI/PyLap))
- **Two-hop sidescatter modelling** using 3D ray tracing
- **Solar context overlays** (solar elevation angle, eclipse fraction)

The software has been tested on Ubuntu Linux 22.04/24.04 and macOS 10.14–15.3 with Python 3.10–3.12.

---

## Background Concepts

**GRAPE / PSWS:** The Personal Space Weather Station is a citizen-science SDR receiver designed by the HamSCI community. It records IQ data from WWV/WWVH and other standard-frequency broadcasts at 2.5, 3.33, 5, 7.85, 10, 14.67, 15, 20, and 25 MHz simultaneously.

**DigitalRF:** A data format and library for storing and accessing baseband radio data as time-indexed HDF5 files. Each "channel" (`ch0_CALLSIGN`) is a directory tree of HDF5 blocks accompanied by metadata.

**Doppler shift:** As the ionosphere changes height (due to sunrise/sunset, solar flares, geomagnetic storms, eclipses), the path length of sky-wave signals changes, producing a measurable frequency shift of a few Hz. The magnitude and sign of the shift reveal ionospheric dynamics.

**PyLap / PHaRLAP:** PyLap is a Python wrapper for the PHaRLAP (Provision of High-Frequency Raytracing Laboratory for Propagation Studies) MATLAB ray-tracing toolbox. It numerically traces HF radio rays through an ionosphere model (typically the International Reference Ionosphere, IRI) to predict propagation modes and Doppler shifts. As of September 2025, PyLap works assuredly with PHaRLAP 4.5.0.

**Propagation modes:** A single HF signal can arrive at a receiver via several distinct ionospheric paths simultaneously (1-hop E layer, 2-hop F layer, etc.). Each mode produces its own trace on a Doppler spectrogram, often offset from the others by several Hz.

---

## Installation

### 1. Clone the repository

```bash
cd ~
git clone https://github.com/g3zil/grapeDRF_doppler_model.git
cd ~/grapeDRF_doppler_model
```

All subsequent commands should be run from this directory.

To pull updates later:

```bash
git pull
```

### 2. Python environment

#### Option A — Open environment (conda or system Python)

Tested with Python 3.10.x on macOS and Ubuntu 22.04.

```bash
python -m pip install -r requirements.txt
```

#### Option B — Externally managed environment (Ubuntu 24.04 / Python 3.12)

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

Remember to activate the virtual environment (`source .venv/bin/activate`) at the start of each session.

### 3. PyLap (optional, for synthetic spectrograms and sidescatter)

Install from [https://github.com/HamSCI/PyLap](https://github.com/HamSCI/PyLap) following its instructions. Note the setup.sh may have issues in a protected environment as of September 2025.

### 4. PostgreSQL (optional, for synthetic spectrogram overlay)

The `grape_fft_spectrogram.py` `DB` option and `synthspec.py` `DB` option write to and read from a local PostgreSQL database named `hamsci`. Contact the upstream author (G3ZIL) for details.

---

## Repository Structure

```
grapeDRF_doppler_model/
├── config/                          # Per-station configuration files
│   ├── N8GA_config.ini
│   ├── W2NAF_config.ini
│   └── heuristics.ini               # Mode-finding heuristics for modefinder.py
├── data/
│   └── psws_grapeDRF/               # DigitalRF data, one subdirectory per station
│       ├── ch0_G4HZX/
│       ├── ch0_N8GA/
│       └── ch0_W2NAF/
├── eclipse_calc/                    # Solar context helper package
├── output/                          # Created at runtime
│   ├── plots/                       # PNG and MP4 outputs, organised by callsign
│   ├── csv/                         # CSV data outputs, organised by callsign
│   └── grapeDRF/                    # Cached pickle files from grapeDRF.py
│
│   ── Core library ──
├── grapeDRF.py                      # GrapeDRF class: data loading & spectrogram plotting
├── load_metadata.py                 # Metadata reader helper module
├── calcSun.py                       # Sun angle / eclipse utilities
│
│   ── Analysis scripts ──
├── grape_digital_RF_metadata.py     # Print metadata for a channel
├── grape_fft_spectrogram.py         # FFT spectrogram plot (+ optional DB overlay)
├── grape_acf_doppler_spread.py      # ACF-based Doppler shift and spread time series
├── grape_fft_CWT_single_plot.py     # Single-interval spectrum with CWT peak fitting
├── grape_fft_CWT_tracking_prophet.py# Experimental multi-mode Doppler tracker
│
│   ── Eclipse / event scripts ──
├── plot_w2naf_grapeDRF_2024eclipse.py  # Reproduce 2024 eclipse plot
├── Gannon_storm_stackplot.py        # May 2024 geomagnetic storm stack plot
├── Gannon_storm_SYM-H_plot.py       # SYM-H index plot for Gannon storm
├── psws_spectrogram_with_colorbar.py
│
│   ── Multi-day summary scripts ──
├── 15MHz_average_quiet_day_doppler.py
├── 15MHz_multiday_summary.py
├── multi_day_colorbar.py
├── quiet_day_stack.py
├── analyze_extracted_dop_shift.py
├── analyze_extracted_signal_to_noise.py
│
│   ── Synthetic spectrogram pipeline ──
├── pathfinder.py                    # Step 1: 2D ray tracing at a single time
├── pathfinder.sh                    # Step 1 (batch): run pathfinder over time series
├── modefinder.py                    # Step 2: assign propagation modes to rays
├── synthspec.py                     # Step 3: compute synthetic Doppler, optional DB upload
│   (grape_fft_spectrogram.py DB)    # Step 4: overlay as-received + synthetic spectrogram
│
│   ── Sidescatter pipeline ──
├── SS_sidescatter.py                # 3D ray tracing for sidescatter
├── SS_sidescatter_plot.py           # Plot ray landing spots and metric
├── SS_animate.sh                    # Animate over time
│
│   ── Mapping ──
├── map_psws.py                      # Map PSWS receiver locations
├── coords_sheet.txt                 # Station coordinate reference sheet
│
├── requirements.txt
├── LICENSE
└── README.md
```

---

## Configuration Files

### Per-station `config.ini`

Located in `config/<CALLSIGN>_config.ini`. Used by `pathfinder.py`, `modefinder.py`, `synthspec.py`, `SS_sidescatter.py`, and `SS_sidescatter_plot.py`.

**Example — WWV Fort Collins, CO → N8GA, Ohio:**

```ini
[settings]
ut = [2024,7,26,0,0]     ; Start UTC as [year,month,day,hour,minute]
r12 = 120                 ; 12-month smoothed sunspot number
freq = 10                 ; Transmit frequency in MHz
tx_grid = DN70LQ          ; Transmitter Maidenhead grid square
rx_grid = EN80EE          ; Receiver Maidenhead grid square
nhops = 2                 ; Maximum number of hops to trace
elev_start = 2            ; Minimum elevation angle (degrees)
elev_stop = 45            ; Maximum elevation angle (degrees)

[metadata]
tx = WWV                  ; Transmitter identifier
rx = N8GA                 ; Receiver callsign

[plots]
legend = upper right      ; Legend location (matplotlib string)
u_dopp_lim = 3            ; Upper Doppler axis limit (Hz)
l_dopp_lim = -3           ; Lower Doppler axis limit (Hz)

[3d_sidescatter]          ; Used only by SS_sidescatter.py
ray_inc = 3               ; Azimuth increment in degrees (3° suits 8 GB RAM)
metric_max_lat = 0        ; Set automatically by SS_sidescatter.py on first run
metric_max_lon = 0
max_metric = 0
```

The `distance`, `bearing`, `metric_max_lat`, `metric_max_lon`, and `max_metric` fields in `[settings]` and `[3d_sidescatter]` are populated automatically by the scripts; leave them at `0` initially.

### `config/heuristics.ini`

Controls mode classification in `modefinder.py`. Heights in km, elevations in degrees.

```ini
[propagation]
min_apogee_E = 85          ; Minimum apogee height for E-layer rays (km)
max_apogee_E = 150         ; Maximum apogee height for E-layer rays (km)
min_apogee_F = 151         ; Minimum apogee height for F-layer rays (km)
min_hdashF-hF = 45         ; Min virtual-height difference distinguishing lo/hi F rays (km)
max_hdashF-hF = 85         ; Max virtual-height difference for same (km)
elev_diff_lo_hi = 0.5      ; Minimum elevation separation between lo and hi ray (degrees)
sep_EloEhi = 5             ; Minimum elevation separation between E lo and hi ray (degrees)
```

---

## Module Reference

### Core Library: `grapeDRF.py`

Provides the `GrapeDRF` class and the `load_grape_drf()` helper for reading DigitalRF GRAPE data and rendering multi-frequency Doppler spectrograms.

#### `load_grape_drf(sDate, eDate, data_dir, channel='ch0')`

Reads a block of raw IQ data from a DigitalRF store and returns a dictionary.

| Parameter | Type | Description |
|-----------|------|-------------|
| `sDate` | `datetime` | Start time (UTC) |
| `eDate` | `datetime` | End time (UTC) |
| `data_dir` | `str` | Path to the DigitalRF data directory |
| `channel` | `str` | Channel name, default `'ch0'` |

**Returns** `dict` with keys:
- `bigarray_dct` — dict mapping centre frequency (MHz) → complex numpy array of IQ samples
- `latest_meta` — metadata dict (centre frequencies, lat, lon, callsign, grid square, etc.)
- `properties` — DigitalRF channel properties (includes `samples_per_second`)
- `timevec_utc` — list of `datetime` objects, one per sample

**Notes:** Results are cached to `output/grapeDRF/<event>.ba.pkl`; subsequent calls with the same arguments use the cache.

#### `class GrapeDRF`

High-level wrapper around `load_grape_drf()` that manages caching and provides plotting methods.

```python
gDRF = GrapeDRF(sDate, eDate, station, output_dir='output/grapeDRF')
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `sDate` | `datetime` | Start time (UTC) |
| `eDate` | `datetime` | End time (UTC) |
| `station` | `str` | Station subdirectory name, e.g. `'w2naf'` |
| `output_dir` | `str` | Directory for cached pickle and output PNG |

**`GrapeDRF.plot_figure(cfreqs=None, png_fpath=None, **kwargs)`**

Renders one subplot per frequency and saves to PNG.

| Parameter | Type | Description |
|-----------|------|-------------|
| `cfreqs` | list of float | Centre frequencies to plot; defaults to all |
| `png_fpath` | `str` | Output path override |
| `**kwargs` | | Passed to `plot_ax()` |

**`GrapeDRF.plot_ax(cfreq, ax, ...)`**

Renders a single frequency panel onto a Matplotlib axes object. Optional overlays:

| Keyword | Default | Description |
|---------|---------|-------------|
| `solar_lat` | `None` | Latitude for solar elevation overlay |
| `solar_lon` | `None` | Longitude for solar elevation overlay |
| `overlaySolarElevation` | `True` | White line showing solar elevation |
| `overlayEclipse` | `False` | White line showing eclipse fraction |
| `cmap` | black→green→yellow→red | Colourmap for PSD |
| `plot_colorbar` | `False` | Add a PSD colorbar |
| `xlim` | `(sDate, eDate)` | Time axis limits |

The spectrogram uses `scipy.signal.spectrogram` with a 1024-point Hann window. Power is expressed in dB.

---

### `load_metadata.py`

Helper module (not a standalone script). Exports:

**`load_grape_drf_metadata(data_dir, channel)`**

Reads the DigitalRF metadata directory and returns a tuple:

```
(date, freqList, s1, s0, fs, theCallsign, grid, lat, lon)
```

| Return value | Description |
|---|---|
| `date` | Date string in `YYYY-MM-DD` format |
| `freqList` | numpy array of centre frequencies (MHz) |
| `s1`, `s0` | Last and first sample indices |
| `fs` | Sample rate (samples/second) |
| `theCallsign` | Station callsign extracted from metadata |
| `grid` | Maidenhead grid square |
| `lat`, `lon` | Receiver latitude and longitude |

---

### `calcSun.py`

Provides solar geometry utilities used by `grapeDRF.py` via the `eclipse_calc` package. Exports a `solarContext.solarTimeseries` class that computes solar elevation and eclipse fraction over a time interval and overlays them on a Matplotlib axes object.

---

## Script Reference

### Eclipse Plotting

#### `plot_w2naf_grapeDRF_2024eclipse.py`

Reproduces a four-frequency Doppler spectrogram from the April 8, 2024 total solar eclipse as seen at W2NAF, Scranton, PA.

**Usage:**

```bash
python plot_w2naf_grapeDRF_2024eclipse.py
```

**Output:** `output/w2naf_2024eclipse/20240408.0000_20240409.0000_w2naf_WDgrape_20_15_10_5.png`

No command-line arguments. Frequencies plotted: 20, 15, 10, 5 MHz. Solar elevation and eclipse fraction are overlaid in white.

---

### Spectrogram and Doppler Analysis

#### `grape_digital_RF_metadata.py`

Prints the metadata for a DigitalRF channel: available centre frequencies, sample rate, date range, callsign, grid square, and location.

**Usage:**

```bash
python3 grape_digital_RF_metadata.py <channel>
```

**Example:**

```bash
python3 grape_digital_RF_metadata.py ch0_G4HZX
```

Use this to discover the frequency index needed by the other scripts.

---

#### `grape_fft_spectrogram.py`

Plots a Doppler spectrogram for a selected frequency and time window from a GRAPE DigitalRF recording. Optionally overlays a synthetic spectrogram from a PostgreSQL database.

**Usage:**

```bash
python3 grape_fft_spectrogram.py <channel> <freq_index> <start_hour> <stop_hour> [DB]
```

| Argument | Type | Description |
|----------|------|-------------|
| `channel` | str | DigitalRF channel directory, e.g. `ch0_G4HZX` |
| `freq_index` | int | Index into the frequency list (from metadata) |
| `start_hour` | int | Start time in decimal hours UTC (0–23) |
| `stop_hour` | int | Stop time; must be ≥ `start_hour + 1` |
| `DB` | optional flag | If present, overlays synthetic spectrogram from PostgreSQL |

**Examples:**

```bash
# 15 MHz, 08:00–13:00 UTC, as-received only
python3 grape_fft_spectrogram.py ch0_G4HZX 6 8 13

# 10 MHz, full day, with synthetic overlay
python3 grape_fft_spectrogram.py ch0_W2NAF 7 0 24 DB
```

**Processing details:**

Each 60-second window of IQ data is Fourier-transformed with a Hann window (1024-point FFT with a 1.63 energy correction factor). Spectrogram power is plotted in dB using a grey contour map. The Doppler axis limits are read from the station's `config.ini`.

**Output:** `output/plots/<callsign>/Spectrogram_<freq>MHz_<date>.png`
With DB: `output/plots/<callsign>/Spectrogram+Synth_<freq>MHz_<date>.png`

Modes in the synthetic overlay are colour-coded:

| Colour | Mode |
|--------|------|
| Firebrick | 1F (1-hop F-layer, low ray) |
| Blue | 2F (2-hop F-layer, low ray) |
| Green | 1E (1-hop E-layer, low ray) |
| Purple | 2E (2-hop E-layer, low ray) |
| Red | 1F high ray |
| Cyan | 2F high ray |
| Lime | 1E high ray |
| Orchid | 2E high ray |

---

#### `grape_acf_doppler_spread.py`

Computes time series of signal+noise (S+N) level, Doppler shift, and Doppler spread using complex autocorrelation. Best suited to intervals where the spectrum is unimodal (single propagation mode). Results at times of multimode propagation should be treated with caution.

**Usage:**

```bash
python3 grape_acf_doppler_spread.py <channel> <freq_index> <start_hour> <stop_hour>
```

**Example:**

```bash
python3 grape_acf_doppler_spread.py ch0_G4HZX 6 8 14
```

**Output:** PNG in `output/plots/<callsign>/`

---

#### `grape_fft_CWT_single_plot.py`

Computes the spectrum for a single one-minute interval and fits Ricker (Mexican-hat) wavelets using the Continuous Wavelet Transform (CWT) to identify up to N peaks.

**Usage:**

```bash
python3 grape_fft_CWT_single_plot.py <channel> <freq_index> <time_decimal_hours> <N_peaks>
```

| Argument | Description |
|----------|-------------|
| `channel` | DigitalRF channel |
| `freq_index` | Frequency index from metadata |
| `time_decimal_hours` | Time of the spectrum in decimal hours (e.g. `14.5` = 14:30 UTC) |
| `N_peaks` | Number of peaks to identify |

**Example:**

```bash
# Find 2 peaks at 14:30 UTC on the 15 MHz channel
python3 grape_fft_CWT_single_plot.py ch0_W2NAF 8 14.5 2
```

**Output:** PNG in `output/plots/<callsign>/`

---

#### `grape_fft_CWT_tracking_prophet.py`

Experimental script. Identifies two Doppler spectral peaks per time interval using CWT and attempts to track which peak belongs to which propagation mode over time. A small hand-labelled training set seeds a time-series forecasting model (Facebook Prophet) which predicts the next value; the closest observed peak is then assigned to that mode.

**Usage:**

```bash
python3 grape_fft_CWT_tracking_prophet.py <channel> <freq_index> <start_decimal_hours> <duration_minutes>
```

**Example:**

```bash
python3 grape_fft_CWT_tracking_prophet.py ch0_W2NAF 8 14.4 80
```

**Note:** This script is under active development and may fail with data-dependent errors.

**Output:** Two PNG plots in `output/plots/<callsign>/` — raw traces and mode-assigned traces.

---

### Synthetic Spectrogram Pipeline

This four-step pipeline requires PyLap. All scripts use the same `config.ini` file and the same start-datetime format (`YYmmddHHMM`).

#### Step 1a — `pathfinder.py`

Traces 2D (great-circle) rays from the transmitter over a sweep of elevation angles (0.005° increments) to find all rays that land within a few km of the receiver.

**Usage:**

```bash
python3 pathfinder.py <config_file> <YYmmddHHMM>
```

**Example:**

```bash
python3 pathfinder.py ./config/N8GA_config.ini 202407260000
```

**Output CSV columns:**

| Column | Description |
|--------|-------------|
| Date | UTC timestamp |
| Hops | Number of ionospheric hops |
| Init_elev | Initial elevation angle (degrees) |
| one_hop_virt_ht | Virtual height of first hop (km) |
| one_hop_apogee | Apogee of first hop (km) |
| 2nd hop apogee | Apogee of second hop, if applicable (km) |
| gnd_range | Ground range (km) |
| phase_path | Phase path length (km) |
| geo_path | Geometric path length (km) |
| pylap_doppler | PyLap's own Doppler estimate (Hz) — may be unreliable as of Sept 2025 |

**Output:** CSV in `output/csv/<callsign>/`

---

#### Step 1b — `pathfinder.sh`

Runs `pathfinder.py` repeatedly at 5-minute intervals over a specified total duration.

**Usage:**

```bash
./pathfinder.sh <config_file_name> <duration_minutes>
```

**Example — 30 minutes of data (6 time steps):**

```bash
./pathfinder.sh N8GA_config.ini 30
```

**Constraint:** The start time in `config.ini` plus the duration must not cross 00:00 UTC (i.e., the interval must stay within a single calendar day).

---

#### Step 2 — `modefinder.py`

Reads the CSV output from `pathfinder.py` and classifies each ray into one of eight propagation modes using configurable heuristics from `config/heuristics.ini`.

**Modes classified:**

| Code | Description |
|------|-------------|
| 1E | 1-hop E-layer, low ray |
| 1Ehi | 1-hop E-layer, high ray |
| 2E | 2-hop E-layer, low ray |
| 2Ehi | 2-hop E-layer, high ray |
| 1F | 1-hop F-layer, low ray |
| 1Fhi | 1-hop F-layer, high ray (may include Pedersen/ducted rays) |
| 2F | 2-hop F-layer, low ray |
| 2Fhi | 2-hop F-layer, high ray |

**Usage:**

```bash
python3 modefinder.py <callsign> <YYmmddHHMM>
```

**Example:**

```bash
python3 modefinder.py N8GA 202407260000
```

**Output:** Colour-coded CSV and a scatter plot of initial elevation vs time in `output/plots/<callsign>/` and `output/csv/<callsign>/`.

---

#### Step 3 — `synthspec.py`

Reads the mode-classified CSV from `modefinder.py` and computes the synthetic Doppler shift for each mode as the finite difference of phase path between successive 5-minute intervals. A correction is applied for jitter in the ray landing distance to smooth the estimates.

**Usage:**

```bash
python3 synthspec.py <callsign> <YYmmddHHMM> [DB]
```

**Example:**

```bash
python3 synthspec.py N8GA 202407260000
```

Add `DB` to upload results to the local PostgreSQL database (required for Step 4 overlay).

**Output:** CSV and plots of synthetic Doppler shift and propagation delay by mode in `output/csv/<callsign>/` and `output/plots/<callsign>/`.

---

#### Step 4 — Overlay (via `grape_fft_spectrogram.py DB`)

Once `synthspec.py DB` has populated the database, run the spectrogram script with the `DB` flag to overlay both datasets:

```bash
python3 grape_fft_spectrogram.py ch0_W2NAF 7 0 24 DB
```

---

### Sidescatter Computation

Two-hop sidescatter uses 3D PyLap ray tracing. A pseudo-transmitter is placed at the receiver position, and rays are traced in 360° azimuth. The product of transmitter and pseudo-transmitter ray landing densities in 1°×1° geographic boxes is used as a "sidescatter likelihood metric". 

**Current limitations:** Northern Hemisphere only; northernmost station must be below 58°N.

---

#### `SS_sidescatter.py`

Traces 3D rays in all azimuths from both the transmitter and the receiver (pseudo-transmitter) at a single time and writes landing coordinates to CSV.

**Usage:**

```bash
python3 SS_sidescatter.py <config_file> <YYmmddHHMM>
```

**Example:**

```bash
python3 SS_sidescatter.py ./config/W2NAF_config.ini 202407270000
```

**Output CSV fields:** `source` (0=TX, 1=pseudo-TX), `bearing` (°), `rayId`, `init_elev` (°), `apogee` (km), `pylap_doppler` (Hz), `landing_lat` (°), `landing_lon` (°).

**Output:** `output/csv/SS/<callsign>/<timestamp>_ground_coords.csv`

---

#### `SS_sidescatter_plot.py`

Reads the landing-coordinate CSV and computes/plots the sidescatter likelihood metric.

**Usage:**

```bash
python3 SS_sidescatter_plot.py <config_file> <YYmmddHHMM> <frame_number>
```

**Example:**

```bash
python3 SS_sidescatter_plot.py ./config/W2NAF_config.ini 202409270000 0
```

`frame_number` is a 0-padded 3-digit integer (max 999) used to name animation frames; use `0` for standalone use.

**Output:** Two PNGs in `output/plots/SS/<callsign>/`: `sidescatter.png` (ray landing map) and `2F_sidescatter_metric_<NNN>.png` (contour map).

---

#### `SS_animate.sh`

Automates a sequence of `SS_sidescatter.py` → `SS_sidescatter_plot.py` calls and stitches the frames into an MP4 animation using `ffmpeg`.

**Usage:**

```bash
./SS_animate.sh <config_file_name> <total_duration_minutes> <frame_interval_minutes>
```

**Example — 18 frames over 6 hours at 20-minute intervals:**

```bash
./SS_animate.sh W2NAF_config.ini 360 20
```

**Notes:** Each frame can take several minutes to compute (approximately 4 minutes on a 4-core i5). ffmpeg may insert or drop frames depending on total frame count. Output files are in `output/plots/SS/<callsign>/`.

---

### Multi-day and Summary Scripts

These scripts analyse extracted Doppler data across multiple days and are primarily designed for 15 MHz observations.

| Script | Purpose |
|--------|---------|
| `15MHz_average_quiet_day_doppler.py` | Computes and plots an average quiet-day Doppler profile at 15 MHz |
| `15MHz_multiday_summary.py` | Multi-day summary plot at 15 MHz |
| `quiet_day_stack.py` | Stack plot of quiet-day data |
| `multi_day_colorbar.py` | Shared colorbar for multi-day plots |
| `analyze_extracted_dop_shift.py` | Statistical analysis of extracted Doppler shift data |
| `analyze_extracted_signal_to_noise.py` | Statistical analysis of extracted S/N data |
| `Gannon_storm_stackplot.py` | Stack plot for the May 2024 Gannon geomagnetic storm |
| `Gannon_storm_SYM-H_plot.py` | SYM-H geomagnetic index plot for the Gannon storm |
| `psws_spectrogram_with_colorbar.py` | Spectrogram with shared colorbar |
| `map_psws.py` | Map plot of PSWS station locations |

---

## Workflow Guides

### Quick Start: Eclipse Plot

This requires only the bundled W2NAF data and no additional setup beyond `requirements.txt`.

```bash
python plot_w2naf_grapeDRF_2024eclipse.py
```

The output PNG appears in `output/w2naf_2024eclipse/`.

---

### Analysing a GRAPE Station Recording

**1. Discover available frequencies and data range:**

```bash
python3 grape_digital_RF_metadata.py ch0_G4HZX
```

Note the index of the frequency you want to analyse (e.g. index 6 = 15 MHz for G4HZX).

**2. Plot a spectrogram:**

```bash
python3 grape_fft_spectrogram.py ch0_G4HZX 6 8 13
```

**3. Extract Doppler shift and spread as time series:**

```bash
python3 grape_acf_doppler_spread.py ch0_G4HZX 6 8 14
```

**4. Identify modes in a specific interval:**

```bash
python3 grape_fft_CWT_single_plot.py ch0_W2NAF 8 14.5 2
```

---

### Full Synthetic Spectrogram Pipeline

Requires PyLap and a local PostgreSQL database.

**1. Create a config file** for your transmitter–receiver pair in `config/CALLSIGN_config.ini` (see [Configuration Files](#configuration-files)).

**2. Run ray tracing over the desired time window:**

```bash
./pathfinder.sh N8GA_config.ini 120    # 2 hours, 5-minute steps
```

**3. Classify propagation modes:**

```bash
python3 modefinder.py N8GA 202407260000
```

**4. Compute synthetic Doppler and upload to database:**

```bash
python3 synthspec.py N8GA 202407260000 DB
```

**5. Plot as-received spectrogram with synthetic overlay:**

```bash
python3 grape_fft_spectrogram.py ch0_N8GA 4 0 2 DB
```

---

### Sidescatter Animation

Requires PyLap and `ffmpeg`.

```bash
# 6-hour animation, frame every 20 minutes
./SS_animate.sh W2NAF_config.ini 360 20
```

Allow several hours of compute time. The MP4 is saved to `output/plots/SS/W2NAF/`.

---

## Data Layout

GRAPE DigitalRF data is stored under `data/psws_grapeDRF/` with one subdirectory per station:

```
data/psws_grapeDRF/
└── ch0_<CALLSIGN>/
    ├── <HDF5 data blocks>
    └── metadata/
        └── <HDF5 metadata blocks>
```

Metadata fields include `center_frequencies`, `lat`, `long`, and callsign/grid information. All scripts derive the station callsign and coordinates from the metadata automatically.

Example workflows in this repository reference the following station recordings (not bundled — obtain from the HamSCI PSWS data portal):

| Channel | Station | Event |
|---------|---------|-------|
| `ch0_G4HZX` | G4HZX (UK) | 29 March 2025 partial eclipse |
| `ch0_N8GA` | N8GA (Ohio) | 26 July 2024 |
| `ch0_W2NAF` | W2NAF (Scranton, PA) | 8 April 2024 solar eclipse |

---

## Output Layout

All outputs are written to `output/` (created automatically):

```
output/
├── plots/
│   ├── <CALLSIGN>/          # Spectrograms, ACF plots, CWT plots
│   └── SS/
│       └── <CALLSIGN>/      # Sidescatter maps, metric contour plots, MP4
├── csv/
│   ├── <CALLSIGN>/          # Ray trace CSV, mode CSV, synthetic Doppler CSV
│   └── SS/
│       └── <CALLSIGN>/      # 3D ray landing coordinate CSV
├── grapeDRF/                # Cached pickle files from GrapeDRF class
└── w2naf_2024eclipse/       # Eclipse plot output
```

---

## Dependencies

All core dependencies are installed via `requirements.txt`. The optional database dependency (`psycopg2`) is included but only needed for the `DB` overlay feature.

| Package | Purpose |
|---------|---------|
| `digital_rf` | Read DigitalRF IQ data and metadata |
| `numpy` | Numerical arrays |
| `scipy` | FFT, spectrogram, CWT, signal processing |
| `matplotlib` | Plotting |
| `Cartopy` | Map projections (sidescatter maps) |
| `astropy` | Astronomical calculations |
| `maidenhead` | Maidenhead grid square ↔ lat/lon conversion |
| `geographiclib` | Geodesic calculations |
| `netCDF4` | IRI ionosphere model data |
| `configparser` | INI configuration file parsing |
| `pandas` | Data manipulation (multi-day scripts) |
| `prophet` | Time-series forecasting (CWT tracker) |
| `pytz` | Timezone-aware datetimes |
| `python_dateutil` | Date arithmetic |
| `tqdm` | Progress bars |
| `ipdb` | Interactive debugging |
| `psycopg2` | PostgreSQL connector (optional, for DB overlay) |
| `PyLap` | HF ray tracing (optional, synthetic spectrogram and sidescatter; install separately) |
| `ffmpeg` | Animation encoding (optional, for SS_animate.sh; install via system package manager) |

**Python version:** 3.10–3.12 tested. **Platform:** Ubuntu Linux 22.04/24.04 and macOS 10.14–15.3.

---

## Acknowledgements

This software is a collaborative effort. The upstream development is led by Gwyn Griffiths (G3ZIL). Rebecca-FP developed this fork as part of her thesis at the University of Scranton.

Thesis advisor: Dr. Nathaniel Frissell (W2NAF).
Committee members: Dr. Juan Serna, Dr. Declan Mulhall.
Collaborators: Gwyn Griffiths, Dr. Kuldeep Pandey, Dr. Sarah Over, Dr. Mary Lou West, Gary Mitkin, Dr. Rob Suggs, Dr. Jay Weitzen.

Funding: NSF Grants AGS-2045755, AGS-2432821, AGS-2432822, AGS-2432824, AGS-2432823, OPP-2332427; NASA Grants 80NSSC23K1322, 80NSSC25K7026.
