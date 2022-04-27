# edited on 2022-03-29 22:54:30
# 本文件专门用于绘制geogrid，检测是否正确

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeat
import matplotlib.ticker as mticker
import numpy as np
import matplotlib.colors as c
from matplotlib.font_manager import FontProperties
from wrf import getvar
import netCDF4 as nc
import cmaps

def draw_geogrid(file,var,level=None,cmap=cmaps.ncl_default):
    fig = plt.figure(figsize=(5, 5))
    axe = plt.subplot(1, 1, 1, projection=ccrs.PlateCarree())
    #axe.add_feature(cfeat.COASTLINE.with_scale("10m"), linewidth=1, color="k",zorder=1)
    #axe.set_extent([120.5, 122, 30.5, 32], crs=ccrs.PlateCarree())
    axe.set_extent([121, 122, 30.7, 31.6], crs=ccrs.PlateCarree())
    gl = axe.gridlines(crs=ccrs.PlateCarree(), draw_labels=True, linewidth=1, color="gray",linestyle=":")
    gl.top_labels, gl.bottom_labels, gl.right_labels, gl.left_labels = True, True, True, True
    gl.xlocator = mticker.FixedLocator(np.arange(121, 122.1, 0.2))
    gl.ylocator = mticker.FixedLocator(np.arange(30.7, 31.7, 0.2))
    X,Y=getvar(nc.Dataset(file),"XLONG_M").values,getvar(nc.Dataset(file),"XLAT_M")
    F=getvar(nc.Dataset(file),var).values
    print("最大值为：{}，最小值为{}".format(np.max(F),np.min(F)))
    classification = np.unique(F)   # 获得本张图内涉及的土地利用分类
    classification=classification.astype(int)
    #classification.insert(0,0)
    print(classification)
    #contourf = axe.contourf(X, Y, F, levels=classification, cmap=cmaps.ncl_default ,zorder=0,extend="both")
    for i in range(len(classification)):
        F[np.where(F==classification[i])]=i
    axe.pcolormesh(X,Y,F, cmap=cmap,shading="auto",rasterized=True,zorder=0)
    axe.plot(121.3667,31.1,"o",color="k",markersize=4,zorder=1,label="闵行")
    axe.plot(121.45,31.4,"X",color="k",markersize=4,zorder=1,label="宝山")
    axe.plot(121.25,31.3667,"*",color="k",markersize=4,zorder=1,label="嘉定")
    axe.plot(121.7833,31.05,"D",color="k",markersize=4,zorder=1,label="南汇")
    axe.plot(121.5,30.8833,"+",color="k",markersize=4,zorder=1,label="奉献")
    axe.plot(121.4333,31.2,"d",color="k",markersize=4,zorder=1,label="徐家汇")
    axe.plot(121.5333,31.2333,"^",color="k",markersize=4,zorder=1,label="浦东")
    axe.plot(121.35,30.7333,"v",color="k",markersize=4,zorder=1,label="金山")
    #fig.colorbar(contourf, drawedges=True, ticks=level,spacing='uniform')  # orientation='vertical'
    #fig.colorbar(pcolor, drawedges=True, ticks=level,spacing='uniform')  # orientation='vertical'
    # pcolor的图例画法
    cmap_list = cmap(np.linspace(0, 1, len(classification)))
    proxy = [plt.Rectangle((0, 0), 1, 1, fc=i) for i in cmap_list]
    l1=plt.legend(proxy, [level[i] for i in classification], loc="upper right", bbox_to_anchor=(1.3,1.1),labelspacing=1,
               prop=FontProperties(fname="./font/SimSun.ttf", size=12))
    l2=plt.legend(loc="lower right",prop=FontProperties(fname="./font/SimSun.ttf", size=12),bbox_to_anchor=(1.212,0.00))
    axe.add_artist(l1)
    ######################
    fig.show()
    plt.show()

if __name__ == '__main__':
    #draw_geogrid(r"/home/fishercat/Build_WRF/Simulations/ucm_modified1/geo_em.d03.nc","HGT_M")
    draw_geogrid(r"D:\Data\WRF-Chem_Files\WRF-Chem_Simulation\lcz_4\geo_em.d03.nc","LU_INDEX",
                 {1:"针叶林",2:"阔叶林",5:"混叶林",6:"封闭灌木丛",7:"开放灌木丛",10:"草地",11:"湿地",12:"耕地", 13:"城市", 14:"耕地植被"
                     ,15:"冰雪",16:"植被稀少的土地",17:"水",19:"荒原",
                  31:"紧凑高层",32:"紧凑中层",33:"紧凑低层",34:"开放高层",35:"开放中层",36:"开放低层",
                  37:"轻量低层",38:"厂区",39:"分散建筑",40:"重工业",41:"人工地表"},
                 cmap=cmaps.circular_2)

