import shutil
from pathlib import Path
import logging
import traceback
from time import time
from os import listdir
import pandas as pd

# from access_files import GPD_SORTING_OUTPUT_PATH

def define_log_file(log_name):
    level = logging.INFO
    format = '  %(message)s'
    handlers = [logging.FileHandler(log_name), logging.StreamHandler()]
    logging.basicConfig(level=level, format=format, handlers=handlers)


def define_dict_rock_walls(source_folder):
    rock_walls = []
    for e in listdir(source_folder):
        if "PIERRE" in e:
            rock_walls.append("-".join(e.split("-")[1:-2]))
    logging.info(len(rock_walls))
    for el in rock_walls:
        logging.info(el)

    logging.info("#"*100)
    rock_walls = set(rock_walls)
    logging.info(len(rock_walls))
    for el in rock_walls:
        logging.info(el)

    different_rock_walls_grouped = {}
    i = 0
    for r_wall  in sorted(list(rock_walls)):
        i += 1
        all_same_r_wall = []
        len_all_same_r_wall= []
        for arch in listdir(source_folder):
            if r_wall + "-FRANCE_PIERRE" in arch:
                all_same_r_wall.append(arch)
                len_arch = int(arch.split("-")[0][4:])
                len_all_same_r_wall.append(len_arch)
        different_rock_walls_grouped[r_wall] = [sum(len_all_same_r_wall), all_same_r_wall]

    return different_rock_walls_grouped


def concat_save_rock_wall(list_paths, rock_name, folder_save):
    logging.info(f"concat:  {rock_name}")
    start_time = time()
    list_dfs = []
    for file in list_paths:
        path = source_folder / file
        one_df = pd.read_csv(path)
        list_dfs.append(one_df)
    concated_arch_df = pd.concat(list_dfs)
    save_name = "len_" + str(len(concated_arch_df)) + "-" + rock_name + "-FRANCE_PIERRE-rock.csv"
    path_save = folder_save  / save_name
    # save df
    logging.info(f"saving: {save_name}")
    concated_arch_df.to_csv(str(path_save), index=False)
    logging.info(f"finished saving in{(time() - start_time):.4f}s\n")


def copy_paste_one_df(values, k, source_folder, folder_save):
    save_name = values[0][:-8] + "-rock.csv"
    source = source_folder / values[0]
    destination = folder_save / save_name
    shutil.copy(source, destination)

    logging.info(k)
    logging.info(values)
    logging.info("save_name")
    logging.info(save_name)


def assemble_rock_walls(different_rock_walls_grouped, source_folder, folder_save):
    start_time = time()
    for (k, v) in different_rock_walls_grouped.items():
        if len(v[1]) == 1:
            logging.info("\nJust one df -> copy and paste it")
            copy_paste_one_df(v[1], k, source_folder, folder_save)

        else:
            logging.info("\nMore than one df -> concatenate dfs and save")
            logging.info(v[1])
            try:
                concat_save_rock_wall(v[1], k, folder_save)
            except Exception as e:
                logging.info("#"*150)
                logging.info("#"*150)
                logging.info("#"*150)
                if hasattr(e, 'message'):
                    logging.info("Problem to concat this root.\nError:")
                    logging.info(e.message)
                    logging.info(traceback.format_exc())
                else:
                    logging.info("Problem to concat this root.\nError:")
                    logging.info(e)
                    logging.info(traceback.format_exc())
    logging.info(f"concat_save_rock_wall executed in{(time() - start_time):.4f}s")


def copy_paste_dfs_not_rock(different_rock_walls_grouped, source_folder, folder_save):

    source_csvs_rock = [e[1] for e in different_rock_walls_grouped.values()]
    source_csvs_rock = [item for sublist in source_csvs_rock for item in sublist]
    for e in listdir(source_folder):
        if e in source_csvs_rock:
            pass
        else:
            source = source_folder / e
            destination = folder_save / e
            shutil.copy(source, destination)


if __name__ == "__main__":

    # source_folder = GPD_SORTING_OUTPUT_PATH / "concat_archetypes" / "final_selection" / "final_after_assemble"
    # folder_save = GPD_SORTING_OUTPUT_PATH / "assembled_by_roof"
    work_folder = Path(r"U:\Work")
    source_folder = work_folder / "assembled_by_roof"
    folder_save = work_folder / "assembled_by_roof_and_rock_wall"

    define_log_file("AppLog_join_rock_wall.log")

    different_rock_walls_grouped = define_dict_rock_walls(source_folder)
    assemble_rock_walls(different_rock_walls_grouped, source_folder, folder_save)
    copy_paste_dfs_not_rock(different_rock_walls_grouped, source_folder, folder_save)

    logging.shutdown()
