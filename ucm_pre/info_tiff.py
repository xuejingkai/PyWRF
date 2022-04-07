# -*- coding: utf-8 -*-
# @Author: Fishercat
# @Date  : 2022-04-05 03:39:18
# @Desc  : 读取tiff文件的信息

from osgeo import gdal, gdalconst

def gettiffinfo(filepath):
    tiff = gdal.Open(filepath, gdalconst.GA_ReadOnly)
    print(gdal.Info(tiff))

if __name__ == '__main__':
    gettiffinfo(r"D:\Data\WRF-Chem_Files\UCM_file\Viirs\viirs_2016_edited.tif")