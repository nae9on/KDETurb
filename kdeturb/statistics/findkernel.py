r"""
This module defines the following functions::

  - gaussian:
  
    This function computes the Gaussian kernel.

"""
#----------------------------------import built-in modules-----------------------------------------
import numpy as np
from sklearn.neighbors import KernelDensity

def data1D(data,which_kernel='gaussian'):
    #Normalize data X \in N(mu,sg^2) => (X-mu)/sg \in N(0,1)
    mu = np.mean(data,axis=0)
    sigma = np.std(data,axis=0)
    normalized_data = (data-mu)/sigma
    #n_features = 1
    n_samples = np.linspace(-4, 4, 1000)[:, np.newaxis]
    kde = KernelDensity(kernel=which_kernel, bandwidth=0.5).fit(normalized_data)
    log_dens = kde.score_samples(n_samples)
    return normalized_data, n_samples, np.exp(log_dens)