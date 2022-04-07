# -*- coding: utf-8 -*-
# @Author: Fishercat
# @Date  : 2022-03-26 01:28:26
# @Desc  : 将大TIFF文件切割为多个小TIFF文件

from osgeo import gdal
import os

origin_folder = r"D:\Data\WRF-Chem Files\Land Cover Data\QingHua_Landuse_2017v1\china_simulation\origin\100E30N.tif"


def get_array_type(array_data):
    """
    输出文件夹下所有文件名
    :param array_data: 输入numpy.array类型
    :return: dtype的名字对应gdal的datatype类型
    """
    if 'int8' in array_data.dtype.name:  # 输入的im_data是一个numpy.array类型，dtype的名字来对应gdal的datatype类型
        datatype = gdal.GDT_Byte
    elif 'int16' in array_data.dtype.name:
        datatype = gdal.GDT_UInt16
    else:
        datatype = gdal.GDT_Float32
    return datatype

def progress(percent, msg, tag):
    """进度回调函数"""
    print(percent, msg, tag)

def crop_tiff(tiff_folder, to_folder, num_x, num_y):
    """
    输出文件夹下所有文件名
    :param tiff_folder: 需要裁剪的tiff文件夹
    :param to_folder: 输出文件夹
    :param num_x: x方向分为多少个文件
    :param num_y: y方向分为多少个文件
    :return: dtype的名字对应gdal的datatype类型
    """
    for filename in os.listdir(tiff_folder):
        tiff_data = gdal.Open(os.path.join(tiff_folder, filename))
        tiff_width, tiff_height = tiff_data.RasterXSize, tiff_data.RasterYSize
        tiff_proj = tiff_data.GetProjection()  # 得到数据集的投影信息
        tiff_geo = tiff_data.GetGeoTransform()  # 得到数据集的地理仿射信息,是一个包含六个元素的元组
        print("开始裁剪：" + filename)
        '''
        GeoTransform[0] /* top left x 左上角x坐标*/
        GeoTransform[1] /* w--e pixel resolution 东西方向上的像素分辨率*/
        GeoTransform[2] /* rotation, 0 if image is "north up" 如果北边朝上，地图的旋转角度*/
        GeoTransform[3] /* top left y 左上角y坐标*/
        GeoTransform[4] /* rotation, 0 if image is "north up" 如果北边朝上，地图的旋转角度*/
        GeoTransform[5] /* n-s pixel resolution 南北方向上的像素分辨率*/
        '''
        tiff_num = 0
        for x in range(num_x):
            for y in range(num_y):
                list_array = tiff_data.ReadAsArray(x * int(tiff_width / num_x), y * int(tiff_height / num_y),
                                                   int(tiff_width / num_x), int(tiff_height / num_y))
                # ReadAsArray(xoff=,yoff=,xsize=,ysize=) 其中xsize与ysize不需要变化
                print("裁剪片段：" + str(
                    [x * int(tiff_width / num_x), y * int(tiff_height / num_y), (x + 1) * int(tiff_width / num_x),
                     (y + 1) * int(tiff_height / num_y)]))
                # 更新裁剪后的位置信息
                local_geotrans = list(tiff_geo)  # 每一张裁剪图的本地放射变化参数，0，3代表左上角坐标
                local_geotrans[0] = tiff_geo[0] + x * tiff_geo[1] * tiff_width / num_x  # 分别更新为裁剪后的每一张局部图的左上角坐标
                local_geotrans[3] = tiff_geo[3] + y * tiff_geo[5] * tiff_height / num_y
                local_geotrans = tuple(local_geotrans)
                # 写入分割后的文件
                print("输出文件：" + filename[0:-4] + str(tiff_num) + ".tif")
                driver = gdal.GetDriverByName("GTiff")
                new_tiff = driver.Create(os.path.join(to_folder, filename[0:-4] + str(tiff_num) + ".tif"),
                                         xsize=int(tiff_width / num_x),
                                         ysize=int(tiff_height / num_y),
                                         bands=1, eType=gdal.GDT_UInt16, # 给出文件的路径，宽度，高度，波段数（倒过来）和数据类型，创建空文件，并确定开辟多大内存，像素值的类型用gdal类型
                                         options=["TILED=YES", "COMPRESS=LZW"])
                # 设置头文件信息：仿射变化参数，投影信息，数据体
                new_tiff.SetGeoTransform(local_geotrans)  # driver对象创建的dataset对象具有SetGeoTransform方法，写入仿射变换参数GEOTRANS
                new_tiff.SetProjection(tiff_proj)  # SetProjection写入投影im_proj
                new_tiff.GetRasterBand(1).WriteArray(
                    list_array)  # i从0开始，因此GetRasterBand(i+1),每个波段里用writearray写入图像信息数组im_data
                print(local_geotrans)
                del new_tiff  # 写完之后释放内存空间
                tiff_num += 1


if __name__ == '__main__':
    crop_tiff(r"D:\Data\WRF-Chem_Files\UCM_file\Landuse\Origin_Tsinghua",
              r"D:\Data\WRF-Chem_Files\UCM_file\Landuse\Cropped_Tsinghua",
              4, 4)
