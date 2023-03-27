import shutil
from pathlib import Path
import logging
import traceback
from time import time
from os import listdir
import pandas as pd
import dask.dataframe as dd

# from access_files import GPD_SORTING_OUTPUT_PATH

# source_folder = GPD_SORTING_OUTPUT_PATH / "concat_archetypes" / "final_selection" / "final_after_assemble"
# folder_save = GPD_SORTING_OUTPUT_PATH / "assembled_by_roof"
work_folder = Path(r"U:\Work")
source_folder = work_folder / "final_selection" / "final_after_assemble"
folder_save = work_folder / "assembled_by_roof"

# define log file
level    = logging.INFO
format   = '  %(message)s'
handlers = [logging.FileHandler('AppLog_join_roof.log'), logging.StreamHandler()]
logging.basicConfig(level = level, format = format, handlers = handlers)



all_studied = ["-".join(el.split("-")[1:])[:-4] for el in listdir(source_folder)]
roots = []
for e in all_studied:
    if e.endswith("FRANCE"):
        roots.append(e + "-nati")
    else:
        without_roof = "_".join(e.split("_")[:-1])
        # print(without_roof)
        roots.append(without_roof + "-toit" )

# print(len(roots))
roots = set(roots)
# print(len(roots))

different_roots_grouped = {}
i = 0
for root in sorted(list(roots)):
    i += 1
    all_same_root = []
    len_all_same_root = []
    for arch in listdir(source_folder):
        if root[:-5] in arch:

            all_same_root.append(arch)
            len_arch = int(arch.split("-")[0][4:])
            len_all_same_root.append(len_arch)
    # print(f"n {i} - root {root} \ntotal len this root: {sum(len_all_same_root)} \n {len_all_same_root} ")
    different_roots_grouped[root] = [sum(len_all_same_root), all_same_root]

different_roots_grouped_ordered = {
    k: different_roots_grouped[k]
    for k in sorted(
        different_roots_grouped, key=different_roots_grouped.get, reverse=False
    )
}

for k,v in different_roots_grouped_ordered.items():
    print("\n",k)
    for e in v:
        print(e)




def concat_save_roof(list_paths, root_name, folder_save):

    logging.info(f"concat:  {root_name}")
    start_time = time()
    list_dfs = []
    for file in list_paths:
        path = source_folder / file
        one_df = pd.read_csv(path)
        list_dfs.append(one_df)
    concated_arch_df = pd.concat(list_dfs)
    save_name = "len_" + str(len(concated_arch_df)) + "-" + root_name + ".csv"
    path_save = folder_save  / save_name

    # save df
    logging.info(f"saving: {save_name}")
    concated_arch_df.to_csv(str(path_save), index=False)
    logging.info(f"finished saving in{(time() - start_time):.4f}s\n")

    # faire un print dpe pas null, ou une stat par archetype

def copy_paste_one_df(values, k, source_folder, folder_save):
    if k.endswith("nati"):
        save_name = values[0][:-4] + "-nati.csv"
    else:
        save_name = values[0][:-4] + "-uniq.csv"
    source = source_folder / values[0]
    destination = folder_save / save_name
    shutil.copy(source, destination)

    logging.info(k)
    logging.info(values)
    logging.info("save_name")
    logging.info(save_name)


start_time = time()
for (k, v) in different_roots_grouped_ordered.items():
    if len(v[1]) == 1:
        logging.info("\nJust one df -> copy and paste it")
        copy_paste_one_df(v[1], k, source_folder, folder_save)

    else:
        logging.info("\nMore than one df -> concatenate dfs and save")
        logging.info(v[1])
        try:
            concat_save_roof(v[1], k, folder_save)
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

logging.info(f"concat_save_roof executed in{(time() - start_time):.4f}s")
logging.shutdown()


