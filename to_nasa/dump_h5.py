import h5py
import matplotlib.pyplot as plt

#f = h5py.File('result/GITCO_j01_d20210302_t0439540_e0449495_b17023_c20210324053346229874_cspp_dev.h5', 'r')
f = h5py.File('result/SVM01_j01_d20210302_t0439540_e0449495_b17023_c20210324053508522635_cspp_dev.h5', 'r')

for k, v in f['All_Data']['VIIRS-M1-SDR_All'].items():
    print(k, v)

plt.imshow(f['All_Data']['VIIRS-M1-SDR_All']['QF1_VIIRSMBANDSDR'], interpolation='none')
plt.show()
