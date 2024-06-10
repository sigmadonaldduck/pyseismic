import sys, site

site_packages = site.getsitepackages()

for path in site_packages:
    sys.path.append(path)

import segyio, segpy
import matplotlib.pyplot as plt

with segyio.open('.\\data_synthesis\\real_gather.sgy', 'r', strict = False) as segy_file:
    trace_data = segyio.tools.collect(segy_file.trace[:])
    
    plt.imshow(trace_data, cmap = 'seismic', aspect = 'auto')
    plt.xlabel('Trace Number')
    plt.ylabel('Sample Numebr')
    plt.title('SEGY File')
    plt.colorbar()
    plt.show()