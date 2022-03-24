# edited on 2022-03-04 22:10:27
# gdal库用于处理ucm所需的数据

from osgeo import gdal
import os


def landuse2binary_folder(tiff_folder, bil_folder, start_lon, end_lon, start_lat, end_lat):
    scale = '-scale min_val max_val'
    options_list = ['-of ENVI']
    options_string = " ".join(options_list)

    start_x, start_y = 0, 0
    for i in range(start_lon, end_lon+1, 10):
        for j in range(end_lat, start_lat-1, -10):
            for num in range(16):
                tiff_file = os.path.join(tiff_folder, str(i).zfill(3) + "E" + str(j) + "N" + str(num) + ".tif")
                if os.path.exists(tiff_file)==True:
                    print("开始转换" + tiff_file)
                    tiff_data = gdal.Open(tiff_file)
                    # 栅格矩阵的列数
                    tif_columns = tiff_data.RasterXSize
                    # 栅格矩阵的行数
                    tif_nrows = tiff_data.RasterYSize

                    if (num) % 4 == 0:
                        start_x_temp = int(start_x + (num) / 4 * tif_columns)
                        start_y_temp = int(start_y)
                    else:
                        start_x_temp = int(start_x_temp)
                        start_y_temp = int(start_y + (num) % 4 * tif_nrows)

                    name_x_s = str(start_x_temp + 1).zfill(5)
                    name_x_e = str(start_x_temp + tif_columns).zfill(5)
                    name_y_s = str(start_y_temp + 1).zfill(5)
                    name_y_e = str(start_y_temp + tif_nrows).zfill(5)

                    gdal.Translate(bil_folder + name_x_s + "-" + name_x_e + "." + name_y_s + "-" + name_y_e, tiff_file,
                                   options=options_string)
                    print(bil_folder + name_x_s + "-" + name_x_e + "." + name_y_s + "-" + name_y_e + "文件编译完成")
                else:
                    print(str(i) + "E" + str(j).zfill(3) + "N" + str(num) + ".tif文件不存在，将跳过")
            start_y = start_y+40000
        start_y = 0
        start_x = start_x + 40000


def landuse2binary_file(tiff_file, bil_folder):
    scale = '-scale min_val max_val'
    options_list = ['-of ENVI']
    options_string = " ".join(options_list)

    print("开始转换" + tiff_file)

    tiff_data = gdal.Open(tiff_file)
    # 栅格矩阵的列数
    tif_columns = tiff_data.RasterXSize
    # 栅格矩阵的行数
    tif_nrows = tiff_data.RasterYSize

    gdal.Translate(bil_folder + "00001" + "-" + str(tif_columns) + "." + "00001" + "-" + str(tif_nrows), tiff_file,
                   options=options_string)
    print(bil_folder + "00001" + "-" + str(tif_columns) + "." + "00001" + "-" + str(tif_nrows) + "文件编译完成")


def get_tiff_detail(tiff_file):
    tiff_data = gdal.Open(tiff_file)
    # 栅格矩阵的列数
    tif_columns = tiff_data.RasterXSize
    # 栅格矩阵的行数
    tif_nrows = tiff_data.RasterYSize
    # print(tiff_data.GetRasterBand(1).ReadAsArray())
    print(tiff_data.GetGeoTransform())
    print(tiff_data.GetProjection())
    print(tif_columns, tif_nrows)
    '''
    GeoTransform[0] /* top left x 左上角x坐标*/
    GeoTransform[1] /* w--e pixel resolution 东西方向上的像素分辨率*/
    GeoTransform[2] /* rotation, 0 if image is "north up" 如果北边朝上，地图的旋转角度*/
    GeoTransform[3] /* top left y 左上角y坐标*/
    GeoTransform[4] /* rotation, 0 if image is "north up" 如果北边朝上，地图的旋转角度*/
    GeoTransform[5] /* n-s pixel resolution 南北方向上的像素分辨率*/
    '''


if __name__ == '__main__':
    #get_tiff_detail(r"D:\Data\WRF-Chem Files\Land Cover Data\test_qinghua_lu_small\110E30N0.TIF")
    #get_tiff_detail(r"/media/fishercat/F3BF1447AE0CCFAE/Data/WRF-Chem Files/Land Cover Data/test_qinghua_lu_small/110E30N0")
    landuse2binary_folder(r"D:\new\re",
                          r"D:\new\bin\\",
                          110,120,30,40)
    # landuse2binary(r"D:\Data\WRF-Chem Files\Land Cover Data\test_qinghua_landuse",r"D:\Data\WRF-Chem Files\Land Cover Data\test_qinghua_binary\\")
