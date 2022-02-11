#这个脚本仅用于读取ncfile的所有keys

import sys
sys.path.append("lib")
from GetKeys import get_ncfile_keys
import netCDF4 as nc
from wrf import getvar

#path:文件路径
#num:间隔多少个换行
path=r'D:\Data\WRF-Chem Files\WRF-Chem Simulation\1.Test\wrfout_1'  #nc文件地址
#path='/home/fishercat/Build_WRF/Examples/test/wrfinput_d01'  #nc文件地址
num=6   #一行多少个变量
print(get_ncfile_keys(path,num))
print(getvar(nc.Dataset(path),'PM2_5_DRY'))
#array('2016-07-21T00:00:00.000000000', dtype='datetime64[ns]')
#array('2016-07-21T06:00:00.000000000', dtype='datetime64[ns]')