# Testing notes

This document records the verification performed before the Zenodo release. All scripts were
exercised from the repository root against the accompanying dataset (archived separately on
Zenodo — see the README "How to cite" section for the data DOI).

## Test environment

- macOS (darwin), conda environment with Python 3.11.13.
- Dependencies installed from `requirements.txt` (`digital_rf`, `matplotlib`, `pandas`, `scipy`,
  `astropy`, `cartopy`, `geographiclib`, `maidenhead`, `prophet`, ...).
- Matplotlib run with the non-interactive `Agg` backend (`MPLBACKEND=Agg`) for headless plotting.
- PyLap / PHaRLAP were **not** installed, so the ray-tracing scripts were syntax/​import-checked
  only (see below).

## Results

### Run end-to-end against real data — PASS

| Script | Example command | Output |
| --- | --- | --- |
| `grape_digital_RF_metadata.py` | `… ch0_G4HZX` | metadata printed |
| `grape_fft_spectrogram.py` | `… ch0_G4HZX 6 8 13` | spectrogram PNG |
| `grape_acf_doppler_spread.py` | `… ch0_G4HZX 6 8 14` | ACF level/Doppler PNG + CSV |
| `grape_fft_CWT_single_plot.py` | `… ch0_W2NAF_2024-04-08 8 14.5 2` | CWT spectrum PNG |
| `grape_fft_CWT_tracking_prophet.py` | `… ch0_W2NAF_2024-04-08 8 14.4 80` | tracking PNG (experimental) |
| `Gannon_storm_SYM-H_plot.py` | `…` | SYM-H PNG |
| `Gannon_storm_stackplot.py` | `…` | multi-day stackplot PNG |
| `15MHz_average_quiet_day_doppler.py` | `…` | quiet-day Doppler PNG |
| `quiet_day_stack.py` | `…` | quiet-day stack PNG |
| `multi_day_colorbar.py` | `…` | multi-day spectrogram PNG |
| `psws_spectrogram_with_colorbar.py` | `…` | spectrogram PNG |
| `map_psws.py` | `…` | station map PNG |

### Multi-day Doppler summary pipeline — PASS (requires upstream step)

`15MHz_multiday_summary.py`, `analyze_extracted_dop_shift.py` and
`analyze_extracted_signal_to_noise.py` read per-day ACF CSVs produced by
`grape_acf_doppler_spread.py`. Generate the inputs first, one run per day, e.g. for 10–14 May 2024
at the 15 MHz frequency index (6):

```
for d in 10 11 12 13 14; do
    python3 grape_acf_doppler_spread.py ch0_W2NAF_2024-05-$d 6 0 24
done
```

This writes `output/csv/W2NAF/ACF_FWL_data__15.0MHz_2024-05-DD_0-24.csv`, which the three summary/
analysis scripts then consume. With those present, all three run clean.

### Ray-tracing scripts — syntax/import checked only

`pathfinder.py`, `modefinder.py`, `synthspec.py`, `SS_sidescatter.py`, `SS_sidescatter_plot.py`
all compile cleanly (`python -m py_compile`). They require PyLap/PHaRLAP (see the README) to run,
which was not available in the test environment, so they were not executed here.

## Fixes made during testing

- `map_psws.py`: created `./output/maps/` before saving (matching the pattern in the other
  scripts) so it no longer fails with `FileNotFoundError`.
- `grape_acf_doppler_spread.py`: the output CSV filename now includes the requested
  start–stop hour range (e.g. `_0-24`), so the multi-day summary/analysis scripts find their
  inputs without manual renaming.
- `analyze_extracted_signal_to_noise.py`: updated to the new ACF CSV name and made its date
  parsing robust to the added hour-range suffix.
- `requirements.txt`: removed `netCDF4` (not imported by any script).
- Removed `plot_w2naf_grapeDRF_2024eclipse.py` (broken and redundant with the Gannon-storm
  stackplot scripts).
