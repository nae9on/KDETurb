#----------------------------------import built-in modules-----------------------------------------
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

#----------------------------import projects internal modules--------------------------------------
#sys.path.insert(0, "/home/akadar/git/kdeturb")
from kdeturb import kdeTurb
from kdeturb.statistics import findkernel
from kdeturb.read import hdf5read

input_path = "D:/kdeturb/ref3D_Coarse"
output_path = "D:/kdeturb/output"
obj = kdeTurb(input_path, output_path)

p1 = np.array([5, 6, 0])

data_list = hdf5read.slice_dataset(obj.h5file,'SF1',obj.timelist,p1,p1)

N = data_list.shape[0]

data_list = data_list.reshape(N,1)

np.random.seed(1)

kernel = 'gaussian'
normalized_data, n_samples, density = findkernel.data1D(data_list,kernel)

true_dens = norm(0, 1).pdf(n_samples[:, 0])

fig, ax = plt.subplots()
ax.fill(n_samples, true_dens, fc='black', alpha=0.2, label='guess distribution')
ax.plot(n_samples, density, '-', label="kernel = '{0}'".format(kernel))
ax.text(2, 0.4, "N={0} points".format(N))
ax.legend(loc='upper left')
ax.plot(normalized_data, -0.005 - 0.01 * np.random.random(N), '+k')

plt.show()