# edited on 2022-03-04 22:10:27
# gdal库用于处理ucm所需的数据

import rasterio
import os


def landuse2binary_folder(tiff_folder, bil_folder):
    start_x, start_y = 0, 0
    for i in range(110, 121, 10):
        for j in range(30, 41, 10):
            for num in range(16):
                tiff_file = os.path.join(tiff_folder, str(i) + "E" + str(j) + "N" + str(num) + ".TIF")
                print("开始转换" + tiff_file)
                tiff_data = rasterio.open(tiff_file)

                if (num) % 4==0:
                    start_x_temp=int(start_x)
                    start_y_temp=int(start_y+(num)/4*10000)
                else:
                    start_x_temp=int(start_x+(num)%4*10000)
                    start_y_temp=int(start_y_temp)

                name_x_s = "0" * (5 - len(str(start_x_temp + 1))) + str(start_x_temp + 1)
                name_x_e = "0" * (5 - len(str(start_x_temp + 10000))) + str(start_x_temp + 10000)
                name_y_s = "0" * (5 - len(str(start_y_temp + 1))) + str(start_y_temp + 1)
                name_y_e = "0" * (5 - len(str(start_y_temp + 10000))) + str(start_y_temp + 10000)

                data = tiff_data.read(1)[::-1]
                data.tofile(bil_folder + name_x_s + "-" + name_x_e + "." + name_y_s + "-" + name_y_e)
                print(bil_folder + name_x_s + "-" + name_x_e + "." + name_y_s + "-" + name_y_e + "文件编译完成")
            start_y = start_y+40000
        start_y = 0
        start_x = start_x + 40000


if __name__ == '__main__':
    landuse2binary_folder(r"/media/fishercat/F3BF1447AE0CCFAE/Data/WRF-Chem Files/Land Cover Data/test_qinghua_lu_small",
                          r"/home/fishercat/Build_WRF/WPS_GEOG/qinghua_lu_2/")
