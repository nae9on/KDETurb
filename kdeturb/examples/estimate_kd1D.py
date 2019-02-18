#----------------------------------import built-in modules-----------------------------------------
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
from socket import gethostname
import sys
import timeit

#----------------------------import projects internal modules--------------------------------------
sys.path.insert(0, "/home/akadar/git/kdeturb")
from kdeturb.read import hdf5read
from kdeturb.statistics import findkernel

begin_program = timeit.default_timer()

#Get the host system name
host = gethostname()
print ("Working on ", host, "computer\n")

#Set Input/Output filename
input_file = "./output/pseudo.h5"
output_file = "./data.csv"

print ("Input file "+input_file+"\n")
print ("Output file "+output_file+"\n")

timekeylist = hdf5read.getDatasetKeys(input_file,0)

p1 = np.array([5, 6, 0])

data_list = hdf5read.slice_dataset(input_file,'U',timekeylist,p1,p1)

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