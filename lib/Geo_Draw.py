# edited on 2022-04-02 21:36:42
# 此文件用于进行平面图绘制，属于库文件

import cartopy.crs as ccrs
import cartopy.feature as cfeat
import cmaps
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from matplotlib.colors import Normalize
from matplotlib.font_manager import FontProperties

import lib.Fontprocess as Fontprocess

Simsun = FontProperties(fname="../font/SimSun.ttf")
Times = FontProperties(fname="../font/Times.ttf")
mpl.rcParams['axes.unicode_minus'] = False
config = {
    "font.family":'serif',
    "mathtext.fontset": 'stix',
    "font.serif": ['SimSun'],
}
mpl.rcParams.update(config)


def subplot_remain(place, extra, fig):
    '''
    图片中留出空位
    :param place: 留空位置
    :param extra: 留空量
    :param fig: 需要操作的图片
    :return:
    '''
    if place == 'bottom':
        fig.subplots_adjust(bottom=extra)
    elif place == 'top':
        fig.subplots_adjust(top=extra)
    elif place == 'left':
        fig.subplots_adjust(left=extra)
    elif place == 'right':
        fig.subplots_adjust(right=extra)


def whether_drawedge(drawedges_bool):
    '''
    判断是否需要绘制标尺线
    :param drawedges_bool: 0表示不绘制，1表示绘制
    :return: bool值
    '''
    if drawedges_bool == 0:
        return False
    else:
        return True


class Figure4wrf():
    def __init__(self, width, height, dpi):
        plt.close('all')
        self.fig = plt.figure(figsize=(width, height), dpi=dpi)

    def init_draw(self, ver_num, hor_num, cur_num, title, title_size, title_y, geo_opt=0):
        if geo_opt == 0:
            self.axe = plt.subplot(ver_num, hor_num, cur_num, projection=ccrs.PlateCarree())
        if geo_opt == 1:
            self.axe = plt.subplot(ver_num, hor_num, cur_num)
        #self.axe.set_title(Fontprocess.zhSimsun_enTNR(title), fontproperties=Simsun, fontsize=title_size, y=title_y)
        self.axe.set_title(Fontprocess.zhSimsun_enTNR(title), fontsize=title_size, y=title_y)
        print("图片初始化完成")

    def geo_draw(self, lake_opt, lake_lw, lake_lc, coastline_lw, coastline_lc, precision):
        # 添加海岸线数据
        self.axe.add_feature(cfeat.COASTLINE.with_scale(precision), linewidth=coastline_lw,
                             color=coastline_lc, zorder=1)
        # 通过下面两行代码可以添加湖泊轮廓线，其他的以此类推
        if lake_opt == 0:
            LAKES_border = cfeat.NaturalEarthFeature('physical', 'lakes', precision, edgecolor=lake_lc,
                                                     facecolor='never')
            self.axe.add_feature(LAKES_border, linewidth=lake_lw, zorder=1)
            print("绘制湖泊")
        if lake_opt == 1:
            print("不绘制湖泊")

    def extent_draw(self, west_lon, east_lon, south_lat, north_lat, extra):
        self.axe.set_extent([west_lon - extra, east_lon + extra, south_lat - extra, north_lat + extra],
                            crs=ccrs.PlateCarree())
        print("绘制地理图")

    def gridline_draw(self, west_lon, east_lon, south_lat, north_lat, major_interval_lon, major_interval_lat,
                      minor_interval_lon, minor_interval_lat, labelsize, labelcolor,
                      grid_lw=1, grid_color="gray", grid_type=":", ticklength=1, xlabel=None, xlabelsize=None):
        '''
        废弃方法
        # 可以控制坐标轴出现的位置，设置False表示隐藏,0表示显示
        if top_labels==0: gl.top_labels = True
        if top_labels==1: gl.top_labels = False
        if bottom_labels==0: gl.bottom_labels = True
        if bottom_labels==1: gl.bottom_labels = False
        if right_labels==0: gl.right_labels = True
        if right_labels==1: gl.right_labels = False
        if left_labels==0: gl.left_labels = True
        if left_labels==1: gl.left_labels = False
        # 自定义给出x轴Locator的位置
        gl.xlocator = mticker.FixedLocator(np.arange(l_x, r_x+big_interval_x, big_interval_x))
        gl.ylocator = mticker.FixedLocator(np.arange(b_y, t_y+big_interval_y, big_interval_y))
        gl.xformatter = LONGITUDE_FORMATTER
        gl.yformatter = LATITUDE_FORMATTER
        gl.xlabel_style = {"color": label_color, "font": Times}
        gl.ylabel_style = {'size': label_size, 'color': label_color, "font": Times}
        '''
        # 绘制网格
        gl = self.axe.gridlines(crs=ccrs.PlateCarree(), draw_labels=True, linewidth=grid_lw, color=grid_color,
                                linestyle=grid_type)
        gl.top_labels, gl.bottom_labels, gl.right_labels, gl.left_labels = False, False, False, False  # 坐标轴的刻度用matplotlib显示
        gl.xlocator = mticker.FixedLocator(np.arange(west_lon, east_lon + major_interval_lon, major_interval_lon))
        gl.ylocator = mticker.FixedLocator(np.arange(south_lat, north_lat + major_interval_lat, major_interval_lat))
        self.axe.set_xticks(np.arange(west_lon, east_lon + major_interval_lon / 2, major_interval_lon),
                            crs=ccrs.PlateCarree())
        self.axe.set_yticks(np.arange(south_lat, north_lat + major_interval_lat / 2, major_interval_lat),
                            crs=ccrs.PlateCarree())
        self.axe.xaxis.set_major_formatter(LongitudeFormatter())
        self.axe.yaxis.set_major_formatter(LatitudeFormatter())
        # 设置minor刻度
        self.axe.set_xticks(np.arange(west_lon, east_lon, minor_interval_lon), crs=ccrs.PlateCarree(), minor=True)
        self.axe.set_yticks(np.arange(south_lat, north_lat, minor_interval_lat), crs=ccrs.PlateCarree(), minor=True)
        self.axe.tick_params(labelcolor=labelcolor, length=ticklength)
        # 设置自定义的x坐标
        if xlabel != None:
            plt.xlabel(xlabel, fontproperties=FontProperties(fname="../font/Times.ttf", size=xlabelsize))
        # label字体设置
        labels = self.axe.get_xticklabels() + self.axe.get_yticklabels()
        [label.set_fontproperties(FontProperties(fname="../font/Times.ttf", size=labelsize)) for label in labels]
        print("绘制地理网格")

    def contourf_draw(self, lon, lat, var, cmap, level=None, extend="neither"):
        if level.any() != None:
            self.contourf = self.axe.contourf(lon, lat, var, levels=level, cmap=cmap, extend=extend, zorder=0)
        else:
            self.contourf = self.axe.contourf(lon, lat, var, cmap=cmap, extend=extend, zorder=0)
        print("最大和最小的值分别是：")
        print(np.max(var).values, np.min(var).values)
        print("绘制填充")

    def contour_draw(self, lon, lat, var, contour_color, labelsize, labelcolor,
                     inline=True, contour_lw=1, contour_style="solid", level=None, fontprecision='%1.0f',
                     alpha=1, contour_opt=0, cmaps=cmaps.amwg_blueyellowred):
        # 非标准化选项
        if contour_opt == 0:
            if level != None:
                contour = self.axe.contour(lon, lat, var, levels=level, colors=contour_color, linewidths=contour_lw,
                                           linestyles=contour_style, alpha=alpha)
            else:
                contour = self.axe.contour(lon, lat, var, colors=contour_color, linewidths=contour_lw,
                                           linestyles=contour_style, alpha=alpha)
        # 标准化选项
        else:
            if level != None:
                contour = self.axe.contour(lon, lat, var, levels=level, cmap=cmaps, linewidths=contour_lw,
                                           linestyles=contour_style, alpha=alpha)
            else:
                contour = self.axe.contour(lon, lat, var, cmap=cmaps, linewidths=contour_lw,
                                           linestyles=contour_style, alpha=alpha)
            norm = mpl.colors.Normalize(vmin=contour.cvalues.min(), vmax=contour.cvalues.max())
            self.contour = plt.cm.ScalarMappable(norm=norm, cmap=contour.cmap)
            self.contour_levels = contour.levels
        if inline == True:
            self.axe.clabel(contour, inline=True, fontsize=labelsize, colors=labelcolor, fmt=fontprecision)
        if inline == False:
            self.axe.clabel(contour, inline=False, fontsize=labelsize, colors=labelcolor, fmt=fontprecision)
        print("等高线绘制完毕")

    def quiver_draw(self, lon, lat, ws1, ws2, interval, quiver_width, quiver_scale, quiver_color, quiver_headwidth,
                    alpha,
                    quiverkey_opt, quiverkey_x, quiverkey_y, quiverkey_ws, quiverkey_text, quiverkey_size,
                    color_quiver=0, color_maps=None, ws_map=None):
        lon, lat, ws1, ws2 = lon[::interval, ::interval], lat[::interval, ::interval], ws1[::interval, ::interval], ws2[
                                                                                                                    ::interval,
                                                                                                                    ::interval]
        # 传统的矢量图，箭头以单色显示
        if color_quiver == 0:
            quiver = self.axe.quiver(lon, lat, ws1, ws2, pivot='mid',
                                     width=quiver_width, scale=quiver_scale, color=quiver_color,
                                     headwidth=quiver_headwidth, alpha=alpha,
                                     transform=ccrs.PlateCarree())
            if quiverkey_opt == 0:
                # 绘制矢量箭头的图例
                self.axe.quiverkey(quiver, quiverkey_x, quiverkey_y, quiverkey_ws,
                                   Fontprocess.zhSimsun_enTNR(quiverkey_text),
                                   labelpos='E', coordinates='axes',
                                   fontproperties={'size': quiverkey_size, 'family': 'Times New Roman'})
        # 将矢量箭头标准化，箭头彩色显示风速
        elif color_quiver == 1:
            color_map = np.zeros_like(ws1, dtype=float)
            windspeed = np.sqrt(ws1 ** 2 + ws2 ** 2)
            ws1 = ws1 / windspeed
            ws2 = ws2 / windspeed
            for i in range(len(ws_map)):
                color_map[np.where((windspeed > ws_map[i][0]) & (windspeed <= ws_map[i][1]))] = i
            norm = Normalize()
            norm.autoscale(color_map)
            self.quiver = self.axe.quiver(lon, lat, ws1, ws2, norm(color_map), cmap=color_maps, pivot='mid',
                                          width=quiver_width, scale=quiver_scale,
                                          headwidth=quiver_headwidth, alpha=alpha,
                                          transform=ccrs.PlateCarree())

    def streamplot_draw(self, xi, yi, height, uv, w, density, color, lw, arrowsize, arrowstyle):
        self.axe.streamplot(xi, yi, uv, w, density=density,
                            color=color, linewidth=lw, arrowsize=arrowsize, arrowstyle=arrowstyle)

    def colorbar_draw(self, rect1, rect2, rect3, rect4, label_opt, hv_opt, labeltext, labelsize, ticksize, rectplace,
                      rectextra
                      , ticks=None, drawedges_bool=0, colorbar_ticklength=2):

        drawedges_bool = whether_drawedge(drawedges_bool)
        # 使用自定义位置
        if label_opt == 0:
            subplot_remain(rectplace, rectextra, self.fig)
            rect = [rect1, rect2, rect3, rect4]  # 分别代表，水平位置，垂直位置，水平宽度，垂直宽度
            cbar_ax = self.fig.add_axes(rect)
            cb = self.fig.colorbar(self.contourf, drawedges=drawedges_bool, cax=cbar_ax, orientation=hv_opt,
                                   spacing='uniform')  # orientation='vertical'

        # 使用默认位置
        else:
            subplot_remain(rectplace, rectextra, self.fig)
            cb = self.fig.colorbar(self.contourf, drawedges=drawedges_bool, orientation=hv_opt,
                                   spacing='uniform')  # orientation='vertical'

        #cb.set_label(Fontprocess.zhSimsun_enTNR(labeltext), fontproperties=Simsun, fontsize=labelsize)
        cb.set_label(Fontprocess.zhSimsun_enTNR(labeltext), fontsize=labelsize)
        cb.ax.tick_params(length=colorbar_ticklength)
        # 下面两行是指定colorbar刻度字体的方法，绘图的坐标也同样适用
        labels = cb.ax.get_xticklabels() + cb.ax.get_yticklabels()
        [label.set_fontproperties(FontProperties(fname="../font/Times.ttf", size=ticksize)) for label in labels]
        if ticks.any() != None:  # 如果ticks不为None，那么就会报错，然后就可以进入下面的设置ticks
            print("colorbar_ticks不为空")
            cb.set_ticks(ticks)

    def colorbar_draw_quiver(self, rect1, rect2, rect3, rect4, label_opt, hv_opt, labeltext, labelsize, ticksize,
                             rectplace, rectextra
                             , ticks=None, drawedges_bool=0, colorbar_ticklength=2):
        drawedges_bool = whether_drawedge(drawedges_bool)
        bound = []
        for i in ticks:
            bound.append(i[0])
        ticks = np.array(bound) / bound[-1]
        # 使用自定义位置
        if label_opt == 0:
            subplot_remain(rectplace, rectextra, self.fig)
            rect = [rect1, rect2, rect3, rect4]  # 分别代表，水平位置，垂直位置，水平宽度，垂直宽度
            cbar_ax = self.fig.add_axes(rect)
            cb = self.fig.colorbar(self.quiver, ticks=ticks, cax=cbar_ax, drawedges=drawedges_bool, orientation=hv_opt,
                                   spacing='uniform')  # orientation='vertical'
        # 使用默认位置
        else:
            cb = self.fig.colorbar(self.quiver, ticks=ticks, drawedges=drawedges_bool, orientation=hv_opt,
                                   spacing='uniform')  # orientation='vertical'
        if hv_opt == 'vertical':
            cb.ax.set_yticklabels(bound)
        if hv_opt == 'horizontal':
            cb.ax.set_xticklabels(bound)
        #cb.set_label(Fontprocess.zhSimsun_enTNR(labeltext), fontproperties=Simsun, fontsize=labelsize)
        cb.set_label(Fontprocess.zhSimsun_enTNR(labeltext), fontsize=labelsize)
        cb.ax.tick_params(length=colorbar_ticklength)
        # 下面两行是指定colorbar刻度字体的方法，绘图的坐标也同样适用
        labels = cb.ax.get_xticklabels() + cb.ax.get_yticklabels()
        [label.set_fontproperties(FontProperties(fname="../font/Times.ttf", size=ticksize)) for label in labels]

    def colorbar_draw_contour(self, rect1, rect2, rect3, rect4, label_opt, hv_opt, labeltext, labelsize, ticksize,
                              rectplace, rectextra
                              , drawedges_bool=0, colorbar_ticklength=2):
        drawedges_bool = whether_drawedge(drawedges_bool)
        if label_opt == 0:
            subplot_remain(rectplace, rectextra, self.fig)
            rect = [rect1, rect2, rect3, rect4]  # 分别代表，水平位置，垂直位置，水平宽度，垂直宽度
            cbar_ax = self.fig.add_axes(rect)
            cb = self.fig.colorbar(self.contour, ticks=self.contour_levels, cax=cbar_ax, drawedges=drawedges_bool,
                                   orientation=hv_opt, spacing='uniform')  # orientation='vertical'
        else:
            cb = self.fig.colorbar(self.contour, drawedges=drawedges_bool, orientation=hv_opt,
                                   spacing='uniform')  # orientation='vertical'
        #cb.set_label(Fontprocess.zhSimsun_enTNR(labeltext), fontproperties=Simsun, fontsize=labelsize)
        cb.set_label(Fontprocess.zhSimsun_enTNR(labeltext), fontsize=labelsize)
        cb.ax.tick_params(length=colorbar_ticklength)
        # 下面两行是指定colorbar刻度字体的方法，绘图的坐标也同样适用
        labels = cb.ax.get_xticklabels() + cb.ax.get_yticklabels()
        [label.set_fontproperties(FontProperties(fname="../font/Times.ttf", size=ticksize)) for label in labels]

    def adjust_subplot(self, wspace, hspace):
        plt.subplots_adjust(wspace=wspace, hspace=hspace)

    def save_fig(self, path, save_dpi, bbox_inches):
        self.fig.savefig(path, dpi=save_dpi, bbox_inches=bbox_inches)

    def fig_show(self):
        self.fig.show()
        plt.show()
