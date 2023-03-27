import geopandas as gpd

from access_files import QGIS_INPUT_PATH

file_loc = QGIS_INPUT_PATH / "50geoclimate" / "simplified" / "geo50_TYPO_S.shp"
check_typo = gpd.read_file(file_loc, rows=slice(0, 100))
check_typo.to_csv(r"check_typo.csv")

file_loc_no_local = (
    QGIS_INPUT_PATH
    / "50geoclimate"
    / "simplified_without_local"
    / "geo50_TYPO_S_nolocal.shp"
)
check_typo_no_local = gpd.read_file(file_loc_no_local, rows=slice(0, 100))
check_typo_no_local.to_csv(r"check_typo_no_local.csv")
