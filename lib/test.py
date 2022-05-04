from osgeo import gdal
import numpy as np


tiff=gdal.Open(r"D:\Data\WRF-Chem_Files\Population_Data\sh_ghspop_2015.tif")
tiff=gdal.Open(r"D:\Data\WRF-Chem_Files\Land_Use_Data\LCZ_Shanghai\Landset8\9_Anthro_heat\sh_landscan_2016.tif")
data = tiff.GetRasterBand(1).ReadAsArray()
#data=np.float64(data)
print(np.max(data)/np.sum(data))