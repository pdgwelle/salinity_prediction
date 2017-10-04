import numpy as np
import pandas as pd
import math



import tifffile as tf

import dirs

def build_npz_file(tif_array, temp_csv, ucr_intermediate_with_degrees_field_i_table, path, buffer_y, buffer_x):

    def get_numbers_of_landsat_images(tif_array, number_of_fixed_bands = 95, number_of_landsat_bands = 9):
        total_number_of_bands = np.shape(tif_array)[2]
        width = np.shape(tif_array)[1]
        height = np.shape(tif_array)[0]
        number_of_variable_bands = total_number_of_bands - number_of_fixed_bands
        number_of_landsat_images = number_of_variable_bands/number_of_landsat_bands
        total_landsat_bands = number_of_landsat_bands*number_of_landsat_images
        return width, height, number_of_landsat_images, total_number_of_bands, total_landsat_bands

    def label_landsat_bands(satellite_field, width, height, number_landsat7_images, number_of_landsat_bands = 9):
        #(['B1', 'B2', 'B3', 'B4', 'B5', 'B7', 'cfmask', year])
        landsat_all = satellite_field[:,:,:number_landsat7_images*number_of_landsat_bands]
        reshaped_landsat = np.reshape(landsat_all, (height , width, number_of_landsat_bands, number_landsat7_images), order='F')
        landsat_array, date_array_help = np.split(reshaped_landsat, [number_of_landsat_bands-1], axis=2)
        date_array = date_array_help[0,0,0,:]
        return {'satellite_data' : landsat_array, 'observation_date' : date_array}

    def label_additional_data_bands(satellite_field, total_number_of_bands, total_landsat_bands, time_observations_years = 7):
        crops = satellite_field[:, :, total_landsat_bands : total_landsat_bands+time_observations_years]
        precip_starting_index = total_landsat_bands+time_observations_years
        number_precip_observations = time_observations_years*12
        precip = satellite_field[:, :, precip_starting_index : precip_starting_index+number_precip_observations]
        elev_starting_index = precip_starting_index+number_precip_observations
        elevation = satellite_field[:, :, elev_starting_index : elev_starting_index+3]
        field = satellite_field[0, 0, total_number_of_bands-1]
        return {'crop_layer' : crops, 'precipitation' : precip, 'elevation' : elevation, 'FieldID': field}

    def label_temp(temperature_field):
        filter_temp = temperature_field.ix[:, 'air']
        temperature = filter_temp.as_matrix()
        return{'temperature' : temperature}

    def salinity_array(ucr_intermediate_with_degrees_field_i_table, width, height, buffer_y, buffer_x):
        sal_table = pd.read_csv(ucr_intermediate_with_degrees_field_i_table)
        sal_array = np.nan * np.ones((height, width))
        x_min = np.min(sal_table.ix[:, 'x'])
        y_max = np.max(sal_table.ix[:, 'y'])
        i = 0
        while i < len(sal_table.ix[:, 'x']):
            sal_array[(y_max - sal_table.ix[i, 'y']) / 30 + buffer_y, (sal_table.ix[i, 'x'] - x_min) / 30 + buffer_x] = sal_table.ix[i, 'Salinity']
            i += 1

        return {'salinity' : sal_array}

    def merge_dicts(*dicts):
        out_dict = {}
        for dictionary in dicts:
            out_dict.update(dictionary)
        return out_dict

    def assigning_nan_to_landsat(data_dict):
        satellite_data = data_dict['satellite_data'].astype(float)
        satellite_data[np.where(satellite_data == 20000)] = np.nan
        satellite_data[np.where(satellite_data == -9999)] = np.nan
        CFMask = satellite_data[:,:,6,:]
        cloudy_indices = np.where(CFMask !=0)
        satellite_data[cloudy_indices[0],cloudy_indices[1],:6,cloudy_indices[2]] = np.nan#not correct?!!!
        return {'satellite_data': satellite_data}

    def create_npz_with_nan(satellite_dict, data_dict, path):
        del data_dict['satellite_data']
        out_dict = merge_dicts(satellite_dict, data_dict)
        np.savez(path, **out_dict)

    satellite_field = tf.imread(tif_array)
    temperature_field = pd.read_csv(temp_csv)

    width, height, landsat_img, total_bands, total_landsat_bands = get_numbers_of_landsat_images(satellite_field)
    satellite_dict = label_landsat_bands(satellite_field, width, height, landsat_img)
    additional_data_dict = label_additional_data_bands(satellite_field, total_bands, total_landsat_bands)
    temp_dict = label_temp(temperature_field)
    sal_dict = salinity_array(ucr_intermediate_with_degrees_field_i_table, width, height, buffer_y, buffer_x)
    data_dict = merge_dicts(satellite_dict, additional_data_dict, temp_dict, sal_dict)
    
    satellite_dict = assigning_nan_to_landsat(data_dict)
    create_npz_with_nan(satellite_dict, data_dict, path)

    return

