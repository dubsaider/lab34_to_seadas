import pycstruct

def readproj(file):
    file.seek(62, 0)
    type = int.from_bytes(file.read(1), 'little')
    file.seek(0)
    
    if type == 1:
        # Raw data
        pro_rawdata = pycstruct.StructDef(default_byteorder='little')

        # Main part
        pro_rawdata.add('uint8', 'format_type')
        pro_rawdata.add('utf-8', 'sat_name', length=13)
        pro_rawdata.add('uint32', 'sat_id')
        pro_rawdata.add('uint32', 'rev_num')
        pro_rawdata.add('uint16', 'begin_year')
        pro_rawdata.add('uint16', 'begin_day')
        pro_rawdata.add('uint32', 'begin_time')
        pro_rawdata.add('uint8', 'main_reserve_1', length=8)
        pro_rawdata.add('uint8', 'service', length=22)
        pro_rawdata.add('uint8', 'main_reserve_2', length=2)
        pro_rawdata.add('uint8', 'data_type', length=2)

        # HRPT
        pro_rawdata.add('uint16', 'frames_without_sync_glitch')
        pro_rawdata.add('uint16', 'frames_with_sync_glitch')
        pro_rawdata.add('uint16', 'frames_without_time_glitch')
        pro_rawdata.add('uint16', 'frames_with_time_glitch')
        pro_rawdata.add('uint16', 'gaps')
        pro_rawdata.add('uint16', 'string_desc')
        pro_rawdata.add('uint16', 'string_len')
        pro_rawdata.add('uint32', 'hrpt_mask')
        pro_rawdata.add('uint16', 'num_missed_pixel')
        pro_rawdata.add('uint16', 'num_pixel')
        pro_rawdata.add('uint16', 'turn_type')
        pro_rawdata.add('uint8', 'hrpt_reserve', length=40)

        # NORAD
        pro_rawdata.add('uint32', 'turn_num')
        pro_rawdata.add('uint16', 'set_num')
        pro_rawdata.add('uint16', 'ephemerid_type')
        pro_rawdata.add('uint16', 'turn_year')
        pro_rawdata.add('float64', 'day_based')
        pro_rawdata.add('float64', 'av_movement')
        pro_rawdata.add('float64', 'drag_term')
        pro_rawdata.add('float64', 'orbital_tilt')
        pro_rawdata.add('float64', 'ascending_node')
        pro_rawdata.add('float64', 'eccentricity')
        pro_rawdata.add('float64', 'perigee')
        pro_rawdata.add('float64', 'anomaly')
        pro_rawdata.add('uint8', 'norad_reserve', length=54)

        # Geographic correction data
        pro_rawdata.add('uint16', 'num_correction')
        pro_rawdata.add('int16', 'tbus')
        pro_rawdata.add('int16', 'time_correction')
        pro_rawdata.add('float64', 'roll')
        pro_rawdata.add('float64', 'pitch')
        pro_rawdata.add('float64', 'yaw')
        pro_rawdata.add('uint8', 'geo_reserve', length=226)

        # Deserialize
        pro = pro_rawdata.deserialize(file.read())

        return pro
    elif type == 2:
        # Single-channel data
        pro_single_channel = pycstruct.StructDef(default_byteorder='little')

        # Main part
        pro_single_channel.add('uint8', 'format_type')
        pro_single_channel.add('utf-8', 'sat_name', length=13)
        pro_single_channel.add('uint32', 'sat_id')
        pro_single_channel.add('uint32', 'rev_num')
        pro_single_channel.add('uint16', 'begin_year')
        pro_single_channel.add('uint16', 'begin_day')
        pro_single_channel.add('uint32', 'begin_time')
        pro_single_channel.add('uint8', 'main_reserve_1', length=8)
        pro_single_channel.add('uint8', 'service', length=22)
        pro_single_channel.add('uint8', 'main_reserve_2', length=2)
        pro_single_channel.add('uint8', 'data_type', length=2)

        # Single-channel
        pro_single_channel.add('uint32', 'process_stage')
        pro_single_channel.add('uint16', 'channel')
        pro_single_channel.add('uint16', 'stirng_size')
        pro_single_channel.add('uint16', 'max_string_len')
        pro_single_channel.add('uint16', 'num_missed_pixel')
        pro_single_channel.add('uint16', 'num_pixel')
        pro_single_channel.add('uint16', 'turn_type')
        pro_single_channel.add('int16', 'max_pixel')
        pro_single_channel.add('float64', 'coeff_a')
        pro_single_channel.add('float64', 'coeff_b')
        pro_single_channel.add('uint8', 'single_ch_reserve', length=30)

        # NORAD
        pro_single_channel.add('uint32', 'turn_num')
        pro_single_channel.add('uint16', 'set_num')
        pro_single_channel.add('uint16', 'ephemerid_type')
        pro_single_channel.add('uint16', 'turn_year')
        pro_single_channel.add('float64', 'day_based')
        pro_single_channel.add('float64', 'av_movement')
        pro_single_channel.add('float64', 'drag_term')
        pro_single_channel.add('float64', 'orbital_tilt')
        pro_single_channel.add('float64', 'ascending_node')
        pro_single_channel.add('float64', 'eccentricity')
        pro_single_channel.add('float64', 'perigee')
        pro_single_channel.add('float64', 'anomaly')
        pro_single_channel.add('uint8', 'norad_reserve', length=54)

        # Correction
        pro_single_channel.add('uint16', 'num_correction')
        pro_single_channel.add('int16', 'tbus')
        pro_single_channel.add('int16', 'time_correction')
        pro_single_channel.add('float64', 'roll')
        pro_single_channel.add('float64', 'pitch')
        pro_single_channel.add('float64', 'yaw')
        pro_single_channel.add('uint8', 'geo_reserve', length=226)

        # Deserialize
        pro =  pro_single_channel.deserialize(file.read())

        return pro
    elif type == 3:
        # Projections data
        pro_projection = pycstruct.StructDef(default_byteorder='little')

        # Main part
        pro_projection.add('uint8', 'format_type')
        pro_projection.add('utf-8', 'sat_name', length=13)
        pro_projection.add('uint32', 'sat_id')
        pro_projection.add('uint32', 'rev_num')
        pro_projection.add('uint16', 'begin_year')
        pro_projection.add('uint16', 'begin_day')
        pro_projection.add('uint32', 'begin_time')
        pro_projection.add('uint8', 'main_reserve_1', length=8)
        pro_projection.add('uint8', 'service', length=22)
        pro_projection.add('uint8', 'main_reserve_2', length=2)
        pro_projection.add('uint8', 'data_type', length=2)

        # Projections
        pro_projection.add('uint32', 'process_stage')
        pro_projection.add('uint16', 'channel')
        pro_projection.add('int16', 'max_pixel')
        pro_projection.add('uint16', 'projection_type')
        pro_projection.add('uint16', 'lines')
        pro_projection.add('uint16', 'pixels')
        pro_projection.add('float32', 'latitude')
        pro_projection.add('float32', 'longtitude')
        pro_projection.add('float32', 'lat_size')
        pro_projection.add('float32', 'lon_size')
        pro_projection.add('float32', 'lat_step')
        pro_projection.add('float32', 'lon_step')

        # Transformations to physical quantities
        pro_projection.add('float64', 'coeff_a')
        pro_projection.add('float64', 'coeff_b')
        pro_projection.add('uint8', 'reserve2', length=10)

        # NORAD
        pro_projection.add('uint32', 'turn_num')
        pro_projection.add('uint16', 'set_num')
        pro_projection.add('uint16', 'ephemerid_type')
        pro_projection.add('uint16', 'turn_year')
        pro_projection.add('float64', 'day_based')
        pro_projection.add('float64', 'av_movement')
        pro_projection.add('float64', 'drag_term')
        pro_projection.add('float64', 'orbital_tilt')
        pro_projection.add('float64', 'ascending_node')
        pro_projection.add('float64', 'eccentricity')
        pro_projection.add('float64', 'perigee')
        pro_projection.add('float64', 'anomaly')
        pro_projection.add('uint8', 'norad_reserve', length=54)

        # Correction
        pro_projection.add('uint16', 'num_correction')
        pro_projection.add('int16', 'tbus')
        pro_projection.add('int16', 'time_correction')
        pro_projection.add('float64', 'roll')
        pro_projection.add('float64', 'pitch')
        pro_projection.add('float64', 'yaw')
        pro_projection.add('uint8', 'geo_reserve', length=226)

        # Deserialize
        pro = pro_projection.deserialize(file.read())
        
        return pro
    else:
        # Telemetry data
        pro_telemetry = pycstruct.StructDef(default_byteorder='little')

        # Main part
        pro_telemetry.add('uint8', 'format_type')
        pro_telemetry.add('utf-8', 'sat_name', length=13)
        pro_telemetry.add('uint32', 'sat_id')
        pro_telemetry.add('uint32', 'rev_num')
        pro_telemetry.add('uint16', 'begin_year')
        pro_telemetry.add('uint16', 'begin_day')
        pro_telemetry.add('uint32', 'begin_time')
        pro_telemetry.add('uint8', 'main_reserve_1', length=8)
        pro_telemetry.add('uint8', 'service', length=22)
        pro_telemetry.add('uint8', 'main_reserve_2', length=2)
        pro_telemetry.add('uint8', 'data_type', length=2)

        # AVHRR NOAA HRPT
        pro_telemetry.add('uint16', 'string_num')
        pro_telemetry.add('uint16', 'channel_num')
        pro_telemetry.add('uint8', 'avhrr_reserve', length=444)

        # Deserialize
        pro = pro_telemetry.deserialize(file.read())

        return pro
