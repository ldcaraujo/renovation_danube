import numpy as np
import geopandas as gpd
from datetime import datetime, timedelta

from access_files import QGIS_INPUT_PATH


def timenow():
    time = datetime.utcnow() + timedelta(hours=2)
    return time.strftime("%H:%M:%S")


print("start 0 - ", timenow())
file_loc = QGIS_INPUT_PATH / "50geoclimate" / "MAPUCE Total" / "Mapuce_Total_V5.shp"

# ~7min30seg to charge table
geo50 = gpd.read_file(file_loc)
print("end 0 - ", timenow())


print(list(geo50.columns))
geo50_use = geo50[["TYPO", "Ville", "geometry"]]
print(list(geo50_use.columns))

print("start 1 - ", timenow())
print(len(geo50_use.TYPO.unique()))
print("end 1- ", timenow())

conditions = [
    (geo50_use["TYPO"] == "pcif")
    | (geo50_use["TYPO"] == "pcio")
    | (geo50_use["TYPO"] == "pd")
    | (geo50_use["TYPO"] == "psc"),
    (geo50_use["TYPO"] == "icif")
    | (geo50_use["TYPO"] == "icio")
    | (geo50_use["TYPO"] == "id"),
    (geo50_use["TYPO"] == "ba"),
    (geo50_use["TYPO"] == "bgh"),
    (geo50_use["TYPO"] == "local"),
]

# create a list of the values we want to assign for each condition
values = ["P", "I", "BA", "IGH", "local"]

# create a new column and use np.select to assign values to it using our lists as arguments
geo50_use["TYPO_S"] = np.select(conditions, values)

print("start 2- ", timenow())
path_save_geoc = QGIS_INPUT_PATH / "50geoclimate" / "simplified" / "geo50_TYPO_S.shp"
geo50_use.to_file(path_save_geoc)


geo50_use_nolocal = geo50_use[geo50_use["TYPO_S"] != "local"]
path_save_geoc_nolocal = (
    QGIS_INPUT_PATH
    / "50geoclimate"
    / "simplified_without_local"
    / "geo50_TYPO_S_nolocal.shp"
)
geo50_use_nolocal.to_file(path_save_geoc_nolocal)
print("end 3- ", timenow())
