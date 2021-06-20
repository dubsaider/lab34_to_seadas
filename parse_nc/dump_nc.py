import matplotlib.pyplot as plt

from netCDF4 import Dataset

#rootgrp = Dataset("V2021105041200.L1B-M_JPSS1.nc", "r", format="NETCDF4")
rootgrp = Dataset("V2021105041200.GEO-M_JPSS1.nc", "r", format="NETCDF4")

#print(rootgrp.groups)
print(rootgrp.groups['navigation_data'])
data = rootgrp.groups['navigation_data'].variables['earth_moon_distance']

plt.plot(data)
#plt.imshow(data, interpolation='none')
plt.show()
