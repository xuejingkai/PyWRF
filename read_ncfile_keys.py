#这个脚本仅用于读取ncfile的所有keys

import sys
sys.path.append("lib")
from GetKeys import get_ncfile_keys
import netCDF4 as nc
from wrf import getvar
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeat
import matplotlib.ticker as mticker
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import cmaps
import matplotlib as mpl
from matplotlib.font_manager import FontProperties
import Fontprocess
import numpy as np
from matplotlib.colors import Normalize
Simsun = FontProperties(fname="./font/SimSun.ttf")
Times = FontProperties(fname="./font/Times.ttf")
mpl.rcParams['axes.unicode_minus']=False
config = {
    "mathtext.fontset":'stix',
}
mpl.rcParams.update(config)


#path:文件路径
#num:间隔多少个换行
path=r'/home/fishercat/Build_WRF/Examples/Test/geo_em.d01.nc'  #nc文件地址
#path='/home/fishercat/Build_WRF/Examples/test/wrfinput_d01'  #nc文件地址
num=6   #一行多少个变量
print(get_ncfile_keys(path,num))
for i in getvar(nc.Dataset(path),'LU_INDEX').values:
    print(i)
#print(getvar(nc.Dataset(path),'LU_INDEX'))
#array('2016-07-21T00:00:00.000000000', dtype='datetime64[ns]')
#array('2016-07-21T06:00:00.000000000', dtype='datetime64[ns]')
fig=plt.figure(figsize=(5,5),dpi=100)
axe=plt.subplot(1,1,1,projection=ccrs.PlateCarree())
axe.add_feature(cfeat.COASTLINE.with_scale('10m'), linewidth=1,color='black',zorder=1)
contourf = axe.contourf(getvar(nc.Dataset(path),'XLONG_M').values, getvar(nc.Dataset(path),'XLAT_M').values, getvar(nc.Dataset(path),'LU_INDEX'),
                        cmap=cmaps.amwg_blueyellowred, extend='neither',zorder=0)
cb = fig.colorbar(contourf, orientation='horizontal',spacing='uniform')  # orientation='vertical'
fig.show()
plt.show()