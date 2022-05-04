# edited on 2022.03.31.15:26
# This script is used for file rename.

import os

file_folder=r"/media/fishercat/TOSHIBA/WRF-Chem Files/WRF-Simulation/ucm_modifiedParam"

for file in os.listdir(file_folder):
    if ":" in file:
        new_filename=file.replace(":","-")
        os.rename(os.path.join(file_folder,file),os.path.join(file_folder,new_filename))
        print(file+" is rename to: "+new_filename)
    else:
        continue
