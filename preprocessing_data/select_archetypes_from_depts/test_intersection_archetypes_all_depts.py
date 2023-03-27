from os import listdir

import pandas as pd

# charge Danube data base
from access_files import DATA_PATH

danube_path = (
    DATA_PATH / "Danube" / "20220616_BddMAPUCE_MAP_V16.4-draft-export-utf8.csv"
)
danube = pd.read_csv(danube_path, sep=";")
# create column with Danube archetypes
danube["archetype"] = (
    danube["PERIODE"].astype(str)
    + "-"
    + danube["NOM_TYPOLOGIE"].astype(str)
    + "-"
    + danube["USAGE"].astype(str)
    + "-"
    + danube["TERRITOIRE"].astype(str)
)
# list of all Danube archetypes
archs_danube = list(danube["archetype"])
print(archs_danube[:2])
print(f"danube_archs len of {len(archs_danube)}")
print(len(set(archs_danube)))

# ///////////////////////
# charge archetypes from dept archs outputs
arch_per_dept_paths = DATA_PATH / "_output_code" / "archetypes_per_dept_tables"
files_archs_depts = listdir(arch_per_dept_paths)

print(files_archs_depts[:2])
archs_depts = ["-".join(file_name.split("-")[:4]) for file_name in files_archs_depts]
print(f"archs_depts len of {len(archs_depts)}")
print(archs_depts[:2])

print("#" * 50 + "\n")
intersection = set(archs_danube) & set(archs_depts)
print(f"intersection type {type(intersection)}")
print(f"intersection len of {len(intersection)}")
print(intersection)

print("#" * 50 + "\n")
archs_just_danube = set(archs_danube) - intersection
print(f"archs_just_danube type {type(archs_just_danube)}")
print(f"archs_just_danube len of {len(archs_just_danube)}")
print(archs_just_danube)
print("#" * 50 + "\n")
archs_just_depts = set(archs_depts) - intersection
print(f"archs_just_depts type {type(archs_just_depts)}")
print(f"archs_just_depts len of {len(archs_just_depts)}")
print(archs_just_depts)
print("#" * 50 + "\n")
