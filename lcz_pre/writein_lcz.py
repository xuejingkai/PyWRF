# -*- coding: utf-8 -*-
# @Author: Fishercat
# @Date  : 2022-03-26 01:28:26
# @Desc  : 将2017以及2015清华的landcover数据重分类至MODIFIED_IGBP_MODIS_NOAH的ucm模式

import gdalconst
from osgeo import gdal
import numpy as np

def search_most_class(array,x,y):
    '''
    搜索检索点范围内出现次数组多的城市分类
    @param array: 数据
    @param x: 检索点列
    @param y: 检索点行
    @return: most_class
    '''
    r=2
    while True:
        range_data=array[y-r:y+r,x-r:x+r]
        range_data=range_data[np.where(range_data>30)] # 只保留大于30的部分
        if range_data.size!=0:
            most_class = np.argmax(np.bincount(range_data.flatten()))  # 首先需要将数组转化为1维，之后找出现次数最多的分类（使用了bincount()与argmax()）
            print("{}范围内出现次数最多的分类为：{}".format(2*r+1,most_class))
            break
        else:
            print("没有找到城市分类，将扩大范围至r={}".format(r+2))
            r+=2
    return most_class

def edit_tiff_lcz(edt_tiff,to_tiff,lcz_tiff):
    '''
    这是修改版的lcz文件与原有分类结合。
    加入新功能：对未进行分类的城市地表进行检索，并将最近范围内最多的城市地表类型赋予其值
    @param originclass_tiff: 原有的分类文件
    @param lcz_tiff: 训练后的lcz文件
    @param dst_tiff: 保存文件
    @return: None
    '''
    print(edt_tiff+"开始修改")
    # 获取lczmap的数据
    lcz_tiff_data = gdal.Open(lcz_tiff,gdalconst.GA_ReadOnly)
    lcz_width,lcz_height=lcz_tiff_data.RasterXSize,lcz_tiff_data.RasterYSize
    lcz_tiff_band = lcz_tiff_data.GetRasterBand(1)
    lcz_list_array = lcz_tiff_band.ReadAsArray()
    # 获取基础landuse数据
    edt_tiff_data = gdal.Open(edt_tiff,gdalconst.GA_ReadOnly)
    edt_tiff_width, edt_tiff_height = edt_tiff_data.RasterXSize, edt_tiff_data.RasterYSize
    edt_tiff_proj = edt_tiff_data.GetProjection()  # 得到数据集的投影信息
    edt_tiff_geo = edt_tiff_data.GetGeoTransform()  # 得到数据集的地理仿射信息,是一个包含六个元素的元组
    edt_tiff_band = edt_tiff_data.GetRasterBand(1)
    edt_list_array = edt_tiff_band.ReadAsArray()
    # 将lcz写入基础landuse数据
    for i in range(lcz_height):        #i表示纬度索引
        for j in range(lcz_width):    #j表示经度索引
            edt_y,edt_x=i+487,j+838
            if lcz_list_array[i,j]==1:
                edt_list_array[edt_y, edt_x]=31
            elif lcz_list_array[i,j]==2:
                edt_list_array[edt_y, edt_x]=32
            elif lcz_list_array[i,j]==3:
                edt_list_array[edt_y, edt_x]=33
            elif lcz_list_array[i,j]==4:
                edt_list_array[edt_y, edt_x]=34
            elif lcz_list_array[i,j]==5:
                edt_list_array[edt_y, edt_x]=35
            elif lcz_list_array[i,j]==6:
                edt_list_array[edt_y, edt_x]=36
            elif lcz_list_array[i,j]==7:
                edt_list_array[edt_y, edt_x]=37
            elif lcz_list_array[i,j]==8:
                edt_list_array[edt_y, edt_x]=38
            elif lcz_list_array[i,j]==9:
                edt_list_array[edt_y, edt_x]=39
            elif lcz_list_array[i,j]==10:
                edt_list_array[edt_y, edt_x]=40
            elif lcz_list_array[i,j]==105:
                edt_list_array[edt_y, edt_x]=41
            else:
                continue
        print("进度为："+str((i)/(lcz_height+1)))
    # 将lcz范围内没有触及到的13分类重新进行分类
    count_13=0
    for i in range(lcz_height):        #i表示纬度索引
        for j in range(lcz_width):    #j表示经度索引
            edt_y,edt_x=i+487,j+838
            if edt_list_array[edt_y,edt_x]==13:
                print(edt_y,edt_x)
                edt_list_array[edt_y, edt_x]=search_most_class(edt_list_array,edt_x,edt_y)
                count_13+=1
    print("共有{}个13分类点没有进行分类,占比为{}%".format(count_13,count_13/(lcz_height*lcz_width)*100))
    driver = gdal.GetDriverByName('GTiff')
    file2 = driver.Create(to_tiff, xsize=edt_tiff_width, ysize=edt_tiff_height, bands=1,
                          eType=gdal.GDT_UInt16, options=["TILED=YES", "COMPRESS=LZW"])
    file2.GetRasterBand(1).WriteArray(edt_list_array)
    file2.SetGeoTransform(edt_tiff_geo)  # driver对象创建的dataset对象具有SetGeoTransform方法，写入仿射变换参数GEOTRANS
    file2.SetProjection(edt_tiff_proj)  # SetProjection写入投影im_proj
    print("修改完成")

if __name__ == '__main__':
    #readasarray后，list[i,j]为第几行，第几列
    edit_tiff_lcz(r"D:\Data\WRF-Chem_Files\Land_Use_Data\LCZ_Shanghai\Landset8\7_Combine\tsinghua_2015_shanghai_100m.tif",
                  r"D:\Data\WRF-Chem_Files\Land_Use_Data\LCZ_Shanghai\Landset8\7_Combine\tsinghua_2015_shanghai_100m_lcz_2_test.tif",
                  r"D:\Data\WRF-Chem_Files\Land_Use_Data\LCZ_Shanghai\Landset8\5_Resample\LCZC_2_resampled.tif")