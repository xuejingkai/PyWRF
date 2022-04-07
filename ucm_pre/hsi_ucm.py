# -*- coding: utf-8 -*-
# @Author: Fishercat
# @Date  : 2022-04-05 03:39:18
# @Desc  : 用于HSI系数以及ucm模式数据重写

import numpy as np
from osgeo import gdal, gdalconst

def write_HSI(ndvi_file, viirs_file, output_file):
    print("开始处理")
    ndvi_tiff = gdal.Open(ndvi_file, gdalconst.GA_ReadOnly)
    viirs_file = gdal.Open(viirs_file, gdalconst.GA_ReadOnly)
    ndvi_band = ndvi_tiff.GetRasterBand(1)
    ndvi_list = ndvi_band.ReadAsArray()
    viirs_band = viirs_file.GetRasterBand(1)
    viirs_list = viirs_band.ReadAsArray()
    ref_band = ndvi_tiff.GetRasterBand(2)
    ref_list = ref_band.ReadAsArray()

    hsi_list = (1 - ndvi_list + viirs_list) / (1 - viirs_list + ndvi_list + viirs_list * ndvi_list)
    hsi_list[np.where(hsi_list == np.inf)] = np.percentile(hsi_list, 99)
    hsi_list[np.where(ref_list != 0)] = 0

    driver = gdal.GetDriverByName('GTiff')
    hsi_tiff = driver.Create(output_file, xsize=ndvi_tiff.RasterXSize, ysize=ndvi_tiff.RasterYSize,
                             bands=1, eType=gdal.GDT_Float32, options=["TILED=YES", "COMPRESS=LZW"])
    hsi_tiff.SetProjection(ndvi_tiff.GetProjection())  # SetProjection写入投影im_proj
    hsi_tiff.SetGeoTransform(ndvi_tiff.GetGeoTransform())  # SetGeoTransform写入地理信息
    hsi_tiff.GetRasterBand(1).WriteArray(hsi_list)

    nor_hsi_list = hsi_list.copy()
    # 去除异常巨大的值
    nor_hsi_list[np.where(hsi_list >= np.percentile(hsi_list, 99))] = np.percentile(hsi_list, 99)
    # 去除小于0的值，这些值往往代表水体等
    nor_hsi_list[np.where(hsi_list < 0)] = 0
    # 标准化
    print("开始标准化")
    nor_hsi_list = (nor_hsi_list - np.min(nor_hsi_list)) / (np.max(nor_hsi_list) - np.min(nor_hsi_list))
    driver = gdal.GetDriverByName('GTiff')
    nor_hsi_tiff = driver.Create(output_file[0:-4] + "_nor.tif", xsize=ndvi_tiff.RasterXSize,
                                 ysize=ndvi_tiff.RasterYSize,
                                 bands=1, eType=gdal.GDT_Float32, options=["TILED=YES", "COMPRESS=LZW"])
    nor_hsi_tiff.SetProjection(ndvi_tiff.GetProjection())  # SetProjection写入投影im_proj
    nor_hsi_tiff.SetGeoTransform(ndvi_tiff.GetGeoTransform())  # SetGeoTransform写入地理信息
    nor_hsi_tiff.GetRasterBand(1).WriteArray(nor_hsi_list)
    del nor_hsi_tiff, hsi_tiff

def write_HSI_threshold(ndvi_file, viirs_file, output_file):
    print("开始处理")
    ndvi_tiff = gdal.Open(ndvi_file, gdalconst.GA_ReadOnly)
    viirs_file = gdal.Open(viirs_file, gdalconst.GA_ReadOnly)
    ndvi_band = ndvi_tiff.GetRasterBand(1)
    ndvi_list = ndvi_band.ReadAsArray()
    viirs_band = viirs_file.GetRasterBand(1)
    viirs_list = viirs_band.ReadAsArray()
    ref_band = ndvi_tiff.GetRasterBand(2)
    ref_list = ref_band.ReadAsArray()

    hsi_list = (1 - ndvi_list + viirs_list) / (1 - viirs_list + ndvi_list + viirs_list * ndvi_list)
    hsi_list[np.where(ref_list != 0)] = 0

    driver = gdal.GetDriverByName('GTiff')
    hsi_tiff = driver.Create(output_file, xsize=ndvi_tiff.RasterXSize, ysize=ndvi_tiff.RasterYSize,
                             bands=1, eType=gdal.GDT_Float32, options=["TILED=YES", "COMPRESS=LZW"])
    hsi_tiff.SetProjection(ndvi_tiff.GetProjection())  # SetProjection写入投影im_proj
    hsi_tiff.SetGeoTransform(ndvi_tiff.GetGeoTransform())  # SetGeoTransform写入地理信息
    hsi_tiff.GetRasterBand(1).WriteArray(hsi_list)

    print("将数据分类至UCM种类")
    ucm_hsi_list = hsi_list.copy()
    # 按照数值比例将其分为CIT,HIR,LIR
    ucm_hsi_list[np.where(hsi_list >= np.percentile(hsi_list, 95))] = 33
    ucm_hsi_list[
        np.where(np.logical_and(hsi_list < np.percentile(hsi_list, 95),
                                hsi_list > np.percentile(hsi_list, 80)))] = 32
    ucm_hsi_list[np.where(hsi_list <= np.percentile(hsi_list, 80))] = 31
    #ucm_hsi_list[np.where(np.logical_and(hsi_list <= np.percentile(hsi_list, 85),hsi_list > np.percentile(hsi_list, 55)))] = 31
    #ucm_hsi_list[np.where(hsi_list <= np.percentile(hsi_list, 55))] = 0

    driver = gdal.GetDriverByName('GTiff')
    nor_hsi_tiff = driver.Create(output_file[0:-4] + "_ucm.tif", xsize=ndvi_tiff.RasterXSize,
                                 ysize=ndvi_tiff.RasterYSize,
                                 bands=1, eType=gdal.GDT_Float32, options=["TILED=YES", "COMPRESS=LZW"])
    nor_hsi_tiff.SetProjection(ndvi_tiff.GetProjection())  # SetProjection写入投影im_proj
    nor_hsi_tiff.SetGeoTransform(ndvi_tiff.GetGeoTransform())  # SetGeoTransform写入地理信息
    nor_hsi_tiff.GetRasterBand(1).WriteArray(ucm_hsi_list)
    del nor_hsi_tiff, hsi_tiff

def write_ucm_shanghai(origin_LU, x_start, x_end, y_start, y_end, hsi_data):
    lu_data = gdal.Open(origin_LU, gdalconst.GA_ReadOnly)
    band_lu = lu_data.GetRasterBand(1)
    lu_all = band_lu.ReadAsArray()
    lu_shanghai = lu_all[y_start:y_end, x_start:x_end]
    urb_data = gdal.Open(hsi_data, gdalconst.GA_ReadOnly)
    band_urb = urb_data.GetRasterBand(1)
    listarray_urb = band_urb.ReadAsArray()
    lu_shanghai[np.where(np.logical_and(lu_shanghai == 13, listarray_urb > np.percentile(listarray_urb, 95)))] = 33
    lu_shanghai[
        np.where(np.logical_and(np.logical_and(lu_shanghai == 13, listarray_urb < np.percentile(listarray_urb, 95)),
                                listarray_urb > np.percentile(listarray_urb, 70)))] = 32
    lu_shanghai[np.where(np.logical_and(lu_shanghai == 13, listarray_urb < np.percentile(listarray_urb, 70)))] = 31
    lu_all[y_start:y_end, x_start:x_end] = lu_shanghai
    # 修改landuse
    driver = gdal.GetDriverByName('GTiff')
    lu_edit_tiff = driver.Create(origin_LU[0:-4] + "_urb.tif",
                                 xsize=lu_data.RasterXSize, ysize=lu_data.RasterYSize,
                                 bands=1, eType=gdal.GDT_UInt16, options=["TILED=YES", "COMPRESS=LZW"])
    lu_edit_tiff.GetRasterBand(1).WriteArray(lu_all)
    lu_edit_tiff.SetGeoTransform(lu_data.GetGeoTransform())  # driver对象创建的dataset对象具有SetGeoTransform方法，写入仿射变换参数GEOTRANS
    lu_edit_tiff.SetProjection(lu_data.GetProjection())  # SetProjection写入投影im_proj
    print("修改后的土地利用数据修改完成")
    del lu_edit_tiff
    # 创建urb_param
    urb_param = np.zeros((y_end - y_start, x_end - x_start))
    urb_param[np.where(lu_shanghai == 31)] = 1
    urb_param[np.where(lu_shanghai == 32)] = 2
    urb_param[np.where(lu_shanghai == 33)] = 3
    urb_tiff = driver.Create(r"D:\Data\WRF-Chem_Files\UCM_file\Urban_classification\urb_param.tif",
                             xsize=x_end - x_start, ysize=y_end - y_start,
                             bands=1, eType=gdal.GDT_UInt16, options=["TILED=YES", "COMPRESS=LZW"])
    urb_tiff.GetRasterBand(1).WriteArray(urb_param)
    urb_tiff.SetGeoTransform(urb_data.GetGeoTransform())  # driver对象创建的dataset对象具有SetGeoTransform方法，写入仿射变换参数GEOTRANS
    urb_tiff.SetProjection(urb_data.GetProjection())  # SetProjection写入投影im_proj
    print("URB_PARAM创建完成")
    del urb_tiff

def write_ucm_shanghai_threshold(origin_LU, x_start, x_end, y_start, y_end, urb_clas):
    lu_data = gdal.Open(origin_LU, gdalconst.GA_ReadOnly)
    band_lu = lu_data.GetRasterBand(1)
    lu_all = band_lu.ReadAsArray()
    lu_shanghai = lu_all[y_start:y_end, x_start:x_end]
    urb_data = gdal.Open(urb_clas, gdalconst.GA_ReadOnly)
    band_urb = urb_data.GetRasterBand(1)
    listarray_urb = band_urb.ReadAsArray()
    lu_shanghai[np.where(np.logical_and(lu_shanghai == 13, listarray_urb == 33))] = 33
    lu_shanghai[np.where(np.logical_and(lu_shanghai == 13, listarray_urb == 32))] = 32
    lu_shanghai[np.where(np.logical_and(lu_shanghai == 13, listarray_urb == 31))] = 31
    lu_all[y_start:y_end, x_start:x_end] = lu_shanghai
    # 修改landuse
    driver = gdal.GetDriverByName('GTiff')
    lu_edit_tiff = driver.Create(origin_LU[0:-4] + "_urb_threshold.tif",
                                 xsize=lu_data.RasterXSize, ysize=lu_data.RasterYSize,
                                 bands=1, eType=gdal.GDT_UInt16, options=["TILED=YES", "COMPRESS=LZW"])
    lu_edit_tiff.GetRasterBand(1).WriteArray(lu_all)
    lu_edit_tiff.SetGeoTransform(lu_data.GetGeoTransform())  # driver对象创建的dataset对象具有SetGeoTransform方法，写入仿射变换参数GEOTRANS
    lu_edit_tiff.SetProjection(lu_data.GetProjection())  # SetProjection写入投影im_proj
    print("修改后的土地利用数据修改完成")
    del lu_edit_tiff
    # 创建urb_param
    urb_param = np.zeros((y_end - y_start, x_end - x_start))
    urb_param[np.where(lu_shanghai == 31)] = 1
    urb_param[np.where(lu_shanghai == 32)] = 2
    urb_param[np.where(lu_shanghai == 33)] = 3
    urb_tiff = driver.Create(r"D:\Data\WRF-Chem_Files\UCM_file\Urban_classification\urb_param_threshold.tif",
                             xsize=x_end - x_start, ysize=y_end - y_start,
                             bands=1, eType=gdal.GDT_UInt16, options=["TILED=YES", "COMPRESS=LZW"])
    urb_tiff.GetRasterBand(1).WriteArray(urb_param)
    urb_tiff.SetGeoTransform(urb_data.GetGeoTransform())  # driver对象创建的dataset对象具有SetGeoTransform方法，写入仿射变换参数GEOTRANS
    urb_tiff.SetProjection(urb_data.GetProjection())  # SetProjection写入投影im_proj
    print("URB_PARAM创建完成")
    del urb_tiff

if __name__ == '__main__':
    write_HSI_threshold(r"D:\Data\WRF-Chem_Files\UCM_file\NDVI\max_ndvi.tif",
                        r"D:\Data\WRF-Chem_Files\UCM_file\Viirs\nor_viirs_threshold.tif",
                        r"D:\Data\WRF-Chem_Files\UCM_file\HSI_data_threshold\hsi_threshold.tif")
    #write_ucm_shanghai(r"D:\Data\WRF-Chem_Files\UCM_file\Landuse\UCM_Shanghai\origin\120E_40N3.tif", 4120, 8120, 4000, 7200,
    #                   r"D:\Data\WRF-Chem_Files\UCM_file\HSI_data\hsi_nor.tif")
    write_ucm_shanghai_threshold(r"D:\Data\WRF-Chem_Files\UCM_file\Landuse\UCM_Shanghai\origin\120E_40N3.tif",
                                 4120, 8120, 4000, 7200,
                                 r"D:\Data\WRF-Chem_Files\UCM_file\HSI_data_threshold\hsi_threshold_ucm.tif")