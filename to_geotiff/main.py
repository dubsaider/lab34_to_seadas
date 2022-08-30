import proformat.readpro as pro
from pyproj import Transformer
import numpy as np
import rasterio
import sys


# Функция для чтения формата данных .pro и последующего создания
# словаря языка Python со всеми данными, которые хранятся в паспорте файла .pro.
# Паспорт - это часть файла .pro содержащая в себе данные, характеризующие сценарий работы с растровыми и географическими данными.
def parse_pro_passport(file):
    return pro.readproj(file)


# Функция для считывания растровых данных и приведению данных к физическим величинам.
def parse_pro_data(file, pro_passport):
    file.seek(512, 0)
    data = np.fromfile(file, dtype='<i2')

    a = pro_passport['coeff_a']
    b = pro_passport['coeff_b']
    rows = pro_passport['lines']
    cols = pro_passport['pixels']

    data = data * a + b  # Приведение растровых данных к физическим величинам, чтобы данные отражали характеристики полученного продукта.
    data = data.reshape(rows, cols)
    
    # До преобразования:
    # -5 : нет данных
    # -7 : земля
    data[data < 0] = np.nan

    return np.flipud(data) # Переворачиваем массив по веритали, для более привычного отображенияю.


# Создание матрицы аффинного преобразования.
def affine_matrix(pro_passport):
    tf = Transformer.from_crs("EPSG:4326", "EPSG:3395", always_xy=True) # Создадим трансформатор перевода из системы координат EPSG:4326 (используется в .pro) в
                                                                        # меркатор EPSG:3395.

    lon = pro_passport['longtitude']
    lat = pro_passport['latitude']
    latsize = pro_passport['lat_size']
    lonsize = pro_passport['lon_size']
    rows = pro_passport['lines']
    cols = pro_passport['pixels']

    bottom_right = tf.transform(lon + lonsize, lat)
    top_left = tf.transform(lon, lat + latsize)
    lonres = (bottom_right[0] - top_left[0]) / cols # Находим сколько нужно отступать долготы на каждый пиксель, что бы присвоить каждому пикселю свою долготу.
    latres = (top_left[1] - bottom_right[1]) / rows # Находим сколько нужно отступать широты на каждый пиксель, что бы присвоить каждому пикселю свою широту.

    lon = top_left[0] # Долгота левой верхней координаты в системе EPSG:3395.
    lat = top_left[1] # Широта левой верхней координаты в системе EPSG:3395.

    return rasterio.transform.from_origin(lon, lat, lonres, latres)


# Функция для создания GeoTIFF файла из файла с форматом .pro.
def create_geotiff(file_name):
    pro_file_name = sys.argv[1] # Считываем имя файла в формате .pro с консоли.
    pro_file = open(pro_file_name, 'rb')

    pro_passport = parse_pro_passport(pro_file)
    data = parse_pro_data(pro_file, pro_passport)
    affine_mat = affine_matrix(pro_passport)
    
    file_name += '.tif'
    geotiff = rasterio.open(                          # Создаем GeoTIFF файл.
                    file_name, 'w', driver='GTiff', 
                    height=pro_passport['lines'], width=pro_passport['pixels'], 
                    count=1, dtype=data.dtype, 
                    crs='EPSG:3395', transform=affine_mat)

    geotiff.write(data, 1)
    geotiff.close()


create_geotiff(sys.argv[2])
