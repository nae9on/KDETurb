#----------------------------------import built-in modules-----------------------------------------
import numpy as np
from socket import gethostname
import sys
import timeit

#----------------------------import projects internal modules--------------------------------------
sys.path.insert(0, "/home/akadar/git/kdeturb")
from kdeturb.read import hdf5read
from kdeturb.statistics import correlation

begin_program = timeit.default_timer()

#Get the host system name
host = gethostname()
print ("Working on ", host, "computer\n")

#Set Input/Output filename
input_file = "./output/pseudo.h5"
output_file = "./data.csv"

print ("Input file "+input_file+"\n")
print ("Output file "+output_file+"\n")

#hdf5read.hdf5info(input_file)

p1 = np.array([5, 6, 0])
p2 = np.array([5, 6, 50])
mid = np.array([5, 6, 25])

keys = hdf5read.getGroupKeys(input_file)
print("Keys ",keys,"\n")

timekeylist = hdf5read.getDatasetKeys(input_file,0)
print("No of time files = ",timekeylist.__len__(),"\n")

mean = correlation.mean(input_file,timekeylist,'L1',p1,p2)
print("calculated mean\n")

variance = correlation.variance(input_file,timekeylist,'L1',p1,p2)
print("calculated variance\n")

Rij = correlation.Rij(input_file,timekeylist,'L1','L2',mid,p1,p2)
print("calculated correlation\n")

X = np.arange(51).reshape(51,1)
Y1 = mean.reshape(51,1)
Y2 = variance.reshape(51,1)
Y3 = Rij.reshape(51,1)

data2write = np.concatenate((X,Y1,Y2,Y3),axis=1)
np.savetxt(output_file, data2write, delimiter=',', header="Index,Mean,Variance,Rij", comments="")

print("writing completed")

end_program = timeit.default_timer()

print ("Total Run Time = "+"%.2f" % (end_program-begin_program)+" sec")



