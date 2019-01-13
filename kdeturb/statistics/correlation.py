r"""
This module defines the following functions::

  - mean:
  
    This function computes the mean.

  - variance:
  
    This function computes the variance.
   
  - Rxx
  
    This function computes the correlations in space 
             
Note::

    The data is extracted from hdf5 file format.
 
"""

#----------------------------------import built-in modules-----------------------------------------
import numpy as np

#----------------------------import projects internal modules--------------------------------------
from kdeturb.read import hdf5read

def mean(filename,varname,timekeylist,p1,p2):
    for i in np.arange(p1.size):
        if(p1[i]>p2[i]):
            p1[i],p2[i]=p2[i],p1[i] #swap
            
    fo = hdf5read.getHDF5FileHandle(filename)
    
    mysum = np.zeros(p2-p1+1);
    
    numfiles = timekeylist.__len__()
    
    for time in timekeylist:
        name = varname + '/' + str(time)
        #print('Read file '+name)
        mysum = mysum + fo[name][p1[0]:p2[0]+1,p1[1]:p2[1]+1,p1[2]:p2[2]+1]

    mean = mysum/numfiles
    return mean

def variance(filename,varname,timekeylist,p1,p2):
    for i in np.arange(p1.size):
        if(p1[i]>p2[i]):
            p1[i],p2[i]=p2[i],p1[i] #swap
            
    fo = hdf5read.getHDF5FileHandle(filename)
    
    mysum = np.zeros(p2-p1+1);
    
    numfiles = timekeylist.__len__()
    
    for time in timekeylist:
        name = varname + '/' + str(time)
        #print('Read file '+name)
        mysum = mysum + np.square(fo[name][p1[0]:p2[0]+1,p1[1]:p2[1]+1,p1[2]:p2[2]+1])

    variance = mysum/numfiles
    return variance

def Rxx(filename,varname,timekeylist,p1,p2,mid):
    for i in np.arange(p1.size):
        if(p1[i]>p2[i]):
            p1[i],p2[i]=p2[i],p1[i] #swap
            
    fo = hdf5read.getHDF5FileHandle(filename)
    
    mysum = np.zeros(p2-p1+1)
    norm1 = 0
    norm2 = np.zeros(p2-p1+1)
    
    numfiles = timekeylist.__len__()
    
    for time in timekeylist:
        name = varname + '/' + str(time)
        #print('Read file '+name)
        pivot = fo[name][mid[0]:mid[0]+1,mid[1]:mid[1]+1,mid[2]:mid[2]+1]
        mysum = mysum + pivot*fo[name][p1[0]:p2[0]+1,p1[1]:p2[1]+1,p1[2]:p2[2]+1]
        norm1 = norm1 + pivot*pivot;
        norm2 = norm2 + np.square(fo[name][p1[0]:p2[0]+1,p1[1]:p2[1]+1,p1[2]:p2[2]+1])

    mysum = mysum/numfiles
    norm1 = norm1/numfiles
    norm2 = norm2/numfiles
    
    Rxx = np.divide(mysum,np.sqrt(norm1)*np.sqrt(norm2))
    return Rxx
