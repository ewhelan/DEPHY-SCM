#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 29 Feb 2024 MUSC WW Emily Gleeson and David Nemec

Modification
"""

## SCLD case SCM-enabled definition

import numpy as np

from dephycf.Case import Case

################################################
# 0. General configuration of the present script
################################################

case_name = 'ENGDAHL'
subcase_name = 'SCLD'
title = f"Forcing and initial conditions for {case_name}/{subcase_name} - SCM-enabled version"

lplot = True     # plot the new version of the case
lcompare = True  # plot comparisons between original and new versions
lverbose = False # print information on variables and case

################################################
# 1. Get the original version of the case
################################################

# initialize the case structure for the original version
case = Case('{0}/{1}'.format(case_name,subcase_name))

# read case information in file
case.read('{0}_{1}_DEF_driver.nc'.format(case_name,subcase_name))

# display some information about the case
if lverbose:
    case.info()

################################################
# 2. Interpolate onto a new grid, same for all the variables
#    and add new variables if needed
################################################

timeout = case.variables['wa'].time.data #As we have the vertical velcity array after running the driver_DEF.py step

# conversion, keeping the original grid of the input data
newcase = case.convert2SCM(time=timeout)

# update some attributes
newcase.set_title(title)
newcase.set_script("DEPHY-SCM/{0}/{1}/driver_SCM.py".format(case_name,subcase_name))

# display some information about the new version of the case
if lverbose:
    newcase.info()

################################################
# 3. Save new version of the case in netcdf file
################################################

# save the new version of the case in netcdf file 
newcase.write('{0}_{1}_SCM_driver.nc'.format(case_name,subcase_name))

################################################
# 4. Plots if asked
################################################

if lplot:
    newcase.plot(rep_images='./images/driver_SCM/',timeunits='days',levunits='hPa')

if lcompare:
    newcase.plot_compare(case,rep_images='./images/compare/',label1="SCM-enabled",label2="Original",timeunits='days',levunits='hPa')
