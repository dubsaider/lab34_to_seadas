import proformat.readpro as pro
from rasterio.plot import show
from pyproj import Transformer
import numpy as np
import rasterio
import sys


# Функция для чтения формата данных .pro и последующего создания
# словаря языка Python со всеми данными, которые хранятся в паспорте файла .pro.
def parse_pro_passport(file):
    return pro.readproj(file) # Преобразования файла формата .pro в словаря языка Python.


# Функция для считывания растровых данных и приведению данных к физическим величинам. 
def parse_pro_data(file, pro_passport):
    file.seek(511, 0) # Смещаем указать на длину поспорта файла .pro, для того, чтобы считать только растровые данные.
    data = np.fromfile(file, dtype='uint16') # Считывание растровых данных с файла с форматом .pro.

    a = pro_passport['coeff_a'] # Коэффициент пересчета значений A
    b = pro_passport['coeff_b'] # Коэффициент пересчета значений B
    rows = pro_passport['lines'] # Количество строк
    cols = pro_passport['pixels'] # Количество пикселов в строке

    data = ((data / 256) * a) + b # Приведение растровых данных к физическим величинам.
    data = data.reshape(rows, cols) # Изменение формы массива данных, форма массива указана в паспорте файла .pro.
    
    return np.flipud(data) # Переворачиваем массив по веритали, для более привычного отображенияю.


# Создание матрицы аффинного преобразования.
def affine_matrix(pro_passport):
    tf = Transformer.from_crs("EPSG:4326", "EPSG:3395", always_xy=True) # Создадим трансформатор перевода из системы координат EPSG:4326 (используется в .pro) в
                                                                        # меркатор EPSG:3395.

    lon = pro_passport['longtitude'] # Долгота
    lat = pro_passport['latitude'] # Широта
    latsize = pro_passport['lat_size'] # Шаг по широте
    lonsize = pro_passport['lon_size'] # Шаг по долготе
    rows = pro_passport['lines'] # Количество строк
    cols = pro_passport['pixels'] # Количество пикселов в строке

    bottom_right = tf.transform(lon + lonsize, lat) # Находим правую нижнюю координату в системе EPSG:3395.
    top_left = tf.transform(lon, lat + latsize) # Находим левую верхнюю координату в системе EPSG:3395.
    lonres = (bottom_right[0] - top_left[0]) / cols # Находим сколько нужно отступать долготы на каждый пиксель, что бы присвоить каждому пикселю свою долготу.
    latres = (top_left[1] - bottom_right[1]) / rows # Находим сколько нужно отступать широты на каждый пиксель, что бы присвоить каждому пикселю свою широту.

    lon = top_left[0] # Долгота левой верхней координаты в системе EPSG:3395.
    lat = top_left[1] # Широта левой верхней координаты в системе EPSG:3395.

    return rasterio.transform.from_origin(lon, lat, lonres, latres) # Создаем матрицу аффинного преобразования.


# Функция для создания GeoTIFF файла из файла с форматом .pro.
def create_geotiff(file_name, data, affine_mat, pro_passport):
    file_name += '.tif' # Создаем имя фала с форматом файла .tif.
    geotiff = rasterio.open(                          # Создаем GeoTIFF файл.
                    file_name, 'w', driver='GTiff', 
                    height=pro_passport['lines'], width=pro_passport['pixels'], 
                    count=1, dtype=data.dtype, 
                    crs='EPSG:3395', transform=affine_mat)

    geotiff.write(data, 1) # Записываем растровые данные в созданный GeoTIFF файл.
    geotiff.close() # Заканчиваем работу с созданием GeoTIFF файла.


pro_file_name = sys.argv[1] # Считываем имя файла в формате .pro с консоли.
pro_file = open(pro_file_name, 'rb') # Читаем файл .pro

pro_passport = parse_pro_passport(pro_file) # Считываем паспорт файла .pro.
data = parse_pro_data(pro_file, pro_passport) # Считываем растровые данные файла .pro.

affine_mat = affine_matrix(pro_passport) # Создаём матрицу аффинного преобразования.
create_geotiff('geotiff_file', data, affine_mat, pro_passport) # Создаём GeoTIFF файл.