# HamSCI Personal Space Weather Station Observations of the Gannon Geomagnetic Storm

Code and documentation accompanying **Rebecca Potter's (KE2EBI) undergraduate thesis** at the
University of Scranton, which uses HamSCI Personal Space Weather Station (PSWS) GRAPE / RX888 HF
Doppler observations to study the May 2024 Gannon geomagnetic storm. This repository contains the
scripts that produce the thesis figures, the shared data engine they build on, and broader HF
Doppler tooling contributed by the project's collaborators.

<!-- After Zenodo mints the DOI, replace the placeholder below:
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)
-->

## How to cite

If you use this software, please cite the Zenodo software archive (DOI to be assigned on release)
and the underlying thesis. See [CITATION.cff](CITATION.cff) for the canonical citation metadata.

The supporting dataset (GRAPE / PSWS HF Doppler recordings and CSVs required to run these scripts)
is archived separately on Zenodo at [doi.org/10.5281/zenodo.20466479](https://doi.org/10.5281/zenodo.20466479)
(DOI `10.5281/zenodo.20466479`). Download and extract it to `./data/` as described under
[Installation](#installation).

## Development history

This repository descends from a line of HamSCI HF Doppler tools, and most of its breadth predates
the thesis:

1. **`w2naf/grapeDRF_doppler_model`** — the original project by Dr. Nathaniel Frissell (W2NAF):
   "code for plotting GRAPE DigitalRF data with Shibaji Chakraborty's HF Doppler Model outputs on
   top," with an early focus on eclipse HF Doppler. It contributed the core `GrapeDRF` spectrogram
   engine and the `eclipse_calc` solar/eclipse library.
2. **`g3zil/grapeDRF_doppler_model`** — a fork by Gwyn Griffiths (G3ZIL) that added the GRAPE
   DigitalRF analysis suite (FFT spectrograms, complex-autocorrelation Doppler/spread, CWT peak
   finding), the PyLap synthetic-spectrogram ray-tracing pipeline, and 3D two-hop sidescatter
   modelling.
3. **`HamSCI/ke2ebi_hf_doppler_undergrad_thesis`** (this repository) — developed by Rebecca Potter
   (KE2EBI) on top of the G3ZIL fork to produce the analyses and figures in her thesis on the 2024
   Gannon storm, then cleaned and archived.

Accordingly, the documentation is organised so that the top-level README covers the thesis workflow,
while the broader G3ZIL and W2NAF tooling is described in the linked
[component documentation](#component-documentation) below.

## Installation

Tested on Ubuntu Linux and macOS.

### Download

Clone the repository and run the software from the resulting directory:
```
cd ~
git clone https://github.com/HamSCI/ke2ebi_hf_doppler_undergrad_thesis.git
cd ~/ke2ebi_hf_doppler_undergrad_thesis
```
Run all further commands in that directory. Update with `git pull`.

### Data

The scripts read their input from `./data/`, which is **not** bundled with the code. Download the
companion dataset from Zenodo (DOI `10.5281/zenodo.20466479`) and extract it so the layout is
`./data/...`:
```
tar xzf data.tar.gz      # creates ./data/
```
See the dataset's own README for the directory layout and a checksum manifest.

### Python dependencies

Install the dependencies in `requirements.txt`:
```
python -m pip install -r requirements.txt
```
Tested with Python 3.10.16 in clean conda environments on macOS 15.3.1 and Ubuntu 22.04.5 LTS, with
3.10.14 on macOS 10.14.6, and with 3.11/3.12 on Ubuntu 24.04. For an externally managed environment,
create a virtual environment first:
```
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

The thesis figures and the GRAPE DRF analysis tools need only these dependencies. The
**ray-tracing** tools (synthetic spectrograms and sidescatter) additionally require PyLap — see
those docs under [Component documentation](#component-documentation).

## How it works (thesis workflow)

The thesis figures are produced by a small set of plotting scripts that sit on top of the shared
`GrapeDRF` engine and the GRAPE DRF analysis tools.

**Input data.** Two kinds of recording under `data/psws_grapeDRF/`:

- `w2naf_rx888/` — a continuous wideband **RX888** DigitalRF recording for W2NAF (Spring Brook, PA)
  spanning 8–29 May 2024. This is the input for the multi-day storm and quiet-day figures.
- `ch0_<CALLSIGN>` — per-station GRAPE DigitalRF channels (single-day stations such as `ch0_G4HZX`,
  `ch0_N8GA`; multi-day stations as one dated directory per day, e.g. `ch0_W2NAF_2024-05-10`).

Plus two CSVs: `SYMH_GannonStorm.csv` (SYM-H index) and `W2NAF_May_2024_quiet_days(15MHz).csv`.

**Shared engine.** `grapeDRF.py` (the `GrapeDRF` class) loads the DigitalRF data, computes Doppler
spectrograms, and overlays the solar elevation angle via `eclipse_calc.solarContext`. The thesis
multi-day spectrogram/stackplot scripts import and drive it. `grape_acf_doppler_spread.py` (a G3ZIL
analysis tool) provides the per-day reduced Doppler / signal-to-noise data. These shared components
are documented in [the engine doc](docs/eclipse_and_engine.md) and
[the GRAPE DRF analysis doc](docs/grape_drf_analysis.md).

**Thesis figure scripts** (see [FIGURES.md](FIGURES.md) for the exact command behind each figure):

| Area | Script(s) |
| --- | --- |
| Transmitter/receiver map | `map_psws.py` |
| Multi-frequency spectrograms (W2NAF) | `psws_spectrogram_with_colorbar.py` |
| SYM-H index | `Gannon_storm_SYM-H_plot.py` |
| Quiet-day stack & average | `quiet_day_stack.py`, `15MHz_average_quiet_day_doppler.py` |
| Storm 15 MHz stackplot | `Gannon_storm_stackplot.py` |
| Per-day reduced Doppler / S+N | `grape_acf_doppler_spread.py` |
| Multi-day summary | `15MHz_multiday_summary.py` |
| Extracted-Doppler / S+N analysis | `analyze_extracted_dop_shift.py`, `analyze_extracted_signal_to_noise.py` |

**Regenerate everything at once:**
```
python make_thesis_figures.py
```
This runs the scripts above (headless) and collects the figures, under their thesis filenames, in
`output/thesis_figures/`. [FIGURES.md](FIGURES.md) maps each thesis figure to its script and exact
command; [TESTING.md](TESTING.md) records the verification performed before release.

## Component documentation

Broader tooling that ships in this repository but is not part of the thesis figure pipeline:

| Document | Contributor | Contents |
| --- | --- | --- |
| [docs/grape_drf_analysis.md](docs/grape_drf_analysis.md) | G3ZIL | GRAPE DigitalRF metadata, FFT spectrograms, autocorrelation Doppler/spread, CWT peak finding and tracking. |
| [docs/synthetic_spectrograms.md](docs/synthetic_spectrograms.md) | G3ZIL | Synthetic Doppler spectrograms from PyLap ray tracing (`pathfinder` → `modefinder` → `synthspec`) and overlay. **Requires PyLap.** |
| [docs/sidescatter.md](docs/sidescatter.md) | G3ZIL | Two-hop sidescatter modelling and animation with 3D PyLap ray tracing. **Requires PyLap.** |
| [docs/eclipse_and_engine.md](docs/eclipse_and_engine.md) | W2NAF | The shared `GrapeDRF` engine, the `eclipse_calc` solar/eclipse library, and the original eclipse Doppler work this repository grew from. |

## License

Copyright (C) 2024–2026 Rebecca Potter (KE2EBI), Gwyn Griffiths (G3ZIL), and Nathaniel A. Frissell
(W2NAF).

Released under the GNU General Public License v3.0 or later — see [LICENSE](LICENSE) for the full
text.

## Acknowledgements

I am very grateful to my thesis advisor, Dr. Nathaniel Frissell, for providing resources,
mentorship, and positive encouragement throughout this project. I am also grateful to my committee
members Dr. Juan Serna and Dr. Declan Mulhall for their constructive feedback and support both in
this project and my overall academic endeavors throughout my time at the University of Scranton. More
thanks go to the collaborators whom I met with weekly to discuss my progress and received advice from
throughout this academic year: Gwyn Griffiths, Dr. Kuldeep Pandey, Dr. Sarah Over, Dr. Mary Lou West,
Gary Mitkin, Dr. Rob Suggs, and Dr. Jay Weitzen. Their expertise and readiness to share it played a
strong role in this project's success.

We are grateful for the support of NSF Grants AGS-2045755, AGS-2432821, AGS-2432822, AGS-2432824,
AGS-2432823, OPP-2332427, and NASA Grants 80NSSC23K1322, 80NSSC25K7026.
