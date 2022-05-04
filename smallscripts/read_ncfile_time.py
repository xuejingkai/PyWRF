#这个脚本仅用于读取时间

import netCDF4 as nc
from lib.Readtime import get_ncfile_time

#仅需要修改一下文件的路径即可
path=r'D:\Data\WRF-Chem_Files\WRF-Chem_Simulation\lcz_7\Final\wrfout_d03_2016-07-23_00-30-00'
ncfile=nc.Dataset(path)
timelist=get_ncfile_time(ncfile=ncfile)
for i in range(len(timelist)):
    print("["+str(i)+"]"+timelist[i])