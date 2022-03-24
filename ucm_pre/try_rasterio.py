import rasterio
from osgeo import gdal

tiff_file = r"D:\new\test\120E40N0.TIF"
tiff_data = rasterio.open(tiff_file)
data = tiff_data.read(1)[::-1]
data.tofile(r"D:\new\test\raster\00001-10000.00001-10000")
#######################################################
options_list = ['-of ENVI']
options_string = " ".join(options_list)
gdal.Translate(r"D:\new\test\gdal\00001-10000.00001-10000", tiff_file,
               options=options_string)