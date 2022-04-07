# -*- coding: utf-8 -*-
# @Author: Fishercat
# @Date  : 2022-03-26 01:28:26
# @Desc  : 用于ndvi文件的修改

from osgeo import gdal,gdalconst
import numpy as np

tiff_data1 = gdal.Open(r"D:\Data\WRF-Chem_Files\UCM_file\NDVI\S2A_MSIL2A_20160305_ndvi_rewrite_edited.tif", gdalconst.GA_ReadOnly)
tiff_data2 = gdal.Open(r"D:\Data\WRF-Chem_Files\UCM_file\NDVI\S2A_MSIL2A_20160504_ndvi_rewrite_edited.tif", gdalconst.GA_ReadOnly)
tiff_data3 = gdal.Open(r"D:\Data\WRF-Chem_Files\UCM_file\NDVI\S2A_MSIL2A_20160630_ndvi_rewrite_edited.tif", gdalconst.GA_ReadOnly)
tiff_data4 = gdal.Open(r"D:\Data\WRF-Chem_Files\UCM_file\NDVI\S2A_MSIL2A_20161217_ndvi_rewrite_edited.tif", gdalconst.GA_ReadOnly)
tiff_proj = tiff_data1.GetProjection()  # 得到数据集的投影信息
tiff_geo = tiff_data1.GetGeoTransform()  # 得到数据集的地理仿射信息,是一个包含六个元素的元组
band1,bandflag1 = tiff_data1.GetRasterBand(1),tiff_data1.GetRasterBand(2)
listarray1, listflag1 = band1.ReadAsArray(),bandflag1.ReadAsArray()
band2,bandflag2 = tiff_data2.GetRasterBand(1),tiff_data2.GetRasterBand(2)
listarray2, listflag2 = band2.ReadAsArray(),bandflag2.ReadAsArray()
band3,bandflag3 = tiff_data3.GetRasterBand(1),tiff_data3.GetRasterBand(2)
listarray3, listflag3 = band3.ReadAsArray(),bandflag3.ReadAsArray()
band4,bandflag4 = tiff_data4.GetRasterBand(1),tiff_data4.GetRasterBand(2)
listarray4, listflag4 = band4.ReadAsArray(),bandflag4.ReadAsArray()
# NumPy np.ufunc.reduce允许沿给定轴累计应用功能。我们可以串联数组并减少numpy.maximum以保持累积的元素最大
listarray_new=np.maximum.reduce([listarray1,listarray2,listarray3,listarray4])
listarray_flag=np.minimum.reduce([listflag1,listflag2,listflag3,listflag4])

# 创建新文件
driver = gdal.GetDriverByName('GTiff')
output_tiff = driver.Create(r"D:\Data\WRF-Chem_Files\UCM_file\NDVI\max_ndvi.tif",
                            xsize=tiff_data1.RasterXSize, ysize=tiff_data1.RasterYSize,
                            bands=2, eType=gdal.GDT_Float64, options=["TILED=YES", "COMPRESS=LZW"])
output_tiff.GetRasterBand(1).WriteArray(listarray_new)
output_tiff.GetRasterBand(2).WriteArray(listarray_flag)
output_tiff.SetGeoTransform(tiff_geo)  # driver对象创建的dataset对象具有SetGeoTransform方法，写入仿射变换参数GEOTRANS
output_tiff.SetProjection(tiff_proj)  # SetProjection写入投影im_proj
del output_tiff