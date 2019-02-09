r"""
This module defines the following functions::

  - hdf5info:
  
    This function prints entire HDF5 file/group structure using recursive method.
    
Note::

 The data is extracted from hdf5 file format.
 
"""

#----------------------------------import built-in modules-----------------------------------------
import h5py
import numpy as np

#----------------------------import projects internal modules--------------------------------------

#Define exceptions
class HDF5Error(Exception):
    """Base class for exceptions in this module."""
    pass

class Input_HDF5Error(HDF5Error):
    """Exception raised for errors in the user input."""
    pass
    
def hdf5info(filename):
    r"""
    :param filename: Full path of the HDF5 file
    :return:
    :raises: ``SOLVER_BadInputError``, When HDF5 file does not exist
    
    Example::
    
     .
    
    """
    try:
        with open(filename):
            fo = h5py.File(filename, 'r')
            print_hdf5structure(fo)
            fo.close()
    except FileNotFoundError as fnf:
        print(fnf)
    except OSError as ose:
        print(ose)    
     
def print_hdf5structure(fo):
    if(isinstance(fo, h5py.Group)):               
        keylist = list(fo.keys())
        valuelist = list(fo.values())
        #print("\n")
        print("No of keys = ", keylist.__len__())
        if(keylist.__len__()>100):
            print("Keylist: ", keylist[0],keylist[1],'....',keylist[keylist.__len__()-2],
                  keylist[keylist.__len__()-1])
        else:
            print("Keylist: ", keylist)
        if(isinstance(valuelist[0], h5py.Dataset)==False): print("\n");
        print_hdf5structure(valuelist[0])
    elif(isinstance(fo, h5py.Dataset)):            
        print("dtype: ", fo.dtype)
        print("shape: ", fo.shape)
        print("\n")
    else:
        print("Unknown HDF5 item: ",fo)
        
def getFileHandle(filename):
    fo = h5py.File(filename, 'r')
    return fo

def getGroupKeys(filename):
    fo = h5py.File(filename, 'r')
    return list(fo.keys())

def getGroupList(filename):
    fo = h5py.File(filename, 'r')
    return list(fo.values())

def getGroup(filename,varno):
    fo = h5py.File(filename, 'r')
    return list(fo.values())[varno]

def getDatasetKeys(filename,varno):
    fo = h5py.File(filename, 'r')
    return list(list(fo.values())[varno].keys())

def getDatasetList(filename,varno):
    fo = h5py.File(filename, 'r')
    return list(list(fo.values())[varno].values())

def getDataset(filename,varno,timeitr):
    fo = h5py.File(filename, 'r')
    return list(list(fo.values())[varno].values())[timeitr]

def slice_dataset(filename,ui,timekeylist,x1,x2):
    for i in np.arange(x1.size):
        if(x1[i]>x2[i]):
            x1[i],x2[i]=x2[i],x1[i] #swap
        
    fo = getFileHandle(filename)
    
    shape = x2-x1+1

    numfiles = timekeylist.__len__()

    extended_shape = np.concatenate((np.array([numfiles]),shape),axis=0)
    data_list = np.zeros(extended_shape)
   
    itr = 0
    
    for time in timekeylist:
        
        name = ui + '/' + str(time)
        if (itr==0 or itr==numfiles-1 or itr%100==0):
            print('Reading file {:d}'.format(itr)+' '+name)

        uixt = fo[ui][time][x1[0]:x2[0]+1,x1[1]:x2[1]+1,x1[2]:x2[2]+1]

        data_list[itr:itr+1,:] = uixt
            
        itr = itr + 1
        
    return data_list