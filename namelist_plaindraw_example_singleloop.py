# edited on 2022-04-02 15:17:46
# 绘制平面图所用的namelist文件，仅用于变量修改，并非执行文件

import cmaps
import numpy as np

# 图片信息设置
fig_width = 12  # 图片的宽
fig_height = 5  # 图片高
fig_dpi = 300  # 图片DPI
ver_num, hor_num = 1, 1  # 一张图片显示子图的行数，列数，第几个子图，用于标记
title = ["T(2m) and Wind(10m) "]  # 子图的标题，务必用list形式表示，需要与子图数量对应
title_end = "time"  # 可以设置为"time"或者"num"用于循环作图时在图片标题尾部自动添加,如果不需要则改为None
time_zone = 8  # 自动根据时区修改为当地时间，8表示UTC+8
title_size = 8  # 子图标题字体大小
title_y = 1.04  # 标题的高度

# 地理信息绘制设置
lake_opt = 0  # 0表示显示湖泊，1表示不显示
lake_lw, lake_lc = 0.8, 'black'  # 湖泊的线宽和线的颜色
coastline_lw, coastline_lc = 0.8, 'black'  # 海岸线的线宽和颜色
precision = '10m'  # 精度，10m，50m和110m，要加引号

# 网格、坐标等信息绘制设置
extra = 0.1  # 经纬度外侧空出的余量
west_lon, east_lon = 121.2, 122.0  # 图片显示范围，西侧和东侧经度
south_lat, north_lat = 30.7, 31.4  # 图片显示范围，南侧和北侧纬度
grid_lw, grid_lc, grid_type = 0, 'gray', ':'  # 网格线宽（0表示无网格）；线颜色；线型（{'-', '--', '-.', ':', ''）
major_interval_lon, major_interval_lat = 0.3, 0.3  # x和y轴的大间隔
minor_interval_lon, minor_interval_lat = 0.3, 0.3  # x和y的小间隔，如果无需小间隔设置和大间隔相同即可
labelsize, labelcolor = 7, 'black'  # 坐标轴字体大小和颜色
ticklength = 4  # 刻度线的高度
xlabellist = None  # x轴的标签文字，不需要写为None，不论多少用list表示：["a", "b", "c", ...]，并且需要与子图数量对应
xlabelsize = 10  # x轴标签的字体大小

# 绘制文件信息设置
multi_file_draw = False  # 是否进行多文件绘制，需要与子图数对应，默认按照从左到右，从上到下的顺序排列
path = [
    r'/media/fishercat/F3BF1447AE0CCFAE/Data/WRF-Chem_Files/WRF-Chem_Simulation/lcz_1/wrfout_d03_2016-07-21']  # 读取文件的路径
contourf_opt = 1  # 是否开启填充
contour_opt = 0  # 是否开启轮廓线绘制
quiver_opt = 1  # 是否开启箭头绘制
var_contourf = 'T2'  # 填充的变量
var_contour = 'rh2'  # 绘制等高线的变量
chem_w = 0  # 摩尔质量，如果无需摩尔质量输入小于等于0的数字
u, v = 'U10', 'V10'  # 经度方向和纬度方向的风速
loop_draw = 0  # 1表示开启循环绘制，会按照下面的时间序列绘制多张图
timelist = range(32, 52, 1)  # 时间列表，建议使用list格式，如果是连续时间也可以使用range方法,e.g.：range(56, 69, 2)
height_contourf = 1  # 填充数据高度，如果没有高度则随便填写一个数字
height_contour = 0  # 轮廓线数据高度，如果没有高度则随便填写一个数字
height_quiver = 0  # 轮廓线数据高度，如果没有高度则随便填写一个数字

# 填充图形信息设置
cmap = cmaps.ncl_default  # 填色的颜色类型，具体参考colormap与cmaps库
contourf_level = np.arange(20, 40, 1)  # 填色的最小值，最大值和间隔，如果要使用默认的则改成None
contourf_ticks = np.arange(20, 40, 2)  # 设置colorbar的ticks，如果不需要写成None
colorbar_extend = 'neither'  # colorbar是否带箭头，'neither'和'both'

# 等高线绘制信息设置
contour_level = np.arange(30, 105, 5)  # 等高线最小值，最大值和间隔
contour_color = "white"  # 等高线颜色
contour_width = 0.8  # 等高线宽度
contour_style = "solid"  # 等高线种类（ 'solid', 'dashed', 'dashdot', 'dotted'）
inline = True  # 字体是否要在线内
contour_fontsize = 0  # 字体大小
contour_fontcolor = 0  # 字体颜色
contour_fontlabel = 0  # 字体是否分开轮廓线（0表示是，1表示否）
contour_fontprecision = '%1.0f'  # 精度（'%1.3f'表示小数点后3位）
contour_alpha = 1  # 等高线的透明度，0~1之间
contour_cmaps_opt = 0  # 0表示不用cmap，1表示用。如果用了1，那么colorbar会默认用contour的cmaps
contour_cmaps = cmaps.seaice_2_r  # contour用的cmap

# 矢量箭头图绘制信息设置
quiver_interval = 3  # 风速间隔多少网格点绘制
quiver_width = 0.0025  # 箭头的线宽
quiver_scale = 150  # 箭头的大小（数字越大越小）
quiver_color = 'black'  # 箭头的颜色
quiver_hw = 4  # 箭头的宽度
quiver_alpha = 1  # 箭头的透明度，0~1之间
quiverkey_opt = 0  # 是否显示quiverkey，0表示不显示
quiverkey_x, quiverkey_y = 0.90, 1.03  # quiverkey的相对位置，x和y
quiverkey_ws = 4  # quiverkey的标注风速
quiverkey_text = '4m/s'  # quiverkey的标注字体
quiverkey_size = 7  # quiverkey的字体大小
color_quiver = 0  # 如果启用（设置为1），需要同时设置cmap_quiver和ws_map共用，用颜色来表示风速箭头
cmap_quiver = cmaps.amwg_blueyellowred  # quiver的cmap
ws_map = [(0, 1), (1, 2), (2, 3), (3, 100)]  # 风速cmap对应的几档风速变色

# 颜色图例绘制信息设置
default_colorbar = 0  # 是否采用自定义的色块位置，0表示是，1表示否
rectplace, rectextra = 'right', 1  # 设置空白子图的位置（bottom，top，right，left），数值表示空白多少，相对子图的比例
rect1, rect2, rect3, rect4 = 0.78, 0.1, 0.015, 0.8  # colorbar的位置,分别是 水平位置，垂直位置，水平宽度，垂直宽度
hv_opt = 'vertical'  # 图例垂直还是水平,vertical或者horizontal
colorbar_labeltext = 'Temperature(^oC)'  # 图例写什么字
colorbar_labelsize = 8  # 标签字体大小
colorbar_ticksize = 8  # 刻度字体大小
drawedges_bool = 1  # 决定颜色边界是否要画上黑色的线条，0表示否，1表示是
colorbar_ticklength = 0  # colorbar的tick突出长度，如果是0就是不突出

# 绘制点
dot_draw        = True   # 是否需要绘制点
dot_x           = [120.8,121.0] # list形式写入点的x坐标
dot_y           = [31.0,31.5]   # list形式写入点的y坐标
dot_color       = ["black","gray"]     # list形式写入每个点的颜色
dot_marker      = ["o","D"] # list形式写入每个点的形状
dot_size        = [4,5] # list形式写入每个点的大小
dot_label       = ["第一个","第二个"] # list形式写入每个点的标签
dot_zorder      = 0.8 # 0~1的数值，决定了高低顺序

# 绘制线
line_draw        = True   # 是否需要绘制线
line_x           = [[120.8,121.0]] # 二维list形式写入线的x坐标（始末）
line_y           = [[31.0,31.5]]   # 二维list形式写入线的y坐标（始末）
line_color       = ["green"]     # list形式写入每条线的颜色
line_style       = ["-"] # list形式写入每条线的形状
line_width       = [1] # list形式写入每条线的线宽
line_zorder      = 0.5 # 0~1的数值，决定了高低顺序

# 绘制标签
legend_draw     = True # 是否需要绘制点的标签
legend_loc      = "lower right" # 标签的位置,支持upper/lower/center+right/left/center,best
x_anchor,y_anchor = 1.1,0.1     # 标签的偏离位置
legend_title    = "标题" # 标签标题
legend_markerscale     = 0.75  # 标签内的marker大小
legend_labelspacing    = 1     # 标签内的空格大小
legend_fonttype        = "../font/SimSun.ttf" # 输入字体ttf文件的地址
legend_fontsize        = 8 #字体大小

# 子图间距设置
wspace, hspace = 0.0, 0.2  # 子图的横向间距和纵向间距

# 图片保存信息设置
fig_path = r"/media/fishercat/F3BF1447AE0CCFAE/Data/WRF-Chem_Files/WRF-Chem_Simulation/lcz_1/"  # 图片保存路径
fig_name_base = "t2_wind"  # 图片保存的基础名
fig_name_end = "time"  # 循环作图时图片的后缀
save_dpi = 600  # 保存图片的DPI值
bbox_inches = "tight"  # 设置保存图片的空白边大小，去除空白边用tight，如果不去除则改为None
