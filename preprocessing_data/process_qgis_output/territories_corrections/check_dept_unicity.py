import pandas as pd
import geopandas as gpd
from time import time
from os import listdir
from pathlib import Path

from access_files import QGIS_OUTPUT_OLD_TER, QGIS_OUTPUT_NEW_TER

start_time = time()

dept_files_path = QGIS_OUTPUT_OLD_TER / "joined_per_dept"

all_dept_file_paths = listdir(dept_files_path)
txt = QGIS_OUTPUT_OLD_TER / "buildings_wrong_file_dept.txt"

with open(txt, 'w') as f:
    i = 0
    probs = []
    for dep in all_dept_file_paths[:2]:

        start_time_dep = time()
        print(dep, file=f)
        file_path = dept_files_path / dep
        file = gpd.read_file(file_path)
        print("end opening data")
        deps_in_dep = file.INSEE_DEP_min.unique()
        if len(deps_in_dep) > 1:
            print("OUCH! There are buildings mixed from more than one department:", file=f)
            print(deps_in_dep)
            dict_dep_lens = {}
            for el in deps_in_dep:
                total_len = len(file)
                len_dep = len(file[file["INSEE_DEP_min"] == el])
                dict_dep_lens[el] = [f"{len_dep / total_len * 100 :.3f}%", len_dep]
            probs.append([dep, dict_dep_lens])
            print(f"department problems :", probs[i], file=f)
            i += 1

        else:
            print("OK", file=f)
        time_dep = time() - start_time_dep
        root_dep = dep.split(".")[:-1]
        print(root_dep)

        print("start saving csv")
        folder_save = QGIS_OUTPUT_NEW_TER / "csvs_per_department"

        name_file = folder_save / f"{root_dep[0]}.csv"
        file.to_csv(name_file, encoding='utf-8-sig')
        print("end saving csv")
        print(f"{time_dep:.1f} s",  file=f)
        print("_"*200, "\n", file=f)

    total_time = time() - start_time
    print("total_time: ", total_time)
    print(f"All department problems", probs, file=f)
