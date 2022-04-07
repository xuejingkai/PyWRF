# edited on 2022-03-29 22:54:30
# 本文件专门用于绘制geogrid，检测是否正确

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeat
import matplotlib.ticker as mticker
import numpy as np
from wrf import getvar
import netCDF4 as nc
import cmaps

def draw_geogrid(file,var,level=None):
    fig = plt.figure(figsize=(5, 5))
    axe = plt.subplot(1, 1, 1, projection=ccrs.PlateCarree())
    axe.add_feature(cfeat.COASTLINE.with_scale("10m"), linewidth=1, color="k",zorder=1)
    #axe.set_extent([120.5, 122, 30.5, 32], crs=ccrs.PlateCarree())
    axe.set_extent([120.8, 122, 30.8, 31.8], crs=ccrs.PlateCarree())
    gl = axe.gridlines(crs=ccrs.PlateCarree(), draw_labels=True, linewidth=1, color="gray",linestyle=":")
    gl.top_labels, gl.bottom_labels, gl.right_labels, gl.left_labels = True, True, True, True
    gl.xlocator = mticker.FixedLocator(np.arange(120.8, 122.1, 0.2))
    gl.ylocator = mticker.FixedLocator(np.arange(30.8, 31.9, 0.2))
    X,Y=getvar(nc.Dataset(file),"XLONG_M").values,getvar(nc.Dataset(file),"XLAT_M")
    F=getvar(nc.Dataset(file),var).values
    print("最大值为：{}，最小值为{}".format(np.max(F),np.min(F)))
    contourf = axe.contourf(X, Y, F, levels=level, cmap=cmaps.t2m_29lev , extend="neither", zorder=0.1)
    axe.plot(121.37,31.1,"o",color="white",markersize=4.5,zorder=1)
    axe.plot(121.45454,31.39692,"s",color="white",markersize=4.5,zorder=1)
    axe.plot(121.25,31.37,"*",color="white",markersize=4.5,zorder=1)
    axe.plot(121.7833,31.05,"v",color="white",markersize=4.5,zorder=1)
    #fig.colorbar(contourf, drawedges=True, ticks=level,spacing='uniform')  # orientation='vertical'
    # 图例画法
    classification=np.unique(F)
    proxy = [plt.Rectangle((0, 0), 1, 1, fc=pc.get_facecolor()[0])
             for pc in contourf.collections]
    plt.legend(proxy, classification)
    fig.show()
    plt.show()

if __name__ == '__main__':
    #draw_geogrid(r"/home/fishercat/Build_WRF/Simulations/ucm_modified1/geo_em.d03.nc","HGT_M")
    draw_geogrid(r"D:\Data\WRF-Chem_Files\WRF-Chem_Simulation\ucm_modifiedParam_1\geo_em.d03.nc","LU_INDEX",
                 [1,2,5,6,7,10,11,12,14,15,16,17,19,31,32,33])

