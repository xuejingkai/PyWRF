# -*- coding: utf-8 -*-
# @Author: cat
# @Date  : 2022年04月19日17:32:18
# @Desc  : 专用于上海市气象局提供的源数据类型，将其转换为xlsx格式，数据格式为RGWST

from datetime import datetime
import xlwt,xlrd
from xlutils.copy import copy
import os
import numpy as np
import time

def creat_xlsx(filename,header):
    '''
    文件创建时写入的头名
    @param filename: 文件名
    @param header: 头文件列表
    @return:
    '''
    wb=xlwt.Workbook()
    for list in header:
        station=str(int(list[0]))
        ws=wb.add_sheet(station)
        ws.write(0,0,'时间')
        ws.write(0,1,'海平面气压')
        ws.write(0,2,'温度')
        ws.write(0,3,'露点温度')
        ws.write(0,4,'相对湿度')
        ws.write(0,5,'风向')
        ws.write(0,6,'风速')
        ws.write(0,7,'观测前1小时降水')
        ws.write(0,8,'观测前6小时降水')
        ws.write(0,9,'观测前24小时降水')
        ws.write(0,10,"经度：")
        ws.write(0,11,list[1])
        ws.write(0,12,"纬度：")
        ws.write(0,13,list[2])
        ws.write(0,14,"站点高度：")
        ws.write(0,15,list[3])
    wb.save(filename)
    del wb

def append_xlsx(filename,valuelist,datelist,onetime):
    '''
    追加写入
    @param filename: 文件名
    @param row: 写入的行数
    @param strlist: 写入内容
    @param date: 写入日期
    @return:
    '''
    wb=xlrd.open_workbook(filename)
    excel = copy(wb)
    a, b = 17.27, 237.7
    c = a * valuelist[:,2] / (b + valuelist[:,2])
    rhlist = np.e ** ((valuelist[:,3] * a - valuelist[:,3] * c - b * c) / (b + valuelist[:,3])) * 100
    valuelist=np.insert(valuelist,4,rhlist,axis=1) # 没有插入时间的情况下，湿度的索引是第3列
    appendcount=0
    for list in valuelist:
        date = datelist[int(appendcount % onetime)]
        if appendcount%onetime==0:
            station = str(int(list[0]))
            nrows = wb.sheet_by_name(station).nrows
            sheet_index = [s.name for s in wb.sheets()].index(station)
            sheet = excel.get_sheet(sheet_index)
            list = list.tolist()
            list[0] = str(date)  # 插入时间
        else:
            sheet=sheet
            nrows=nrows
            list = list.tolist()
            list[0] = str(date)  # 插入时间
        c=0
        for value in list:
            sheet.write(nrows,c,value)
            c+=1
        nrows+=1
        appendcount+=1
    excel.save(filename)
    print("写入完成")
#############################################################################
path = r"D:\Data\气象数据\数据\test"
savepath=r"D:\Data\气象数据\数据\merged\data.xls"
onetime=30
#############################################################################
files= os.listdir(path) #得到文件夹下的所有文件名称
files.sort() # 排序
whetherheader=True
header=[]
count=1
start=time.time()
valuelist,datelist=[],[]
for file in files: #遍历文件夹
    print(file)
    f = open(path+"/"+file,"r",encoding='UTF-8') #打开文件
    first = True
    indexnum=0
    for line in f: #遍历文件，一行行遍历，读取文本
        # 第一行
        if first==True:
            first=False
            strlist = line.split()
            date_list=np.array(strlist)
            date=datetime(int(date_list[1]),int(date_list[2]),int(date_list[3]),int(date_list[4]))
            datelist.append(date)
            print(date)
        else:
            onelist = line.split()
            onelist = np.array(onelist)
            if date<datetime(2018,5,31):
                # 写入头文件
                if whetherheader == True:
                    header.append([onelist[0],onelist[2],onelist[1],onelist[3]])
                    valuelist.append([onelist[0],onelist[7],onelist[8],onelist[9],onelist[10],onelist[11],onelist[12],onelist[13],onelist[14]])
                else:
                    valuelist.insert(count-1+indexnum*count,[onelist[0],onelist[7],onelist[8],onelist[9],onelist[10],onelist[11],onelist[12],onelist[13],onelist[14]])
            else:
                # 写入头文件
                if whetherheader == True:
                    header.append([onelist[0],onelist[3],onelist[2],onelist[4]])
                    valuelist.append([onelist[0],onelist[7],onelist[8],onelist[9],onelist[10],onelist[11],onelist[12],onelist[13],onelist[14]])
                else:
                    valuelist.insert(count-1+indexnum*count,[onelist[0],onelist[7],onelist[8],onelist[9],onelist[10],onelist[11],onelist[12],onelist[13],onelist[14]])
            indexnum+=1
    if whetherheader==True:
        print("创建头文件")
        creat_xlsx(savepath,np.array(header).astype(float))
        whetherheader=False
        del header
    if count%onetime==0 or file==files[-1]:
        print("开始写入")
        append_xlsx(savepath,np.array(valuelist).astype(float),datelist,count)
        count=0
        valuelist,datelist=[],[]
    print(count)
    count+=1
print("总计耗时：{}s".format(time.time()-start))