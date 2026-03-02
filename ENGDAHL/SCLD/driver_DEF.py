#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 29 Feb 2024 MUSC WW Emily Gleeson and David Nemec

Modification
"""

## Bjorg Jenny Engdahl's supercooled liquid (freezing drizzle) case

CASE = 'ENGDAHL'
SUBCASE = 'SCLD'

import sys
sys.path.append('..')

import netCDF4 as nc
import numpy as np

from dephycf.Case import Case
from dephycf import thermo
from dephycf import constants as CC

################################################
# 0. General configuration of the present script
################################################

lplot = True # plot all the variables
lverbose = False # print information about variables and case

################################################
# 1. General information about the case
################################################

case = Case('ENGDAHL/SCLD',
        lat=59.94,
        lon=10.72,
        startDate="20180115105000",
        endDate="20180115135000",
        surfaceType='land',
        zorog=0.)

case.set_title("Forcing and initial conditions for SCLD freezing drizzle case - Original definition")
case.set_reference("https://storage.googleapis.com/jnl-su-j-tadmo-files/journals/1/articles/107/submission/proof/107-1-5506-1-10-20220524.pdf")
case.set_script("DEPHY-SCM/ENGDAHL/SCLD/driver_DEF.py")

################################################
# 2. Input netCDF file
################################################

fin = nc.Dataset('initvalues.nc') #profiles of atmospheric variables
fin2 = nc.Dataset('forcing.nc') #Vertical velocity forcing

################################################
# 2. Initial state
################################################

# Orography
orog = 0
case.add_orography(orog)

# Surface pressure
ps = 99570.
case.add_init_ps(ps)

# Pressure
pressure = fin['p'][:]
print(pressure)
case.add_init_pressure(pressure,lev=pressure,levtype='pressure',levid='lev')

# Height
height  = fin['z'][:]
case.add_init_height(height,lev=pressure,levtype='pressure',levid='lev')
print(height)

# Zonal and meridional wind
u  = fin['u'][:]
v  = fin['v'][:]
case.add_init_wind(u=u,v=v,lev=pressure,levtype='pressure',levid='lev')

# Temperature
temp = fin['t'][:]
case.add_init_temp(temp,lev=pressure,levtype='pressure',levid='lev')

# Specific humidity
qv = fin['qv'][:]
case.add_init_qv(qv,lev=pressure,levtype='pressure',levid='lev')

# Liquid water
ql = fin['ql'][:]
case.add_init_variable('ql',ql,lev=pressure,levtype='pressure',levid='lev')

# TKE
qi = fin['tke'][:]
case.add_init_variable('tke',qi,lev=pressure,levtype='pressure',levid='lev')

################################################
# 3. Forcing
################################################

t0 = 0       
t1 = 37*300 # It's a 3 hour simulation

timeForc = np.arange(t0,t1,300.*1.) # Forcing data are provided evey 5 minutes
levForc = fin['p'][:]

nt, = timeForc.shape
nlev, = levForc.shape


# Forcing vertical velocity
w_forc = fin2['w'][:nt,:]
case.add_vertical_velocity(w=w_forc,time=timeForc,timeid='time',lev=levForc,levtype='pressure',levid='lev')

case.add_surface_fluxes(sens=0., lat=0.,
        forc_wind='ustar', ustar=0.0001)

case.add_surface_skin_temp(297.5)

# Radiation scheme is switched off
case.deactivate_radiation()

# Shallowconvection scheme is switched off
case.deactivate_shallow_convection()

# Turbulence scheme is switched off
case.deactivate_turbulence()

fin.close()
fin2.close()

################################################
# 4. Writing file
################################################

case.write(f'ENGDAHL_SCLD_DEF_driver.nc')

if lverbose:
    case.info()

################################################
# 5. Ploting, if asked
################################################

if lplot:
    case.plot(rep_images='./images/driver_DEF/',timeunits='days',levunits='hPa')
