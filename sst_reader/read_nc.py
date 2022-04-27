import netCDF4 as nc
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeat
import matplotlib.ticker as mticker
import cmaps,os
import numpy as np
from datetime import datetime,timedelta

from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from matplotlib.font_manager import FontProperties

###############################################################################
# sst文件
path=r"ERA5-SST.nc"
# 图片输出的路径
exportpath=r""
min,max,interval,tick_interval=20,40,0.5,1  # 温度最小值，温度最大值，温度的间隔，温度标签间隔
# 箭头的线宽，大小（数字越大越小），颜色，箭头宽度
quiver_width,quiver_scale,quiver_color,quiver_headwidth=0.0025,100,'black',4
# 箭头间隔
quiver_interval=1
quiverkey_x,quiverkey_y=0.87,1.03       #quiverkey的相对位置，x和y
quiverkey_ws,quiverkey_text,quiverkey_size=4,'4m/s',7   #quiverkey的标注风速，标注字体和字体大小
# 时间间隔
timestep=1
var="t2m"
start_lat,end_lat=30.65,31.88
start_lon,end_lon=120.45,122.2
lonlat_interval=0.4
###############################################################################

ncfile=nc.Dataset(path)
keylist=ncfile.variables.keys()
print(keylist)

start_date=datetime(1900,1,1,00,00)
for i in range(0,len(ncfile["time"][:]),timestep):
    plt.close('all')
    hour=int(ncfile["time"][i])
    if var=="sst" or var=="t2m":
        f = np.array(ncfile[var][i, :, :])
        f[np.where(f == -32767)] = 0
        f = f - 273.15
    else:
        f = np.array(ncfile[var][i, :, :])
    print(np.min(f),np.max(f))
    now_date = start_date + timedelta(hours=hour+8)
    print(str(now_date))
    fig = plt.figure(figsize=(5, 5))
    axe = plt.subplot(1, 1, 1, projection=ccrs.PlateCarree())
    axe.set_extent([start_lon, end_lon, start_lat, end_lat], crs=ccrs.PlateCarree())
    axe.set_title(str(now_date) + " "+var, y=1.1, fontsize=12,fontproperties=FontProperties(fname="../font/Times.ttf"))
    gl = axe.gridlines(crs=ccrs.PlateCarree(), draw_labels=True, linewidth=1, color="gray", linestyle=":")
    gl.top_labels, gl.bottom_labels, gl.right_labels, gl.left_labels = False, False, False, False
    gl.xlocator = mticker.FixedLocator(np.arange(start_lon, end_lon, lonlat_interval))
    gl.ylocator = mticker.FixedLocator(np.arange(start_lat, end_lat, lonlat_interval))
    axe.set_xticks(np.arange(start_lon, end_lon, lonlat_interval), crs=ccrs.PlateCarree())
    axe.set_yticks(np.arange(start_lat, end_lat, lonlat_interval), crs=ccrs.PlateCarree())
    axe.xaxis.set_major_formatter(LongitudeFormatter())
    axe.yaxis.set_major_formatter(LatitudeFormatter())
    labels = axe.get_xticklabels() + axe.get_yticklabels()
    [label.set_fontproperties(FontProperties(fname="../font/Times.ttf", size=8)) for label in labels]
    axe.add_feature(cfeat.COASTLINE.with_scale("10m"), linewidth=1, color="k",zorder=1)
    contourf = axe.contourf(ncfile["longitude"][:], ncfile["latitude"][:] , f, levels=np.arange(min,max,interval),  cmap=cmaps.ncl_default , extend="neither", zorder=0)
    ws1,ws2=ncfile["u10"][i, :, :][::quiver_interval], ncfile["v10"][i, :, :][::quiver_interval]
    lat,lon=ncfile["longitude"][:][::quiver_interval], ncfile["latitude"][:][::quiver_interval]
    quiver = axe.quiver(lat,lon, ws1, ws2, pivot='mid',
                             width=quiver_width, scale=quiver_scale, color=quiver_color,
                             headwidth=quiver_headwidth,
                             transform=ccrs.PlateCarree())
    # 绘制矢量箭头的图例
    axe.quiverkey(quiver, quiverkey_x, quiverkey_y, quiverkey_ws,quiverkey_text,
                           labelpos='E', coordinates='axes',
                           fontproperties={'size': quiverkey_size, 'family': 'Times New Roman'})
    fig.subplots_adjust(right=0.85)
    rect = [0.9, 0.1, 0.02, 0.8]  # 分别代表，水平位置，垂直位置，水平宽度，垂直宽度
    cbar_ax = fig.add_axes(rect)
    cb=fig.colorbar(contourf, drawedges=True,cax=cbar_ax,orientation="vertical",ticks=np.arange(min,max+1,tick_interval),spacing='uniform')  # orientation='vertical'
    cb.ax.tick_params(length=0.2)
    labels = cb.ax.get_xticklabels() + cb.ax.get_yticklabels()
    [label.set_fontproperties(FontProperties(fname="../font/Times.ttf", size=7)) for label in labels]
    fig.savefig(os.path.join(exportpath,var+"_"+str(now_date)[0:13].replace(" ","_")+".png"),dpi=500, bbox_inches="tight")