# -*- coding: utf-8 -*-
# @Author: Fishercat
# @Date  : 2022-04-17 15:36:42
# @Desc  : 裁剪landsat8数据

import os
from osgeo import gdal, gdalconst

def resize_tiff(filename, outfilename,outputtype):
    print(filename)
    gdal.Warp(outfilename, gdal.Open(filename, gdalconst.GA_ReadOnly), format='GTiff',
              xRes=15, yRes=15, outputBounds=[301387.5, 3385582.5, 423277.5, 3531292.5],srcNodata=0, dstNodata=0,
              outputType=outputtype, resampleAlg=gdal.GRA_NearestNeighbour, targetAlignedPixels=True,
              srcSRS='EPSG:32651', dstSRS='EPSG:32651')
    print("Warp裁剪完成，将优化TIFF")
    # Warp修改以后需要重新创建一个tiff并写入，因为Wrap函数无法修改部分格式
    tiff_data = gdal.Open(outfilename, gdalconst.GA_ReadOnly)
    tiff_width, tiff_height = tiff_data.RasterXSize, tiff_data.RasterYSize
    tiff_proj = tiff_data.GetProjection()  # 得到数据集的投影信息
    tiff_geo = tiff_data.GetGeoTransform()  # 得到数据集的地理仿射信息,是一个包含六个元素的元组
    band= tiff_data.GetRasterBand(1)
    listarray= band.ReadAsArray()
    del tiff_data
    driver = gdal.GetDriverByName('GTiff')
    # options= ["INTERLEAVE=PIXEL"] 参数。没有这个参数，波段像素组织会错，保存出的图像只有横向的1/3。而且彩色完全不对。
    tiff_new = driver.Create(outfilename, xsize=tiff_width, ysize=tiff_height,
                             bands=1, eType=outputtype, options=["TILED=YES", "COMPRESS=LZW", "INTERLEAVE=BAND"])
    tiff_new.SetProjection(tiff_proj)  # SetProjection写入投影im_proj
    tiff_new.SetGeoTransform(tiff_geo)  # SetGeoTransform写入地理信息
    tiff_new.GetRasterBand(1).WriteArray(listarray)
    del tiff_new
    print("优化完成")

if __name__ == '__main__':
    for i in range(1,8,1):
        filename="atomcor_L1TP_119038_20170308_b"+str(i)+".tif"
        outputname="resize_L1TP_119038_20170308_b"+str(i)+".tif"
        resize_tiff(os.path.join(r"D:\Data\WRF-Chem_Files\Land_Use_Data\LCZ_Shanghai\Landset8\2_Prepare\6_atmos_corr",filename),
                    os.path.join(r"D:\Data\WRF-Chem_Files\Land_Use_Data\LCZ_Shanghai\Landset8\2_Prepare\7_resize2",outputname),
                    gdal.GDT_Float32)
    for i in range(1,8,1):
        filename="atomcor_L1TP_118039_20170402_b"+str(i)+".tif"
        outputname="resize_L1TP_118039_20170402_b"+str(i)+".tif"
        resize_tiff(os.path.join(r"D:\Data\WRF-Chem_Files\Land_Use_Data\LCZ_Shanghai\Landset8\2_Prepare\6_atmos_corr",filename),
                    os.path.join(r"D:\Data\WRF-Chem_Files\Land_Use_Data\LCZ_Shanghai\Landset8\2_Prepare\7_resize2",outputname),
                    gdal.GDT_Float32)
    for i in range(1,8,1):
        filename="atomcor_L1TP_118038_20170402_b"+str(i)+".tif"
        outputname="resize_L1TP_118038_20170402_b"+str(i)+".tif"
        resize_tiff(os.path.join(r"D:\Data\WRF-Chem_Files\Land_Use_Data\LCZ_Shanghai\Landset8\2_Prepare\6_atmos_corr",filename),
                    os.path.join(r"D:\Data\WRF-Chem_Files\Land_Use_Data\LCZ_Shanghai\Landset8\2_Prepare\7_resize2",outputname),
                    gdal.GDT_Float32)