#----------------------------------import built-in modules-----------------------------------------
import numpy as np
import timeit
import matplotlib.pyplot as plt

#----------------------------import projects internal modules--------------------------------------
from kdeturb import kdeTurb
from kdeturb.statistics import basicstats

input_path = "D:/kdeturb/ref3D_Coarse"
output_path = "D:/kdeturb/output"
obj = kdeTurb(input_path, output_path)

p1 = np.array([5, 6, 0])
p2 = np.array([5, 6, 50])
mid = np.array([5, 6, 25])

begin_program = timeit.default_timer()

mean = basicstats.mean(obj,'Vel1',p1,p2)
print("calculated mean\n")

variance = basicstats.variance(obj,'Vel1',p1,p2)
print("calculated variance\n")

Rij = basicstats.Rij(obj,'Vel1','Vel2',mid,p1,p2)
print("calculated Rij\n")

end_program = timeit.default_timer()
print ("Total Computation Time = "+"%.2f" % (end_program-begin_program)+" sec")

X = np.arange(51).reshape(51,1)
Y1 = mean.reshape(51,1)
Y2 = variance.reshape(51,1)
Y3 = Rij.reshape(51,1)

data2write = np.concatenate((X,Y1,Y2,Y3),axis=1)
np.savetxt("D:/kdeturb/data.csv", data2write, delimiter=',', header="Index,Mean,Variance,Rij", comments="")

print("writing completed")

fig = plt.figure()
ax1 = fig.add_subplot(1,3,1)
ax2 = fig.add_subplot(1,3,2)
ax3 = fig.add_subplot(1,3,3)
ax1.plot(X,Y1)
ax2.plot(X,Y2)
ax3.plot(X,Y3)

print("plotting completed")