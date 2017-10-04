import numpy as np
import pandas as pd
import math


import tifffile as tf

import dirs


def final_data_processing(npz_directory, csv_directory, FieldID, start_year = 2007, end_year = 2013):

#satellite_data[rows(height), columns(width), {band1,band2,band3,band4,band5,band7,cfmask,year,datecode},images}
    def averaging_per_year(satellite_data_nan_dict, start_year, end_year):
        satellite_data = satellite_data_nan_dict['satellite_data']
        dict = {}
        for i in range(start_year, end_year+1):
            index = np.where(satellite_data[0,0,7,:] == float(i))
            dict.update({'mean_' + str(i): np.nanmean(satellite_data[:, :, :6, index[0]], axis=3)})
        return dict

    def calculate_max_CRSI_pixel(mean_dict):
        l = list()
        L = list()
        for i in mean_dict:
            year_mean = mean_dict[str(i)]
            numerator = (year_mean[:, :, 3] * year_mean[:, :, 2]) - (year_mean[:, :, 1] * year_mean[:, :, 0])
            denumerator =((year_mean[:, :, 3] * year_mean[:, :, 2]) + (year_mean[:, :, 1] * year_mean[:, :, 0]))
            with np.errstate(divide='ignore', invalid='ignore'):
                l.append(np.sqrt(numerator / denumerator))
            L.append(np.ones((np.shape(year_mean)[0], np.shape(year_mean)[1])) * int(str(i)[5:]))
        crsi_all = np.stack(l, axis=2)
        years_all = np.stack(L, axis=2)
        indices = np.argmax(crsi_all, axis=2)
        row, column = np.indices(np.shape(indices))
        CRSI = crsi_all[row, column, indices]
        max_year = years_all[row, column, indices]
        return {'max_CRSI' : CRSI, 'maxCRSI_year' : max_year}

    def create_csv_for_Regression(npzfile, mean_dict, CRSI_dict, path, start_year, FieldID):
        def get_indices_with_existing_salinity(npzfile):
            salinity = npzfile['salinity']
            indices = np.where(np.logical_not(np.isnan(salinity)))
            return indices, {'salinity': salinity[indices]}

        def get_single_bands_year(mean_dict, indices, start_year):
            bands = np.shape(mean_dict['mean_' + str(start_year)])[2]
            dict = {}
            for i in mean_dict:
                for j in range(1, bands + 1):
                    if j < bands:
                        temp = mean_dict[str(i)][indices]
                        dict.update({'band_' + str(j) + '_' + str(i): temp[:, j - 1]})
                    else:
                        temp = mean_dict[str(i)][indices]
                        dict.update({'band_' + str(j + 1) + '_' + str(i): temp[:, j - 1]})
            return dict

        def get_CRSI_year(CRSI_dict, indices):
            dict = {}
            for i in CRSI_dict:
                dict.update({str(i): CRSI_dict[str(i)][indices]})
            return dict

        def get_elev_crop(npzfile, indices, max_year, FieldID, start_year):
            elev = npzfile['elevation'][indices]
            crop = npzfile['crop_layer'][indices]
            print(np.shape(crop))
            crops = np.zeros(len(max_year))
            for j in range(0, len(max_year)):
                crops[j] = crop[j, int(max_year[j]) - start_year]
            Field_ID = np.ones(len(max_year))*FieldID
            return {'elevation': elev[:, 0], 'aspect': elev[:, 1],
                    'slope': elev[:, 2], 'crops_max_year': crops, 'Field_ID': Field_ID}
        # def get_elev_crop(npzfile, indices):
        #     elev = npzfile['elevation'][indices]
        #     crop = npzfile['crop_layer'][indices]
        #     return {'elevation': elev[:, 0], 'aspect': elev[:, 1],
        #         'slope': elev[:, 2], 'crops_2007': crop[:, 0],
        #         'crops_2008': crop[:, 1], 'crops_2009': crop[:, 2],
        #         'crops_2010': crop[:, 3], 'crops_2011': crop[:, 4],
        #         'crops_2012': crop[:, 5], 'crops_2013': crop[:, 6]}

        def get_temp_of_CRSI_year(npzfile, max_year, start_year):
            temp = npzfile['temperature']
            i = 0
            ave_temp = np.zeros((len(temp) / 12))
            while i < len(temp):
                ave_temp[i / 12] = np.mean(temp[i:(12 + i)])
                i = 12 + i
            temperature = np.zeros(len(max_year))
            for j in range(0, len(max_year)):
                temperature[j] = ave_temp[int(max_year[j]) - start_year]
            return {'average_temperature': temperature}

        def get_total_precip_of_CRSI_year(npzfile, indices, max_year, start_year):
            precip_all = npzfile['precipitation']
            precip_month = precip_all[indices]
            total_precip = np.zeros((np.shape(precip_month)[0], np.shape(precip_month)[1] / 12))
            i = 0
            while i < np.shape(precip_month)[1]:
                    total_precip[:, i / 12] = np.sum(precip_month[:,i:(12+i)], axis=1)
                    i = 12 + i
            precip = np.zeros(len(max_year))
            for j in range(0, len(max_year)):
                precip[j] = total_precip[j, int(max_year[j]) - start_year]
            return {'total_precipitation': precip}

        def merge_dicts(*dicts):
            out_dict = {}
            for dictionary in dicts:
                out_dict.update(dictionary)
            return out_dict

        def dict_to_csv(dict, path):
            data = pd.DataFrame.from_dict(data=dict, orient='columns')
            data.sort_index(axis=1)
            data.to_csv(path_or_buf=path)
            return data

        indices, sal = get_indices_with_existing_salinity(npzfile)
        bands_years = get_single_bands_year(mean_dict, indices, start_year)
        CRSI = get_CRSI_year(CRSI_dict, indices)
        max_year = CRSI['maxCRSI_year']
        additional = get_elev_crop(npzfile, indices, max_year, FieldID, start_year)
        temp = get_temp_of_CRSI_year(npzfile, max_year, start_year)
        precip = get_total_precip_of_CRSI_year(npzfile, indices, max_year, start_year)
        dict = merge_dicts(sal, CRSI, bands_years, additional, temp, precip)
        data = dict_to_csv(dict, path)
        return data

    npzfile = np.load(npz_directory)
    satellite_data_nan_dict = {'satellite_data': npzfile['satellite_data']}
    mean_dict = averaging_per_year(satellite_data_nan_dict, start_year, end_year)
    CRSI_dict = calculate_max_CRSI_pixel(mean_dict)
    data = create_csv_for_Regression(npzfile,mean_dict=mean_dict,CRSI_dict=CRSI_dict, path=csv_directory, start_year=start_year, FieldID=FieldID)

    return data
