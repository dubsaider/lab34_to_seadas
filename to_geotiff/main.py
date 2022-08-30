import argparse
from os.path import commonprefix

import numpy as np
import rasterio
from pyproj import Transformer

import proformat.readpro as pro


parser = argparse.ArgumentParser()
parser.add_argument('in_', metavar='in', nargs='+',
                    help='Один или несколько входных файлов в формате .pro.')
parser.add_argument('out',
                    help='Имя выходного файла в формате GeoTIFF.')
args = parser.parse_args()


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

    data_scaled = data * a + b  # Приведение растровых данных к физическим величинам, чтобы данные отражали характеристики полученного продукта.

    # Восстановим отрицательные (специальные) значения до применения
    # коэффициентов приведения, чтобы сохранить их для возможной
    # дальнейшей обработки.  При записи файла будет также записана
    # nodata маска, которая будет построена по знаку значения.

    # Известные (мне) специальные значения:
    # -5   : облака
    # -7   : земля
    # -100 : ???
    data_scaled[data < 0] = data[data < 0]

    data = data_scaled.reshape(rows, cols)

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
def create_geotiff():
    file_name = args.out
    if not (file_name.endswith('.tif') or file_name.endswith('.tiff')):
        file_name += '.tif'

    # Нам нужно знать, каких размеров нужно создать geotiff, поэтому
    # паспорт первого входного файла дополнительно считываем заранее.
    with open(args.in_[0], 'rb') as pro_file:
        pro_passport_first = parse_pro_passport(pro_file)

    # Для красоты уберём общий префикс и расширение из названия слоя.
    if len(args.in_) > 1:
        band_names = [n.split('.') for n in args.in_]
        p = commonprefix(band_names)
        band_names = [
            '.'.join(n[len(p):-1] if n[-1] == 'pro' else n[len(p):])
            for n in band_names
        ]

    # TODO скопировать больше (все?) данных из паспорта в теги geotiff

    with rasterio.Env(GDAL_TIFF_INTERNAL_MASK=True):
        with rasterio.open(
                file_name, 'w',
                driver='GTiff',
                height=pro_passport_first['lines'],
                width=pro_passport_first['pixels'],
                count=len(args.in_), dtype='float64',
                crs='EPSG:3395', transform=affine_matrix(pro_passport_first),
                compress='deflate', num_threads='all_cpus'
                ) as geotiff:

            mask = np.full(
                (pro_passport_first['lines'], pro_passport_first['pixels']),
                True
            )

            for i, (pro_file_name, band_name) in \
                    enumerate(zip(args.in_, band_names), start=1):
                if not pro_file_name.endswith('.pro'):
                    print(pro_file_name + ' не имеет расширение .pro')

                with open(pro_file_name, 'rb') as pro_file:
                    pro_passport = parse_pro_passport(pro_file)

                    diff = '\n'.join(
                        '{k}: {v1} != {v2}'.format(
                            k=k,
                            v1=pro_passport[k],
                            v2=pro_passport_first[k]
                        )
                        for k in pro_passport.keys()
                        if pro_passport[k] != pro_passport_first[k]
                        and k not in {'coeff_a', 'coeff_b', 'max_pixel'}
                        # Я не знаю, почему резервные поля могут
                        # отличаться, но это так.  На моих данных
                        # отличался только norad_reserve, но я на всякий
                        # случай включил все резервные поля.
                        and not k.endswith('_reserve')
                    )
                    if diff:
                        raise ValueError(
                            'Паспорта входных файлов не совпадают:\n' + diff
                        )

                    data = parse_pro_data(pro_file, pro_passport)

                # rasterio doesn't have the best API ok
                geotiff.write(data, i)
                geotiff.set_band_description(i, band_name)

                mask &= data > 0

            geotiff.write_mask(mask)


if __name__ == '__main__':
    create_geotiff()
