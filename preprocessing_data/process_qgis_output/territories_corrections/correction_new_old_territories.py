
import pandas as pd
from os import listdir
from time import time

from access_files import INPUT_DATA_PATH, QGIS_OUTPUT_OLD_TER, QGIS_OUTPUT_NEW_TER


# Create a dictionary with old and new csv
path_territ_association = INPUT_DATA_PATH / "Danube" / "Carte_territoire" / "territ_dept.xlsx"
df_ter_association = pd.read_excel(path_territ_association)
df_relation_ter = df_ter_association[["INSEE_DEP", "Terr_P1", "Terr_P2"]].set_index("INSEE_DEP")
dict_territ = df_relation_ter.to_dict()

list_csvs = listdir(QGIS_OUTPUT_OLD_TER / "old_territory_csvs_per_department")
for csv_name in list_csvs[35:36]:
    time_start = time()
    print(csv_name)
    # Source path
    source = QGIS_OUTPUT_OLD_TER / "old_territory_csvs_per_department" / csv_name
    # Destination path
    destination = QGIS_OUTPUT_NEW_TER / csv_name
    dept = csv_name[-6:-4]

    print(dept, " - starting changes")
    time_start = time()
    file = pd.read_csv(source, low_memory=False)
    dur_open = time_start - time()
    print(dur_open)


    file["filosofi_part_proprietaire"] = file["Part-prop_mean"]
    file["filosofi_part_pauvrete"] = file["Part-Pauvr_mean"]

    # file["typologie_mapuce_count"] = file["TYPO_count"]
    file["typologie_mapuce"] = file["TYPO_M"]

    file["territory_P1"] = dict_territ["Terr_P1"][dept]
    file["territory_P2_P7"] = dict_territ["Terr_P2"][dept]

    file["geometry_BDNB"] = file["geometry"]

    file = file.drop(['Unnamed: 0', 'INSEE_DEP_min',
                      'Ter_P1_min', 'Ter_P2-7_min',
                      "Part-prop_mean","Part-Pauvr_mean",
                      "TYPO_M", "geometry"
                      ], axis=1)
    try:
        file = file.drop(["TYPO_min", "TYPO_unique", "TYPO_count",
                      ], axis=1)
    except:
        print("PROBLEM in ", "TYPO_min", "TYPO_unique", "TYPO_count",)



    destination = QGIS_OUTPUT_NEW_TER / "csvs_per_department" / csv_name

    file.to_csv(destination, index=False)




