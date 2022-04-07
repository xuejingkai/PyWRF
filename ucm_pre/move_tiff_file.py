# edit on 2022-03-08 13:57:12
# 用于Globeland30数据的处理，将各个文件夹的文件均移到同一个文件夹下

import os
import shutil


def move_file(dir_path, to_path):
    """
    输出文件夹下所有文件名
    :param dir_path: 文件夹路径
    :return:
    """
    for dir in os.listdir(dir_path):
        dir = os.path.join(dir_path, dir)
        if os.path.isdir(dir):
            for file in os.listdir(dir):
                if file.endswith(".tif"):
                    file_path = os.path.join(dir, file)
                    file_to_path = os.path.join(to_path, file)
                    shutil.copyfile(file_path, file_to_path)
                    # shutil.move((file_path,file_to_path))
                    print(file + "复制完成")


if __name__ == '__main__':
    dir_path = r'D:\Data\WRF-Chem_Files\Land_Cover_Data\TsingHua_Landuse_2015v1'
    to_path = r'D:\Data\WRF-Chem_Files\UCM_file\Landuse\Origin_Tsinghua'
    move_file(dir_path, to_path)
