r"""
This module defines the following functions::

  - mean:
  
    This function computes the mean.

  - variance:
  
    This function computes the variance.
   
  - Rxx
  
    This function computes the correlations in space 

"""

#----------------------------------import built-in modules-----------------------------------------
import numpy as np

#----------------------------import projects internal modules--------------------------------------
from kdeturb.read import hdf5read

def mean(filename,ui,timekeylist,x1=None,x2=None):
    if x1 is None:
        x1 = np.array([0, 0, 0])
    if x2 is None:
        fo = hdf5read.getFileHandle(filename)
        # Convert from tuple to numpy array
        x2 = np.asarray(fo[ui][timekeylist[0]].shape)-1       
    return one_point_stats(filename,ui,timekeylist,x1,x2,1)

def variance(filename,ui,timekeylist,x1,x2):
    return one_point_stats(filename,ui,timekeylist,x1,x2,2)

def one_point_stats(filename,ui,timekeylist,x1,x2,p):
    r"""
    :param filename: HDF5 filename
    :param ui: ui(x,t)
    :param timekeylist: list of all the time values
    :param x1: begin of x
    :param x2: end of x
    :param p: power to be raised with
    :return: ``one_point_stats`` -- numpy ndarray with one point statistics
        
    Procedure::
    
     one_point_stats = <ui(x,t)^p>
    
    """
    for i in np.arange(x1.size):
        if(x1[i]>x2[i]):
            x1[i],x2[i]=x2[i],x1[i] #swap
            
    fo = hdf5read.getFileHandle(filename)
    
    print("Dataspace ",fo[ui][timekeylist[0]].shape)
    
    mysum = np.zeros(x2-x1+1)
    
    numfiles = timekeylist.__len__()
    
    itr = 1
    
    for time in timekeylist:
        
        name = ui + '/' + str(time)
        if (itr==1 or itr==numfiles or itr%100==0):
            print('Reading file '+name)

        uixt = fo[ui][time][x1[0]:x2[0]+1,x1[1]:x2[1]+1,x1[2]:x2[2]+1]
        mysum = mysum + np.power(uixt,p)
        itr = itr + 1

    mysum = mysum/numfiles
    
    return mysum

def Rij(filename,ui,uj,timekeylist,x,r1,r2):
    r"""
    :param filename: HDF5 filename
    :param ui: ui(x,t)
    :param uj: uj(x+r,t)
    :param timekeylist: list of all the time values
    :param x: pivot point
    :param r1: begin of r
    :param r2: end of r
    :return: ``Rij`` -- numpy ndarray with correlations
        
    Procedure::
    
     Rij = <ui(x,t)*uj(x+r,t)>
    
    """
    for i in np.arange(r1.size):
        if(r1[i]>r2[i]):
            r1[i],r2[i]=r2[i],r1[i] #swap
            
    fo = hdf5read.getFileHandle(filename)
    
    print("Dataspace ",fo[ui][timekeylist[0]].shape)
    
    print('The pivot is '+ui)
    
    mysum = np.zeros(r2-r1+1)
    norm1 = 0
    norm2 = np.zeros(r2-r1+1)
    
    numfiles = timekeylist.__len__()
    
    itr = 1
    
    for time in timekeylist:
        
        name1 = ui + '/' + str(time)
        name2 = uj + '/' + str(time)
        if (itr==1 or itr==numfiles or itr%100==0):
            print('Reading files '+name1+' and '+name2)

        uixt = fo[ui][time][x[0]:x[0]+1,x[1]:x[1]+1,x[2]:x[2]+1]
        ujxrt = fo[uj][time][r1[0]:r2[0]+1,r1[1]:r2[1]+1,r1[2]:r2[2]+1]
        mysum = mysum + uixt*ujxrt
        norm1 = norm1 + np.square(uixt);
        norm2 = norm2 + np.square(ujxrt)
        itr = itr + 1

    mysum = mysum/numfiles
    norm1 = norm1/numfiles
    norm2 = norm2/numfiles
    
    Rij = np.divide(mysum,np.sqrt(norm1*norm2))
    return Rij
