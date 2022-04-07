# -*- coding: utf-8 -*-
# @Author: Fishercat
# @Date  : 2022-03-26 01:28:26
# @Desc  : 本文件包含以下功能：
#           - 将SNAP导出的NDVI的tiff数据以及下载的VIIRS数据进行修改，由于数据的经纬度混乱，因此需要重新写入
#           - 创建城市化指数图
#           - 修改原有的landuse数据，纳入31，32，33


import numpy as np
from osgeo import gdal, gdalconst


def rewrite_s2andvi(filename, outfilename, north_lat, south_lat, west_lon, east_lon):
    tiff_data = gdal.Open(filename)
    tiff_width, tiff_height = tiff_data.RasterXSize, tiff_data.RasterYSize
    tiff_proj = tiff_data.GetProjection()  # 得到数据集的投影信息
    tiff_geo = tiff_data.GetGeoTransform()  # 得到数据集的地理仿射信息,是一个包含六个元素的元组
    band1, band2 = tiff_data.GetRasterBand(1), tiff_data.GetRasterBand(2)
    listarray1, listarray2 = band1.ReadAsArray(), band2.ReadAsArray()
    # 创建新文件
    driver = gdal.GetDriverByName('GTiff')
    tiff_new = driver.Create(outfilename, xsize=tiff_width, ysize=tiff_height,
                             bands=2, eType=gdal.GDT_Float64, options=["TILED=YES", "COMPRESS=LZW"])
    # 重写坐标信息
    local_geotrans = list(tiff_geo)  # 每一张裁剪图的本地放射变化参数，0，3代表左上角坐标
    local_geotrans[0] = west_lon  # 经度
    local_geotrans[1] = (east_lon - west_lon) / tiff_width  # 经度
    local_geotrans[3] = north_lat  # 纬度
    local_geotrans[5] = (south_lat - north_lat) / tiff_height  # 纬度
    local_geotrans = tuple(local_geotrans)
    tiff_new.SetGeoTransform(local_geotrans)
    tiff_new.GetRasterBand(1).WriteArray(listarray1)
    tiff_new.GetRasterBand(2).WriteArray(listarray2)
    tiff_new.SetProjection(tiff_proj)  # SetProjection写入投影im_proj
    del tiff_new


def warp_s2andvi(filename, outfilename):
    gdal.Warp(outfilename, gdal.Open(filename, gdalconst.GA_ReadOnly), format='GTiff',
              xRes=0.00025, yRes=0.00025, outputBounds=[121.03, 30.70, 122.03, 31.50],
              outputType=gdal.GDT_Float64, resampleAlg=gdal.GRA_NearestNeighbour, targetAlignedPixels=True,
              srcSRS='EPSG:32651', dstSRS='EPSG:4326')
    print("Warp重采样，重投影完成，将优化TIFF")
    # Warp修改以后需要重新创建一个tiff并写入，因为Wrap函数无法修改部分格式
    tiff_data = gdal.Open(outfilename, gdalconst.GA_ReadOnly)
    tiff_width, tiff_height = tiff_data.RasterXSize, tiff_data.RasterYSize
    tiff_proj = tiff_data.GetProjection()  # 得到数据集的投影信息
    tiff_geo = tiff_data.GetGeoTransform()  # 得到数据集的地理仿射信息,是一个包含六个元素的元组
    band1, band2 = tiff_data.GetRasterBand(1), tiff_data.GetRasterBand(2)
    listarray1, listarray2 = band1.ReadAsArray(), band2.ReadAsArray()
    driver = gdal.GetDriverByName('GTiff')
    tiff_new = driver.Create(outfilename[0:-4] + "_edited.tif", xsize=tiff_width, ysize=tiff_height,
                             bands=2, eType=gdal.GDT_Float64, options=["TILED=YES", "COMPRESS=LZW"])
    tiff_new.SetProjection(tiff_proj)  # SetProjection写入投影im_proj
    tiff_new.SetGeoTransform(tiff_geo)  # SetGeoTransform写入地理信息
    tiff_new.GetRasterBand(1).WriteArray(listarray1)
    tiff_new.GetRasterBand(2).WriteArray(listarray2)
    del tiff_new
    print("优化完成")


def warp_viirs(filename, outfilename):
    gdal.Warp(outfilename, gdal.Open(filename, gdalconst.GA_ReadOnly), format='GTiff',
              xRes=0.00025, yRes=0.00025, outputBounds=[121.03, 30.70, 122.03, 31.50],
              outputType=gdal.GDT_Float32, resampleAlg=gdal.GRA_NearestNeighbour, targetAlignedPixels=True,
              dstSRS='EPSG:4326')
    print("Warp重采样，重投影完成，将优化TIFF")
    # Warp修改以后需要重新创建一个tiff并写入，因为Wrap函数无法修改部分格式
    tiff_data = gdal.Open(outfilename, gdalconst.GA_ReadOnly)
    tiff_width, tiff_height = tiff_data.RasterXSize, tiff_data.RasterYSize
    tiff_proj = tiff_data.GetProjection()  # 得到数据集的投影信息
    tiff_geo = tiff_data.GetGeoTransform()  # 得到数据集的地理仿射信息,是一个包含六个元素的元组
    band1 = tiff_data.GetRasterBand(1)
    listarray1 = band1.ReadAsArray()
    driver = gdal.GetDriverByName('GTiff')
    tiff_new = driver.Create(outfilename[0:-4] + "_edited.tif", xsize=tiff_width, ysize=tiff_height,
                             bands=1, eType=gdal.GDT_Float32, options=["TILED=YES", "COMPRESS=LZW"])
    tiff_new.SetProjection(tiff_proj)  # SetProjection写入投影im_proj
    tiff_new.SetGeoTransform(tiff_geo)  # SetGeoTransform写入地理信息
    tiff_new.GetRasterBand(1).WriteArray(listarray1)
    del tiff_new
    print("优化完成")




if __name__ == '__main__':
    # rewrite_s2andvi(r"D:\Data\WRF-Chem_Files\Land_Cover_Data\Sentinel_2_data\6_NDVI\S2A_MSIL2A_20160305_ndvi.tif",
    #                r"D:\Data\WRF-Chem_Files\Land_Cover_Data\Sentinel_2_data\6_NDVI\S2A_MSIL2A_20160305_ndvi_rewrite.tif",
    #                31.50,30.70,121.03,122.03)
    # warp_s2andvi(r"D:\Data\WRF-Chem_Files\Land_Cover_Data\Sentinel_2_data\6_NDVI\S2A_MSIL2A_20161217_ndvi.tif",
    #             r"D:\Data\WRF-Chem_Files\Land_Cover_Data\Sentinel_2_data\6_NDVI\S2A_MSIL2A_20161217_ndvi_rewrite.tif")
    warp_viirs(r"D:\Data\WRF-Chem_Files\Viirs_data\SVDNB_npp_20160101-20161231_75N060E_v10_c201807311200\SVDNB_npp_20160101-20161231_75N060E_vcm-orm_v10_c201807311200.avg_rade9.tif",
               r"D:\Data\WRF-Chem_Files\Viirs_data\viirs_2016.tif")

