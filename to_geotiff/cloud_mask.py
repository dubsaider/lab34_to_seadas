import sys
import main
import rasterio
import numpy as np


def parse_pro_data(file, pro_passport):
    file.seek(512, 0)
    data = np.fromfile(file, dtype='<i2')

    a = pro_passport['coeff_a']
    b = pro_passport['coeff_b']
    rows = pro_passport['lines']
    cols = pro_passport['pixels']

    data_scaled = data * a + b
    data_scaled[data_scaled == -50.0] = 0

    data_scaled[data_scaled > int(sys.argv[3])] = 0
    data_scaled[data_scaled < int(sys.argv[3])] = data_scaled[data_scaled < int(sys.argv[3])] + 255
    
    alpha = data_scaled.copy()
    alpha_map = sorted(np.unique(alpha[data > 0]))
    degrees = [255 - (i * (255 / len(alpha_map))) for i in range(len(alpha_map))]
    
    for i, j in zip(alpha_map, degrees):
        alpha[alpha == i] = j
    
    data = data_scaled.reshape(rows, cols)
    alpha = alpha.reshape(rows, cols)

    return np.flipud(data), np.flipud(alpha)


def create_cloude_mask():
    file_name = sys.argv[2]
    pro_file_name = sys.argv[1]
    pro_file = open(pro_file_name, 'rb')

    pro_passport = main.parse_pro_passport(pro_file)
    data, alpha = parse_pro_data(pro_file, pro_passport)
    affine_mat = main.affine_matrix(pro_passport)

    if not (file_name.endswith('.tif') or file_name.endswith('.tiff')):
        file_name += '.tif'
    
    with rasterio.Env(GDAL_TIFF_INTERNAL_MASK=True):
        with rasterio.open(
                file_name, 'w', driver='GTiff', photometric='RGB',
                height=pro_passport['lines'], width=pro_passport['pixels'],
                count=4, dtype=np.dtype('uint8'), nodata=0,
                crs='EPSG:3395', transform=affine_mat, alpha=True,
                compress='deflate', num_threads='all_cpus'
                ) as geotiff:
            geotiff.write(data, 1)
            geotiff.write(data, 2)
            geotiff.write(data, 3)
            geotiff.write(alpha, 4)
            

if __name__ == "__main__":
    create_cloude_mask()
