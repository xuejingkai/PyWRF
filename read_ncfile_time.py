#这个脚本仅用于读取时间

import netCDF4 as nc
import sys
sys.path.append("lib")
from Readtime import get_ncfile_time

#仅需要修改一下文件的路径即可
path=r'D:\Data\WRF-Chem Files\WRF-Chem Simulation\1.Test\wrfout_1'
ncfile=nc.Dataset(path)
timelist=get_ncfile_time(ncfile=ncfile)
for i in range(len(timelist)):
    print("["+str(i)+"]"+timelist[i])