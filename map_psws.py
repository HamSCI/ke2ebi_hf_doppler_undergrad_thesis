# Plotting PSWS on map of contiguous US

from geographiclib.geodesic import Geodesic
geod = Geodesic.WGS84

import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
import cartopy  
import cartopy.crs as ccrs


filename = 'coords_example_sheet.txt'
data     = np.genfromtxt(filename, dtype=None, encoding='utf-8')

print(data[0:])
'''
callsign = data['f0']
lat      = data['f1']
long     = data['f2']

# WWV
call_0 = 'WWV'
lat_0  = 40.6683
lon_0  = -105.0384

# Messy code start ======================================================
all_stations = []
all_lats = []
all_lons = []
all_invl = []
all_dist = []
all_az = []
all_lat_mid = []
all_lon_mid = []

for i in range(len(station_name)):
    call_1 = station_name[i]                                     
    lat_1 = latitude[i]
    lon_1 = longitude[i]
    #calculate distance and azimuth
    invl = geod.InverseLine(lat_0,lon_0,lat_1,lon_1)         
    dist = invl.s13*1e-3  # Distance in km
    az = invl.azi1
    #calculate midpoint
    #tmp = invl.Position(invl.s13/2,Geodesic.STANDARD)
    #lat_mid = tmp['lat2']
    #lon_mid = tmp['lon2']
    #append to lists
    all_stations.append(call_1)
    all_lats.append(lat_1)
    all_lons.append(lon_1)
    all_invl.append(invl)
    all_dist.append(dist)
    all_az.append(az)
    #all_lat_mid.append(lat_mid)
    #all_lon_mid.append(lon_mid)

# Messy code end ========================================================




# Set up figure
plt.rcParams['font.size']        = 18
plt.rcParams['font.weight']      = 'bold'
plt.rcParams['axes.titleweight'] = 'bold'
plt.rcParams['axes.grid']        = True
plt.rcParams['axes.xmargin']     = 0
plt.rcParams['grid.linestyle']   = ':'

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

# Add markers for transmitter, receiver, and midpoint
ax.scatter(lon_0, lat_0, marker='*', s=500, label=call_0)

ax.add_feature(cartopy.feature.COASTLINE)
ax.add_feature(cartopy.feature.BORDERS, linestyle=':')
ax.set_title('')
ax.gridlines(draw_labels=True)
ax.legend(loc='lower right',prop={'size':'x-small','weight':'normal'},framealpha=1)
ax.set_xlim(xlim)
ax.set_ylim(ylim)

plt.tight_layout()
plt.show()
'''