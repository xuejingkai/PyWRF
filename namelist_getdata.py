# -*- coding: utf-8 -*-
# @Author: cat
# @Date  : 2022年04月18日21:35:22
# @Desc  : 用于数据提取的namelist文件，设置参数后执行文件在execute_file中

import numpy as np

ncfilename = r'/media/fishercat/F3BF1447AE0CCFAE/Data/WRF-Chem_Files/WRF-Chem_Simulation/lcz_1/wrfout_d03_2016-07-21'  # .nc文件的地址
timezone = 8  # 设置时区
inheight = False  # 是否沿着高度输出数据，需要先确保数据存在高度，将启用heightrange与timenum
intime = False  # 是否沿着时间输出数据，将启用timerange与heightnum
inall = True  # 同时输出所有高度与时间的数据，将同时启用heightrange和timerange
heightnum = 2  # 如果数据存在高度，并且仅沿时间输出，输出数据的高度层，高度编号可以通过read_ncfile_height获得
heightrange = np.arange(0, 5, 1)  # 仅在inheight为True时生效，高度的层数范围，高度编号可以通过read_ncfile_height获得
timerange = np.arange(40, 50, 2)  # 需要沿时间输出的话，时间的范围，仅在inheight为False时有效，时间编号可以使用read_ncfile_time获得
timenum = 5  # 仅在inheight=True时生效，输出指定时间编号的变量，时间编号可以使用read_ncfile_time获得
var = "tc"  # 提取的变量名
precision = '%.3f'  # 数据精度，.x表示保留x位小数
pos_precision = '%.7f'  # 坐标的精度，同上
savefolder = r'/media/fishercat/F3BF1447AE0CCFAE/Data/WRF-Chem_Files/WRF-Chem_Simulation/lcz_1/'  # 文件保存到的文件夹
savemode = "csv"  # 可以选择csv或者xlsx格式
