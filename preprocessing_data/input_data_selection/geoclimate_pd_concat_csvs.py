import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

direc = r"C:\Data\ROBERT\52_geoclimate"
city_fold = os.listdir(direc)


city_files_path = [os.path.join(direc, fold, "BUILDING_TYPO.csv") for fold in city_fold]

city_dfs = [pd.read_csv(files_path) for files_path in city_files_path]
cities_geoclimate = pd.concat(city_dfs)
cities_geoclimate.to_csv(QGIS_INPUT_PATH / "50geoclimate" / "pd_cities_geoclimate.csv")
