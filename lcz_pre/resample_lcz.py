# -*- coding: utf-8 -*-
# @Author: Fishercat
# @Date  : 2022-03-26 01:28:26
# @Desc  : 将tiff文件重采样，可以提升或降低分辨率,专用于lcz
import numpy as np
from osgeo import gdal,gdalconst
import os,time

def resample_lcz(inputfile,outputfile,resolution,method,type,bound1=301387.5,bound2=3385582.5,bound3=423277.5,bound4=3531292.5):
    start=time.time()
    tiff_data = gdal.Open(inputfile, gdalconst.GA_ReadOnly)
    print("开始转换：" + inputfile)
    gdal.Warp(outputfile, tiff_data, format='GTiff',
              xRes=resolution, yRes=resolution,
              outputBounds=[bound1,bound2,bound3,bound4],
              outputType=type, resampleAlg=method, targetAlignedPixels=True,
              srcSRS='EPSG:32651', dstSRS='EPSG:32651')
    print("转换完成，耗时为：{}s".format(time.time()-start))
    print("开始优化")
    del tiff_data
    rewrite_tiff = gdal.Open(outputfile, gdalconst.GA_ReadOnly)
    retiff_width, retiff_height = rewrite_tiff.RasterXSize, rewrite_tiff.RasterYSize
    retiff_proj = rewrite_tiff.GetProjection()  # 得到数据集的投影信息
    retiff_geo = rewrite_tiff.GetGeoTransform()  # 得到数据集的地理仿射信息,是一个包含六个元素的元组
    retiff_band = rewrite_tiff.GetRasterBand(1)
    retiff_list = retiff_band.ReadAsArray()
    del rewrite_tiff
    driver = gdal.GetDriverByName('GTiff')
    tiff_new = driver.Create(outputfile, xsize=retiff_width, ysize=retiff_height,
                             bands=1, eType=type, options=["TILED=YES", "COMPRESS=LZW"])
    tiff_new.SetProjection(retiff_proj)  # SetProjection写入投影im_proj
    tiff_new.SetGeoTransform(retiff_geo)  # SetGeoTransform写入地理信息
    tiff_new.GetRasterBand(1).WriteArray(retiff_list)
    tiff_new.GetRasterBand(1).ComputeStatistics(True)   # 统计值
    tiff_new.BuildOverviews('average', [2, 4, 8, 16, 32, 64, 128])  # 金字塔
    del tiff_new
    print("优化完成，耗时为：{}s".format(time.time() - start))

def resample_ndvi(inputfile,outputfile,resolution,method,type,raster_band,bound1=301387.5,bound2=3385582.5,bound3=423277.5,bound4=3531292.5):
    start=time.time()
    tiff_data = gdal.Open(inputfile, gdalconst.GA_ReadOnly)
    print("开始转换：" + inputfile)
    gdal.Warp(outputfile, tiff_data, format='GTiff',
              xRes=resolution, yRes=resolution,
              outputBounds=[bound1,bound2,bound3,bound4],
              outputType=type, resampleAlg=method, targetAlignedPixels=True,
              srcSRS='EPSG:32651', dstSRS='EPSG:32651')
    print("转换完成，耗时为：{}s".format(time.time()-start))
    print("开始优化")
    del tiff_data
    rewrite_tiff = gdal.Open(outputfile, gdalconst.GA_ReadOnly)
    retiff_width, retiff_height = rewrite_tiff.RasterXSize, rewrite_tiff.RasterYSize
    retiff_proj = rewrite_tiff.GetProjection()  # 得到数据集的投影信息
    retiff_geo = rewrite_tiff.GetGeoTransform()  # 得到数据集的地理仿射信息,是一个包含六个元素的元组
    retiff_band = rewrite_tiff.GetRasterBand(raster_band)
    retiff_list = retiff_band.ReadAsArray()
    del rewrite_tiff
    driver = gdal.GetDriverByName('GTiff')
    tiff_new = driver.Create(outputfile, xsize=retiff_width, ysize=retiff_height,
                             bands=1, eType=type, options=["TILED=YES", "COMPRESS=LZW"])
    tiff_new.SetProjection(retiff_proj)  # SetProjection写入投影im_proj
    tiff_new.SetGeoTransform(retiff_geo)  # SetGeoTransform写入地理信息
    tiff_new.GetRasterBand(1).WriteArray(retiff_list)
    tiff_new.GetRasterBand(1).WriteArray(retiff_list)
    tiff_new.GetRasterBand(1).ComputeStatistics(True)   # 统计值
    tiff_new.BuildOverviews('average', [2, 4, 8, 16, 32, 64, 128])  # 金字塔
    del tiff_new
    print("优化完成，耗时为：{}s".format(time.time() - start))

def resample_pop(inputfile,outputfile,resolution,method,type,raster_band,bound1=301387.5,bound2=3385582.5,bound3=423277.5,bound4=3531292.5):
    start=time.time()
    tiff_data = gdal.Open(inputfile, gdalconst.GA_ReadOnly)
    print("开始转换：" + inputfile)
    gdal.Warp(outputfile, tiff_data, format='GTiff',
              xRes=resolution, yRes=resolution,
              outputBounds=[bound1,bound2,bound3,bound4],
              outputType=type, resampleAlg=method, targetAlignedPixels=False,
              srcSRS='EPSG:4326', dstSRS='EPSG:4326')
    print("转换完成，耗时为：{}s".format(time.time()-start))
    print("开始优化")
    del tiff_data
    rewrite_tiff = gdal.Open(outputfile, gdalconst.GA_ReadOnly)
    retiff_width, retiff_height = rewrite_tiff.RasterXSize, rewrite_tiff.RasterYSize
    retiff_proj = rewrite_tiff.GetProjection()  # 得到数据集的投影信息
    retiff_geo = rewrite_tiff.GetGeoTransform()  # 得到数据集的地理仿射信息,是一个包含六个元素的元组
    retiff_band = rewrite_tiff.GetRasterBand(raster_band)
    retiff_list = retiff_band.ReadAsArray()
    del rewrite_tiff
    driver = gdal.GetDriverByName('GTiff')
    tiff_new = driver.Create(outputfile, xsize=retiff_width, ysize=retiff_height,
                             bands=1, eType=type, options=["TILED=YES", "COMPRESS=LZW"])
    tiff_new.SetProjection(retiff_proj)  # SetProjection写入投影im_proj
    tiff_new.SetGeoTransform(retiff_geo)  # SetGeoTransform写入地理信息
    tiff_new.GetRasterBand(1).WriteArray(retiff_list)
    tiff_new.GetRasterBand(1).WriteArray(retiff_list)
    tiff_new.GetRasterBand(1).ComputeStatistics(True)   # 统计值
    tiff_new.BuildOverviews('average', [2, 4, 8, 16, 32, 64, 128])  # 金字塔
    del tiff_new
    print("优化完成，耗时为：{}s".format(time.time() - start))

if __name__ == '__main__':
    #resample_lcz(r"D:\Data\WRF-Chem_Files\Land_Use_Data\LCZ_Shanghai\Landset8\7_Combine\temp.tif",
    #              r"D:\Data\WRF-Chem_Files\Land_Use_Data\LCZ_Shanghai\Landset8\7_Combine\tsinghua_2015_shanghai_100m.tif",
    #              100,gdal.GRA_Mode,gdal.GDT_UInt16,bound1=217500,bound2=3325000,bound3=450000,bound4=3580000)
    #resample_lcz(r"D:\Data\WRF-Chem_Files\Land_Use_Data\LCZ_Shanghai\Landset8\4_LCZ_Shanghai\L1TP\version2\LCZC_2.tif",
    #              r"D:\Data\WRF-Chem_Files\Land_Use_Data\LCZ_Shanghai\Landset8\5_Resample\LCZC_2_resampled.tif",
    #              100,gdal.GRA_Mode,gdal.GDT_UInt16,bound1=301300,bound2=3385500,bound3=423300,bound4=3531300)
    #resample_lcz(r"D:\Data\WRF-Chem_Files\Albedo\MCD43A3_BSA_shortwave.tif",
    #             r"D:\Data\WRF-Chem_Files\Albedo\MCD43A3_BSA_shortwave_resample.tif",
    #             100,gdal.GRA_Bilinear,gdal.GDT_Int16,bound1=301300,bound2=3385500,bound3=423300,bound4=3531300)
    #resample_lcz(r"D:\Data\WRF-Chem_Files\Emissitive\GLASS03A01.V40.A2017305.h28v05.2019361_GLASS03A01.tif",
    #             r"D:\Data\WRF-Chem_Files\Emissitive\GLASSBBE5.tif",
    #             100,gdal.GRA_Bilinear,gdal.GDT_Int16,bound1=301300,bound2=3385500,bound3=423300,bound4=3531300)
    #resample_ndvi(r"D:\Data\WRF-Chem_Files\NDVI\FromLandsat8\ndvi_landsat8.tif",
    #              r"D:\Data\WRF-Chem_Files\NDVI\FromLandsat8\ndwiflag_landsat8_resampled.tif",
    #              100,gdal.GRA_NearestNeighbour,gdal.GDT_Int16,3,bound1=301300,bound2=3385500,bound3=423300,bound4=3531300)
    #resample_ndvi(r"D:\Data\WRF-Chem_Files\NDVI\FromLandsat8\ndvi_landsat8.tif",
    #              r"D:\Data\WRF-Chem_Files\NDVI\FromLandsat8\ndvi_landsat8_resampled.tif",
    #              100,gdal.GRA_Cubic,gdal.GDT_Float32,1,bound1=301300,bound2=3385500,bound3=423300,bound4=3531300)
    resample_pop(r"D:\Data\WRF-Chem_Files\Population_Data\sh_landscan_2016.tif",
                  r"D:\Data\WRF-Chem_Files\Population_Data\sh_landscan_2016_resampled.tif",
                  0.001049841,gdal.GRA_Average,gdal.GDT_Float32,1,bound1=120.8988428,bound2=30.6905337,bound3=121.9035407,bound4=31.8506080)