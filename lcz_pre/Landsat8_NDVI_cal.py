# -*- coding: utf-8 -*-
# @Author: Fishercat
# @Date  : 2022-04-24 20:22:20
# @Desc  : 根据landsat8计算NDVI值

from osgeo import gdal,gdalconst
import numpy as np

def ndvi_ls8_cal(landsat8_path,dst_path):
    '''
    水体分割参考文献：[1]王大钊,王思梦,黄昌.Sentinel-2和Landsat8影像的四种常用水体指数地表水体提取对比[J].国土资源遥感,2019,31(03):157-165.
    @param landsat8_path: landsat8文件路径
    @param dst_path: 保存路径
    @return: None
    '''
    ls8_tiff=gdal.Open(landsat8_path,gdalconst.GA_ReadOnly)
    width,height=ls8_tiff.RasterXSize,ls8_tiff.RasterYSize
    proj = ls8_tiff.GetProjection()  # 得到数据集的投影信息
    geo = ls8_tiff.GetGeoTransform()  # 得到数据集的地理仿射信息,是一个包含六个元素的元组
    nir_band=ls8_tiff.GetRasterBand(5)
    r_band=ls8_tiff.GetRasterBand(4)
    g_band=ls8_tiff.GetRasterBand(3)
    nir_data=nir_band.ReadAsArray()
    r_data=r_band.ReadAsArray()
    g_data=g_band.ReadAsArray()
    ndvi=(nir_data-r_data)/(nir_data+r_data)
    ndwi=(g_data-nir_data)/(g_data+nir_data)
    ndwi_flag=np.zeros_like(ndwi)
    # 取1%~99%的置信区间
    ndvi[np.where(ndvi<=np.percentile(ndvi,1))]=np.percentile(ndvi,1)
    ndvi[np.where(ndvi>=np.percentile(ndvi,99))]=np.percentile(ndvi,99)
    # 水体分割阈值
    ndwi_flag[np.where(ndwi<=0.27)]=0 # 陆地
    ndwi_flag[np.where(ndwi>0.27)]=1 # 水体
    # 保存文件
    driver = gdal.GetDriverByName('GTiff')
    ndvi_file = driver.Create(dst_path, xsize=width,ysize=height, bands=3,
                                eType=gdal.GDT_Float32, options=["TILED=YES", "COMPRESS=LZW"])
    ndvi_file.GetRasterBand(1).WriteArray(ndvi)
    ndvi_file.GetRasterBand(2).WriteArray(ndwi)
    ndvi_file.GetRasterBand(3).WriteArray(ndwi_flag)
    ndvi_file.SetGeoTransform(geo)  # driver对象创建的dataset对象具有SetGeoTransform方法，写入仿射变换参数GEOTRANS
    ndvi_file.SetProjection(proj)  # SetProjection写入投影im_proj
    ndvi_file.FlushCache()
    ndvi_file.GetRasterBand(1).ComputeStatistics(True)
    ndvi_file.GetRasterBand(2).ComputeStatistics(True)

if __name__=="__main__":
    dst_path = r"D:\Data\WRF-Chem_Files\NDVI\FromLandsat8\ndvi_landsat8.tif"
    landsat8_path = r"D:\Data\WRF-Chem_Files\Land_Use_Data\LCZ_Shanghai\Landset8\3_Mosaic\mosaic_shangahi\L1TP_201704_mosaicSH.tif"
    ndvi_ls8_cal(landsat8_path,dst_path)


