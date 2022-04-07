# -*- coding: utf-8 -*-
# @File  : Sentinel2_2_geotiff.py
# @Author: Fishercat
# @Date  : 2022-03-17 22:56:33
# @Desc  : 读取Sentinel2并转为Geo_tiff
import os
import numpy as np
from osgeo import gdal, osr, ogr
import glob
# os.environ['CPL_ZIP_ENCODING'] = 'UTF-8'

def S2tif(filename):
    # 打开栅格数据集
    print(filename)
    root_ds = gdal.Open(filename)
    print(type(root_ds))
    # 返回结果是一个list，list中的每个元素是一个tuple，每个tuple中包含了对数据集的路径，元数据等的描述信息
    # tuple中的第一个元素描述的是数据子集的全路径
    ds_list = root_ds.GetSubDatasets()  # 获取子数据集。该数据以数据集形式存储且以子数据集形式组织
    visual_ds = gdal.Open(ds_list[0][0])  # 打开第1个数据子集的路径。ds_list有4个子集，内部前段是路径，后段是数据信息
    #visual_ds = gdal.Open(ds_list[1][0])  # 假如要获得20m分辨率的波段集合，只需要修改这一句
    visual_arr = visual_ds.ReadAsArray()  # 将数据集中的数据读取为ndarray

    # 创建.tif文件
    band_count = visual_ds.RasterCount  # 波段数
    xsize = visual_ds.RasterXSize
    ysize = visual_ds.RasterYSize
    out_tif_name = filename.split(".SAFE")[0] + ".tif"
    driver = gdal.GetDriverByName("GTiff")
    out_tif = driver.Create(out_tif_name, xsize, ysize, band_count, gdal.GDT_Float32)
    out_tif.SetProjection(visual_ds.GetProjection())  # 设置投影坐标
    out_tif.SetGeoTransform(visual_ds.GetGeoTransform())

    for index, band in enumerate(visual_arr):
        print(index)
        band = np.array([band])
        for i in range(len(band[:])):
            # 数据写出
            out_tif.GetRasterBand(index + 1).WriteArray(band[i])  # 将每个波段的数据写入内存，此时没有写入硬盘
    out_tif.FlushCache()  # 最终将数据写入硬盘
    out_tif = None  # 注意必须关闭tif文件


if __name__ == "__main__":
    '''
    SAFE_Path = (r'E:\RSDATA\Sentinel2\L2A')
    data_list = glob.glob(SAFE_Path + "\\*.SAFE")

    #filename = ('E:\\RSDATA\\Sentinel2\\L2A\\S2A_MSIL2A_20210220T024731_N9999_R132_T51STA_20210306T024402.SAFE\\MTD_MSIL2A.xml')
    for i in range(len(data_list)):
        data_path = data_list[i]
        filename = data_path + "\\MTD_MSIL2A.xml"
        S2tif(filename)
        print(data_path + "-----转tif成功")
    '''
    S2tif(r"D:\Data\WRF-Chem_Files\Land_Cover_Data\S2A\S2A_MSIL2A_20161230T024112_N9999_R089_T51RUQ_20220317T131549.SAFE\MTD_MSIL2A.xml")
    print("----转换结束----")

