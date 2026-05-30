# Plotting PSWS on map of contiguous US

import os
from geographiclib.geodesic import Geodesic
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
import cartopy  
import cartopy.crs as ccrs

geod = Geodesic.WGS84

filename = 'coords_sheet.txt'
data     = np.genfromtxt(filename, dtype=[('callsign','U10'),('lat',float),('lon',float)], encoding='utf-8', ndmin=1, skip_header=1)  #U10 allows up to 10 characters; may make it bigger

callsign = data['callsign']
lat      = data['lat']
lon      = data['lon']

# Transmitters
transmitters = {
    'WWV': {'lat': 40.6683, 'lon': -105.0384, 'color': 'yellow'},
    'CHU': {'lat': 45.2964, 'lon': -75.7561, 'color': 'lime'}
}

# Path colors
path_colors = {'WWV': 'royalblue', 'CHU': 'firebrick'}
mid_colors  = {'WWV': 'royalblue', 'CHU': 'firebrick'}

# --- Compute geodesic data ---
def compute_geodesic(tx_lat, tx_lon, rx_lat, rx_lon):
    invl = geod.InverseLine(tx_lat, tx_lon, rx_lat, rx_lon)
    dist = invl.s13 * 1e-3
    az   = invl.azi1
    mid  = invl.Position(invl.s13 / 2, Geodesic.STANDARD)
    path_pts = [invl.Position(s, Geodesic.STANDARD)
                for s in np.linspace(0, invl.s13, 100)]
    path_lats = [p['lat2'] for p in path_pts]
    path_lons = [p['lon2'] for p in path_pts]
    return dict(invl=invl, dist=dist, az=az,
                lat_mid=mid['lat2'], lon_mid=mid['lon2'],
                path_lats=path_lats, path_lons=path_lons)

stations = []
for call, rx_lat, rx_lon in zip(callsign, lat, lon):
    entry = {'call': call, 'lat': rx_lat, 'lon': rx_lon}
    for tx_name, tx in transmitters.items():
        entry[tx_name] = compute_geodesic(tx['lat'], tx['lon'], rx_lat, rx_lon)
    stations.append(entry)

# Print summary table
print("\n" + "="*105)
print(f"{'Station':<10} {'WWV Dist (km)':<15} {'WWV Midpoint':<28} {'CHU Dist (km)':<15} {'CHU Midpoint':<28}")
print("="*105)

for s in stations:
    wwv_mid = f"({s['WWV']['lat_mid']:.2f}, {s['WWV']['lon_mid']:.2f})"
    chu_mid = f"({s['CHU']['lat_mid']:.2f}, {s['CHU']['lon_mid']:.2f})"
    print(f"{s['call']:<10} {s['WWV']['dist']:<15.2f} {wwv_mid:<28} {s['CHU']['dist']:<15.2f} {chu_mid:<28}")
print("="*105 + "\n")

## World
#xlim = (-180, 180)
#ylim = (-90, 90)

## CONUS + Canada
#xlim = (-130, -56)
#ylim = (20, 80)

# Continental US (CONUS)
xlim    = (-130,-56)
ylim    = (20,55)

fig = plt.figure(figsize=(15,8))
ax  = fig.add_subplot(111, projection=ccrs.PlateCarree())

ax.add_feature(cartopy.feature.COASTLINE)
ax.add_feature(cartopy.feature.BORDERS, linestyle=':')
#ax.gridlines(draw_labels=True)
ax.gridlines(draw_labels=True, x_inline=False, y_inline=False,
             xlabel_style={'size': 16, 'weight': 'bold'}, ylabel_style={'size': 16, 'weight': 'bold'})
ax.set_xlim(xlim)
ax.set_ylim(ylim)

# Transmitters
for tx_name, tx in transmitters.items():
    ax.scatter(tx['lon'], tx['lat'], marker='*', s=500,
               color=tx['color'], label=tx_name, zorder=5,
               transform=ccrs.PlateCarree())
    # Transmitter name label
    ax.text(tx['lon'] + 0.5, tx['lat'] + 0.5, tx_name,
            fontsize=10, fontweight='bold', transform=ccrs.PlateCarree(),
            ha='left', va='bottom')

# Paths, midpoints, and receivers
path_labeled = {tx: False for tx in transmitters}
mid_labeled  = {tx: False for tx in transmitters}
rx_labeled   = False

for s in stations:
    # Receiver marker
    rx_label = s['call'] if not rx_labeled else None
    ax.scatter(s['lon'], s['lat'], marker='^', s=250,
               color='red', label=rx_label, zorder=5,
               transform=ccrs.PlateCarree())
    rx_labeled = True

    # Station name label
    ax.text(s['lon'] + 0.5, s['lat'] + 0.5, s['call'],
            fontsize=10, weight='bold', transform=ccrs.PlateCarree(),
            ha='left', va='bottom')

    for tx_name in transmitters:
        g = s[tx_name]
        color = path_colors[tx_name]

        # Geodesic path
        path_label = f'{tx_name} path' if not path_labeled[tx_name] else None
        ax.plot(g['path_lons'], g['path_lats'], lw=2,
                color=color, alpha=0.7, label=path_label,
                transform=ccrs.PlateCarree())
        path_labeled[tx_name] = True

        # Midpoint
        mid_label = f'{tx_name} midpoint' if not mid_labeled[tx_name] else None
        ax.scatter(g['lon_mid'], g['lat_mid'], s=80, color=color,
                   marker='o', edgecolors='black', linewidths=0.5,
                   label=mid_label, zorder=4, transform=ccrs.PlateCarree())
        mid_labeled[tx_name] = True


plt.tight_layout()
os.makedirs('./output/maps', exist_ok=True)
plt.savefig('./output/maps/psws_map.png', dpi=300, bbox_inches='tight')
plt.show()
