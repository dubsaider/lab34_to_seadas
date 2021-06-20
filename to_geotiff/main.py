from rasterio.enums import ColorInterp
from rasterio.transform import Affine
import proformat.readpro as pro
from rasterio.plot import show
from pyproj import Transformer
import numpy as np
import rasterio

def normalize(array):
    array_min, array_max = array.min(), array.max()
    return ((array - array_min)/(array_max - array_min))

filen = 'samples/chl_oc2.pro'
file = open(filen, 'rb')
prof = pro.readproj(file)
file.seek(511, 0)

data = np.fromfile(file, dtype='uint16')
data = (data * prof['coeff_a']) + prof['coeff_b']
data = data.astype(np.uint16)
data = data.reshape(prof['lines'], prof['pixels'])
data = np.flipud(data)

lon = prof['longtitude']
lat = prof['latitude']
latsize = prof['lat_size']
lonsize = prof['lon_size']
latres = prof['lat_step']
lonres = prof['lon_step']
rows = prof['lines']
cols = prof['pixels']

tf = Transformer.from_crs("EPSG:4326", "EPSG:3395", always_xy=True)

top_left = tf.transform(lon, lat + latsize)
bottom_right = tf.transform(lon + lonsize, lat) 
latres = (top_left[1] - bottom_right[1]) / rows 
lonres = (bottom_right[0] - top_left[0]) / cols
lon = top_left[0]
lat = top_left[1]

transform = rasterio.transform.from_origin(lon, lat, lonres, latres)

new_dataset = rasterio.open(
                    'result.tif', 
                    'w', 
                    driver='GTiff', 
                    height=rows, 
                    width=cols, 
                    count=1, 
                    dtype=data.dtype, 
                    crs='EPSG:3395',
                    transform=transform,
                    )

new_dataset.write(data, 1)
new_dataset.close()

file.close()
