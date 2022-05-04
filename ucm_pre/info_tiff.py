# -*- coding: utf-8 -*-
# @Author: Fishercat
# @Date  : 2022-04-05 03:39:18
# @Desc  : 读取tiff文件的信息

from osgeo import gdal, gdalconst

def gettiffinfo(filepath):
    tiff = gdal.Open(filepath, gdalconst.GA_ReadOnly)
    print(gdal.Info(tiff))

if __name__ == '__main__':
    #gettiffinfo(r"D:\Data\WRF-Chem_Files\Land_Use_Data\LCZ_Shanghai\Landset8\2_Prepare\4_resize\resize_L1TP_119038_20170308_b1.tif")
    #gettiffinfo(r"D:\Data\WRF-Chem_Files\Land_Use_Data\LCZ_Shanghai\Landset8\2_Prepare\3_b10b11_resize\15m_118038_b10.tif")
    #gettiffinfo(r"D:\Data\WRF-Chem_Files\Land_Use_Data\LCZ_Shanghai\Landset8\5_Resample\LCZC_resampled.tif")
    #gettiffinfo(r"D:\Data\WRF-Chem_Files\Land_Use_Data\LCZ_Shanghai\Landset8\7_Combine\tsinghua_2015_shanghai_100m_lcz_2_wgs84.tif")
    #gettiffinfo(r"D:\Data\WRF-Chem_Files\NDVI\FromLandsat8\ndvi_landsat8_resampled.tif")
    gettiffinfo(r"D:\Data\WRF-Chem_Files\Land_Use_Data\LCZ_Shanghai\Landset8\9_Anthro_heat\sh_lczc_100m_wgs84.tif")
    gettiffinfo(r"D:\Data\WRF-Chem_Files\Population_Data\sh_landscan_2016_resampled.tif")
    #gettiffinfo(r"D:\Data\WRF-Chem_Files\Land_Use_Data\LCZ_Shanghai\Landset8\4_Mosaic\L2SP\mosaic_shanghai_20170402.tif")