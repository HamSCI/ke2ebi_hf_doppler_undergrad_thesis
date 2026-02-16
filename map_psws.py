# Plotting PSWS on map of contiguous US

from geographiclib.geodesic import Geodesic
geod = Geodesic.WGS84

import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
import cartopy  
import cartopy.crs as ccrs

filename = 'coords_sheet.txt'
data     = np.genfromtxt(filename, dtype=[('callsign','U10'),('lat',float),('lon',float)], encoding='utf-8', ndmin=1, skip_header=1)  #U10 allows up to 10 characters; may make it bigger

callsign = data['callsign']
lat      = data['lat']
lon      = data['lon']

# Transmitters
call_WWV = 'WWV'
lat_WWV  = 40.6683
lon_WWV  = -105.0384

call_CHU = 'CHU'
lat_CHU = 45.2964
lon_CHU = -75.7561

# Messy code start ======================================================
all_psws = []
all_psws_lats = []
all_psws_lons = []
all_invl = []
all_dist = []
all_az = []
all_lat_mid = []
all_lon_mid = []

for i in range(len(callsign)):
    psws_call = callsign[i]                                     
    psws_lat = lat[i]
    psws_lon = lon[i]
    #calculate distance and azimuth
    invl = geod.InverseLine(lat_WWV,lon_WWV,psws_lat,psws_lon)         
    dist = invl.s13*1e-3  # Distance in km
    az = invl.azi1
    #calculate midpoint
    tmp = invl.Position(invl.s13/2,Geodesic.STANDARD)
    lat_mid = tmp['lat2']
    lon_mid = tmp['lon2']
    #append to lists
    all_psws.append(psws_call)
    all_psws_lats.append(psws_lat)
    all_psws_lons.append(psws_lon)
    all_invl.append(invl)
    all_dist.append(dist)
    all_az.append(az)
    all_lat_mid.append(lat_mid)
    all_lon_mid.append(lon_mid)

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
ax.scatter(lon_WWV, lat_WWV, marker='*', s=500, label=call_WWV)
ax.scatter(lon_CHU, lat_CHU, marker='*', s=500, label=call_CHU)

for i in range(len(all_psws)):
    ax.scatter(all_psws_lons[i],all_psws_lats[i],marker='^',s=250,label=all_psws[i])

ax.add_feature(cartopy.feature.COASTLINE)
ax.add_feature(cartopy.feature.BORDERS, linestyle=':')
ax.set_title('')
ax.gridlines(draw_labels=True)
ax.legend(loc='lower right',prop={'size':'x-small','weight':'normal'},framealpha=1)
ax.set_xlim(xlim)
ax.set_ylim(ylim)

plt.tight_layout()
plt.show()