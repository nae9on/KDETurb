#----------------------------------import built-in modules-----------------------------------------
from socket import gethostname
import sys
import timeit

#----------------------------import projects internal modules--------------------------------------
sys.path.insert(0, "/home/akadar/git/kdeturb")
from kdeturb.read import hdf5read
from kdeturb.statistics import basicstats

begin_program = timeit.default_timer()

#Get the host system name
host = gethostname()
print ("Working on", host, "computer\n")

#Set Input/Output filename
input_file = "/media/sf_Desktop/debug_sngm/output/pcf0.h5"
output_file = "./pc.vtk"

print ("Input file "+input_file+"\n")
print ("Output file "+output_file+"\n")

#hdf5read.hdf5info(input_file)

keys = hdf5read.getGroupKeys(input_file)
print("Keys ",keys,"\n")

timekeylist = hdf5read.getDatasetKeys(input_file,0)
print("No of time files = ",timekeylist.__len__(),"\n")

mean = basicstats.mean(input_file,'PC',timekeylist)
print("Calculated mean\n")

