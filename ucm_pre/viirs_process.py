# -*- coding: utf-8 -*-
# @Author: Fishercat
# @Date  : 2022-03-26 01:28:26
# @Desc  : 用于将dnp-viirs文件数值标准化

from osgeo import gdal,gdalconst
import numpy as np

tiff_data = gdal.Open(r"D:\Data\WRF-Chem_Files\UCM_file\Viirs\viirs_2016_edited.tif", gdalconst.GA_ReadOnly)
tiff_proj = tiff_data.GetProjection()  # 得到数据集的投影信息
tiff_geo = tiff_data.GetGeoTransform()  # 得到数据集的地理仿射信息,是一个包含六个元素的元组
band = tiff_data.GetRasterBand(1)
listarray = band.ReadAsArray()

#nor_list=(listarray-np.min(listarray))/(np.max(listarray)-np.min(listarray))
listarray[np.where(listarray < 20)] = 20
nor_list=(listarray-20)/(np.max(listarray)-20)
print(np.max(listarray),np.min(listarray))

# 创建新文件
driver = gdal.GetDriverByName('GTiff')
output_tiff = driver.Create(r"D:\Data\WRF-Chem_Files\UCM_file\Viirs\nor_viirs_threshold.tif",
                            xsize=tiff_data.RasterXSize, ysize=tiff_data.RasterYSize,
                            bands=1, eType=gdal.GDT_Float32, options=["TILED=YES", "COMPRESS=LZW"])
output_tiff.GetRasterBand(1).WriteArray(nor_list)
output_tiff.SetGeoTransform(tiff_geo)  # driver对象创建的dataset对象具有SetGeoTransform方法，写入仿射变换参数GEOTRANS
output_tiff.SetProjection(tiff_proj)  # SetProjection写入投影im_proj
del output_tiff
