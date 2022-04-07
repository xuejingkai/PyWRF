# -*- coding: utf-8 -*-
# @Author: Fishercat
# @Date  : 2022-03-26 01:28:26
# @Desc  : 本文件用于下载清华的landuse数据，需要进行小部分的修改

import requests
from bs4 import BeautifulSoup
import re,os

#url = 'http://data.ess.tsinghua.edu.cn/fromglc2017v1.html'
url = 'http://data.ess.tsinghua.edu.cn/fromglc2015_v1.html'
proxy={'http':'http://127.0.0.1:7890','https':'http://127.0.0.1:7890'}
download_path="D:\Data\WRF-Chem_Files\Land_Cover_Data\TsingHua_Landuse_2015v1"

req=requests.get(url,proxies=proxy)
bs=BeautifulSoup(req.content,'html.parser')
for i in bs.find_all('tr'):
    download_url=re.findall('href=\"(.+?)\">',str(i))[0]
    #<tr><td>180W60N.tif</td><td><a href="http://data.ess.tsinghua.edu.cn/data/fromglc2017/180W60N.tif">180W60N.tif</a></td></tr>
    print(download_url)
    download_req = requests.get(download_url)
    with open(os.path.join(download_path,download_url.split("Fromglc2015tif/")[1]), 'wb') as f:
        print(os.path.join(download_path,download_url.split("Fromglc2015tif/")[1]))
        f.write(download_req.content)
    print(download_url+"下载完成")