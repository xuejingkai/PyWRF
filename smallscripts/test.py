import netCDF4 as nc
path=r'D:\Data\WRF-Chem_Files\WRF-Chem_Simulation\noucm_defaultParam_modis\wrfout_d03_2016-07-21_00-00-00'
n=nc.Dataset(path)
print(n["GRDFLX"])