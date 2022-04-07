# -*- coding: utf-8 -*-
# @Author: Fishercat
# @Date  : 2022-03-26 01:28:26
# @Desc  : 将2017以及2015清华的landcover数据重分类至MODIFIED_IGBP_MODIS_NOAH的ucm模式

'''
    older : new
    1 : 31（ucm） 低密度人口   12(common)
    8 : 32（ucm） 高密度人口   13(common)
    9 : 33（ucm） 工厂等      16(common)
    2 : 5
    3 : 10
    4 : 7
    5 : 11
    6 : 17
    7 : 19
    10 ：15
'''

from osgeo import gdal
import os
import numpy as np
import time
from crop_tiff import get_array_type


def reclassify_TsinghuaLU_2017(origin_folder, to_folder):
    for filename in os.listdir(origin_folder):
        print(filename + "开始重分类")
        file = gdal.Open(os.path.join(origin_folder, filename))
        band = file.GetRasterBand(1)
        listarray_origin = band.ReadAsArray()
        tiff_proj = file.GetProjection()  # 得到数据集的投影信息
        tiff_geo = file.GetGeoTransform() # 得到数据集的地理仿射信息,是一个包含六个元素的元组
        time_start = time.time()
        # reclassification
        listarray = listarray_origin.copy() #此前这里没有添加copy方法，导致出现了一个很严重的错误，即位于后部分的代码会将之前修改好的数值继续修改
        listarray[np.where(listarray_origin == 1)] = 12
        listarray[np.where(listarray_origin == 8)] = 13
        listarray[np.where(listarray_origin == 9)] = 16
        print(filename + "已完成30%，耗时"+str(time.time() - time_start)+"s")
        listarray[np.where(listarray_origin == 2)] = 5
        listarray[np.where(listarray_origin == 3)] = 10
        listarray[np.where(listarray_origin == 4)] = 7
        print(filename + "已完成60%，耗时"+str(time.time() - time_start)+"s")
        listarray[np.where(listarray_origin == 5)] = 11
        listarray[np.where(listarray_origin == 6)] = 17
        listarray[np.where(listarray_origin == 7)] = 19
        listarray[np.where(listarray_origin == 10)] = 15
        # create new file
        driver = gdal.GetDriverByName('GTiff')
        file2 = driver.Create(os.path.join(to_folder, filename), xsize=file.RasterXSize, ysize=file.RasterYSize,
                              bands=1, eType=gdal.GDT_UInt16,options=["TILED=YES", "COMPRESS=LZW"])
        file2.GetRasterBand(1).WriteArray(listarray)
        file2.SetGeoTransform(tiff_geo)  # driver对象创建的dataset对象具有SetGeoTransform方法，写入仿射变换参数GEOTRANS
        file2.SetProjection(tiff_proj)  # SetProjection写入投影im_proj
        print(filename + "重分类完成，耗时"+str(time.time() - time_start)+"s")
        del file2

def reclassify_TsinghuaLU_2015(origin_folder, to_folder):
    for filename in os.listdir(origin_folder):
        print(filename + "开始重分类")
        file = gdal.Open(os.path.join(origin_folder, filename))
        band = file.GetRasterBand(1)
        listarray_origin = band.ReadAsArray()
        tiff_proj = file.GetProjection()  # 得到数据集的投影信息
        tiff_geo = file.GetGeoTransform() # 得到数据集的地理仿射信息,是一个包含六个元素的元组
        time_start = time.time()
        # reclassification
        listarray = listarray_origin.copy() #此前这里没有添加copy方法，导致出现了一个很严重的错误，即位于后部分的代码会将之前修改好的数值继续修改
        # 农田类
        listarray[np.where(listarray_origin == 11)] = 12    # 稻田
        listarray[np.where(listarray_origin == 12)] = 12    # 温室
        listarray[np.where(listarray_origin == 13)] = 12    # 其他农田
        listarray[np.where(listarray_origin == 14)] = 14    # 果树林
        listarray[np.where(listarray_origin == 15)] = 16    # 贫瘠农田
        # 森林类
        listarray[np.where(listarray_origin == 21)] = 2     # 阔叶林
        listarray[np.where(listarray_origin == 22)] = 2     # 阔叶林
        listarray[np.where(listarray_origin == 23)] = 1     # 针叶林
        listarray[np.where(listarray_origin == 24)] = 1     # 针叶林
        listarray[np.where(listarray_origin == 25)] = 5     # 混合
        listarray[np.where(listarray_origin == 26)] = 5     # 混合
        print(filename + "已完成35%，耗时" + str(time.time() - time_start) + "s")
        # 草地类
        listarray[np.where(listarray_origin == 31)] = 10    # 草地
        listarray[np.where(listarray_origin == 32)] = 10    # 草地
        listarray[np.where(listarray_origin == 33)] = 10    # 草地
        # 灌木丛
        listarray[np.where(listarray_origin == 41)] = 7     # 灌木丛
        listarray[np.where(listarray_origin == 42)] = 6     # 灌木丛
        # 湿地
        listarray[np.where(listarray_origin == 51)] = 11    # 沼泽
        listarray[np.where(listarray_origin == 52)] = 11    # 泥地
        listarray[np.where(listarray_origin == 53)] = 11    # 泥地
        # 海洋
        listarray[np.where(listarray_origin == 0)] = 17     # 海洋
        listarray[np.where(listarray_origin == 60)] = 17    # 海洋
        print(filename + "已完成70%，耗时" + str(time.time() - time_start) + "s")
        # 荒原
        listarray[np.where(listarray_origin == 71)] = 19    # 荒原-树木
        listarray[np.where(listarray_origin == 72)] = 19    # 荒原-草
        # 城市
        listarray[np.where(listarray_origin == 80)] = 13    # 城市
        # 光秃秃的土地
        listarray[np.where(listarray_origin == 90)] = 16    # bareland
        listarray[np.where(listarray_origin == 92)] = 16    # bareland
        # 冰雪
        listarray[np.where(listarray_origin == 101)] = 15   # snow
        listarray[np.where(listarray_origin == 102)] = 15   # ice
        # 云
        listarray[np.where(listarray_origin == 120)] = 17   # cloud
        # create new file
        driver = gdal.GetDriverByName('GTiff')
        file2 = driver.Create(os.path.join(to_folder, filename), xsize=file.RasterXSize, ysize=file.RasterYSize,
                              bands=1, eType=gdal.GDT_UInt16,options=["TILED=YES", "COMPRESS=LZW"])
        file2.GetRasterBand(1).WriteArray(listarray)
        file2.SetGeoTransform(tiff_geo)  # driver对象创建的dataset对象具有SetGeoTransform方法，写入仿射变换参数GEOTRANS
        file2.SetProjection(tiff_proj)  # SetProjection写入投影im_proj
        print(filename + "重分类完成，耗时"+str(time.time() - time_start)+"s")
        del file2

def reclassify_TsinghuaLU_URB(origin_file,to_file):
    file = gdal.Open(origin_file)
    band = file.GetRasterBand(1)
    listarray_origin = band.ReadAsArray()
    tiff_proj = file.GetProjection()  # 得到数据集的投影信息
    tiff_geo = file.GetGeoTransform()  # 得到数据集的地理仿射信息,是一个包含六个元素的元组
    # reclassification
    listarray = listarray_origin.copy()  # 此前这里没有添加copy方法，导致出现了一个很严重的错误，即位于后部分的代码会将之前修改好的数值继续修改
    listarray[np.where(listarray_origin == 1)] = 22  # LR
    listarray[np.where(listarray_origin == 2)] = 23  # HR
    listarray[np.where(listarray_origin == 3)] = 24  # CIT
    # create new file
    driver = gdal.GetDriverByName('GTiff')
    file2 = driver.Create(to_file, xsize=file.RasterXSize, ysize=file.RasterYSize,
                          bands=1, eType=gdal.GDT_UInt16, options=["TILED=YES", "COMPRESS=LZW"])
    file2.GetRasterBand(1).WriteArray(listarray)
    file2.SetGeoTransform(tiff_geo)  # driver对象创建的dataset对象具有SetGeoTransform方法，写入仿射变换参数GEOTRANS
    file2.SetProjection(tiff_proj)  # SetProjection写入投影im_proj
    print("URB文件生成完成")
    del file2

if __name__ == '__main__':
    #origin_folder = r'D:\Data\WRF-Chem Files\Land Cover Data\QingHua_Landuse_2017v1\china_simulation\cropped_tiff'
    origin_folder = r'D:\Data\WRF-Chem_Files\UCM_file\URB_PARAM\urb_param.tif'
    to_folder = r'D:\Data\WRF-Chem_Files\UCM_file\urban_fraction\frc_urb2d.tif'
    #reclassify_TsinghuaLU_2015(origin_folder, to_folder)
    reclassify_TsinghuaLU_URB(origin_folder,to_folder)
