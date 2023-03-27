
import pandas as pd
from os import listdir
import shutil

from preprocessing_data.process_qgis_output.create_danube_entries import create_territory_1dep, create_archetype
from access_files import DATA_PATH, QGIS_OUTPUT_OLD_TER, QGIS_OUTPUT_NEW_TER


# Create a dictionary with old and new csv
path_territ_association = DATA_PATH / "Danube" / "Carte_territoire" / "territ_dept.xlsx"
df = pd.read_excel(path_territ_association)
df_relation_ter = df[["INSEE_DEP","Terr_P1","Terr_P2"]].set_index("INSEE_DEP")
dict_territ = df_relation_ter.to_dict()

## If just the modified territories that are targeted, the following code can be used:
# diff_P1 = set(df[df.Terr_P1 != df.P1Old].INSEE_DEP)
# diff_P2 = set(df[df.Terr_P2 != df.P2Old].INSEE_DEP)
# diff = diff_P2
# diff.update(diff_P1)
# df_diff = df[df["INSEE_DEP"].isin(diff)][["INSEE_DEP","Terr_P1","Terr_P2"]].set_index("INSEE_DEP")
# dict_territ = df_diff.to_dict()



list_csvs = listdir(QGIS_OUTPUT_OLD_TER / "csvs_per_department")
for csv_name in list_csvs:
    # Source path
    source = QGIS_OUTPUT_OLD_TER / csv_name
    # Destination path
    destination = QGIS_OUTPUT_NEW_TER / csv_name
    dept = csv_name[-6:-4]

    if dept in diff:
        print(dept, " : CHANGED")
        file = pd.read_csv(source)
        file["Ter_P1_min"] = dict_territ["Terr_P1"][dept]
        file["Ter_P2-7_min"] = dict_territ["Terr_P2"][dept]

        create_territory_1dep(file)
        create_archetype(file)
        arch = file.archetype.unique()[0]
        dept_nb = file.INSEE_DEP_min.unique()[0]
        # ***destination = fr"{folder_new_csvs}\{arch}-dep{dept_nb}-len{len(file)}.csv"


        file.to_csv(destination)


    else:
        try:
        # Copying the other files without alteration
            shutil.copy(source, destination)
            print(dept, "File copied successfully.")
        # If source and destination are same
        except shutil.SameFileError:
            print("Source and destination represents the same file.")
        # If there is any permission issue
        except PermissionError:
            print("Permission denied.")
        # For other errors
        except:
            print("Error occurred while copying file.")

