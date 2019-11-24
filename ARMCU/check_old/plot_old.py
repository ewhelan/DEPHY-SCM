import os
import sys
sys.path.append('../../utils/')

import numpy as np
import netCDF4 as nc
import SCM_utils as utils

import time

rep_images = './images/setup_old/'

if not(os.path.exists(rep_images)):
    os.makedirs(rep_images)

data = {}

f = nc.Dataset('ARMCu_driver_RR_new3.nc','r')

for var in f.variables:
    if not(var in f.dimensions) and not(var in ['bounds_lat','bounds_lon']):
        print var
        data[var] = utils.read(var,f)
        #data[var].info()
        data[var].plot(rep_images=rep_images)

f.close()