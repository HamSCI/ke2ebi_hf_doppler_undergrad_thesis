#!/usr/bin/env bash
#
# make_thesis_figures.sh
# -----------------------
# Regenerate every figure used in the KE2EBI thesis with a single command and
# collect them, under their thesis filenames, in output/thesis_figures/ so they
# can be compared directly against the Overleaf Figures/ directory.
#
# Usage (from the repository root, with the dataset extracted to ./data/):
#     ./make_thesis_figures.sh
#
# Set PYTHON to choose an interpreter (default: python3), e.g.
#     PYTHON=/path/to/conda/envs/drf-plot-py311/bin/python ./make_thesis_figures.sh
#
# Figures are rendered headless (matplotlib Agg backend), so no display is
# needed. See FIGURES.md for the figure-by-figure mapping this script automates.

set -uo pipefail
cd "$(dirname "$0")"

PYTHON="${PYTHON:-python3}"
export MPLBACKEND=Agg

FIG="output/thesis_figures"
LOG="$(mktemp)"
mkdir -p "$FIG"
trap 'rm -f "$LOG"' EXIT

produced=0
missing=()

echo "Interpreter : $($PYTHON --version 2>&1)"
echo "Output dir  : $FIG"
echo

# run <label> -- <command...>   : run a figure script, streaming nothing but
# capturing its output to $LOG (the grapeDRF scripts print their .png path there).
run() {
    local label="$1"; shift
    [ "$1" = "--" ] && shift
    printf '%-44s ' "$label"
    if "$@" >"$LOG" 2>&1; then
        echo "[ok]"
    else
        echo "[FAILED]  (see output below)"
        sed 's/^/      | /' "$LOG" | tail -8
    fi
}

# grab <dest> <fallback> : copy the figure this run produced into $FIG/<dest>.
# Prefers the .png path the script printed; falls back to a known default path.
grab() {
    local dest="$1" fallback="$2" src
    src=$(grep -oE '[^[:space:]]+\.png' "$LOG" | tail -1)
    [ -z "$src" ] && src="$fallback"
    if [ -f "$src" ]; then
        cp -f "$src" "$FIG/$dest"; echo "      -> $dest"; produced=$((produced+1))
    else
        echo "      !! MISSING (expected $src)"; missing+=("$dest")
    fi
}

# copy <dest> <src> : copy a fixed-path figure into $FIG/<dest>.
copy() {
    local dest="$1" src="$2"
    if [ -f "$src" ]; then
        cp -f "$src" "$FIG/$dest"; echo "      -> $dest"; produced=$((produced+1))
    else
        echo "      !! MISSING (expected $src)"; missing+=("$dest")
    fi
}

echo "Chapter 2"
run "Fig 2.1  path_lengths"            -- $PYTHON map_psws.py
grab "path_lengths.png"                "output/maps/psws_map.png"

run "Fig 2.4  May 8 spectrogram"       -- $PYTHON psws_spectrogram_with_colorbar.py
grab "May8_5_10_15MHz.png"             ""

run "Fig 2.3  May 10 spectrogram"      -- $PYTHON psws_spectrogram_with_colorbar.py 2024-05-10
grab "May10_5_10_15MHz.png"            ""

run "Fig 2.5  SYM-H plot"              -- $PYTHON Gannon_storm_SYM-H_plot.py
grab "Custom_SYM-H_Plot.png"           "output/Gannon_SYM-H_Plot.png"

echo
echo "Chapter 3"
run "Fig 3.1  quiet-day stack"         -- $PYTHON quiet_day_stack.py
grab "quiet_day_stack.png"             ""

# 15MHz_average_quiet_day_doppler.py writes two fixed-path figures in one run.
run "Fig 3.2/3.3  quiet-day average"   -- $PYTHON 15MHz_average_quiet_day_doppler.py
copy "quiet_time_avg.png"              "output/W2NAF_May_2024_15MHz_quiet_time_avg.png"
copy "sunrise_peak_May2024_avg.png"    "output/15_MHz_quiet_time_avg_window.png"

run "Fig 3.4  Gannon stackplot"        -- $PYTHON Gannon_storm_stackplot.py
grab "Gannon_stackplot.png"            ""

# Figs 3.5-3.9: per-day reduced Doppler + S+N. grape_acf_doppler_spread.py writes
# the Doppler and Level panels as separate PNGs (and the per-day ACF CSVs the
# summary below needs); we stack the two panels into the thesis ACF_Combined_*.png.
echo "Figs 3.5-3.9  per-day ACF (Doppler + S+N)"
for d in 10 11 12 13 14; do
    run "    2024-05-$d ACF"           -- $PYTHON grape_acf_doppler_spread.py "ch0_W2NAF_2024-05-$d" 6 0 24
done
$PYTHON - "$FIG" <<'PY'
import sys, os
from PIL import Image
figdir = sys.argv[1]
src = os.path.join("output", "plots", "W2NAF")
for d in range(10, 15):
    date = f"2024-05-{d}"
    top = os.path.join(src, f"ACF_Doppler_15.0MHz_{date}.png")
    bot = os.path.join(src, f"ACF_Level_15.0MHz_{date}.png")
    out = os.path.join(figdir, f"ACF_Combined_15.0MHz_{date}.png")
    if not (os.path.exists(top) and os.path.exists(bot)):
        print(f"      !! MISSING panels for {date}")
        continue
    a, b = Image.open(top), Image.open(bot)
    w = max(a.width, b.width)
    canvas = Image.new("RGBA", (w, a.height + b.height), "white")
    canvas.paste(a, (0, 0)); canvas.paste(b, (0, a.height))
    canvas.convert("RGB").save(out)
    print(f"      -> ACF_Combined_15.0MHz_{date}.png")
PY

# Fig 3.10 needs the per-day ACF CSVs generated in the loop above.
run "Fig 3.10  15 MHz multi-day summary" -- $PYTHON 15MHz_multiday_summary.py
grab "15_MHz_summary.png"              ""

echo
echo "============================================================"
total=$(ls -1 "$FIG"/*.png 2>/dev/null | wc -l | tr -d ' ')
echo "Done. $total figure(s) written to $FIG/"
if [ "${#missing[@]}" -gt 0 ]; then
    echo "Missing: ${missing[*]}"
fi
echo
echo "Note: the thesis ACF_Combined_*.png figures are the Doppler and S+N panels"
echo "stacked here automatically; in the thesis they were combined by hand, so the"
echo "layout (two titles vs. one shared title) differs slightly. See FIGURES.md."
echo "Chapter-1 figures and collins_figure.png are external images, not generated."
