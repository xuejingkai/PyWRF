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
    axe.set_extent([120.5, 122, 30.5, 32], crs=ccrs.PlateCarree())
    gl = axe.gridlines(crs=ccrs.PlateCarree(), draw_labels=True, linewidth=1, color="gray",linestyle=":")
    gl.top_labels, gl.bottom_labels, gl.right_labels, gl.left_labels = True, True, True, True
    gl.xlocator = mticker.FixedLocator(np.arange(120.5, 123 , 0.3))
    gl.ylocator = mticker.FixedLocator(np.arange(30.5, 33 , 0.3))
    X,Y=getvar(nc.Dataset(file),"XLONG_M").values,getvar(nc.Dataset(file),"XLAT_M")
    F=getvar(nc.Dataset(file),var).values
    print("最大值为：{}，最小值为{}".format(np.max(F),np.min(F)))
    contourf = axe.contourf(X, Y, F, levels=level, cmap=cmaps.grads_default , extend="neither", zorder=0)
    fig.colorbar(contourf, drawedges=True, ticks=level,spacing='uniform')  # orientation='vertical'
    fig.show()
    plt.show()

if __name__ == '__main__':
    #draw_geogrid(r"/home/fishercat/Build_WRF/Simulations/ucm_modified1/geo_em.d03.nc","HGT_M")
    draw_geogrid(r"D:\Data\WRF-Chem_Files\WRF-Chem_Simulation\noucm_defaultParam\geo_em.d03.nc","LU_INDEX",range(1,22,1))

