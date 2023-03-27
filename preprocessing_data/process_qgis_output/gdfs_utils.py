from functools import partial
from multiprocessing import Pool
from time import time
import logging

# import geopandas as gpd
import pandas as pd


def read_dept_file(file_path):
    # ATTENTION: change the way to read depending on type of file
    start = time()
    dept_nb = str(file_path).split("_")[-1].split(".")[0]
    # dept_gdf = gpd.read_file(file_path)  # for SIG files
    dept_gdf = pd.read_csv(file_path, low_memory=False)  # for csv files
    logging.info("*"*100)
    logging.info(f"\nDept. {dept_nb} \nopened in {(time() - start):.4f}s")
    return dept_nb, dept_gdf


def open_gdfs(file_paths, processes=3):
    return dict(Pool(processes).map(read_dept_file, file_paths))


def split_per_archetype(output_path, tuple_dep):
    dept_nb = tuple_dep[0]
    dep_gdf = tuple_dep[1]
    archs = list(filter(None, list(dep_gdf.archetype.unique())))
    for arch in archs:
        dep_arch = dep_gdf[dep_gdf.archetype == arch]
        dep_arch.to_csv(output_path / f"{arch}-dep{dept_nb}-len{len(dep_arch)}.csv")


def pool_save_archetypes(gdfs, output_path, processes=3):
    return Pool(processes).map(partial(split_per_archetype, output_path), gdfs.items())
