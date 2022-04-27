# -*- coding: utf-8 -*-
# @Author: Fishercat
# @Date  : 2022-04-22 20:36:07
# @Desc  : 合成MCD43A3图像

from osgeo import gdal

pathlist=[r"D:\Data\WRF-Chem_Files\Albedo\MCD43A3_OriginData\MCD43A3_20170412\MCD43A3.A2017102.mosaic.006.2022112143007.mcrpgs_000501768218.Albedo_WSA_shortwave-Albedo_WSA_shortwave.tif",
          r"D:\Data\WRF-Chem_Files\Albedo\MCD43A3_OriginData\MCD43A3_20170414\MCD43A3.A2017104.mosaic.006.2022112143707.mcrpgs_000501768219.Albedo_WSA_shortwave-Albedo_WSA_shortwave.tif",
          r"D:\Data\WRF-Chem_Files\Albedo\MCD43A3_OriginData\MCD43A3_COMBINE\MCD43A3.A2017109.mosaic.006.2022112154214.mcrpgs_000501768231.Albedo_WSA_shortwave-Albedo_WSA_shortwave.tif",
          r"D:\Data\WRF-Chem_Files\Albedo\MCD43A3_OriginData\MCD43A3_COMBINE\MCD43A3.A2017113.mosaic.006.2022112154218.mcrpgs_000501768231.Albedo_WSA_shortwave-Albedo_WSA_shortwave.tif",
          r"D:\Data\WRF-Chem_Files\Albedo\MCD43A3_OriginData\MCD43A3_COMBINE3\MCD43A3.A2017140.mosaic.006.2022113164523.mcrpgs_000501768784.Albedo_WSA_shortwave-Albedo_WSA_shortwave.tif",
          r"D:\Data\WRF-Chem_Files\Albedo\MCD43A3_OriginData\MCD43A3_COMBINE3\MCD43A3.A2017144.mosaic.006.2022113164523.mcrpgs_000501768784.Albedo_WSA_shortwave-Albedo_WSA_shortwave.tif"]

tiff=gdal.Open(pathlist[0])
tiff_width, tiff_height = tiff.RasterXSize, tiff.RasterYSize
tiff_proj = tiff.GetProjection()  # 得到数据集的投影信息
tiff_geo = tiff.GetGeoTransform()  # 得到数据集的地理仿射信息,是一个包含六个元素的元组
data = tiff.GetRasterBand(1).ReadAsArray()
print(tiff_width,tiff_height)
tiff2=gdal.Open(pathlist[1])
data2 = tiff2.GetRasterBand(1).ReadAsArray()
tiff3=gdal.Open(pathlist[2])
data3 = tiff3.GetRasterBand(1).ReadAsArray()
tiff4=gdal.Open(pathlist[3])
data4 = tiff4.GetRasterBand(1).ReadAsArray()
tiff5=gdal.Open(pathlist[4])
data5 = tiff5.GetRasterBand(1).ReadAsArray()
tiff6=gdal.Open(pathlist[5])
data6 = tiff6.GetRasterBand(1).ReadAsArray()
new_data=data
for j in range(tiff_width):
    for i in range(tiff_height):
        count=0
        value=0
        if data[i,j]<30000:
            value=value+data[i,j]
            count+=1
        if data2[i,j]<30000:
            value=value+data2[i,j]
            count += 1
        if data3[i,j]<30000:
            value=value+data3[i,j]
            count += 1
        if data4[i,j]<30000:
            value=value+data4[i,j]
            count += 1
        if data5[i,j]<30000:
            value=value+data5[i,j]
            count += 1
        if data6[i,j]<30000:
            value=value+data6[i,j]
            count += 1
        if count==0:
            new_data[i, j] = -1
        else:
            new_data[i,j]=value/count
    print(j/tiff_width)
driver = gdal.GetDriverByName('GTiff')
albedo_file = driver.Create(r"D:\Data\WRF-Chem_Files\Albedo\MCD43A3_WSA_shortwave.tif", xsize=tiff_width, ysize=tiff_height, bands=1,
                            eType=gdal.GDT_Int16, options=["TILED=YES", "COMPRESS=LZW"])
albedo_file.GetRasterBand(1).WriteArray(new_data)
albedo_file.SetGeoTransform(tiff_geo)  # driver对象创建的dataset对象具有SetGeoTransform方法，写入仿射变换参数GEOTRANS
albedo_file.SetProjection(tiff_proj)  # SetProjection写入投影im_proj
albedo_file.FlushCache()
albedo_file.GetRasterBand(1).ComputeStatistics(True)