import pycstruct


def read_main_part(file):
    main_part = pycstruct.StructDef(default_byteorder='little')
    main_part.add('uint8', 'format_type')
    main_part.add('utf-8', 'sat_name', length=13)
    main_part.add('uint32', 'sat_id')
    main_part.add('uint32', 'rev_num')
    main_part.add('uint16', 'begin_year')
    main_part.add('uint16', 'begin_day')
    main_part.add('uint32', 'begin_time')
    main_part.add('uint8', 'main_reserve_1', length=8)
    main_part.add('uint8', 'service', length=22)
    main_part.add('uint8', 'main_reserve_2', length=2)
    main_part.add('uint8', 'data_type', length=2)
    return main_part.deserialize(file.read(64))

def read_norad_part(file):
    norad_part = pycstruct.StructDef(default_byteorder='little')
    norad_part.add('uint32', 'turn_num')
    norad_part.add('uint16', 'set_num')
    norad_part.add('uint16', 'ephemerid_type')
    norad_part.add('uint16', 'turn_year')
    norad_part.add('float64', 'day_based')
    norad_part.add('float64', 'av_movement')
    norad_part.add('float64', 'drag_term')
    norad_part.add('float64', 'orbital_tilt')
    norad_part.add('float64', 'ascending_node')
    norad_part.add('float64', 'eccentricity')
    norad_part.add('float64', 'perigee')
    norad_part.add('float64', 'anomaly')
    norad_part.add('uint8', 'norad_reserve', length=54)
    return norad_part.deserialize(file.read(128))

def read_correction_part(file):
    correction_part = pycstruct.StructDef(default_byteorder='little')
    correction_part.add('uint16', 'num_correction')
    correction_part.add('int16', 'tbus')
    correction_part.add('int16', 'time_correction')
    correction_part.add('float64', 'roll')
    correction_part.add('float64', 'pitch')
    correction_part.add('float64', 'yaw')
    correction_part.add('uint8', 'geo_reserve', length=226)
    return correction_part.deserialize(file.read(256))

def read_hrpt_part(file):
    hrpt_part = pycstruct.StructDef(default_byteorder='little')
    hrpt_part.add('uint16', 'frames_without_sync_glitch')
    hrpt_part.add('uint16', 'frames_with_sync_glitch')
    hrpt_part.add('uint16', 'frames_without_time_glitch')
    hrpt_part.add('uint16', 'frames_with_time_glitch')
    hrpt_part.add('uint16', 'gaps')
    hrpt_part.add('uint16', 'string_desc')
    hrpt_part.add('uint16', 'string_len')
    hrpt_part.add('uint32', 'hrpt_mask')
    hrpt_part.add('uint16', 'num_missed_pixel')
    hrpt_part.add('uint16', 'num_pixel')
    hrpt_part.add('uint16', 'turn_type')
    hrpt_part.add('uint8', 'hrpt_reserve', length=40)
    return hrpt_part.deserialize(file.read(30))

def read_single_channel_part(file):
    single_channel_part = pycstruct.StructDef(default_byteorder='little')
    single_channel_part.add('uint32', 'process_stage')
    single_channel_part.add('uint16', 'channel')
    single_channel_part.add('uint16', 'string_size')
    single_channel_part.add('uint16', 'max_string_len')
    single_channel_part.add('uint16', 'num_missed_pixel')
    single_channel_part.add('uint16', 'num_pixel')
    single_channel_part.add('uint16', 'turn_type')
    single_channel_part.add('int16', 'max_pixel')
    single_channel_part.add('float64', 'coeff_a')
    single_channel_part.add('float64', 'coeff_b')
    single_channel_part.add('uint8', 'single_ch_reserve', length=30)
    return single_channel_part.deserialize(file.read(42))

def read_projection_part(file):
    projection_part = pycstruct.StructDef(default_byteorder='little')
    projection_part.add('uint32', 'process_stage')
    projection_part.add('uint16', 'channel')
    projection_part.add('int16', 'max_pixel')
    projection_part.add('uint16', 'projection_type')
    projection_part.add('uint16', 'lines')
    projection_part.add('uint16', 'pixels')
    projection_part.add('float32', 'latitude')
    projection_part.add('float32', 'longtitude')
    projection_part.add('float32', 'lat_size')
    projection_part.add('float32', 'lon_size')
    projection_part.add('float32', 'lat_step')
    projection_part.add('float32', 'lon_step')
    projection_part.add('float64', 'coeff_a')
    projection_part.add('float64', 'coeff_b')
    projection_part.add('uint8', 'reserve2', length=10)
    return projection_part.deserialize(file.read(64))

def read_telemetry_part(file):
    telemetry_part = pycstruct.StructDef(default_byteorder='little')
    telemetry_part.add('uint16', 'string_num')
    telemetry_part.add('uint16', 'channel_num')
    telemetry_part.add('uint8', 'avhrr_reserve', length=444)
    return telemetry_part.deserialize(file.read(446))

# Функция для побитового считывания паспорта файла .pro.
# Подробное описание паспорта и самого формата .pro, можно найти на сайте: http://www.satellite.dvo.ru/gate.html?name=Content&pa=showpage&pid=14
def readproj(file):
    file.seek(62, 0) # Переносим указатель 62 бита, чтобы определить тип данных файла .pro.
    type = int.from_bytes(file.read(1), 'little') # Считываем бит занятый под оперделение типа фала .pro.
    file.seek(0)
    
    main_part = read_main_part(file)

    if type == 1:
        hrpt_part = read_hrpt_part(file)
        norad_part = read_norad_part(file)
        correction_part = read_correction_part(file)
        return {**main_part, **hrpt_part, **norad_part, **correction_part}
    elif type == 2:
        single_channel_part = read_single_channel_part(file)
        norad_part = read_norad_part(file)
        correction_part = read_correction_part(file)
        return {**main_part, **single_channel_part, **norad_part, **correction_part}
    elif type == 3:
        projection_part = read_projection_part(file)
        norad_part = read_norad_part(file)
        correction_part = read_correction_part(file)
        return {**main_part, **projection_part, **norad_part, **correction_part}
    else:
        telemetry_part = read_telemetry_part(file)
        return {**main_part, **telemetry_part}
