# -*- coding: utf-8 -*-
# @Author: Fishercat
# @Date  : 2022-04-17 16:29:36
# @Desc  : 合并landsat8多波段数据

from osgeo import gdal, gdalconst

def resize_tiff(filename_base, outfilename):
    data_list=[]
    num_list=[1,2,3,4,5,6,7,10,11]
    for i in range(9):
        print("正在读取文件："+filename_base+str(num_list[i])+".tif")
        tiff_data = gdal.Open(filename_base+str(num_list[i])+".tif", gdalconst.GA_ReadOnly)
        band = tiff_data.GetRasterBand(1)
        data_list.append(band.ReadAsArray())
    tiff_width, tiff_height = tiff_data.RasterXSize, tiff_data.RasterYSize
    tiff_proj = tiff_data.GetProjection()  # 得到数据集的投影信息
    tiff_geo = tiff_data.GetGeoTransform()  # 得到数据集的地理仿射信息,是一个包含六个元素的元组
    del tiff_data
    driver = gdal.GetDriverByName('GTiff')
    tiff_new = driver.Create(outfilename, xsize=tiff_width, ysize=tiff_height,
                             bands=9, eType=gdal.GDT_Float32,
                             options=["TILED=YES", "COMPRESS=LZW", "BIGTIFF=YES", "INTERLEAVE=PIXEL"])
    tiff_new.SetProjection(tiff_proj)  # SetProjection写入投影im_proj
    tiff_new.SetGeoTransform(tiff_geo)  # SetGeoTransform写入地理信息
    print("开始写入："+outfilename)
    for i in range(9):
        print("写入波段：{}".format(num_list[i]))
        tiff_new.GetRasterBand(i+1).WriteArray(data_list[i])
        tiff_new.GetRasterBand(i+1).SetDescription("band"+str(num_list[i]))
    '''
    在下一段代码中，你可以计算数据集中每个波段的统计信息
    这不是必须的，但它使一些软件更容易显示它
    统计数据包括平均值，最小值，最大值和标准差
    GIS可以使用此信息来拉伸屏幕上的数据并使其看起来更好
    在计算统计数据之前，你必须确保数据已写入磁盘而不是仅缓存在内存中，因此这是对FlushCache的调用
    然后循环遍历波段并计算每个波段的统计数据
    将False传递给此函数会告诉你需要实际统计信息而不是估计值，它可能来自概览图层（尚不存在）或从像元子集中采样
    如果估计值可以接受，那么你可以传递True；这也将使计算更快，因为不是每个像元都需要检查：
    '''
    print("开始计算统计值")
    tiff_new.FlushCache()
    for i in range(9):
        print("统计波段：{}".format(i+1))
        tiff_new.GetRasterBand(i+1).ComputeStatistics(True)
    '''
    最后一件事是为数据集构建概览图层
    由于这些像元值是连续数据，因此使用平均插值而不是默认的最近邻法
    你还可以指定要构建的五个级别的概视图
    碰巧有五个级别是你需要为此特定图像获取大小为256的图像块
    '''
    print("开始构建金字塔")
    tiff_new.BuildOverviews('average', [2, 4, 8, 16, 32, 64, 128])
    del tiff_new
    print("合并完成")

if __name__ == '__main__':
    resize_tiff(r"D:\Data\WRF-Chem_Files\Land_Use_Data\LCZ_Shanghai\Landset8\2_Prepare\4_resize\resize_L1TP_118038_20170402_b",
                r"D:\Data\WRF-Chem_Files\Land_Use_Data\LCZ_Shanghai\Landset8\2_Prepare\5_merge\merge_L1TP_118038_20170402.tif")
    resize_tiff(r"D:\Data\WRF-Chem_Files\Land_Use_Data\LCZ_Shanghai\Landset8\2_Prepare\4_resize\resize_L1TP_119038_20170308_b",
                r"D:\Data\WRF-Chem_Files\Land_Use_Data\LCZ_Shanghai\Landset8\2_Prepare\5_merge\merge_L1TP_119038_20170308.tif")
    resize_tiff(r"D:\Data\WRF-Chem_Files\Land_Use_Data\LCZ_Shanghai\Landset8\2_Prepare\4_resize\resize_L1TP_118039_20170402_b",
                r"D:\Data\WRF-Chem_Files\Land_Use_Data\LCZ_Shanghai\Landset8\2_Prepare\5_merge\merge_L1TP_118039_20170402.tif")
