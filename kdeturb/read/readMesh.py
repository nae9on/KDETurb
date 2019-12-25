"""
This module defines functions for reading mesh file
"""

#----------------------------------import built-in modules-----------------------------------------
import sys

#----------------------------import projects internal modules--------------------------------------

def extract(x, func):
    arr = []; start = 0
    for i,c in enumerate(x):
        if(c==' ' or i==len(x)-1):
            if(c=='\n'):
                arr.append(func(x[start:i]))
            else:
                arr.append(func(x[start:i+1]))
            start = i+1
    return arr

def getMesh(filename):
    try:
        with open(filename) as f:
            lines = f.readlines()
    except (FileNotFoundError):
        print("Mesh file {0} not found, raising sys.exit(1)".format(filename))
        sys.exit(1)                
    dim = extract(lines[0],int)
    delta = extract(lines[1],float)
    origin = extract(lines[2],float)
    return dim, delta, origin