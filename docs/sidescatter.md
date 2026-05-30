# Two-hop sidescatter computation and visualisation (G3ZIL)

This set of scripts, developed by Gwyn Griffiths (G3ZIL), uses 3D PyLap ray tracing to model two-hop
sidescatter with a simplified approach: a pseudo-transmitter is placed at the receiver and
reciprocity is assumed. The product of transmitter and pseudo-transmitter ray landing spots in
1° × 1° boxes is derived and plotted. The code automatically sets the ionosphere grid bounding box
and the plotting extent to suit the transmitter/receiver geometry. It is not used to produce the
thesis figures; it is broader tooling that ships in this repository. For the thesis workflow, see
the [top-level README](../README.md).

> **Requirement:** these scripts require the ray-tracing package PyLap, installed from
> [GitHub](https://github.com/HamSCI/PyLap) (see the [synthetic spectrograms doc](synthetic_spectrograms.md)
> for PyLap/PHaRLAP notes).

**Current limitations:**
- Northern Hemisphere only.
- The northernmost of tx and rx must be below 58°N, else the grid would extend beyond the North Pole.
- Automatic metric amplitude scaling for the contour map in animations is still being refined.

Plots are written to `./output/plots/SS/<callsign>/` and CSV data files to `./output/csv/SS/<callsign>/`.

## Part 1: Ray landing spots for transmitter and pseudo-transmitter

`SS_sidescatter.py` takes two command-line arguments, the config file name and the specified time in
`YYmmddHHMM` format. The `config.ini` file (example below) is an extended version of the one used for
2D great-circle paths:
```
python3 SS_sidescatter.py ./config/W2NAF_config.ini 202407270000
```

`config.ini` — this example is for CHU, Ottawa to W2NAF PA. Several parameters start at 0; scripts
write results for these parameters for use by subsequent scripts. The elevation step interval is 1°
and the azimuth scan is a full 360°. Computer memory limits the azimuth resolution: 3° is used here
for an 8 GB machine.

```ini
[settings]
ut = [2024,9,27,0,0]
r12 = 114
freq = 14.67
tx_grid = FN25CH
rx_grid = FN21EI
nhops = 1
elev_start = 3
elev_stop = 45
distance = 0
bearing = 0
[metadata]
tx = CHU
rx = W2NAF
[plots]
legend = upper right
u_dopp_lim = 3
l_dopp_lim = -3
[3d_sidescatter]
ray_inc = 3
metric_max_lat = 0
metric_max_lon = 0
max_metric = 0
```

The output is `<timestamp>_ground_coords.csv` in `./output/csv/SS/<callsign>`, where `<timestamp>` is
the second command-line parameter and `<callsign>` is from the config file name. An example:

```
0,0.0,2,5.0,154.513,-4.461,70.004264,-75.479248
0,0.0,3,6.0,158.077,-4.566,67.67416,-75.53916
0,0.0,4,7.0,161.799,-4.697,65.972454,-75.570397
```

where the fields are: source (0 = tx, 1 = pseudo-tx at rx), ray bearing (°), rayId, initial
elevation (°), apogee (km), PyLap Doppler (Hz), landing-spot lat (°), landing-spot lon (°).

## Part 2: Ray landing spots and the sidescatter likelihood metric

`SS_sidescatter_plot.py` takes three command-line arguments: the config file name, the specified time
in `YYmmddHHMM` format, and a frame number for use with the `SS_animate.sh` bash script. In
stand-alone use the frame number is chosen by the user (max 999).
```
python3 SS_sidescatter_plot.py ./config/W2NAF_config.ini 202409270000 0
```
Two plot files are written to `./output/plots/SS/<callsign>`: `sidescatter.png` (the ray landing
spots) and `2F_sidescatter_metric_000.png` (a contour map of the sidescatter likelihood metric,
where `000` is the zero-padded frame number).

Here is an example ray-landing-spot map for CHU to W2NAF on 14.67 MHz at 00:00 UTC on 27 September
2024:

<img width="560" height="480" alt="sidescatter" src="https://github.com/user-attachments/assets/d43d450e-58a0-46e0-9d3c-304c180825e2" />

And the plot of the sidescatter likelihood metric:

<img width="560" height="448" alt="2F_sidescatter_metric_000" src="https://github.com/user-attachments/assets/9a32c588-214e-4eae-9edf-42698a8203d4" />

## Part 3: Sidescatter metric image sequence and animation

`SS_animate.sh` runs `SS_sidescatter.py` then `SS_sidescatter_plot.py` a user-defined number of times
at user-defined intervals to generate multiple sidescatter likelihood metric plots and an mp4
animation of those frames, stored in `./output/plots/SS/<callsign>`. Each frame can take minutes to
generate (e.g. ~4 minutes on a 4-core i5). The script takes three command-line parameters: the config
file name, the total duration in minutes, and the frame interval in minutes. This example produces
simulations every 20 minutes for 360 minutes (≈18 frames):
```
./SS_animate.sh W2NAF_config.ini 360 20
```
Note that ffmpeg (which generates the mp4) can both insert and drop frames depending on how many you
have. Example animation:

https://github.com/user-attachments/assets/95268232-11b4-41ee-9da1-0c760e2c7cab
