# -*- coding: utf-8 -*-
# @Author: Fishercat
# @Date  : 2022-04-24 20:22:24
# @Desc  : 计算各个分类的各种值，包括Albedo，emissivity，urban fraction

from osgeo import gdal,gdalconst
import numpy as np

def cal_class_albedo(lcz_path,bsa_shortwave_path,wsa_shortwave_path):
    '''
    计算公式参考文献：
    An Y, Meng X, Zhao L, et al.
    Performance of GLASS and MODIS Satellite Albedo products in diagnosing Albedo variations during different time scales and special weather conditions in the Tibetan Plateau[J].
    Remote Sensing, 2020, 12(15): 2456.
    @param lcz_path: lcz文件地址
    @param bsa_shortwave_path: bsa短波文件地址
    @param wsa_shortwave_path: wsa短波文件地址
    @return : None
    '''
    lcz_tiff=gdal.Open(lcz_path)
    lcz_band=lcz_tiff.GetRasterBand(1)
    lcz_classification=lcz_band.ReadAsArray()
    width,height=lcz_tiff.RasterXSize,lcz_tiff.RasterYSize
    bsa_tiff=gdal.Open(bsa_shortwave_path)
    wsa_tiff=gdal.Open(wsa_shortwave_path)
    bsa_band,wsa_band=bsa_tiff.GetRasterBand(1),wsa_tiff.GetRasterBand(1)
    bsa_data = bsa_band.ReadAsArray()
    wsa_data = wsa_band.ReadAsArray()

    r=0.122+0.85*np.exp(-4.8*np.cos(25.5*np.pi/180))
    print("大气散射比例为：{}".format(r))

    albedo_list = []
    for i in range(11):
        albedo_list.append([])
    print(width, height)
    for row in range(height):
        for col in range(width):
            if lcz_classification[row, col] < 11:
                index = int(lcz_classification[row, col] - 1)
                if bsa_data[row,col]>0:
                    albedo=bsa_data[row,col]*(1-r)+wsa_data[row,col]*r
                    albedo_list[index].append(albedo)
            if lcz_classification[row, col] == 105:
                if bsa_data[row, col] >0:
                    albedo = bsa_data[row, col] * (1 - r) + wsa_data[row, col] * r
                    albedo_list[10].append(albedo)
        print(row / height)

    for i in range(11):
        list = albedo_list[i]
        array = np.array(list)
        array = array*0.001
        if np.shape(array)[0] == 0:
            continue
        else:
            print("{}分类的平均albedo值为：{},共有{}个值：".format(i + 1, np.sum(array) / np.shape(array)[0], np.shape(array)[0]))
            array_without99 = array[np.where(array < np.percentile(array, 95))]
            print("{}分类，去除最大值以后的平均albedo值为：{},共有{}个值：".format(i + 1,
                                                              np.sum(array_without99) / np.shape(array_without99)[0],
                                                              np.shape(array_without99)[0]))

def cal_class_bbe(lcz_path,bbe_path):
    '''
    计算使用的数据：GLASS-BBE-1km
    @param lcz_path: lcz文件地址
    @param bbe_path: bbe文件地址
    @return : None
    '''
    lcz_tiff=gdal.Open(lcz_path)
    lcz_band=lcz_tiff.GetRasterBand(1)
    lcz_classification=lcz_band.ReadAsArray()
    width,height=lcz_tiff.RasterXSize,lcz_tiff.RasterYSize
    bbe_tiff=gdal.Open(bbe_path)
    bbe_band=bbe_tiff.GetRasterBand(1)
    bbe_data = bbe_band.ReadAsArray()
    bbe_data=bbe_data/10000

    bbe_list = []
    for i in range(11):
        bbe_list.append([])
    print(width, height)
    for row in range(height):
        for col in range(width):
            if lcz_classification[row, col] < 11:
                index = int(lcz_classification[row, col] - 1)
                if bbe_data[row,col]>0:
                    bbe=bbe_data[row,col]
                    bbe_list[index].append(bbe)
            if lcz_classification[row, col] == 105:
                if bbe_data[row, col] >0:
                    bbe = bbe_data[row, col]
                    bbe_list[10].append(bbe)
        print(row / height)

    for i in range(11):
        list = bbe_list[i]
        array = np.array(list)
        if np.shape(array)[0] == 0:
            continue
        else:
            print("{}分类的平均emissivity值为：{},共有{}个值：".format(i + 1, np.sum(array) / np.shape(array)[0], np.shape(array)[0]))
            array_without99 = array[np.where(array < np.percentile(array, 95))]
            print("{}分类，去除最大值以后的平均emissivity值为：{},共有{}个值：".format(i + 1,
                                                              np.sum(array_without99) / np.shape(array_without99)[0],
                                                              np.shape(array_without99)[0]))

def cal_class_urbfrc(lcz_path,ndvi_path,ndwiflags_path):
    '''
    计算使用的数据：Landsat8生成的ndvi计算不渗水表面占比，即urbfrc
    参考文献：[1]张本昀,喻铮铮,刘良云,张震宇,孙婷婷.北京山区植被覆盖动态变化遥感监测研究[J].地域研究与开发,2008(01):108-112.
    参考文中的操作，取累计百分数1%与99%作为置信区间。
    @param lcz_path: lcz文件地址
    @param ndvi_path: ndvi文件地址
    @param ndwiflags_path: ndwiflags文件地址
    @return : None
    '''
    lcz_tiff=gdal.Open(lcz_path)
    lcz_band=lcz_tiff.GetRasterBand(1)
    lcz_classification=lcz_band.ReadAsArray()
    width,height=lcz_tiff.RasterXSize,lcz_tiff.RasterYSize
    ndvi_tiff=gdal.Open(ndvi_path)
    ndvi_band=ndvi_tiff.GetRasterBand(1)
    ndvi_origin = ndvi_band.ReadAsArray()
    ndvi_data=ndvi_origin.copy() # 复制一个数组，用来修改置信区间
    ndwiflags_tiff=gdal.Open(ndwiflags_path) # ndvi值
    ndwiflags_band=ndwiflags_tiff.GetRasterBand(1)
    ndwiflags_data = ndwiflags_band.ReadAsArray() # 水体分割标识
    # 取1%~99%为置信区间
    low_per,hi_per=5,95
    ndvi_soil=np.percentile(ndvi_origin[np.where(ndwiflags_data==0)],low_per)
    ndvi_veg=np.percentile(ndvi_origin[np.where(ndwiflags_data==0)],hi_per)
    ndvi_data[np.where(ndwiflags_data==1)]=np.percentile(ndvi_origin[np.where(ndwiflags_data==0)],low_per)
    ndvi_data[np.where(ndvi_origin<np.percentile(ndvi_origin[np.where(ndwiflags_data==0)],low_per))]=np.percentile(ndvi_origin[np.where(ndwiflags_data==0)],low_per)
    ndvi_data[np.where(ndvi_origin>np.percentile(ndvi_origin[np.where(ndwiflags_data==0)],hi_per))]=np.percentile(ndvi_origin[np.where(ndwiflags_data==0)],hi_per)

    ndvi_list = []
    print(width, height)
    for i in range(11):
        if i==10:
            index=105
        else:
            index=i+1
        ndvi_temp=ndvi_data[np.where(lcz_classification==index)]
        previous_frc=(ndvi_temp-ndvi_soil)/(ndvi_veg-ndvi_soil)
        imprevious_frc=1-previous_frc
        ndvi_list.append(imprevious_frc.flatten())
        print(i/10)
    '''
    老方法，速度过于慢
    for row in range(height):
        for col in range(width):
            if lcz_classification[row, col] < 11:
                index = int(lcz_classification[row, col] - 1)
                # 只有陆地才记录ndvi值
                if ndwiflags_data[row,col]==0:
                    ndvi=ndvi_data[row,col]
                    previous_frc=(ndvi-ndvi_soil)/(ndvi_veg-ndvi_soil)
                    ndvi_list[index].append(1-previous_frc)
            if lcz_classification[row, col] == 105:
                if ndwiflags_data[row,col]==0:
                    ndvi=ndvi_data[row,col]
                    previous_frc=(ndvi-ndvi_soil)/(ndvi_veg-ndvi_soil)
                    ndvi_list[10].append(1-previous_frc)
        print(row / height)
    '''

    for i in range(11):
        array = ndvi_list[i]
        if np.shape(array)[0] == 0:
            continue
        else:
            print("{}分类的平均urbfrc值为：{},共有{}个值：".format(i + 1, np.sum(array) / np.shape(array)[0], np.shape(array)[0]))
            array_without99 = array[np.where(array > np.percentile(array, 5))]
            print("{}分类，去除最小值以后的平均urbfrc值为：{},共有{}个值：".format(i + 1,
                                                              np.sum(array_without99) / np.shape(array_without99)[0],
                                                              np.shape(array_without99)[0]))

def cal_class_anthheat(poplationtiff,lcztiff):
    '''
    计算各个分区下的人为产数据，注意两个输入的tiff必须格点相同
    @param poplationtiff: 人口数据
    @param lcztiff: lcz的tiff文件
    @return : None
    '''
    coal_all=11712.39
    coal_industry=5740.55
    ep_coal2j=29271 # epsilon_s
    electricity_all=1486.02
    electricity_industry=798.18
    base_anthroheat=(coal_all-coal_industry)*ep_coal2j*10000*1000*1000/31536000/100/100+(electricity_all-electricity_industry)*100000000*1000/8760/100/100 # 非工业区的人工产热
    ind_anthroheat=(coal_industry)*ep_coal2j*10000*1000*1000/31536000/100/100+(electricity_industry)*100000000*1000/8760/100/100 # 工业区的人工产热
    person_anthroheat=(175*16.5+75*7.5)/24 # 每个人的平均产热

    class_tiff=gdal.Open(lcztiff,gdalconst.GA_ReadOnly)
    width,height=class_tiff.RasterXSize,class_tiff.RasterYSize
    lcz_classification=class_tiff.GetRasterBand(1).ReadAsArray()
    pop_tiff=gdal.Open(poplationtiff,gdalconst.GA_ReadOnly)
    population_array = pop_tiff.GetRasterBand(1).ReadAsArray()
    population_woind_array = population_array[np.where(np.logical_and(lcz_classification < 10, lcz_classification!=8))] # 筛选非工业区域与人居住区的人口
    population_ind_array = population_array[np.where(np.logical_or(np.logical_or(lcz_classification == 8 , lcz_classification == 10),lcz_classification==105))] # 筛选工业区域的人口
    pop_woind_sum=np.sum(np.float64(population_woind_array))
    pop_ind_sum=np.sum(np.float64(population_ind_array))

    ah_list = []
    for i in range(11):
        ah_list.append([])
    print(width, height)
    for row in range(height):
        for col in range(width):
            # 非工业区
            if lcz_classification[row, col] < 8:
                index = int(lcz_classification[row, col] - 1)
                if population_array[row,col]>0:
                    pop=population_array[row,col]
                    ah_list[index].append(pop/pop_woind_sum*base_anthroheat+pop*person_anthroheat/100/100)
            # 工业区
            elif lcz_classification[row, col] == 8:
                if population_array[row, col] >0:
                    pop=population_array[row,col]
                    ah_list[7].append(pop/pop_ind_sum*ind_anthroheat+pop*person_anthroheat/100/100)
            # 非工业区
            elif lcz_classification[row, col] == 9:
                if population_array[row, col] >0:
                    pop=population_array[row,col]
                    ah_list[8].append(pop/pop_woind_sum*base_anthroheat+pop*person_anthroheat/100/100)
            # 工业区
            elif lcz_classification[row, col] == 10:
                if population_array[row, col] >0:
                    pop=population_array[row,col]
                    ah_list[9].append(pop/pop_ind_sum*ind_anthroheat+pop*person_anthroheat/100/100)
            # 工业区
            elif lcz_classification[row, col] == 105:
                if population_array[row, col] >0:
                    pop=population_array[row,col]
                    ah_list[10].append(pop/pop_ind_sum*ind_anthroheat+pop*person_anthroheat/100/100)

        print(row / height)

    for i in range(11):
        list = ah_list[i]
        array = np.array(list)
        if np.shape(array)[0] == 0:
            continue
        else:
            print("{}分类的平均anthropogenic heat值为：{},共有{}个值：".format(i + 1, np.sum(array) / np.shape(array)[0], np.shape(array)[0]))
            array_without5 = array[np.where(array > np.percentile(array, 5))]
            print("{}分类，去除最大值以后的平均emissivity值为：{},共有{}个值：".format(i + 1, np.sum(array_without5) / np.shape(array_without5)[0],np.shape(array_without5)[0]))

if __name__=="__main__":
    sza_path = r"D:\Data\WRF-Chem_Files\Albedo\MCD43A2\MCD43A2.A2017094.mosaic.006.2022112105504.mcrpgs_000501768092.BRDF_Albedo_LocalSolarNoon-BRDF_Albedo_LocalSolarNoon.tif"
    bsa_shortwave_path = r"D:\Data\WRF-Chem_Files\Albedo\MCD43A3_BSA_shortwave_resample.tif"
    wsa_shortwave_path = r"D:\Data\WRF-Chem_Files\Albedo\MCD43A3_WSA_shortwave_resample.tif"
    bbe_path=r"D:\Data\WRF-Chem_Files\Emissitive\GLASS_BBE_Combine.tif"
    ndvi_path=r"D:\Data\WRF-Chem_Files\NDVI\FromLandsat8\ndvi_landsat8_resampled.tif"
    ndwiflags_path=r"D:\Data\WRF-Chem_Files\NDVI\FromLandsat8\ndwiflag_landsat8_resampled.tif"
    lcz_path = r"D:\Data\WRF-Chem_Files\Land_Use_Data\LCZ_Shanghai\Landset8\5_Resample\LCZC_2_resampled.tif"
    lcz_path_hire = r"D:\Data\WRF-Chem_Files\Land_Use_Data\LCZ_Shanghai\Landset8\4_LCZ_Shanghai\L1TP\version2\LCZC_2.tif"
    ndvi_path_hire=r"D:\Data\WRF-Chem_Files\NDVI\FromLandsat8\ndvi_landsat8_hire.tif"
    ndwiflags_path_hire=r"D:\Data\WRF-Chem_Files\NDVI\FromLandsat8\ndwiflag_landsat8_hire.tif"
    population_path=r"D:\Data\WRF-Chem_Files\Land_Use_Data\LCZ_Shanghai\Landset8\9_Anthro_heat\sh_landscan_2016_resampled.tif"
    poplcz_path=r"D:\Data\WRF-Chem_Files\Land_Use_Data\LCZ_Shanghai\Landset8\9_Anthro_heat\sh_lczc_100m_wgs84.tif"
    #cal_class_albedo(lcz_path,bsa_shortwave_path,wsa_shortwave_path)
    #cal_class_bbe(lcz_path,bbe_path)
    #cal_class_urbfrc(lcz_path,ndvi_path,ndwiflags_path)
    #cal_class_urbfrc(lcz_path_hire,ndvi_path_hire,ndwiflags_path_hire)
    cal_class_anthheat(population_path,poplcz_path)