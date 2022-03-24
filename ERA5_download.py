# -*- coding: utf-8 -*-
"""
Edited on 2022-02-27 15:14:12

@author: Fishercat
"""

import cdsapi

yy='2016';
mm='7'
c = cdsapi.Client()
for a in range(21,26):#此为day,小于10，就是01,02.....

    if int(a) < 10:
        aa =  "0" + str(a)
        a=aa
    aa=str(a)

    c.retrieve(
        'reanalysis-era5-single-levels',
        {
            'product_type':'reanalysis',
            'format':'grib2',
            'year': yy,
            'month': mm,
            'day': aa,
            'time': '00/to/23/by/1',
            'grid': [0.25, 0.25],
            'variable':[
                '10m_u_component_of_wind','10m_v_component_of_wind','2m_dewpoint_temperature',
                '2m_temperature', 'land_sea_mask', 'mean_sea_level_pressure',
                'sea_ice_cover', 'sea_surface_temperature', 'skin_temperature',
                'snow_depth', 'soil_temperature_level_1', 'soil_temperature_level_2',
                'soil_temperature_level_3', 'soil_temperature_level_4', 'surface_pressure',
                'volumetric_soil_water_layer_1', 'volumetric_soil_water_layer_2', 'volumetric_soil_water_layer_3',
                'volumetric_soil_water_layer_4', 'cloud_base_height', 'high_cloud_cover', 'low_cloud_cover',
                'medium_cloud_cover', 'total_cloud_cover', 'total_column_cloud_ice_water',
                'total_column_cloud_liquid_water', 'surface_net_solar_radiation', 'surface_net_thermal_radiation'
            ],
        },
        'sl-ERA5-'+yy+mm+aa+'00-23.grib')
    print(str(yy)+'-'+str(mm)+'-'+str(aa)+' download completed')
    c.retrieve(
        'reanalysis-era5-pressure-levels',
        {
            'product_type':'reanalysis',
            'format':'grib2',
            'pressure_level':[
                '1','2','3',
                '5','7','10',
                '20','30','50',
                '70','100','125',
                '150','175','200',
                '225','250','300',
                '350','400','450',
                '500','550','600',
                '650','700','750',
                '775','800','825',
                '850','875','900',
                '925','950','975',
                '1000'
            ],
                'year':yy,
                'month':mm,
                'day': aa,
                'time': '00/to/23/by/1',
                'grid':[0.25, 0.25],
            'variable':[
                'geopotential','relative_humidity','specific_humidity',
                'temperature','u_component_of_wind','v_component_of_wind',
            ]
        },
        'pl-ERA5-'+yy+mm+aa+'00-23.grib')