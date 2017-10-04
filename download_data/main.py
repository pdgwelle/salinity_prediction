# -*- coding: utf-8 -*-
"""
Created on Fri Jun 02 11:29:18 2017

@author: Kathrin
"""

import sys

import pandas as pd
import numpy as np

import dirs
import ee_analysis
import reprojection
import tif_to_npz
import npz_to_csv

##### PREP DATA
def reproject():
	reprojection.prepare_data(number_of_fields=22)

#####Google-Earth-Engine Analysis#####
def earth_engine_analysis():
	for field_index in range(1,23): 
		ee_analysis.export_image_from_field(field_index)

#####Creating .npz of all available data#####
def create_npz():
	for field_index in range(1,23): 
	    input_image = dirs.intermediate_directory + '\\FieldA' + str(field_index) + '.tif'
	    input_temperature = dirs.intermediate_directory + '\\mean_temperature_field' + str(field_index) + '.csv'
	    input_salinity = dirs.Fields_intermediate + '\\ucr_with_degrees_field' + str(field_index) + '.csv'
	    out_path = dirs.ML_Outputs +'\\ML_numpy_dataA' + str(field_index) + '.npz'

	    if field_index == 19:
	      tif_to_npz.build_npz_file(input_image, input_temperature, input_salinity, out_path, buffer_y=20, buffer_x=21)
	      print('EXTRARUNDE')
	    else:
	      tif_to_npz.build_npz_file(input_image, input_temperature, input_salinity, out_path, buffer_y=21, buffer_x=21)

	    print(field_index)

#####Final Preprocessing, Creating .npz without cloudy and missing data + Tables for Regression#####
def create_csv():
	out_df = pd.DataFrame()
	for field_index in range(1,23): 
	    print(field_index)
	    npz_directory = dirs.ML_Outputs + '\\ML_numpy_dataA' + str(field_index) + '.npz'
	    csv_directory = dirs.intermediate_directory + '\\Regression_csv\\regression_data_Field' + str(field_index) + '.csv'
	    data = npz_to_csv.final_data_processing(npz_directory, csv_directory, FieldID = field_index)
	    out_df = out_df.append(data, ignore_index=True)
	out_df.to_csv(dirs.outputs_directory + '\\data.csv')

if __name__ == '__main__':
	if(len(sys.argv) < 2):
		print "Please include an argument."
		print "Current acceptable arguments are reproject, earth_engine_analysis, create_npz, and create_csv"
		print "Example: python main.py earth_engine_analysis"
		sys.exit()

	command = sys.argv[1]

	if command == "reproject": 
		reproject()
	if command == "earth_engine_analysis": 
		earth_engine_analysis()
	if command == "create_npz": 
		create_npz()
	if command == "create_csv": 
		create_csv()