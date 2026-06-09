#!/usr/bin/env python3
"""
make_thesis_figures.py
----------------------
Regenerate every figure used in the KE2EBI thesis with a single command and
collect them, under their thesis filenames, in output/thesis_figures/ so they
can be compared directly against the Overleaf Figures/ directory.

Usage (from the repository root, with the dataset extracted to ./data/):
    python make_thesis_figures.py

The figure scripts are run with the same interpreter that runs this file, so
just invoke it with the Python environment that has the dependencies installed.
Figures are rendered headless (matplotlib Agg backend); no display is needed.
See FIGURES.md for the figure-by-figure mapping this script automates.
"""

import os
import re
import sys
import shutil
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parent
os.chdir(REPO)

PY = sys.executable                      # run child scripts with this same interpreter
ENV = {**os.environ, "MPLBACKEND": "Agg"}
FIG = Path("output") / "thesis_figures"
FIG.mkdir(parents=True, exist_ok=True)

missing = []


def run(label, *cmd):
    """Run a figure script; print status; return its captured stdout text."""
    print(f"{label:<44} ", end="", flush=True)
    proc = subprocess.run([PY, *cmd], env=ENV, capture_output=True, text=True)
    if proc.returncode == 0:
        print("[ok]")
    else:
        print("[FAILED]  (see output below)")
        for line in (proc.stdout + proc.stderr).splitlines()[-8:]:
            print(f"      | {line}")
    return proc.stdout


def grab(out_text, dest, fallback=""):
    """Copy the .png the script printed (or a known fallback) into FIG/dest."""
    found = re.findall(r"[^\s]+\.png", out_text)
    src = Path(found[-1]) if found else Path(fallback)
    _place(src, dest)


def copy(dest, src):
    """Copy a fixed-path figure into FIG/dest."""
    _place(Path(src), dest)


def _place(src, dest):
    if src and src.is_file():
        shutil.copyfile(src, FIG / dest)
        print(f"      -> {dest}")
    else:
        print(f"      !! MISSING (expected {src})")
        missing.append(dest)


print(f"Interpreter : {sys.version.split()[0]} ({PY})")
print(f"Output dir  : {FIG}\n")

print("Chapter 2")
out = run("Fig 2.1  path_lengths", "map_psws.py")
grab(out, "path_lengths.png", "output/maps/psws_map.png")

out = run("Fig 2.4  May 8 spectrogram", "psws_spectrogram_with_colorbar.py")
grab(out, "May8_5_10_15MHz.png")

out = run("Fig 2.3  May 10 spectrogram", "psws_spectrogram_with_colorbar.py", "2024-05-10")
grab(out, "May10_5_10_15MHz.png")

out = run("Fig 2.5  SYM-H plot", "Gannon_storm_SYM-H_plot.py")
grab(out, "Custom_SYM-H_Plot.png", "output/Gannon_SYM-H_Plot.png")

print("\nChapter 3")
out = run("Fig 3.1  quiet-day stack", "quiet_day_stack.py")
grab(out, "quiet_day_stack.png")

# 15MHz_average_quiet_day_doppler.py writes two fixed-path figures in one run.
run("Fig 3.2/3.3  quiet-day average", "15MHz_average_quiet_day_doppler.py")
copy("quiet_time_avg.png", "output/W2NAF_May_2024_15MHz_quiet_time_avg.png")
copy("sunrise_peak_May2024_avg.png", "output/15_MHz_quiet_time_avg_window.png")

out = run("Fig 3.4  Gannon stackplot", "Gannon_storm_stackplot.py")
grab(out, "Gannon_stackplot.png")

# Figs 3.5-3.9: per-day reduced Doppler + S+N. grape_acf_doppler_spread.py writes
# the Doppler and Level panels as separate PNGs (and the per-day ACF CSVs the
# summary below needs); we stack the two panels into the thesis ACF_Combined_*.png.
print("Figs 3.5-3.9  per-day ACF (Doppler + S+N)")
acf_dir = Path("output") / "plots" / "W2NAF"
for d in range(10, 15):
    run(f"    2024-05-{d} ACF", "grape_acf_doppler_spread.py",
        f"ch0_W2NAF_2024-05-{d}", "6", "0", "24")

from PIL import Image  # noqa: E402  (Pillow ships with matplotlib)
for d in range(10, 15):
    date = f"2024-05-{d}"
    top = acf_dir / f"ACF_Doppler_15.0MHz_{date}.png"
    bot = acf_dir / f"ACF_Level_15.0MHz_{date}.png"
    dest = f"ACF_Combined_15.0MHz_{date}.png"
    if not (top.is_file() and bot.is_file()):
        print(f"      !! MISSING panels for {date}")
        missing.append(dest)
        continue
    a, b = Image.open(top), Image.open(bot)
    w = max(a.width, b.width)
    canvas = Image.new("RGBA", (w, a.height + b.height), "white")
    canvas.paste(a, (0, 0))
    canvas.paste(b, (0, a.height))
    canvas.convert("RGB").save(FIG / dest)
    print(f"      -> {dest}")

# Fig 3.10 needs the per-day ACF CSVs generated in the loop above.
out = run("Fig 3.10  15 MHz multi-day summary", "15MHz_multiday_summary.py")
grab(out, "15_MHz_summary.png")

total = len(list(FIG.glob("*.png")))
print("\n" + "=" * 60)
print(f"Done. {total} figure(s) written to {FIG}/")
if missing:
    print("Missing: " + ", ".join(missing))
print(
    "\nNote: the thesis ACF_Combined_*.png figures are the Doppler and S+N panels\n"
    "stacked here automatically; in the thesis they were combined by hand, so the\n"
    "layout (two titles vs. one shared title) differs slightly. See FIGURES.md.\n"
    "Chapter-1 figures and collins_figure.png are external images, not generated."
)
