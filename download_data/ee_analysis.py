import numpy as np
import pandas as pd
import math

import ee
ee.Initialize()

import dirs

Fusion_Table_Field_1 = ee.FeatureCollection('ft:1rrcNOppcOV0na_6JHEmP8ycdQFP6ywHbheFV3wIi')
Fusion_Table_Field_2 = ee.FeatureCollection('ft:19rJUyf1HEqGFo1jMpkJ1-fsJV7WUlNOltVDMoLX1')
Fusion_Table_Field_3 = ee.FeatureCollection('ft:1R8vN0XlfE8wt22qfDgKNQ2nOnxQdp3bNifl01TgZ')
Fusion_Table_Field_4 = ee.FeatureCollection('ft:1gT2Ga-d3P8cKo0oUV9NPo25uFETfj9elqb_d9Tyr')
Fusion_Table_Field_5 = ee.FeatureCollection('ft:1i-qZRKlRPavbNPRIBCGLlHWqEr8uO5ninOudb_Ng')
Fusion_Table_Field_6 = ee.FeatureCollection('ft:1aLFSaWGfWonPwBcZ4IJPq-475zpzleS3Yh2zD09Q')
Fusion_Table_Field_7 = ee.FeatureCollection('ft:1pycN-8TvbR955LmbfETeAPGtQx9eJhRF5Dfaz2OM')
Fusion_Table_Field_8 = ee.FeatureCollection('ft:1uKwBKKhJtgWPfv3EtYssRNGWdUD6Rs5NZI5wuU63')
Fusion_Table_Field_9 = ee.FeatureCollection('ft:1zGUGjN3b_SVAyBil8styHJPfxf8jYEwz2tRWKJEd')
Fusion_Table_Field_10 = ee.FeatureCollection('ft:1zcgTzJ7uOo6LVxdI4pRTZRalKYMm3aFOVBOPB-UB')
Fusion_Table_Field_11 = ee.FeatureCollection('ft:1Z0ABnpqOqdLaXKLvdZEfuObaqMCfG98_YJprpM4h')
Fusion_Table_Field_12 = ee.FeatureCollection('ft:1hhASXotpHuL6Jw1YUoF-yVT81h035oLm-UNA2VbJ')
Fusion_Table_Field_13 = ee.FeatureCollection('ft:1tvvmMplT-rqFy2qr27g2aQp3rNA5QB7UA-OVoZkG')
Fusion_Table_Field_14 = ee.FeatureCollection('ft:1If-KPk4E8aHBht3CFLxgG_R0tZ4SUg6xLldWKZ6k')
Fusion_Table_Field_15 = ee.FeatureCollection('ft:1_un2eXsAg23SQNUlKeEdweIgw2igd5lxhW95sfUH')
Fusion_Table_Field_16 = ee.FeatureCollection('ft:1eXW_SExNomJ9yWfkYUrHDTo0pzZw5J6RApeZHdvx')
Fusion_Table_Field_17 = ee.FeatureCollection('ft:1zdnJlHfba4xoBa6E6hnywBIGz4Q4l5DI90DMK65A')
Fusion_Table_Field_18 = ee.FeatureCollection('ft:1DQih_EnaIq6MyTYxV5HTpAhRm3zPegRTRsCUVRln')
Fusion_Table_Field_19 = ee.FeatureCollection('ft:1XAedrGrZaLJYq15HPcWivtYlMmsg9_Sa3x-9zgXe')
Fusion_Table_Field_20 = ee.FeatureCollection('ft:18--k354WJBBQeeR9WmZNW330LC7F6hvNcFSOKojo')
Fusion_Table_Field_21 = ee.FeatureCollection('ft:1w3vVi440gNuOJMdlHJ3f_-ik3WUmzrChOFCLnje2')
Fusion_Table_Field_22 = ee.FeatureCollection('ft:1VcjBYp1ecNRXr0RXRU8nwqDM5Ja_hh8mUKLBi_xW')
crs_7 = 'EPSG:32610'
crs_8 = 'EPSG:32610'
crs_9 = 'EPSG:32610'
crs_10 = 'EPSG:32610'
crs_11 = 'EPSG:32610'
crs_12 = 'EPSG:32610'
crs_13 = 'EPSG:32610'
crs_14 = 'EPSG:32610'
crs_15 = 'EPSG:32610'
crs_16 = 'EPSG:32610'
crs_19 = 'EPSG:32610'
crs_20 = 'EPSG:32610'
crsTransform_7 = [30, 0, 596385, 0, -30, 4257315]
crsTransform_8 = [30, 0, 596385, 0, -30, 4257315]
crsTransform_9 = [30, 0, 596385, 0, -30, 4257315]
crsTransform_10 = [30, 0, 596385, 0, -30, 4257315]
crsTransform_11 = [30, 0, 596385, 0, -30, 4257315]
crsTransform_12 = [30, 0, 596385, 0, -30, 4257315]
crsTransform_13 = [30, 0, 596385, 0, -30, 4257315]
crsTransform_14 = [30, 0, 596385, 0, -30, 4257315]
crsTransform_15 = [30, 0, 596385, 0, -30, 4257315]
crsTransform_16 = [30, 0, 596385, 0, -30, 4257315]
crsTransform_19 = [30, 0, 596385, 0, -30, 4257315]
crsTransform_20 = [30, 0, 596385, 0, -30, 4257315]
crs_1 = 'EPSG:32611'
crs_2 = 'EPSG:32611'
crs_3 = 'EPSG:32611'
crs_4 = 'EPSG:32611'
crs_5 = 'EPSG:32611'
crs_6 = 'EPSG:32611'
crs_17 = 'EPSG:32611'
crs_18 = 'EPSG:32611'
crs_21 = 'EPSG:32611'
crs_22 = 'EPSG:32611'
crsTransform_1 = [30, 0, 155985, 0, -30, 4101915]
crsTransform_2 = [30, 0, 155985, 0, -30, 4101915]
crsTransform_3 = [30, 0, 155985, 0, -30, 4101915]
crsTransform_4 = [30, 0, 155985, 0, -30, 4101915]
crsTransform_5 = [30, 0, 155985, 0, -30, 4101915]
crsTransform_6 = [30, 0, 155985, 0, -30, 4101915]
crsTransform_17 = [30, 0, 155985, 0, -30, 4101915]
crsTransform_18 = [30, 0, 155985, 0, -30, 4101915]
crsTransform_21 = [30, 0, 155985, 0, -30, 4101915]
crsTransform_22 = [30, 0, 155985, 0, -30, 4101915]


def export_image_from_field(field_index, description = 'CMU_Research', description_temp = 'AVE Temp', start_date = '2007-01-01', end_date = '2013-12-31'):
    extrema_i = pd.read_csv(dirs.extreme_degrees)['extrema_field_' + str(field_index)]
    table = eval('ee_analysis.Fusion_Table_Field_' + str(field_index))
    out_name = 'FieldA'+str(field_index)
    out_name_temp='mean_temperature_field'+str(field_index)
    crs=eval('ee_analysis.crs_' + str(field_index))
    crsTransform=eval('ee_analysis.crsTransform_' + str(field_index))

    rect, rect_coordinates = create_rectangle(extrema_i)
    image = get_image_7years(table, rect, start_date, end_date)
    print(rect.getInfo())
    task_1 = export_image(image, description, out_name, rect_coordinates, crs, crsTransform)
    task_2 = export_temp_csv(start_date, end_date, description_temp, out_name_temp, rect)
    return task_1, task_2


def create_rectangle(extrema_i):#rect of same size as the one from ee code in gee
# check
    def delta_lat(meters):
        magic_number = 111111.0#ee.Number(math.pi).multiply(6371000.785).divide(180)  # transformation number
        dl = ee.Number(meters).divide(magic_number)
        d2 = ee.Number(meters).divide(magic_number)
        return dl,d2

# check (working with min max need two)
    def delta_lon(meters, min_lat, max_lat):
        magic_number = 111111.0#ee.Number(math.pi).multiply(6371000.785).divide(180)
        min_lat_rad = ee.Number(min_lat).divide(180).multiply(math.pi)
        max_lat_rad = ee.Number(max_lat).divide(180).multiply(math.pi)
        d_min = ee.Number(meters).multiply(ee.Number(1)).divide(min_lat_rad.cos()).divide(magic_number)
        d_max = ee.Number(meters).multiply(ee.Number(1)).divide(max_lat_rad.cos()).divide(magic_number)
        return d_min, d_max

    buffer_size_meters = 600
    d_lat_up, d_lat_down = delta_lat(buffer_size_meters)
    d_min_lon, d_max_lon = delta_lon(buffer_size_meters, extrema_i[1], extrema_i[3])
    lower_lat = ee.Number(extrema_i[1]).subtract(d_lat_down)
    lower_lon = ee.Number(extrema_i[0]).subtract(d_min_lon)  # how to call
    upper_lat = ee.Number(extrema_i[3]).add(d_lat_up)
    upper_lon = ee.Number(extrema_i[2]).add(d_max_lon)
    rect = ee.Geometry.Rectangle(lower_lon, lower_lat, upper_lon, upper_lat)
    rect_coordinates = rect.coordinates()

    return rect, rect_coordinates


def get_image_7years(table, rect, start_date, end_date):

    def get_image_collections():
        landsat_7_collection = ee.ImageCollection('LANDSAT/LE7_SR')#check
        crop_layer_collection = ee.ImageCollection(['USDA/NASS/CDL/2007b','USDA/NASS/CDL/2008','USDA/NASS/CDL/2009','USDA/NASS/CDL/2010','USDA/NASS/CDL/2011','USDA/NASS/CDL/2012','USDA/NASS/CDL/2013'])#check
        national_elevation = ee.Image('USGS/NED')#check
        return landsat_7_collection, crop_layer_collection, national_elevation

    def get_precip_monthly_average(start_date, end_date):

        def set_month_year_int(image):
            y = image.date().get('year').int16()
            m = image.date().get('month').int16()
            return image.set({'month': m, 'year': y})

        def get_monthly_mean(y):
            months = ee.List.sequence(1, 12)
            def go_over_months(m):
                monthly_image = ee.Image(precipitation_collection_daily.filterMetadata('year', 'equals', y)
                                         .filterMetadata('month', 'equals', m)
                                         .select('precipitation').sum()########## SUM() ?!!!!!#######
                                         .set('year', y)
                                         .set('month', m)
                                         .set('date', ee.Date.fromYMD(y, m, 1)))
                return monthly_image

            list_of_monthly_images_one_year = ee.List(months.map(go_over_months))
            return list_of_monthly_images_one_year

        precipitation_collection_daily = ee.ImageCollection('UCSB-CHG/CHIRPS/PENTAD').filterDate(start_date,end_date)
        precipitation_collection_daily = ee.ImageCollection(precipitation_collection_daily.map(set_month_year_int))

        years = ee.List.sequence(ee.Date(start_date).get('year'), ee.Date(end_date).get('year'))
        precipitation_collection = ee.ImageCollection(years.map(get_monthly_mean).flatten())
        return precipitation_collection

    def stack_ls7(image_1, image_2):
        millis_to_day = 1000 * 60 * 60 * 24
        date_code = image_1.date().millis().long().divide(millis_to_day).int16()#days
        year = image_1.date().get('year').int16()
        return ee.Image(image_2).addBands(ee.Image(image_1)
            .select("B1","B2","B3","B4","B5","B7")#
            .addBands(ee.Image(image_1).select("cfmask").toInt16()
            .addBands(ee.Image.constant(year)).toInt16()
            .addBands(ee.Image.constant(date_code)).toInt16()))

    def stack_crop_to_landsat(image_1, image_2):#check
        date_code = image_1.date().get('year').int16()
        helper = ee.String('cropland_')
        new_band = helper.cat(ee.Number.format(date_code))
        old_names = image_1.bandNames()
        new_names = old_names.set(-1, new_band)
        return ee.Image(image_2).addBands(ee.Image(image_1)
                                      .rename(new_names).select(new_band).int16())

    def stack_precip_to_landsat(image_1, image_2):#check
        year = ee.Date(image_1.get('date')).get('year').int16()
        month = ee.Date(image_1.get('date')).get('month').int16()
        helper = ee.String('precipitation_')
        new_band_1 = helper.cat(ee.Number.format(year))
        new_band_2 = new_band_1.cat(ee.Number.format(month))
        old_names = image_1.bandNames()
        new_names = old_names.set(-1, new_band_2)
        return ee.Image(image_2).addBands(ee.Image(image_1)
                                      .rename(new_names).select(new_band_2).int16())#maybe float()?

    landsat_7_collection, crop_layer_collection, national_elevation = get_image_collections()

    landsat_7_collection = landsat_7_collection.filterDate(start_date, end_date).filterBounds(rect)#left as it was
    out_image = ee.Image(landsat_7_collection.iterate(stack_ls7, ee.Image(-1000))).slice(1)

    crop_layer_collection = crop_layer_collection.filterBounds(rect)  # hopefully working keep in mind/worked in GEE
    out_image = ee.Image(crop_layer_collection.iterate(stack_crop_to_landsat, out_image))

    precipitation_collection = get_precip_monthly_average(start_date, end_date)
    out_image = ee.Image(precipitation_collection.iterate(stack_precip_to_landsat, out_image))


    out_image = out_image.addBands(national_elevation).int16()#left as it was
    out_image = out_image.addBands(ee.Terrain.aspect(national_elevation)).int16()
    out_image = out_image.addBands(ee.Terrain.slope(national_elevation)).int16()

    fkey = ee.Number(table.first().get('FieldID'))
    out_image = out_image.addBands(ee.Image.constant(fkey).int16())

    return out_image

def export_temp_csv(start_date, end_date, description_temp, out_name_temp, rect, scale=30):
    def get_temp_monthly_average(start_date, end_date):

        def temp_set_month_year_int(image):
            y = image.date().get('year').int16()
            m = image.date().get('month').int16()
            return image.set({'month': m, 'year': y})

        def temp_get_monthly_mean(y):
            months = ee.List.sequence(1, 12)
            def temp_go_over_months(m):
                monthly_image = ee.Image(temperature_collection_daily.filterMetadata('year', 'equals', y)
                                         .filterMetadata('month', 'equals', m)
                                         .select('air').mean()
                                         .set('year', y)
                                         .set('month', m)
                                         .set('date', ee.Date.fromYMD(y, m, 1)))
                return monthly_image

            list_of_monthly_images_one_year = ee.List(months.map(temp_go_over_months))
            return list_of_monthly_images_one_year

        temperature_collection_daily = ee.ImageCollection('NCEP_RE/surface_temp').filterDate(start_date,end_date)
        temperature_collection_daily = ee.ImageCollection(temperature_collection_daily.map(temp_set_month_year_int))

        years = ee.List.sequence(ee.Date(start_date).get('year'), ee.Date(end_date).get('year'))
        temperature_collection = ee.ImageCollection(years.map(temp_get_monthly_mean).flatten())
        return temperature_collection

    def temp_to_feature_collection(image):
        feature = ee.Feature(None, ee.Dictionary(image.reduceRegion(ee.Reducer.mean(),
                                            geometry = rect, scale = ee.Number(scale))
                    .set('year', image.get('year')))
                    .set('month', image.get('month')))
        return feature

    def export_table(feature_collection, description_temp, out_name_temp):  # left alone

        task = ee.batch.Export.table.toDrive(collection = feature_collection, folder = description_temp,
                                             description = out_name_temp, fileFormat = 'CSV')
        task.start()
        return task

    temperature_collection = get_temp_monthly_average(start_date, end_date)
    temp_feature_collection = ee.FeatureCollection(temperature_collection.map(temp_to_feature_collection))
    task = export_table(temp_feature_collection, description_temp, out_name_temp)
    return task


def export_image(image, description, out_name, rect_coordinates, crs, crsTransform):#left alone
   task = ee.batch.Export.image.toDrive(image = image, folder = description, description = out_name,
                                        crs=crs, crsTransform=crsTransform, region=rect_coordinates.getInfo()[0])
   task.start()
   return task



#running the code:
#extrema_1 = pd.read_csv(dirs.extreme_degrees)['extrema_field_' + str(7)]

#task = export_image_from_field(extrema_i = extrema_1, table = Fusion_Table_Field_7, description = 'CMU_Research', out_name = 'Field7_test',
##                                description_temp = 'average_temp', out_name_temp='mean_temperature',
#                                start_date = '2007-01-01', end_date = '2013-12-31',crs=crs_7, crsTransform=crsTransform_7)