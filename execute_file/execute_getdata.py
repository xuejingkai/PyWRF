# -*- coding: utf-8 -*-
# @Author: cat
# @Date  : 2022年04月18日22:13:06
# @Desc  : 用于提取文件数据，为执行文件，默认使用的配置文件为namelist_getdata.py

import os
import pandas as pd
from namelist_getdata import *
import netCDF4 as nc
from wrf import getvar, to_np
from lib.Readtime import get_ncfile_time

def get_2Ddata(data, height):
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
        data=data
        print("数据为二维")
    return data

def save_file(name,mode,data,precision):
    data_df=pd.DataFrame(data)
    if mode=="csv":
        data_df.to_csv(name+".csv",float_format=precision,index=False,header=False)
    if mode=="xlsx":
        writer=pd.ExcelWriter(name+".xlsx")
        data_df.to_excel(writer,"sheet",float_format=precision,index=False,header=False)
        writer.save()
    print("{}文件保存完成".format(name))

ncfile=nc.Dataset(ncfilename)
timelist=get_ncfile_time(ncfile,timezone=timezone)
if inheight==True:
    if intime==True or inall==True:
        raise Exception("inheight为True，请检查其他参数")
    else:
        print("将沿着高度输出")
        alldata=to_np(getvar(ncfile, var, timeidx=timenum))
        lat=to_np(getvar(ncfile, "lat"))
        lon=to_np(getvar(ncfile, "lon"))
        for height in heightrange:
            print("写入高度为:{}".format(height))
            savefilename=os.path.join(savefolder,var+"_"+str(timelist[timenum]).replace(":","").replace(" ","-")+"_"+str(height))
            data=get_2Ddata(alldata,height)
            save_file(savefilename,savemode,data,precision)
        print("写入经纬度文件")
        save_file(os.path.join(savefolder,"lattitude"), savemode, lat, pos_precision)
        save_file(os.path.join(savefolder,"longitude"), savemode, lon, pos_precision)
elif intime==True:
    if inheight==True or inall==True:
        raise Exception("inheight为True，请检查其他参数")
    else:
        print("将沿着时间输出")
        lat=to_np(getvar(ncfile, "lat"))
        lon=to_np(getvar(ncfile, "lon"))
        for time in timerange:
            print("写入时间为:{}".format(time))
            alldata=to_np(getvar(ncfile, var,timeidx=time))
            savefilename=os.path.join(savefolder,var+"_"+str(timelist[time]).replace(":","")+"_"+str(heightnum))
            data=get_2Ddata(alldata,heightnum)
            save_file(savefilename,savemode,data, precision)
        print("写入经纬度文件")
        save_file(os.path.join(savefolder,"lattitude"), savemode, lat, pos_precision)
        save_file(os.path.join(savefolder,"longitude"), savemode, lon, pos_precision)
elif inall==True:
    if inheight==True or intime==True:
        raise Exception("inall为True，请检查其他参数")
    else:
        print("将输出所有变量")
        lat=to_np(getvar(ncfile, "lat"))
        lon=to_np(getvar(ncfile, "lon"))
        for time in timerange:
            for height in heightrange:
                print("写入时间为:{}，高度为：{}".format(time,height))
                alldata=to_np(getvar(ncfile, var,timeidx=time))
                savefilename=os.path.join(savefolder,var+"_"+str(timelist[time]).replace(":","")+"_"+str(height))
                data=get_2Ddata(alldata,height)
                save_file(savefilename,savemode,data, precision)
        print("写入经纬度文件")
        save_file(os.path.join(savefolder,"lattitude"), savemode, lat, pos_precision)
        save_file(os.path.join(savefolder,"longitude"), savemode, lon, pos_precision)