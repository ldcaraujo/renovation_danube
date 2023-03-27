import shutil
from pathlib import Path
import logging
import traceback
from time import time
from os import listdir
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt



work_folder = Path(r"U:\WORK\assembled_same_U")
source_folder = work_folder / "with_complete_dpe_data" / "all"

csv = r"dpe_all3-len_1010-P1-I-HABITAT-FRANCE_BOIS_TUILE-uniq.csv"
path = source_folder / csv


dpe = pd.read_csv(path)

# Create density and unity density for each data
x_roof = dpe.adedpe202006_logtype_ph_u.to_numpy()
len_dens_roof = round((max(x_roof) - min(x_roof))/0.01)+1
print("len_dens_roof", len_dens_roof)
x_d_roof = np.linspace(min(x_roof), max(x_roof), len_dens_roof)
density_roof = sum((abs(xi - x_d_roof) < 0.01) for xi in x_roof)
unity_density_roof = density_roof / density_roof.sum()

x_wall = dpe.adedpe202006_logtype_mur_u_ext.to_numpy()
len_dens_wall = round((max(x_wall) - min(x_wall))/0.01)+1
print("len_dens_wall",len_dens_wall)
x_d_wall = np.linspace(min(x_wall), max(x_wall), len_dens_wall)
density_wall = sum((abs(xi - x_d_wall) < 0.01) for xi in x_wall)
unity_density_wall = density_wall / density_wall.sum()

#plot
format_roof = {"color":"firebrick", "alpha":0.5, "label":'Tuile'}
format_wall = {"color":"cadetblue", "alpha":0.5, "label":'Ardoise'}

plt.fill_between(x_d_wall, unity_density_wall, **format_wall)

plt.fill_between(x_d_roof, unity_density_roof, **format_roof)
plt.legend(loc=9)


# x_wind = dpe.adedpe202006_logtype_baie_type_vitrage.to_numpy()
# len_dens_wind = round((max(x_wind) - min(x_wind))/0.01)+1
# print("len_dens_wind",len_dens_wind)
# x_d_wind = np.linspace(min(x_wind), max(x_wind), len_dens_wind)
# density_wind = sum((abs(xi - x_d_wind) < 0.01) for xi in x_wind)
# unity_density_wind = density_wind / density_wind.sum()