import os

import pandas as pd
import numpy as np

import dirs
from scipy import stats

def get_standard_mean_std(npz_data, file_name):
	data = npz_data[file_name]
	means = pd.Series(np.nanmean(data), dtype=float, index=[file_name + '_mean'])
	stds = pd.Series(np.nanstd(data), dtype=float, index=[file_name + '_std'])
	return means, stds

def get_satellite_data(npz_data):
	data = npz_data['satellite_data']
	bands = range(8)
	means = pd.Series(0, dtype=float, index=['satellite_mean_' + str(band) for band in bands])
	stds = pd.Series(0, dtype=float, index=['satellite_std_' + str(band) for band in bands])
	for band in bands:
		means['satellite_mean_' + str(band)] = np.nanmean(data[:,:,band,:])
		stds['satellite_std_' + str(band)] = np.nanstd(data[:,:,band,:])
	return means, stds

def get_elevation_data(npz_data):
	data = npz_data['elevation']
	elements = range(3)
	means = pd.Series(0, dtype=float, index=['elevation_mean_' + str(element) for element in elements])
	stds = pd.Series(0, dtype=float, index=['elevation_std_' + str(element) for element in elements])
	for element in elements:
		means['elevation_mean_' + str(element)] = np.nanmean(data[:,:,element])
		stds['elevation_std_' + str(element)] = np.nanstd(data[:,:,element])
	return means, stds

def get_crop_data(npz_data):
	data = npz_data['crop_layer']
	elements = range(7)
	modes = pd.Series(0, dtype=float, index=['crop_layer_mode_' + str(element) for element in elements])
	unique_elements = pd.Series(0, dtype=float, index=['crop_layer_uniq_vals_' + str(element) for element in elements])
	for element in elements:
		modes['crop_layer_mode_' + str(element)] = stats.mode(data[:,:,element], axis=None).mode[0]
		unique_elements['crop_layer_uniq_vals_' + str(element)] = len(np.unique(data[:,:,element]))
	return modes, unique_elements

if __name__ == '__main__':

	field_indices = range(1,23)
	for field_index in field_indices:

		file_name = dirs.ML_Outputs + '\\ML_numpy_dataA' + \
			str(field_index) + '.npz'
		npz_data = np.load(file_name)

		row = pd.Series()

		means, stds = get_satellite_data(npz_data)
		row = row.append(means).append(stds)

		means, stds = get_elevation_data(npz_data)
		row = row.append(means).append(stds)

		means, stds = get_standard_mean_std(npz_data, 'temperature')
		row = row.append(means).append(stds)

		means, stds = get_standard_mean_std(npz_data, 'precipitation')
		row = row.append(means).append(stds)

		modes, unique_elements = get_crop_data(npz_data)
		row = row.append(modes).append(unique_elements)

		means, stds = get_standard_mean_std(npz_data, 'salinity')
		row = row.append(means).append(stds)

		means, stds = get_standard_mean_std(npz_data, 'observation_date')
		row = row.append(means).append(stds)

		means, stds = get_standard_mean_std(npz_data, 'FieldID')
		row = row.append(means).append(stds)

		row.name = 'Field_' + str(field_index)

		if(field_index == 1):
			out_df = pd.DataFrame(columns=row.index)
		out_df = out_df.append(row)

	out_df.to_csv(dirs.intermediate_directory + '\\data_check.csv')







