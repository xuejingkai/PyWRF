# edited on 2022-04-02 19:43:01
# 执行绘制平面图命令，配置参数使用namelist_plaindraw.py

import os

import netCDF4 as nc
from wrf import getvar, to_np

from lib.Geo_Draw import Figure4wrf
from lib.Readtime import get_ncfile_time
from namelist_plaindraw_example import *


def create_title(title_base, title_end_type, num, ncfile, time_zone):
    '''
    用于合成子图标题
    :param title_base: 子图的基础标题
    :param title_end_type: 子图末尾添加的类型
    :param num: 当前子图数字
    :param ncfile: netCDF文件
    :param time_zone: 时区
    :return: 合成后的title
    '''
    if title_end_type == None:
        title = title_base
    elif title_end_type == "time":
        time = str(get_ncfile_time(ncfile, timezone=time_zone)[num])
        title = title_base + time
        print("当前图片时间：{}，时区为：UTC{}".format(time, time_zone))
    elif title_end_type == "num":
        title = title_base + str(num)
        print("当前图片编号为：{}".format(num))
    else:
        raise Exception("title_end设置错误，请重新设置")
    return title

def get_data_from_3Ddata(data, height):
    '''
    如果数据存在高度，则提取对应高度的数据
    :param data: 子图的基础标题
    :param height: 子图末尾添加的类型
    :return: 提取对应高度后的数据
    '''
    # 如果是三维数据则提取对应高度
    if data.ndim == 3:
        data = data[height, :, :]
        print('数据为三维')
    else:
        print("数据为二维")
    return data

def create_savepath(fig_path, fig_name_base, fig_name_end_type, num, ncfile, time_zone):
    '''
    用于合成图片保存路径
    :param fig_path: 图片保存文件夹
    :param fig_name_base: 图片保存基础名字
    :param fig_name_end_type: 图片末尾添加的类型
    :param num: 当前子图数字
    :param ncfile: netCDF文件
    :param time_zone: 时区
    :return: 合成后的title
    '''
    if fig_name_end_type == None:
        filename = fig_name_base
    elif fig_name_end_type == "time":
        filename = fig_name_base + str(get_ncfile_time(ncfile, timezone=time_zone)[num])
    elif fig_name_end_type == "num":
        filename = fig_name_base + str(num)
    else:
        raise Exception("title_end设置错误，请重新设置")
    return os.path.join(fig_path, filename.replace(":", "-") + ".png")


# 计算一个图片中消耗多少个时间
if multi_file_draw == True:
    num_in_fig = 1
else:
    num_in_fig = ver_num * hor_num

# 开始循环绘制
for fig_num in range(int(len(timelist) / num_in_fig)):
    fig = Figure4wrf(fig_width, fig_height, fig_dpi)
    for cur_num in range(ver_num * hor_num):
        # 是否需要开启对比绘图模式
        if multi_file_draw == True:
            num = timelist[fig_num]
            ncfile = nc.Dataset(path[cur_num])
        else:
            num = timelist[cur_num + fig_num * ver_num * hor_num]
            ncfile = nc.Dataset(path[0])
        # 设置标题
        axe_title = create_title(title[cur_num], title_end, num, ncfile, time_zone)
        # 开始进行绘制
        # 初始化图片
        fig.init_draw(ver_num, hor_num, cur_num + 1, axe_title, title_size, title_y)
        # 地理信息绘制
        fig.geo_draw(lake_opt, lake_lw, lake_lc, coastline_lw, coastline_lc, precision)
        # 图形范围绘制
        fig.extent_draw(west_lon, east_lon, south_lat, north_lat, extra)
        # 网格绘制
        # 设置x轴label（如果存在）
        if xlabellist != None:
            xlabel = xlabellist[cur_num]
            fig.gridline_draw(west_lon, east_lon, south_lat, north_lat, major_interval_lon, major_interval_lat,
                              minor_interval_lon, minor_interval_lat, labelsize, labelcolor, grid_lw=grid_lw,
                              grid_color=grid_lc, grid_type=grid_type, ticklength=ticklength, xlabel=xlabel,
                              xlabelsize=xlabelsize)
        else:
            fig.gridline_draw(west_lon, east_lon, south_lat, north_lat, major_interval_lon, major_interval_lat,
                              minor_interval_lon, minor_interval_lat, labelsize, labelcolor, grid_lw=grid_lw,
                              grid_color=grid_lc, grid_type=grid_type, ticklength=ticklength)
        # 数据绘制
        lon = to_np(getvar(ncfile, 'lon'))
        lat = to_np(getvar(ncfile, 'lat'))
        if contourf_opt == 1:
            contourf_var = getvar(ncfile, var_contourf, timeidx=num)  # 如果是华氏度之类的物理量需要换算，可以自行进行修改factor的值
            if var_contourf == "T2":
                contourf_var = contourf_var - 273.15
            contourf_var = get_data_from_3Ddata(contourf_var, height_contourf)
            # 化学变量的计算
            if chem_w > 0:
                contourf_var = contourf_var * 1000 / 22.4 * chem_w * 273.15 / (getvar(ncfile, 'tk', timeidx=num)) * (
                    getvar(ncfile, 'pressure', timeidx=num)) / 1013.25
            fig.contourf_draw(lon, lat, contourf_var, cmap, level=contourf_level, extend=colorbar_extend)
        if contour_opt == 1:
            contour_var = getvar(ncfile, var_contourf, timeidx=num)
            contour_var = get_data_from_3Ddata(contour_var, height_contour)
            fig.contour_draw(lon, lat, contour_var, contour_color, contour_fontsize, contour_fontcolor, inline=inline,
                             contour_lw=contour_width, contour_style=contour_style, level=contour_level,
                             fontprecision=contour_fontprecision, alpha=contour_alpha, contour_opt=contour_cmaps_opt,
                             cmaps=contour_cmaps)
        if quiver_opt == 1:
            quiver_var1 = getvar(ncfile, u, timeidx=num)
            quiver_var2 = getvar(ncfile, v, timeidx=num)
            quiver_var1 = get_data_from_3Ddata(quiver_var1, height_quiver)
            quiver_var2 = get_data_from_3Ddata(quiver_var2, height_quiver)
            fig.quiver_draw(lon, lat, quiver_var1, quiver_var2, quiver_interval, quiver_width, quiver_scale,
                            quiver_color, quiver_hw, quiver_alpha, quiverkey_opt, quiverkey_x, quiverkey_y,
                            quiverkey_ws, quiverkey_text, quiverkey_size, color_quiver=color_quiver,
                            color_maps=cmap_quiver, ws_map=ws_map)
    # 绘制颜色图例
    fig.colorbar_draw(rect1, rect2, rect3, rect4, default_colorbar, hv_opt, colorbar_labeltext, colorbar_labelsize,
                      colorbar_ticksize, rectplace, rectextra, ticks=contourf_ticks, drawedges_bool=drawedges_bool,
                      colorbar_ticklength=colorbar_ticklength)
    # 调节子图间距
    fig.adjust_subplot(wspace, hspace)
    # 保存图片
    if multi_file_draw == True:
        savepath = create_savepath(fig_path, fig_name_base, fig_name_end, timelist[fig_num], ncfile, time_zone)
    else:
        savepath = create_savepath(fig_path, fig_name_base, fig_name_end, timelist[fig_num * ver_num * hor_num], ncfile,
                                   time_zone)
    fig.save_fig(savepath, save_dpi=save_dpi, bbox_inches=bbox_inches)
