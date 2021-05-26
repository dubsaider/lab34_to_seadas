import h5py
import matplotlib.pyplot as plt

from graph import plot

f = h5py.File('result/GITCO_j01_d20210302_t0439540_e0449495_b17023_c20210324053346229874_cspp_dev.h5', 'r')

print(f['All_Data']['VIIRS-IMG-GEO-TC_All']['Height'])

plt.imshow(f['All_Data']['VIIRS-IMG-GEO-TC_All']['Height'], interpolation='none')
plt.show()
