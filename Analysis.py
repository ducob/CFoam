##########################################################################################
#### Sets the working directory ##########################################################
import os, sys
import locale
os.chdir('/Users/ducobouter/Analysis/Measurement/')

##########################################################################################
from ExtractData import * #Import function to extract and organise data from the raw files
from CFoamPlot import * #Library containing CFoam plot functions
from CFoamFunctions import * #Library containing CFoam analysis functions

##########################################################################################
import scipy as sp
import numpy as np
import matplotlib.pyplot as plt
import decimal
import math
import datetime
import os.path
from copy import deepcopy #To copy data sets to variables instead of making references

##########################################################################################
# Maps names to integers given for data sets and measurement lists in the data files
execfile('CFoamMap.py')

##########################################################################################
# General plotting bolean.
plotting = False
##########################################################################################

##########################################################################################
#### Executes the desired Analysis Sequence ##############################################

#execfile('Sets/1st_measurement.py')
#execfile('Sets/top_bottom_difference.py')
#execfile('Sets/heat_leak.py')
#execfile('Sets/flow_curve.py')
execfile('Sets/2nd_measurement.py')

##########################################################################################
