
from osgeo import gdal
import numpy as np

def lcz_pre(lcz,edtlcz):
    print(lcz+"开始修改")
    # 获取lczmap的数据
    lcz_tiff_data = gdal.Open(lcz)
    lcz_width,lcz_height=lcz_tiff_data.RasterXSize,lcz_tiff_data.RasterYSize
    lcz_proj=lcz_tiff_data.GetProjection()
    lcz_geo=lcz_tiff_data.GetGeoTransform()
    lcz_tiff_band = lcz_tiff_data.GetRasterBand(1)
    lcz_list_array = lcz_tiff_band.ReadAsArray()
    # 将lcz修改为wrf需要的格式
    lcz_list_array[np.where(lcz_list_array == 1)] = 31
    lcz_list_array[np.where(lcz_list_array == 2)] = 32
    lcz_list_array[np.where(lcz_list_array == 3)] = 33
    lcz_list_array[np.where(lcz_list_array == 4)] = 34
    lcz_list_array[np.where(lcz_list_array == 5)] = 35
    lcz_list_array[np.where(lcz_list_array == 6)] = 36
    lcz_list_array[np.where(lcz_list_array == 7)] = 37
    lcz_list_array[np.where(lcz_list_array == 8)] = 38
    lcz_list_array[np.where(lcz_list_array == 9)] = 39
    lcz_list_array[np.where(lcz_list_array == 10)] = 40
    lcz_list_array[np.where(lcz_list_array == 105)] = 41
    lcz_list_array[np.where(lcz_list_array==101)]=42
    lcz_list_array[np.where(lcz_list_array==102)]=42
    lcz_list_array[np.where(lcz_list_array==103)]=42
    lcz_list_array[np.where(lcz_list_array==104)]=42
    lcz_list_array[np.where(lcz_list_array==106)]=42
    lcz_list_array[np.where(lcz_list_array==107)]=42
    driver = gdal.GetDriverByName('GTiff')
    edttiff = driver.Create(edtlcz, xsize=lcz_width, ysize=lcz_height, bands=1,
                            eType=gdal.GDT_UInt16, options=["TILED=YES", "COMPRESS=LZW"])
    edttiff.GetRasterBand(1).WriteArray(lcz_list_array)
    edttiff.SetGeoTransform(lcz_geo)  # driver对象创建的dataset对象具有SetGeoTransform方法，写入仿射变换参数GEOTRANS
    edttiff.SetProjection(lcz_proj)  # SetProjection写入投影im_proj
    print("修改完成")

if __name__ == '__main__':

    #edit_tiff(r"D:\Data\WRF-Chem Files\Land Cover Data\QingHua_Landuse_2017v1\china_simulation\120E40N3.tif",
    #          r"D:\Data\WRF-Chem Files\Land Cover Data\QingHua_Landuse_2017v1\china_simulation\120E40N3_new3.tif",
    #          r"D:\Data\WRF-Chem Files\Land Cover Data\中国土地利用数据（1980-2015）\中国土地利用数据1980-2015\lucc2015\TIFF\rc_lucc2015_wgs84.tif")
    #edit_tiff_value(r"D:\Data\WRF-Chem Files\Land Cover Data\QingHua_Landuse_2017v1\china_simulation\120E40N3.tif",
    #                r"D:\Data\WRF-Chem Files\Land Cover Data\QingHua_Landuse_2017v1\china_simulation\120E40N3_new.tif",4000,8400,2000,8400)
    #readasarray后，list[i,j]为第几行，第几列
    lcz_pre(r"D:\Data\WRF-Chem_Files\Land_Use_Data\LCZ_Shanghai\Landset8\5_Resample\LCZC_resampled.tif",
            r"D:\Data\WRF-Chem_Files\Land_Use_Data\LCZ_Shanghai\Landset8\5_Resample\LCZC_resampled_ucm.tif")