# -*- coding: utf-8 -*-
"""
Created on Fri Jun 02 11:30:28 2017

@author: Kathrin
"""
#import pandas as pd

import os

#Top level directories
base_directory = os.path.realpath('../../..')
data_directory = base_directory + '\\data'
outputs_directory = base_directory + '\\outputs'
intermediate_directory = base_directory + '\\intermediate'

#Data directories
ucr_salinity_data = data_directory + '\\ucr_salinity\\WSJVSalinityDatasetForMauter.csv'

#Intermediate directories
ArcGIS_intermediate = intermediate_directory + '\\ArcPy'
Fields_intermediate = intermediate_directory + '\\Fields'
Regression_intermediate = intermediate_directory + '\\Regression_csv'

#Intermediate files
ucr_with_degrees = intermediate_directory + '\\ucr_with_degrees.csv'
extreme_degrees = intermediate_directory + '\\fields_degree_extrema.csv'
#ucr_intermediate_with_degrees = intermediate_directory + '\\ArcMap_Output.csv'#ArcMap_Output.csv is result from arcmap (not python)

#Ouputs directories
ML_Outputs = outputs_directory + '\\ML_Outputs'
ML_Outputs_nan = outputs_directory + '\\ML_Outputs_nan'
ML_numpy_output = outputs_directory +'\\ML_numpy_data.npz'

regression_data = outputs_directory + '\\data.csv' 