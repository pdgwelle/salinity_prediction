# -*- coding: utf-8 -*-
"""
Created on Fri Jun 02 11:31:39 2017

@author: Kathrin
"""
import numpy as np
import pandas as pd
import math

import archook
archook.get_arcpy()
import arcpy

import tifffile as tf

import dirs


def prepare_data(number_of_fields):
    #transformation into degrees using arcpy
    def UTM_Zone11_into_GCS_WGS84(ucr_salinity_data):
        arcpy.env.overwriteOutput = True
        # read in the file and make event layer
        arcpy.MakeXYEventLayer_management(ucr_salinity_data, in_x_field='x', in_y_field='y',
                                          out_layer='event_layer', spatial_reference='WGS 1984 UTM Zone 11N')
        # following already executed, and existing:
        arcpy.FeatureClassToFeatureClass_conversion(in_features='event_layer', out_path=dirs.ArcGIS_intermediate,
                                                    out_name='helping_file')
        helping_file = dirs.ArcGIS_intermediate + '\\helping_file.shp'
        helping_projection = dirs.ArcGIS_intermediate + '\\helping_projection.shp'
        arcpy.Project_management(in_dataset=helping_file,
                                 out_dataset=helping_projection, out_coor_system=4326)
        arcpy.AddXY_management(in_features=helping_projection)
        arcpy.TableToTable_conversion(helping_projection, dirs.intermediate_directory, 'ucr_with_degrees.csv')

    #extracting extreme values
    def get_extrema(ucr_with_degrees, number_of_fields):
        table = pd.read_csv(ucr_with_degrees)
        i = 1
        extrema = pd.DataFrame(index = ['min_lon','min_lat', 'max_lon', 'max_lat'])
        while i <= number_of_fields:
            intermediate = table[table['FieldID'] == i]
            min_lon_i = np.min(intermediate['POINT_X'])
            min_lat_i = np.min(intermediate['POINT_Y'])
            max_lon_i = np.max(intermediate['POINT_X'])
            max_lat_i = np.max(intermediate['POINT_Y'])
            extrema["extrema_field_" + str(i)] = [min_lon_i, min_lat_i, max_lon_i, max_lat_i]
            #print(i)
            i +=1
        extrema.to_csv(path_or_buf = dirs.intermediate_directory + '\\fields_degree_extrema.csv')

    def split_into_one_field_csv(ucr_with_degrees, number_of_fields):
        data = pd.read_csv(ucr_with_degrees)
        i = 1
        while i <= number_of_fields:
            intermediate = data[data['FieldID'] == i]
            intermediate.to_csv(path_or_buf=dirs.Fields_intermediate + '\\ucr_with_degrees_field' + str(i) + '.csv', )
            i += 1

    UTM_Zone11_into_GCS_WGS84(dirs.ucr_salinity_data)
    get_extrema(dirs.ucr_with_degrees, number_of_fields)
    split_into_one_field_csv(dirs.ucr_with_degrees, number_of_fields)

    return #how to print output?!


#
# def build_npz_file(tif_array, temp_csv, ucr_intermediate_with_degrees_field_i_table, path,  buffer_y, buffer_x):
#
#     def get_numbers_of_landsat_images(tif_array, number_of_fixed_bands = 95, number_of_landsat_bands = 9):
#         total_number_of_bands = np.shape(tif_array)[2]
#         width = np.shape(tif_array)[1]
#         height = np.shape(tif_array)[0]
#         number_of_variable_bands = total_number_of_bands - number_of_fixed_bands
#         number_of_landsat_images = number_of_variable_bands/number_of_landsat_bands
#         total_landsat_bands = number_of_landsat_bands*number_of_landsat_images
#         return width, height, number_of_landsat_images, total_number_of_bands, total_landsat_bands
#
#     def label_landsat_bands(satellite_field, width, height, number_landsat7_images, number_of_landsat_bands = 9):
#         #(['B1', 'B2', 'B3', 'B4', 'B5', 'B7', 'cfmask', year])
#         landsat_all = satellite_field[:,:,:number_landsat7_images*number_of_landsat_bands]
#         reshaped_landsat = np.reshape(landsat_all, (height , width, number_of_landsat_bands, number_landsat7_images), order='F')
#         landsat_array, date_array_help = np.split(reshaped_landsat, [number_of_landsat_bands-1], axis=2)
#         date_array = date_array_help[0,0,0,:]
#         return {'satellite_data' : landsat_array, 'observation_date' : date_array}
#
#     def label_additional_data_bands(satellite_field, total_number_of_bands, total_landsat_bands, time_observations_years = 7):
#         crops = satellite_field[:, :, total_landsat_bands : total_landsat_bands+time_observations_years]
#         precip_starting_index = total_landsat_bands+time_observations_years
#         number_precip_observations = time_observations_years*12
#         precip = satellite_field[:, :, precip_starting_index : precip_starting_index+number_precip_observations]
#         elev_starting_index = precip_starting_index+number_precip_observations
#         elevation = satellite_field[:, :, elev_starting_index : elev_starting_index+3]
#         field = satellite_field[0, 0, total_number_of_bands-1]
#         return {'crop_layer' : crops, 'precipitation' : precip, 'elevation' : elevation, 'FieldID': field}
#
#     def label_temp(temperature_field):
#         filter_temp = temperature_field.ix[:, 'air']
#         temperature = filter_temp.as_matrix()
#         return{'temperature' : temperature}
#
#     def salinity_array(ucr_intermediate_with_degrees_field_i_table, width, height, buffer_y, buffer_x):
#         sal_table = pd.read_csv(ucr_intermediate_with_degrees_field_i_table)
#         sal_array = np.nan * np.ones((height, width))
#         x_min = np.min(sal_table.ix[:, 'x'])
#         y_max = np.max(sal_table.ix[:, 'y'])
#         i = 0
#         while i < len(sal_table.ix[:, 'x']):
#             sal_array[(y_max - sal_table.ix[i, 'y']) / 30 + buffer_y, (sal_table.ix[i, 'x'] - x_min) / 30 + buffer_x] = sal_table.ix[i, 'Salinity']
#             i += 1
#
#         return {'salinity' : sal_array}
#
#     def merge_dicts(*dicts):
#         dict = {}
#         for dictionary in dicts:
#             dict.update(dictionary)
#         return dict
#
#     satellite_field = tf.imread(tif_array)
#     temperature_field = pd.read_csv(temp_csv)
#
#     width, height, landsat_img, total_bands, total_landsat_bands = get_numbers_of_landsat_images(satellite_field)
#     satellite_dict = label_landsat_bands(satellite_field,width, height, landsat_img)
#     additional_data_dict = label_additional_data_bands(satellite_field, total_bands, total_landsat_bands)
#     temp_dict = label_temp(temperature_field)
#     sal_dict = salinity_array(ucr_intermediate_with_degrees_field_i_table, width, height, buffer_y, buffer_x)
#
#     dict = merge_dicts(satellite_dict, additional_data_dict, temp_dict, sal_dict)
#     np.savez(path, **dict)
#
#     return
#
#
#
# def final_data_processing(npz_file, path_1, path_2, start_year = 2007, end_year = 2013):
#     def assigning_nan_to_landsat(npzfile):
#         satellite_data = npzfile['satellite_data'].astype(float)
#         satellite_data[np.where(satellite_data == 20000)] = np.nan
#         satellite_data[np.where(satellite_data == -9999)] = np.nan
#         CFMask = satellite_data[:,:,6,:]
#         cloudy_indices = np.where(CFMask !=0)
#         satellite_data[cloudy_indices[0],cloudy_indices[1],:6,cloudy_indices[2]] = np.nan#not correct?!!!
#         return {'satellite_data': satellite_data}
#
#
#     def create_npz_with_nan(dict1, npzfile, path):
#         dict = {}
#         for i in npzfile.files:
#             if str(i) != 'satellite_data':
#                 dict.update({str(i): npzfile[str(i)]})
#
#         def merge_dicts(*dicts):
#             dict = {}
#             for dictionary in dicts:
#                 dict.update(dictionary)
#             return dict
#
#         dictionary = merge_dicts(dict1, dict)
#         np.savez(path, **dictionary)
#         return
#
#
#     def averaging_per_year(satellite_data_nan_dict, start_year, end_year):
#         satellite_data = satellite_data_nan_dict['satellite_data']
#         dict = {}
#         for i in range(start_year, end_year+1):
#             index = np.where(satellite_data[0,0,7,:] == float(i))
#             dict.update({'mean_' + str(i): np.nanmean(satellite_data[:, :, :6, index[0]], axis=3)})
#         return dict
#
#     def calculate_max_CRSI_pixel(mean_dict):
#         l = list()
#         L = list()
#         for i in mean_dict:
#             year_mean = mean_dict[str(i)]
#             numerator = (year_mean[:, :, 3] * year_mean[:, :, 2]) - (year_mean[:, :, 1] * year_mean[:, :, 0])
#             denumerator =((year_mean[:, :, 3] * year_mean[:, :, 2]) + (year_mean[:, :, 1] * year_mean[:, :, 0]))
#             with np.errstate(divide='ignore', invalid='ignore'):
#                 l.append(np.sqrt(numerator / denumerator))
#             L.append(np.ones((np.shape(year_mean)[0], np.shape(year_mean)[1])) * int(str(i)[5:]))
#         crsi_all = np.stack(l, axis=2)
#         years_all = np.stack(L, axis=2)
#         indices = np.argmax(crsi_all, axis=2)
#         row, column = np.indices(np.shape(indices))
#         CRSI = crsi_all[row, column, indices]
#         max_year = years_all[row, column, indices]
#         return {'max_CRSI' : CRSI, 'maxCRSI_year' : max_year}
#
#
#
#     def create_csv_for_Regression(npzfile, mean_dict, CRSI_dict, path, start_year):
#         def get_indices_with_existing_salinity(npzfile):
#             salinity = npzfile['salinity']
#             indices = np.where(np.logical_not(np.isnan(salinity)))
#             return indices, {'salinity': salinity[indices]}
#
#         def get_single_bands_year(mean_dict, indices, start_year):
#             bands = np.shape(mean_dict['mean_' + str(start_year)])[2]
#             dict = {}
#             for i in mean_dict:
#                 for j in range(1, bands + 1):
#                     if j < bands:
#                         temp = mean_dict[str(i)][indices]
#                         dict.update({'band_' + str(j) + '_' + str(i): temp[:, j - 1]})
#                     else:
#                         temp = mean_dict[str(i)][indices]
#                         dict.update({'band_' + str(j + 1) + '_' + str(i): temp[:, j - 1]})
#             return dict
#
#         def get_CRSI_year(CRSI_dict, indices):
#             dict = {}
#             for i in CRSI_dict:
#                 dict.update({str(i): CRSI_dict[str(i)][indices]})
#             return dict
#
#         def get_elev_crop(npzfile, indices):
#             elev = npzfile['elevation'][indices]
#             crop = npzfile['crop_layer'][indices]
#             return {'elevation': elev[:, 0], 'aspect': elev[:, 1],
#                 'slope': elev[:, 2], 'crops_2007': crop[:, 0],
#                 'crops_2008': crop[:, 1], 'crops_2009': crop[:, 2],
#                 'crops_2010': crop[:, 3], 'crops_2011': crop[:, 4],
#                 'crops_2012': crop[:, 5], 'crops_2013': crop[:, 6]}
#
#         def get_temp_of_CRSI_year(npzfile, max_year, start_year):
#             temp = npzfile['temperature']
#             i = 0
#             ave_temp = np.zeros((len(temp) / 12))
#             while i < len(temp):
#                 ave_temp[i / 12] = np.mean(temp[i:(12 + i)])
#                 i = 12 + i
#             temperature = np.zeros(len(max_year))
#             for j in range(0, len(max_year)):
#                 temperature[j] = ave_temp[int(max_year[j]) - start_year]
#             return {'average_temperature': temperature}
#
#         def get_total_precip_of_CRSI_year(npzfile, max_year, start_year):
#             precip_all = npzfile['precipitation']
#             precip_month = precip_all[indices]  # integers....rounding errors??
#             total_precip = np.zeros((np.shape(precip_month)[0], np.shape(precip_month)[1] / 12))
#             i = 0
#             while i < np.shape(precip_month)[1]:
#                 if ((int(i) / 12 + start_year) % 4 == 0):  # 366 days per year
#                     days_month = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
#                     total = precip_month[:, i:(12 + i)] * days_month
#                     total_precip[:, i / 12] = np.sum(total, axis=1)
#                     i = 12 + i
#                 else:
#                     days_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
#                     total = precip_month[:, i:(12 + i)] * days_month
#                     total_precip[:, i / 12] = np.sum(total, axis=1)
#                     i = 12 + i
#
#             precip = np.zeros(len(max_year))
#             for j in range(0, len(max_year)):
#                 precip[j] = total_precip[j, int(max_year[j]) - start_year]
#             return {'total_precipitation': precip}
#
#         def merge_dicts(*dicts):
#             dict = {}
#             for dictionary in dicts:
#                 dict.update(dictionary)
#             return dict
#
#         def dict_to_csv(dict, path):
#             data = pd.DataFrame.from_dict(data=dict, orient='columns')
#             data.sort_index(axis=1)
#             data.to_csv(path_or_buf=path)
#             return
#
#         indices, sal = get_indices_with_existing_salinity(npzfile)
#         bands_years = get_single_bands_year(mean_dict, indices, start_year)
#         CRSI = get_CRSI_year(CRSI_dict, indices)
#         max_year = CRSI['maxCRSI_year']
#         additional = get_elev_crop(npzfile, indices)
#         temp = get_temp_of_CRSI_year(npzfile, max_year, start_year)
#         precip = get_total_precip_of_CRSI_year(npzfile, max_year, start_year)
#         dict = merge_dicts(sal, CRSI, bands_years, additional, temp, precip)
#         dict_to_csv(dict, path)
#         return
#
#
#     npzfile = np.load(npz_file)
#     satellite_data_nan_dict = assigning_nan_to_landsat(npzfile)
#     create_npz_with_nan(dict1 = satellite_data_nan_dict, npzfile = npzfile, path = path_1)
#     mean_dict = averaging_per_year(satellite_data_nan_dict, start_year, end_year)
#     CRSI_dict = calculate_max_CRSI_pixel(mean_dict)
#     create_csv_for_Regression(npzfile,mean_dict=mean_dict,CRSI_dict=CRSI_dict, path=path_2, start_year=start_year)
#
#     return





#support.final_data_processing()

