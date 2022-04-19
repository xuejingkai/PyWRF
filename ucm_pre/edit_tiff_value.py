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

def edit_tiff_lcz(edt_tiff,to_tiff,lcz_tiff):
    print(edt_tiff+"开始修改")
    # 获取lczmap的数据
    lcz_tiff_data = gdal.Open(lcz_tiff)
    lcz_width,lcz_height=lcz_tiff_data.RasterXSize,lcz_tiff_data.RasterYSize
    lcz_tiff_band = lcz_tiff_data.GetRasterBand(1)
    lcz_list_array = lcz_tiff_band.ReadAsArray()
    # 获取基础landuse数据
    edt_tiff_data = gdal.Open(edt_tiff)
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
    driver = gdal.GetDriverByName('GTiff')
    file2 = driver.Create(to_tiff, xsize=edt_tiff_width, ysize=edt_tiff_height, bands=1,
                          eType=gdal.GDT_UInt16, options=["TILED=YES", "COMPRESS=LZW"])
    file2.GetRasterBand(1).WriteArray(edt_list_array)
    file2.SetGeoTransform(edt_tiff_geo)  # driver对象创建的dataset对象具有SetGeoTransform方法，写入仿射变换参数GEOTRANS
    file2.SetProjection(edt_tiff_proj)  # SetProjection写入投影im_proj
    print("修改完成")

if __name__ == '__main__':

    #edit_tiff(r"D:\Data\WRF-Chem Files\Land Cover Data\QingHua_Landuse_2017v1\china_simulation\120E40N3.tif",
    #          r"D:\Data\WRF-Chem Files\Land Cover Data\QingHua_Landuse_2017v1\china_simulation\120E40N3_new3.tif",
    #          r"D:\Data\WRF-Chem Files\Land Cover Data\中国土地利用数据（1980-2015）\中国土地利用数据1980-2015\lucc2015\TIFF\rc_lucc2015_wgs84.tif")
    #edit_tiff_value(r"D:\Data\WRF-Chem Files\Land Cover Data\QingHua_Landuse_2017v1\china_simulation\120E40N3.tif",
    #                r"D:\Data\WRF-Chem Files\Land Cover Data\QingHua_Landuse_2017v1\china_simulation\120E40N3_new.tif",4000,8400,2000,8400)
    #readasarray后，list[i,j]为第几行，第几列
    edit_tiff_lcz(r"D:\Data\WRF-Chem_Files\Land_Use_Data\LCZ_Shanghai\Landset8\7_Combine\tsinghua_2015_shanghai_100m.tif",
                  r"D:\Data\WRF-Chem_Files\Land_Use_Data\LCZ_Shanghai\Landset8\7_Combine\tsinghua_2015_shanghai_100m_lcz.tif",
                  r"D:\Data\WRF-Chem_Files\Land_Use_Data\LCZ_Shanghai\Landset8\5_Resample\LCZC_resampled.tif")