import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import geopandas as gpd
from datetime import datetime, timezone, timedelta

from access_files import QGIS_INPUT_PATH

file_loc = (
    QGIS_INPUT_PATH
    / "Territoire"
    / "Carte_Territoires_Dabube_V2022-06-15"
    / "Carte_Territoires_Danube_V2022-06-15.shp"
)
territ = gpd.read_file(file_loc)


def timenow():
    time = datetime.utcnow() + timedelta(hours=2)
    return time.strftime("%H:%M:%S")


print("start - ", timenow())
filo.to_crs(2154)
print(territ.crs)
territ_use = territ[["INSEE_DEP", "Ter_P1", "Ter_P2-7", "geometry"]]
print(list(territ_use.columns))
territ_use.to_file(
    QGIS_INPUT_PATH / "Territoire" / "ter_useful_cols" / "territoire_useful_cols.shp"
)
print("end - ", timenow())
