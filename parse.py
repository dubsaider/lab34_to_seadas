import sys

import pycstruct

pro = pycstruct.StructDef(default_byteorder='little')
pro.add('uint8', 'type')
pro.add('utf-8', 'name', length=13)
pro.add('uint32', 'identificator')
pro.add('uint32', 'pass')
pro.add('uint16', 'begin_year')
pro.add('uint16', 'begin_day')
pro.add('uint32', 'begin_time')
pro.add('uint8', 'reserve', length=8)
pro.add('uint8', 'service', length=22)
pro.add('uint8', 'reserve1', length=2)
pro.add('uint8', 'data_type', length=2)

pro.add('uint32', 'process_stage')
pro.add('uint16', 'channel')
pro.add('int16', 'max')
pro.add('uint16', 'projection_type')
pro.add('uint16', 'lines')
pro.add('uint16', 'pixels')
pro.add('float32', 'latitude')
pro.add('float32', 'longtitude')
pro.add('float32', 'lat_size')
pro.add('float32', 'lon_size')
pro.add('float32', 'lat_step')
pro.add('float32', 'lon_step')

pro.add('float64', 'coeff_a')
pro.add('float64', 'coeff_b')
pro.add('uint8', 'reserve2', length=10)

pro.add('uint32', 'pass_number')
pro.add('uint16', 'element_set_number')
pro.add('uint16', 'ephemeride_type')
pro.add('uint16', 'year2')
pro.add('float64', 'day2')
pro.add('float64', 'movement')
pro.add('float64', 'resistance')
pro.add('float64', 'inclination')
pro.add('float64', 'sfnsfna')
pro.add('float64', 'eccentricity')
pro.add('float64', 'perigee')
pro.add('float64', 'anomaly')
pro.add('uint8', 'reserve3', length=54)

pro.add('uint16', 'correction_version_number')
pro.add('int16', 'clock_TBUS_correction')
pro.add('int16', 'clock_correction')
pro.add('float64', 'roll')
pro.add('float64', 'pitch')
pro.add('float64', 'yaw')
pro.add('uint8', 'reserve4', length=226)

if __name__ == '__main__':
    with open(sys.argv[1], 'rb') as f:
        res = pro.deserialize(f.read())

    for k, v in res.items():
        print(k, v)
