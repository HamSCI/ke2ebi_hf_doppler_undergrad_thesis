# Thesis figure → script map

This table maps each figure in Rebecca Potter's (KE2EBI) thesis to the script that produces it and
the exact command used. Run every command from the repository root with the dataset extracted to
`./data/` (see the README). Figure numbers follow the chapter order in which the figures are
rendered; they may shift by ±1 if the thesis is recompiled with figures added, removed, or toggled.

## Regenerate every figure at once

To rebuild all of the code-generated thesis figures in one step, run:

```
python make_thesis_figures.py
```

It runs each script below (headless, using the same interpreter you invoke it with) and
collects the results under their thesis filenames in `output/thesis_figures/` for direct
comparison against the Overleaf `Figures/` directory. The five `ACF_Combined_*.png` figures
are produced by stacking the Doppler and S+N panels (see the ACF note below).

All multi-day `W2NAF` figures read the continuous wideband **RX888** Digital RF recording in
`data/psws_grapeDRF/w2naf_rx888/`, so their titles read "W2NAF (RX888)". (Earlier thesis figures
mislabeled this instrument as "GRAPE1"; those figures were regenerated and corrected.)

## Chapter 1 — Background (external images, not produced by this code)

| Fig | File | Source |
| --- | --- | --- |
| 1.1 | `Ionosphere_Layers_en.png` | External / public-domain illustration |
| 1.2 | `Currents.jpg` | External illustration |

## Chapter 2 — Instrumentation and data

| Fig | Thesis file | Script | Command | Notes |
| --- | --- | --- | --- | --- |
| 2.1 | `path_lengths.png` | `map_psws.py` | `python map_psws.py` | Output saved as `output/maps/psws_map.png`; reads `coords_sheet.txt`. |
| 2.2 | `collins_figure.png` | — | — | External, cited (Collins). |
| 2.3 | `May10_5_10_15MHz.png` | `psws_spectrogram_with_colorbar.py` | `python psws_spectrogram_with_colorbar.py 2024-05-10` | Date passed as a CLI arg. |
| 2.4 | `May8_5_10_15MHz.png` | `psws_spectrogram_with_colorbar.py` | `python psws_spectrogram_with_colorbar.py` | Default date is 8 May 2024. |
| 2.5 | `Custom_SYM-H_Plot.png` | `Gannon_storm_SYM-H_plot.py` | `python Gannon_storm_SYM-H_plot.py` | Output saved as `output/Gannon_SYM-H_Plot.png`; reads `data/SYMH_GannonStorm.csv`. |

The grape1drf receiver photograph (`grape1drf.jpeg`) is currently disabled in the thesis
(`\iffalse`) and is an external photo, not produced by this code.

## Chapter 3 — Results

| Fig | Thesis file | Script | Command | Notes |
| --- | --- | --- | --- | --- |
| 3.1 | `quiet_day_stack.png` | `quiet_day_stack.py` | `python quiet_day_stack.py` | Curated set of seven Kp≤2 May-2024 days, listed at the top of the script. |
| 3.2 | `quiet_time_avg.png` | `15MHz_average_quiet_day_doppler.py` | `python 15MHz_average_quiet_day_doppler.py` | First figure; reads `data/W2NAF_May_2024_quiet_days(15MHz).csv`. |
| 3.3 | `sunrise_peak_May2024_avg.png` | `15MHz_average_quiet_day_doppler.py` | `python 15MHz_average_quiet_day_doppler.py` | Second (windowed) figure from the same run. |
| 3.4 | `Gannon_stackplot.png` | `Gannon_storm_stackplot.py` | `python Gannon_storm_stackplot.py` | Default is 10–14 May 2024; optional `START_DATE NUM_DAYS` args. |
| 3.5 | `ACF_Combined_15.0MHz_2024-05-10.png` | `grape_acf_doppler_spread.py` | `python grape_acf_doppler_spread.py ch0_W2NAF_2024-05-10 6 0 24` | See ACF note below. |
| 3.6 | `ACF_Combined_15.0MHz_2024-05-11.png` | `grape_acf_doppler_spread.py` | `python grape_acf_doppler_spread.py ch0_W2NAF_2024-05-11 6 0 24` | " |
| 3.7 | `ACF_Combined_15.0MHz_2024-05-12.png` | `grape_acf_doppler_spread.py` | `python grape_acf_doppler_spread.py ch0_W2NAF_2024-05-12 6 0 24` | " |
| 3.8 | `ACF_Combined_15.0MHz_2024-05-13.png` | `grape_acf_doppler_spread.py` | `python grape_acf_doppler_spread.py ch0_W2NAF_2024-05-13 6 0 24` | " |
| 3.9 | `ACF_Combined_15.0MHz_2024-05-14.png` | `grape_acf_doppler_spread.py` | `python grape_acf_doppler_spread.py ch0_W2NAF_2024-05-14 6 0 24` | " |
| 3.10 | `15_MHz_summary.png` | `15MHz_multiday_summary.py` | see below | Four-panel SYM-H / spectrogram / Doppler / S+N summary. |

`multi_day_storm.png` (from `multi_day_colorbar.py`) is currently disabled in the thesis
(`\iffalse`) and is not part of the final document. Run `python multi_day_colorbar.py` (optional
`START_DATE NUM_DAYS` args) to regenerate it.

### ACF_Combined figures (3.5–3.9)

`grape_acf_doppler_spread.py` computes the reduced Doppler shift and signal-plus-noise level and
the sudden-commencement (SSC) marker, but writes the **Doppler** and **S+N level** panels as two
**separate** PNGs (`output/plots/W2NAF/ACF_Doppler_15.0MHz_<date>.png` and
`ACF_Level_15.0MHz_<date>.png`). The thesis `ACF_Combined_*.png` figures stack those two panels
into one image; that stacking was done by hand, so the single combined PNG is not emitted by the
current code. The underlying data and both panels are fully reproducible.

### 15 MHz multi-day summary (3.10)

This figure requires per-day ACF CSVs first. Generate them, then run the summary:

```
for d in 10 11 12 13 14; do
    python grape_acf_doppler_spread.py ch0_W2NAF_2024-05-$d 6 0 24
done
python 15MHz_multiday_summary.py
```

The summary script defaults to the 10–14 May 2024 window used in the thesis; the storm-phase
markers and per-day origins are tied to that window and are set at the top of the script.

## Unused images in the thesis `Figures/` directory

`15MHz_look.png`, `doppler_symh_may10_14.png`, and `w2naf_10May2024.png … w2naf_14May2024.png`
exist in the Overleaf `Figures/` directory but are not referenced by any `\includegraphics`; they
are superseded drafts and do not appear in the compiled thesis.
