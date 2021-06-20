import numpy as np
import netCDF4

def copy_group(src, dst):
    for name in src.ncattrs():
        dst.setncattr(name, src.getncattr(name))

    for name, dimension in src.dimensions.items():
        dst.createDimension(name, len(dimension) if not dimension.isunlimited() else None)

    for name, variable in src.variables.items():
        if name.startswith('M') and 'uncert' in name:
        #if name != 'M01':
            continue

        print(name)

        y = dst.createVariable(
            name,
            variable.datatype,
            variable.dimensions,
            fill_value=getattr(variable, '_FillValue', None),
            zlib=False,
            endian=variable.endian()
        )
        for n in variable.ncattrs():
            if n != '_FillValue':
                y.setncattr(n, variable.getncattr(n))
        y[:] = variable[:]

    for name, group in src.groups.items():
        dstgroup = dst.createGroup(name)
        copy_group(group, dstgroup)


with (
            netCDF4.Dataset('V2021105041200.L1B-M_JPSS1.nc', 'r') as src,
            netCDF4.Dataset('stripped.nc', 'w', format='NETCDF4') as dst
        ):
    copy_group(src, dst)
