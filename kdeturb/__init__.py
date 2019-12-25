"""
This module defines the main class for the kdeturb package
"""

#----------------------------------import built-in modules-----------------------------------------
from socket import gethostname

#----------------------------import projects internal modules--------------------------------------
from kdeturb.read import hdf5read, readMesh 

# objects imported when "from kdeturb import *" is executed
__all__ = [
    'kdeTurb'
    ]

class kdeTurb:
   """   
   Main class for the kdeturb project   
   """
   
   objCount = 0

   def __init__(self, input_path, output_path):
                      
      self.input_path = input_path
      
      self.output_path = output_path
      
      self.h5file = input_path+"/output/pseudo.h5"
      
      self.meshFile = input_path+"/input/wireframe.txt"
      
      self.fhandle = hdf5read.getFileHandle(self.h5file)
      
      self.varlist = hdf5read.getGroupKeys(self.h5file)
      
      self.timelist = hdf5read.getDatasetKeys(self.h5file,0)
      
      self.dim, self.delta, self.origin = readMesh.getMesh(self.meshFile)
      
      #Get the host system name
      self.host = gethostname()
      
      kdeTurb.objCount += 1
      
      print("Initialized class object")
      
      self.displayMetadata()
            
   def displayMetadata(self):
       
       print("List of variables\n", self.varlist)

       print("List of times\n", self.timelist)
       
       print("Mesh: dim",self.dim, self.delta, self.origin)
       
       print ("Working on ", self.host, "computer\n")
       
       kdeTurb.displayCount()
       
       print('\n')
      
   def displayCount():
       
     print("Total Object count =", kdeTurb.objCount)