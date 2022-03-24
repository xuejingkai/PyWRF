# edited on 2022-03-24 14:04:36
# 用于ndvi文件的修改

from osgeo import gdal
import numpy as np

tiff_data1 = gdal.Open(r"D:\Data\WRF-Chem_Files\Land_Cover_Data\Sentinel_2_data\7_Export_NDVI\S2A_MSIL2A_20160305_ndvi_rewrite_edited.tif")
tiff_data2 = gdal.Open(r"D:\Data\WRF-Chem_Files\Land_Cover_Data\Sentinel_2_data\7_Export_NDVI\S2A_MSIL2A_20160504_ndvi_rewrite_edited.tif")
tiff_data3 = gdal.Open(r"D:\Data\WRF-Chem_Files\Land_Cover_Data\Sentinel_2_data\7_Export_NDVI\S2A_MSIL2A_20160630_ndvi_rewrite_edited.tif")
tiff_data4 = gdal.Open(r"D:\Data\WRF-Chem_Files\Land_Cover_Data\Sentinel_2_data\7_Export_NDVI\S2A_MSIL2A_20161217_ndvi_rewrite_edited.tif")
tiff_proj = tiff_data1.GetProjection()  # 得到数据集的投影信息
tiff_geo = tiff_data1.GetGeoTransform()  # 得到数据集的地理仿射信息,是一个包含六个元素的元组
band1 = tiff_data1.GetRasterBand(1)
listarray1 = band1.ReadAsArray()
band2 = tiff_data2.GetRasterBand(1)
listarray2 = band2.ReadAsArray()
band3 = tiff_data3.GetRasterBand(1)
listarray3 = band3.ReadAsArray()
band4 = tiff_data4.GetRasterBand(1)
listarray4 = band4.ReadAsArray()
listarray_new=np.maximum.reduce([listarray1,listarray2,listarray3,listarray4])

# create new file
driver = gdal.GetDriverByName('GTiff')
output_tiff = driver.Create(r"D:\Data\WRF-Chem_Files\Land_Cover_Data\Sentinel_2_data\7_Export_NDVI\max_ndvi.tif",
                            xsize=tiff_data1.RasterXSize, ysize=tiff_data1.RasterYSize,
                            bands=1, eType=gdal.GDT_Float64, options=["TILED=YES", "COMPRESS=LZW"])
output_tiff.GetRasterBand(1).WriteArray(listarray_new)
output_tiff.SetGeoTransform(tiff_geo)  # driver对象创建的dataset对象具有SetGeoTransform方法，写入仿射变换参数GEOTRANS
output_tiff.SetProjection(tiff_proj)  # SetProjection写入投影im_proj
del output_tiff