# -*- coding: utf-8 -*-
# @Author: Fishercat
# @Date  : 2022-04-23 01:16:22
# @Desc  : 计算albedo值；根据分类进行统计各个分类的平均albedo

from osgeo import gdal,gdalconst
import numpy as np

def gen_albedo_tiff(envi_path):
    # 参考文献：
    # Liang S. Narrowband to broadband conversions of land surface albedo I: Algorithms[J].
    # Remote sensing of environment, 2001, 76(2): 213-238.
    tiff=gdal.Open(envi_path)
    tiff_width, tiff_height = tiff.RasterXSize, tiff.RasterYSize
    tiff_proj = tiff.GetProjection()  # 得到数据集的投影信息
    tiff_geo = tiff.GetGeoTransform()  # 得到数据集的地理仿射信息,是一个包含六个元素的元组
    b = tiff.GetRasterBand(2).ReadAsArray()/10000
    r = tiff.GetRasterBand(4).ReadAsArray()/10000
    nir = tiff.GetRasterBand(5).ReadAsArray()/10000
    sir1 = tiff.GetRasterBand(6).ReadAsArray()/10000
    sir2 = tiff.GetRasterBand(7).ReadAsArray()/10000

    albedo=0.356*b+0.13*r+0.373*nir+0.085*sir1+0.072*sir2-0.0018

    driver = gdal.GetDriverByName('GTiff')
    albedo_file = driver.Create(r"D:\Data\WRF-Chem_Files\Land_Use_Data\LCZ_Shanghai\Landset8\8_Albedo\albedo2.tif", xsize=tiff_width, ysize=tiff_height, bands=1,
                                eType=gdal.GDT_Float32, options=["TILED=YES", "COMPRESS=LZW"])
    albedo_file.GetRasterBand(1).WriteArray(albedo)
    albedo_file.SetGeoTransform(tiff_geo)  # driver对象创建的dataset对象具有SetGeoTransform方法，写入仿射变换参数GEOTRANS
    albedo_file.SetProjection(tiff_proj)  # SetProjection写入投影im_proj
    albedo_file.FlushCache()
    albedo_file.GetRasterBand(1).ComputeStatistics(True)

def cal_class_albedo(albedo,lcztiff):
    '''
    统计
    @param albedo: albedo的tiff文件
    @param lcztiff: lcz的tiff文件
    @return : None
    '''
    albedo_list=[]
    for i in range(11):
        albedo_list.append([])
    lcz_data=gdal.Open(lcztiff,gdalconst.GA_ReadOnly)
    width,height=lcz_data.RasterXSize,lcz_data.RasterYSize
    lcz_classification=lcz_data.GetRasterBand(1).ReadAsArray()[2500:9000,1800:7000]
    albedo_tiff=gdal.Open(albedo,gdalconst.GA_ReadOnly)
    albedo_value=albedo_tiff.GetRasterBand(1).ReadAsArray()[2500:9000,1800:7000]
    print(width,height)
    for row in range(6500):
        for col in range(5200):
            if lcz_classification[row,col]<11:
                index=int(lcz_classification[row,col]-1)
                albedo_list[index].append(albedo_value[row,col])
            if lcz_classification[row, col] == 105:
                albedo_list[10].append(albedo_value[row,col])
        print(row/6500)
    for i in range(11):
        list=albedo_list[i]
        array=np.array(list)
        if np.shape(array)[0]==0:
            continue
        else:
            print("{}分类的平均albedo值为：{},共有{}个值：".format(i + 1, np.sum(array)/np.shape(array)[0], np.shape(array)[0]))
            array_without99=array[np.where(array<np.percentile(array,99))]
            print("{}分类，去除最大值以后的平均albedo值为：{},共有{}个值：".format(i + 1, np.sum(array_without99) / np.shape(array_without99)[0], np.shape(array_without99)[0]))



if __name__=="__main__":
    envi_path=r"D:\Data\WRF-Chem_Files\Land_Use_Data\LCZ_Shanghai\Landset8\8_Albedo\albedo_origin_L1TP.tif"
    envi_path=r"D:\Data\WRF-Chem_Files\Land_Use_Data\LCZ_Shanghai\Landset8\2_Prepare\8_merge2\merge_L1TP_118039_20170402.tif"
    albedo_path=r"D:\Data\WRF-Chem_Files\Land_Use_Data\LCZ_Shanghai\Landset8\8_Albedo\albedo.tif"
    lcz_path=r"D:\Data\WRF-Chem_Files\Land_Use_Data\LCZ_Shanghai\Landset8\4_LCZ_Shanghai\L1TP\version2\LCZC_2.tif"
    gen_albedo_tiff(envi_path)
    #cal_class_albedo(albedo_path,lcz_path)