# edited on 2022-03-10 02:20:15
# 用于将需要的清华tiff数据复制到另一个文件夹

import os
import shutil

def copy_tiff_file(file_folder,to_folder,start_lat,end_lat,start_lon,end_lon,lat_ori="N",lon_ori="E"):
    """
    输出文件夹下所有文件名
    :param file_folder: 文件夹路径
    :param to_folder: 复制到的路径
    :param start_lat: 开始的纬度
    :param end_lat: 结束的纬度
    :param start_lon: 开始的经度
    :param end_lon: 结束的经度
    :param lat_ori: 北纬还是南纬
    :param lon_ori: 东经还是西经
    :return:
    """
    for lat in range(start_lat,end_lat+1,10):
        for lon in range(start_lon,end_lon+1,10):
            try:
                filename=str(lon)+lon_ori+"_"+str(lat)+lat_ori+".tif"
                file = os.path.join(file_folder, filename)
                file_to_path = os.path.join(to_folder, filename)
                shutil.copyfile(file, file_to_path)
                #shutil.move((file_path,file_to_path))
                print(file + "复制完成")
            except:
                print(filename+"不存在")


if __name__ == '__main__':
    file_folder = r'D:\Data\WRF-Chem_Files\Land_Cover_Data\TsingHua_Landuse_2015v1'
    to_folder = r'D:\Data\WRF-Chem_Files\UCM_file\Landuse\Origin_Tsinghua'
    copy_tiff_file(file_folder,to_folder,20,70,50,140)