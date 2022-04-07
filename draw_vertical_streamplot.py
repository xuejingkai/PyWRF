import netCDF4 as nc
import xarray as xr
import cmaps
from wrf import getvar,ll_to_xy,to_np,vertcross,CoordPair,interplevel
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeat
import matplotlib.ticker as mticker
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import cmaps
import matplotlib as mpl
from matplotlib.font_manager import FontProperties
import sys
sys.path.append("lib")
from lib.Readtime import get_ncfile_time
import numpy as np
from matplotlib.colors import Normalize
Simsun = FontProperties(fname="./font/SimSun.ttf")
Times = FontProperties(fname="./font/Times.ttf")
mpl.rcParams['axes.unicode_minus']=False
config = {
    "mathtext.fontset":'stix',
}
mpl.rcParams.update(config)

ncfile=nc.Dataset(r'D:\Data\WRF-Chem_Files\WRF-Chem_Simulation\ucm_modifiedParam_1\wrfout_d03_2016-07-21_00-00-00')

time=106
ua=getvar(ncfile,'ua',timeidx=time)
va=getvar(ncfile,'va',timeidx=time)
wa=getvar(ncfile,'wa',timeidx=time)
wa=wa*200
p=getvar(ncfile,'pressure',timeidx=time)
lat=getvar(ncfile,'lat')
lon=getvar(ncfile,'lon')
height=getvar(ncfile,'height')
hgt=getvar(ncfile,'HGT')
height2earth=height-hgt
start_lat,start_lon=31.2,121.0
end_lat,end_lon=31.2,122.0
startpoint=CoordPair(lat=start_lat,lon=start_lon)
endpoint=CoordPair(lat=end_lat,lon=end_lon)
ua_vert=vertcross(ua,p,wrfin=ncfile,start_point=startpoint,end_point=endpoint,latlon=True)
va_vert=vertcross(va,p,wrfin=ncfile,start_point=startpoint,end_point=endpoint,latlon=True)
wa_vert=vertcross(wa,p,wrfin=ncfile,start_point=startpoint,end_point=endpoint,latlon=True)
print(wa_vert)


lonlist,latlist=[],[]
plist=ua_vert.coords['vertical']
print(plist)
for i in range(len(ua_vert.coords['xy_loc'])):
    s = str(ua_vert.coords['xy_loc'][i].values)
    lonlist.append(float(s[s.find('lon=')+4:s.find('lon=')+12]))
    latlist.append(float(s[s.find('lat=')+4:s.find('lat=')+12]))
print(lonlist)
print(latlist)
hlist=[]
for i in range(1000,700,-30):
    hlist.append(float(np.max(interplevel(height2earth,p,i)).values))
hlist=np.array([int(i) for i in hlist])
print(hlist)
plist=to_np(plist)

fig=plt.figure(figsize=(12,8),dpi=150)
axe_1=plt.subplot(1,1,1) #这里可以设置多个子图，第一个参数表示多少行，第二个表示多少列，第三个表示第几个子图
axe_1.set_title(str(get_ncfile_time(ncfile,timezone=8)[time]),fontsize=12)
start_x, end_x=start_lon,end_lon
small_p, big_p=700,1000
big_interval_x,small_interval_x,big_interval_p,small_interval_p=0.1,0.1,30,30
#axe_1.set_xlim(start_x, end_x)
axe_1.set_ylim(650,1000)  # 设置图的范围

axe_1.grid(color='gray', linestyle=':', linewidth=0.7)
axe_1.invert_yaxis()#翻转纵坐标
plt.xticks(fontsize=8, color='black')  # 这一行代码用于修改刻度的字体
plt.yticks(fontsize=8, color='black')  # 这一行代码用于修改刻度的字体
#t_level=np.arange(0,29,0.1)
#contourf = axe_1.contourf(lonlist, plist, tc_vert,levels=t_level,cmap=cmaps.amwg_blueyellowred)

interval=1
interval_y=1
ua_vert,va_vert,wa_vert=to_np(ua_vert),to_np(va_vert),to_np(wa_vert)
ws_vert=np.sqrt(ua_vert**2+va_vert**2)
wdir_vert = np.arctan2(va_vert,ua_vert)*180/np.pi
line_angel=np.arctan2(end_lat-start_lat,end_lon-start_lon)*180/np.pi
vl_angel=wdir_vert-line_angel
vl_angel=np.cos(vl_angel/180*np.pi)
print(line_angel)
ws_vert=ws_vert*vl_angel
print(ws_vert)
xi=np.mgrid[start_lon:end_lon:complex(str(len(lonlist)) + 'j')]
print(xi-lonlist)
yi=to_np(plist)
yi=yi[::-1]

x=[]
y1=[]
y = plist.tolist()
for i in range(len(yi)):
    x.append(xi)
for i in range(len(xi)):
    y1.append(yi)
y=np.array(y1)
y=y.T
x=np.array(x)
xp,yp=[],[]
for j in range(31):
    for i in range(50):
        xp.append(j)
for j in range(31):
    for i in range(50):
        yp.append(i+55)
start_point=np.array([xp,yp])
axe_1.streamplot(xi, yi, ws_vert[::-1], wa_vert[::-1], density=2,color='green', linewidth=0.5, arrowsize=1, arrowstyle='-|>',integration_direction='both')
#quiver = axe_1.quiver(x, y, ws_vert, wa_vert, pivot='mid', width=0.001, scale=130, color='black', headwidth=4,alpha=1)

axe2=axe_1.twinx()
axe2.set_yticklabels(hlist)

fig.show()
plt.show()
