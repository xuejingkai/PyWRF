#这个脚本仅用于读取ncfile的所有keys

from lib.GetKeys import get_ncfile_keys
import netCDF4 as nc
from wrf import getvar
import numpy as np

path=r'D:\Data\WRF-Chem_Files\WRF-Chem_Simulation\ucm_modifiedParam_1\wrfout_d03_2016-07-21_00-00-00'  #nc文件地址
num=6   #一行多少个变量
print(get_ncfile_keys(path,num))
ncfile=nc.Dataset(path)
print(ncfile["ZNU"])