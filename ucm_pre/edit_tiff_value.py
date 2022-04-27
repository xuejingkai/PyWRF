# edited on 2022-03-11 01:09:52
# 修改tiff某个点的值

from osgeo import gdal
import numpy as np
from crop_tiff import get_array_type
import random

def edit_tiff_point_value():
    return

def edit_tiff_value(tiff,to_tiff,start_x,end_x,start_y,end_y,):
    print(tiff+"开始修改")
    tiff_data = gdal.Open(tiff)
    tiff_width, tiff_height = tiff_data.RasterXSize, tiff_data.RasterYSize
    tiff_proj = tiff_data.GetProjection()  # 得到数据集的投影信息
    tiff_geo = tiff_data.GetGeoTransform()  # 得到数据集的地理仿射信息,是一个包含六个元素的元组
    tiff_band = tiff_data.GetRasterBand(1)
    list_array = tiff_band.ReadAsArray()
    for i in range(start_x,end_x,1):
        for j in range(start_y,end_y,1):
            if list_array[i,j]==17:
                list_array[i,j]=31
            '''
            elif list_array[i,j]==13:
                list_array[i,j]=32
            '''
        print("当前进度为："+str((i-start_x)/(end_x-start_x)))
    driver = gdal.GetDriverByName('GTiff')
    file2 = driver.Create(to_tiff, tiff_width, tiff_height, 1,
                          get_array_type(list_array))
    file2.GetRasterBand(1).WriteArray(list_array)
    file2.SetGeoTransform(tiff_geo)  # driver对象创建的dataset对象具有SetGeoTransform方法，写入仿射变换参数GEOTRANS
    file2.SetProjection(tiff_proj)  # SetProjection写入投影im_proj
    print("修改完成")

def edit_tiff(edt_tiff,to_tiff,ref_tiff):
    print(edt_tiff+"开始修改")
    ref_tiff_data = gdal.Open(ref_tiff)
    ref_tiff_geo = ref_tiff_data.GetGeoTransform()  # 得到数据集的地理仿射信息,是一个包含六个元素的元组
    ref_tiff_band = ref_tiff_data.GetRasterBand(1)
    ref_list_array = ref_tiff_band.ReadAsArray()

    edt_tiff_data = gdal.Open(edt_tiff)
    edt_tiff_width, edt_tiff_height = edt_tiff_data.RasterXSize, edt_tiff_data.RasterYSize
    edt_tiff_proj = edt_tiff_data.GetProjection()  # 得到数据集的投影信息
    edt_tiff_geo = edt_tiff_data.GetGeoTransform()  # 得到数据集的地理仿射信息,是一个包含六个元素的元组
    edt_tiff_band = edt_tiff_data.GetRasterBand(1)
    edt_list_array = edt_tiff_band.ReadAsArray()
    print(np.where(edt_list_array==17))

    for i in range(2000,2100,1):        #i表示纬度索引
        for j in range(4650,4750,1):    #j表示经度索引
            if ref_list_array[i,j]==31:
                lat = ref_tiff_geo[5] * i + ref_tiff_geo[3]
                lon=ref_tiff_geo[1]*j+ref_tiff_geo[0]

                edt_tiff_row = int((lat - edt_tiff_geo[3]) / edt_tiff_geo[5])
                edt_tiff_col=int((lon-edt_tiff_geo[0])/edt_tiff_geo[1])
                '''方案1
                for a in range(325):
                    row=random.randint(edt_tiff_row-25,edt_tiff_row+25)
                    col=random.randint(edt_tiff_col-25,edt_tiff_col+25)
                    edt_list_array[row,col]=31
                '''
                '''方案2
                for row in range(edt_tiff_row-25,edt_tiff_row+25,1):
                    for col in range(edt_tiff_col-25,edt_tiff_col+25,1):
                        edt_list_array[row,col]=31
                '''
                '''方案3
                random_row_s=random.randint(edt_tiff_row-25,edt_tiff_row)
                random_row_e=random.randint(edt_tiff_row,edt_tiff_row+25)
                random_col_s=random.randint(edt_tiff_col-25,edt_tiff_col)
                random_col_e=random.randint(edt_tiff_col,edt_tiff_col+25)
                for row in range(random_row_s,random_row_e,1):
                    for col in range(random_col_s,random_col_e,1):
                        edt_list_array[row,col]=31
                '''
                for row in range(edt_tiff_row-25,edt_tiff_row+25,1):
                    for col in range(edt_tiff_col-25,edt_tiff_col+25,1):
                        if edt_list_array[row,col]==13:
                            edt_list_array[row, col]=31

            elif ref_list_array[i,j]==32:
                lat = ref_tiff_geo[5] * i + ref_tiff_geo[3]
                lon=ref_tiff_geo[1]*j+ref_tiff_geo[0]

                edt_tiff_row = int((lat - edt_tiff_geo[3]) / edt_tiff_geo[5])
                edt_tiff_col=int((lon-edt_tiff_geo[0])/edt_tiff_geo[1])

                for row in range(edt_tiff_row-25,edt_tiff_row+25,1):
                    for col in range(edt_tiff_col-25,edt_tiff_col+25,1):
                        if edt_list_array[row,col]==13:
                            edt_list_array[row, col]=32

            elif ref_list_array[i,j]==33:
                lat = ref_tiff_geo[5] * i + ref_tiff_geo[3]
                lon=ref_tiff_geo[1]*j+ref_tiff_geo[0]

                edt_tiff_row = int((lat - edt_tiff_geo[3]) / edt_tiff_geo[5])
                edt_tiff_col=int((lon-edt_tiff_geo[0])/edt_tiff_geo[1])

                for row in range(edt_tiff_row-25,edt_tiff_row+25,1):
                    for col in range(edt_tiff_col-25,edt_tiff_col+25,1):
                        if edt_list_array[row,col]==13:
                            edt_list_array[row, col]=33

        print("进度为："+str((i-2000)/100))
    driver = gdal.GetDriverByName('GTiff')
    file2 = driver.Create(to_tiff, edt_tiff_width, edt_tiff_height, 1,
                          get_array_type(edt_list_array))
    file2.GetRasterBand(1).WriteArray(edt_list_array)
    file2.SetGeoTransform(edt_tiff_geo)  # driver对象创建的dataset对象具有SetGeoTransform方法，写入仿射变换参数GEOTRANS
    file2.SetProjection(edt_tiff_proj)  # SetProjection写入投影im_proj



if __name__ == '__main__':
    # readasarray后，list[i,j]为第几行，第几列
    #edit_tiff(r"D:\Data\WRF-Chem Files\Land Cover Data\QingHua_Landuse_2017v1\china_simulation\120E40N3.tif",
    #          r"D:\Data\WRF-Chem Files\Land Cover Data\QingHua_Landuse_2017v1\china_simulation\120E40N3_new3.tif",
    #          r"D:\Data\WRF-Chem Files\Land Cover Data\中国土地利用数据（1980-2015）\中国土地利用数据1980-2015\lucc2015\TIFF\rc_lucc2015_wgs84.tif")
    edit_tiff_value(r"D:\Data\WRF-Chem Files\Land Cover Data\QingHua_Landuse_2017v1\china_simulation\120E40N3.tif",
                    r"D:\Data\WRF-Chem Files\Land Cover Data\QingHua_Landuse_2017v1\china_simulation\120E40N3_new.tif",4000,8400,2000,8400)