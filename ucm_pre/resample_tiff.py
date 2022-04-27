# -*- coding: utf-8 -*-
# @Author: Fishercat
# @Date  : 2022-03-26 01:28:26
# @Desc  : 将tiff文件重采样，可以提升或降低分辨率

from osgeo import gdal,gdalconst
import os,time

def resample_tiff(input_folder,output_folder,resolution,method,type):
    for filename in os.listdir(input_folder):
        start=time.time()
        tiff_data = gdal.Open(os.path.join(input_folder, filename), gdalconst.GA_ReadOnly)
        tiff_width, tiff_height = tiff_data.RasterXSize, tiff_data.RasterYSize
        tiff_geo = tiff_data.GetGeoTransform()  # 得到数据集的地理仿射信息,是一个包含六个元素的元组
        print("开始转换：" + filename)
        print("经纬度范围为：" + str([tiff_geo[0], tiff_geo[3] + tiff_height * tiff_geo[5], tiff_geo[0] + tiff_width * tiff_geo[1],tiff_geo[3]]))
        gdal.Warp(os.path.join(output_folder,filename), tiff_data, format='GTiff',
                  xRes=resolution, yRes=resolution,
                  outputBounds=[tiff_geo[0], tiff_geo[3]+tiff_height*tiff_geo[5], tiff_geo[0]+tiff_width*tiff_geo[1], tiff_geo[3]],
                  outputType=type, resampleAlg=method, targetAlignedPixels=True,
                  dstSRS='EPSG:4326')
        print("转换完成，耗时为：{}s".format(time.time()-start))
        print("开始优化")
        del tiff_data
        rewrite_tiff = gdal.Open(os.path.join(output_folder,filename), gdalconst.GA_ReadOnly)
        retiff_width, retiff_height = rewrite_tiff.RasterXSize, rewrite_tiff.RasterYSize
        retiff_proj = rewrite_tiff.GetProjection()  # 得到数据集的投影信息
        retiff_geo = rewrite_tiff.GetGeoTransform()  # 得到数据集的地理仿射信息,是一个包含六个元素的元组
        retiff_band = rewrite_tiff.GetRasterBand(1)
        retiff_list = retiff_band.ReadAsArray()
        del rewrite_tiff
        driver = gdal.GetDriverByName('GTiff')
        tiff_new = driver.Create(os.path.join(output_folder,filename), xsize=retiff_width, ysize=retiff_height,
                                 bands=1, eType=type, options=["TILED=YES", "COMPRESS=LZW"])
        tiff_new.SetProjection(retiff_proj)  # SetProjection写入投影im_proj
        tiff_new.SetGeoTransform(retiff_geo)  # SetGeoTransform写入地理信息
        tiff_new.GetRasterBand(1).WriteArray(retiff_list)
        del tiff_new
        print("优化完成，耗时为：{}s".format(time.time() - start))

if __name__ == '__main__':
    #resample_tiff(r"D:\Data\WRF-Chem_Files\UCM_file\Landuse\UCM_Shanghai\temp",
    #              r"D:\Data\WRF-Chem_Files\UCM_file\Landuse\Resample\Modified2_ucmfile\Tsinghua_9km",
    #              0.0625,gdal.GRA_Mode,gdal.GDT_UInt16)
    resample_tiff(r"D:\Data\WRF-Chem_Files\Land_Use_Data\LCZ_Shanghai\Landset8\4_LCZ_Shanghai\L1TP\LCZC.tif",
                  r"D:\Data\WRF-Chem_Files\Land_Use_Data\LCZ_Shanghai\Landset8\5_Resample\LCZC_resampled.tif",
                  100,gdal.GRA_Mode,gdal.GDT_UInt16)