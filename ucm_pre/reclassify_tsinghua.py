# edited on 2022-03-10 12:02:39
# 将2017清华的landcover数据重分类至MODIFIED_IGBP_MODIS_NOAH的ucm模式
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


def reclassify_TsinghuaLU(origin_folder, to_folder):
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


if __name__ == '__main__':
    #origin_folder = r'D:\Data\WRF-Chem Files\Land Cover Data\QingHua_Landuse_2017v1\china_simulation\cropped_tiff'
    origin_folder = r'D:\new\test_py2'
    to_folder = r'D:\new\re'
    reclassify_TsinghuaLU(origin_folder, to_folder)
