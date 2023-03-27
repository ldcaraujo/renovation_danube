import pandas as pd
from time import time
import logging
import traceback

from access_files import GPD_SORTING_OUTPUT_PATH

# # charge archetypes from dept archs outputs
# from select_archetypes_from_depts.analysis_archs_depts_vs_danube import (
#     depts_archetypes_names,
# )

# charge archetypes from dept archs outputs
from preprocessing_data.select_archetypes_from_depts.analysis_archs_depts_vs_catalogue import (
    depts_archetypes_names,
)

TEST = False

if TEST:
    QGIS_OUTPUT_NEW_TER, GPD_SORTING_OUTPUT_PATH = (
        path / "test" for path in (QGIS_OUTPUT_NEW_TER, GPD_SORTING_OUTPUT_PATH)
    )


# define log file
level    = logging.INFO
format   = '  %(message)s'
handlers = [logging.FileHandler('AppLog_concat_archetypes_all_depts.log'), logging.StreamHandler()]
logging.basicConfig(level = level, format = format, handlers = handlers)


archs_depts_set, archs_depts, files_archs_depts = depts_archetypes_names()

if TEST:
    archs_depts_set= ["P1-P-HABITAT-FRANCE_PIERRE_CALCAIRE_TUILE"]


different_archs_grouped = {}
i = 0
for arch_in_set in sorted(list(archs_depts_set)):
    i += 1
    all_same_archs = []
    len_all_same_archs = []
    for arch in files_archs_depts:
        if arch_in_set + "-" in arch:
            all_same_archs.append(arch)
            len_arch = int(arch.split("-")[-1][3:-4])
            len_all_same_archs.append(len_arch)
    logging.info(f"n {i} - arch {arch_in_set} \ntotal len this arch: {sum(len_all_same_archs)} \n {len_all_same_archs}")
    for e in all_same_archs:
        logging.info(e)
    logging.info("\n")
    different_archs_grouped[arch_in_set] = [sum(len_all_same_archs), all_same_archs]


different_archs_grouped_ordered = {
    k: different_archs_grouped[k]
    for k in sorted(
        different_archs_grouped, key=different_archs_grouped.get, reverse=True
    )
}

def concat_save_archetypes(list_paths, arch_name):
    logging.info(f"concat:  {arch_name}")
    start_time = time()
    list_dfs = []
    for file in list_paths:
        path = GPD_SORTING_OUTPUT_PATH / "archetypes_per_dept_tables" / file
        one_df = pd.read_csv(path)
        list_dfs.append(one_df)
    concated_arch_df = pd.concat(list_dfs)

    # correct the order of the columns
    concated_arch_df = concated_arch_df.loc[:, ~concated_arch_df.columns.str.contains('^Unnamed')]
    middle_cols = concated_arch_df.columns.drop(["archetype", "period", "typology", 'usage', 'territory',
                                                 'territory_P1', 'territory_P2_P7',
                                                 'typologie_mapuce', 'typologie_mapuce_sigle', 'typologie_transf_BDNB',
                                                 'count_usage_niv_1', 'count_usage_niv_2', 'count_usage_niv_3',
                                                 "geometry_BDNB"
                                                 ])
    rearranged_cols_order = ["archetype", "period", "typology", 'usage', 'territory',
                             'territory_P1', 'territory_P2_P7',
                             'typologie_mapuce', 'typologie_mapuce_sigle', 'typologie_transf_BDNB',
                             'count_usage_niv_1', 'count_usage_niv_2', 'count_usage_niv_3'
                             ] + list(middle_cols) + ["geometry_BDNB"]
    concated_arch_df = concated_arch_df[rearranged_cols_order]
    # rename cols in French
    cols_rename_french = {
        "archetype":"archétype",
        "period" : "période",
        "typology" : "typologie",
        'territory' : "territoire",
        'territory_P1' : "carte_territoire_P1",
        'territory_P2_P7' : "carte_territoire_P2_P7",
        'typologie_transf_BDNB' : "typologie_méthode_bdnb",
        'count_usage_niv_1' : "quant_usage_bdnb_n1",
        'count_usage_niv_2' : "quant_usage_bdnb_n2",
        'count_usage_niv_3' : "quant_usage_bdnb_n3"
    }
    concated_arch_df.rename(columns=cols_rename_french, inplace=True)

    # save df
    save_name = "len_" + str(len(concated_arch_df)) + "-" + arch_name + ".csv"
    logging.info(f"saving: {save_name}")
    path_save = GPD_SORTING_OUTPUT_PATH / "concat_archetypes" / "all_first_level_concat" / save_name
    concated_arch_df.to_csv(str(path_save), index=False)
    logging.info(f"finished saving in{(time() - start_time):.4f}s\n")

    # faire un print dpe pas null, ou une stat par archetype


start_time = time()
for (k, v) in different_archs_grouped_ordered.items():
    try:
        concat_save_archetypes(v[1], k)
    except Exception as e:
        logging.info("#"*150)
        logging.info("#"*150)
        logging.info("#"*150)
        if hasattr(e, 'message'):
            logging.info("Problem to concat this arch.\nError:")
            logging.info(e.message)
            logging.info(traceback.format_exc())

        else:
            logging.info("Problem to concat this arch.\nError:")
            logging.info(e)
            logging.info(traceback.format_exc())

logging.info(f"concat_save_archetypes executed in{(time() - start_time):.4f}s")
# 56 min
# 36 min
logging.shutdown()

