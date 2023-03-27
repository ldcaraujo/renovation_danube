import geopandas as gpd
from datetime import datetime, timedelta

from access_files import QGIS_INPUT_PATH

file_loc = (
    QGIS_INPUT_PATH
    / "Filosofi"
    / "Travail_Filosofi"
    / "Filosofi2015_carreaux_200m_metropole_V3.shp"
)
filo = gpd.read_file(file_loc)


def timenow():
    time = datetime.utcnow() + timedelta(hours=2)
    return time.strftime("%H:%M:%S")


print("start - ", timenow())
filo.to_crs(2154)
print(filo.crs)
filo_use = filo[["Part-prop", "Part-Pauvr", "geometry"]]
print(list(filo_use.columns))
path_save_filosofi = (
    QGIS_INPUT_PATH / "Filosofi" / "Filosofi_useful" / "filosofi_useful_cols.shp"
)
filo_use.to_file(path_save_filosofi)
print("end - ", timenow())
