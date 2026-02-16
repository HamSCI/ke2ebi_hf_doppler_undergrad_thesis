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

# Messy code start - WWV ======================================================
# WWV lists
all_psws = []
all_psws_lats = []
all_psws_lons = []
all_invl_WWV = []
all_dist_WWV = []
all_az_WWV = []
all_lat_mid_WWV = []
all_lon_mid_WWV = []

# CHU lists
all_invl_CHU = []
all_dist_CHU = []
all_az_CHU = []
all_lat_mid_CHU = []
all_lon_mid_CHU = []

for i in range(len(callsign)):
    psws_call = callsign[i]                                     
    psws_lat = lat[i]
    psws_lon = lon[i]

    #calculate distance and azimuth for WWV
    invl_WWV = geod.InverseLine(lat_WWV, lon_WWV, psws_lat, psws_lon)         
    dist_WWV = invl_WWV.s13*1e-3  # Distance in km
    az_WWV = invl_WWV.azi1
    tmp_WWV = invl_WWV.Position(invl_WWV.s13/2, Geodesic.STANDARD)
    lat_mid_WWV = tmp_WWV['lat2']
    lon_mid_WWV = tmp_WWV['lon2']

     # Calculate for CHU
    invl_CHU = geod.InverseLine(lat_CHU, lon_CHU, psws_lat, psws_lon)         
    dist_CHU = invl_CHU.s13*1e-3  # Distance in km
    az_CHU = invl_CHU.azi1
    tmp_CHU = invl_CHU.Position(invl_CHU.s13/2, Geodesic.STANDARD)
    lat_mid_CHU = tmp_CHU['lat2']
    lon_mid_CHU = tmp_CHU['lon2']

    # Append to lists (only need one set of PSWS info)
    all_psws.append(psws_call)
    all_psws_lats.append(psws_lat)
    all_psws_lons.append(psws_lon)

    #append to lists
    all_psws.append(psws_call)
    all_psws_lats.append(psws_lat)
    all_psws_lons.append(psws_lon)
    
    # WWV data
    all_invl_WWV.append(invl_WWV)
    all_dist_WWV.append(dist_WWV)
    all_az_WWV.append(az_WWV)
    all_lat_mid_WWV.append(lat_mid_WWV)
    all_lon_mid_WWV.append(lon_mid_WWV)

    # CHU data
    all_invl_CHU.append(invl_CHU)
    all_dist_CHU.append(dist_CHU)
    all_az_CHU.append(az_CHU)
    all_lat_mid_CHU.append(lat_mid_CHU)
    all_lon_mid_CHU.append(lon_mid_CHU)
# Messy code end ========================================================

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

range_step = 1

# Plot PSWS
for i in range(len(all_psws)):
    ax.scatter(all_psws_lons[i],all_psws_lats[i],marker='^',s=250,label=all_psws[i])

    # Plot WWV paths and midpoints
    if i == 0:
        ax.scatter(all_lon_mid[i], all_lat_mid[i], s=250, label='Midpoint')
    else:
        ax.scatter(all_lon_mid[i], all_lat_mid[i], s=250)
        
    invl = all_invl_WWV[i]  # Make sure you're using the correct one for station i
    ranges = np.linspace(0, invl.s13, 100)  # 100 points across full path in meters
    glats = []
    glons = []
    for s in ranges:
        tmp = invl.Position(s, Geodesic.STANDARD)
        glats.append(tmp['lat2'])
        glons.append(tmp['lon2'])
        
    ax.plot(glons,glats,lw=3,transform=ccrs.PlateCarree())

# Plot CHU paths and midpoints

for i in range(len(all_psws)):
    if i == 0:
        ax.scatter(all_lon_mid_CHU[i], all_lat_mid_CHU[i], s=150, color='red', label='CHU Midpoint')
    else:
        ax.scatter(all_lon_mid_CHU[i], all_lat_mid_CHU[i], s=150, color='red')
        
    invl = all_invl_CHU[i]
    ranges = np.linspace(0, invl.s13, 100)
    glats = []
    glons = []
    for s in ranges:
        tmp = invl.Position(s, Geodesic.STANDARD)
        glats.append(tmp['lat2'])
        glons.append(tmp['lon2'])
        
    ax.plot(glons, glats, lw=3, color='red', transform=ccrs.PlateCarree())

 # Finalize Figure
ax.add_feature(cartopy.feature.COASTLINE)
ax.add_feature(cartopy.feature.BORDERS, linestyle=':')
ax.set_title('')
ax.gridlines(draw_labels=True)
ax.legend(loc='lower right',prop={'size':'x-small','weight':'normal'},framealpha=1)
ax.set_xlim(xlim)
ax.set_ylim(ylim)

plt.tight_layout()
plt.show()