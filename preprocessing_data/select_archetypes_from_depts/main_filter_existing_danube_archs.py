import shutil
from os import listdir
import pandas as pd

from preprocessing_data.select_archetypes_from_depts.analysis_archs_depts_vs_catalogue import (
    provide_danube_archs_from_catalogue, define_multiple_territories_and_france)
from access_files import GPD_SORTING_OUTPUT_PATH


NOT_DIR_DAN_PATH = GPD_SORTING_OUTPUT_PATH / "concat_archetypes" / "by_category" / "not_directly_in_danube"

def filter_archs_directly_in_danube(folder, dan_exist):
    i=0
    for file in listdir(folder):
        i+=1
        print(i)
        print("file: ", file)

        arch_bdnb = "-".join(file.split("-")[1:])[:-4]
        print(arch_bdnb)

        source = folder / file
        if arch_bdnb in dan_exist:
            if arch_bdnb.endswith("ZINC"):
                print("#"*100,"Attention ZINC\n\n")
            print("YES - the archetype is directly described in danube")
            destination = GPD_SORTING_OUTPUT_PATH / "concat_archetypes" / "by_category" / "archs_in_first_level_danube"
            shutil.copy(source, destination)
        # else:
        #     print("NO - the archetype is not directly described in danube")

        # Copy the content of source to destination


def select_possible_danube_to_be_analysed(folder, archs_danube, to_print=True):
    entries_3_bdnb = {"-".join(file.split("-")[1:-1])   for file in listdir(folder)}
    not_representative_territory_danube = ["FRANCE_BOIS_ARDOISE",
                                           "FRANCE_PIERRE_GALET_TUILE",
                                           "FRANCE_PIERRE_VOLCANIQUE_ARDOISE"]
    dan_ter_not_representative = []
    dan_not_present_in_bdnb = []
    dan_existent = []
    for arch in archs_danube:
        if any(ter in arch for ter in not_representative_territory_danube):
            dan_ter_not_representative.append(arch)
        else:
            if any(entries3 in arch for entries3 in entries_3_bdnb):
                dan_existent.append(arch)
            else:
                dan_not_present_in_bdnb.append(arch)

    dan_not_analysed = dan_ter_not_representative + dan_not_present_in_bdnb
    if to_print:
        print(f"\nExistent danube archetypes in BDNB: {len(dan_existent)}")
        print(f"\nNon analysed danube archetypes: {len(dan_not_analysed)}")

        print(f"\nArchetypes with a not representative territory in danube: {len(dan_ter_not_representative)}")
        for e in dan_ter_not_representative:
            print(e)

        print(f"\nArchetypes danube without correspondence in BDNB: {len(dan_not_present_in_bdnb)}")
        for e in dan_not_present_in_bdnb:
            print(e)

    return dan_existent, dan_not_analysed


def concat_unique_france(unique_france, to_concat_archs_folder):
    concat_archs_files = listdir(to_concat_archs_folder)
    concat_need_1france = []
    for france1 in unique_france:
        concat_need = [arch for arch in concat_archs_files if france1 in arch]
        concat_need_1france.append(concat_need)

        for file in [item for sublist in concat_need_1france for item in sublist]:
            source_france_unique = to_concat_archs_folder / file
            destination_france_unique = NOT_DIR_DAN_PATH / "france_unique" / "teritorry_france_unique_NOT_reassembled"
            shutil.copy(source_france_unique, destination_france_unique)

        print(f"\n All france1 - {france1} has {len(concat_need)} archetypes to concat:")
        list_dfs = []
        for csv in concat_need:
            print(csv)
            path_csv = destination_france_unique / csv
            df_csv = pd.read_csv(path_csv)
            list_dfs.append(df_csv)
        assembled_one_france_unique = pd.concat(list_dfs)
        # assembled_one_france_unique.drop(["Unnamed: 0", "Unnamed: 0.1"], axis=1, inplace=True)
        assembled_one_france_unique["archétype"] = france1
        assembled_one_france_unique["territoire"] = "FRANCE"
        path_save_assembled_france_unique = (NOT_DIR_DAN_PATH / "france_unique" /
                                             "teritorry_france_unique_reassembled" /
                                             f"len_{len(assembled_one_france_unique)}-{france1}.csv")
        assembled_one_france_unique.to_csv(path_save_assembled_france_unique, index=False)
    return concat_need_1france


def solve_case_pierre_ardoise(dan_exist, folder_first_level):
    pierre_ardoise_archs_danube = [elem for elem in dan_exist if elem.endswith("FRANCE_PIERRE_ARDOISE")]
    print(pierre_ardoise_archs_danube)

    all_ter_same_3_entries_danube = [elem for elem in dan_exist if elem.startswith("P1-I-BATIMENT DE SANTE")]
    print(all_ter_same_3_entries_danube)
    # it divides all the pierre_ardoise in one group and the rest in the group france

    all_ter_same_3_entries_bdnb = [elem for elem in listdir(folder_first_level) if "P1-I-BATIMENT DE SANTE" in elem]
    print(len(all_ter_same_3_entries_bdnb))
    print(all_ter_same_3_entries_bdnb)

    group_france = []
    group_pierre_ardoise = []
    for ele in all_ter_same_3_entries_bdnb:
        print("\n",ele)
        # if ele.endswith("ARDOISE.csv"):
        #     if "PIERRE" in ele:
        if ("ARDOISE" in ele) and ("PIERRE" in ele):
            group_pierre_ardoise.append(ele)
        else:
            group_france.append(ele)

    print(len(group_pierre_ardoise))
    print(group_pierre_ardoise)

    print(len(group_france))
    print(group_france)

    def open_list_of_csvs_concat(to_concat_list, folder_source, folder_to_save, name, ter):
        to_concat_dfs = []
        for csv in to_concat_list:
            path_csv = folder_source / csv
            df = pd.read_csv(path_csv)
            to_concat_dfs.append(df)
        df_all = pd.concat(to_concat_dfs)
        df_all["archétype"] = name
        df_all["territoire"] = ter
        # name = "-".join(csv.split("-")[1:])
        path_to_save = folder_to_save / f"len_{len(df_all)}-{name}.csv"
        df_all.to_csv(path_to_save, index=False)

    folder_save_pierre = NOT_DIR_DAN_PATH / "pierre_ardoise"
    name_save_piar = "P1-I-BATIMENT DE SANTE-FRANCE_PIERRE_ARDOISE"
    ter_pierard = "FRANCE_PIERRE_ARDOISE"
    open_list_of_csvs_concat(group_pierre_ardoise, folder_first_level, folder_save_pierre, name_save_piar, ter_pierard)

    folder_save_france = NOT_DIR_DAN_PATH / "france_multiple_but_not_all"
    name_save_france = "P1-I-BATIMENT DE SANTE-FRANCE"
    ter_fr = "FRANCE"
    open_list_of_csvs_concat(group_france, folder_first_level, folder_save_france, name_save_france, ter_fr)


def check_other_ter_france_p1_to_concat(p1_multiple_france, dan_exist):
    # check which archetypes still need to concat for territory france with multiple, but not all territories for P1
    p1_multiple_france_short = [[elem for elem in sublist if not elem.endswith("FRANCE") ] for sublist in p1_multiple_france]
    to_concat = []

    print(len(p1_multiple_france_short))
    for e in p1_multiple_france_short:
        if (len(e) < 15):
            print("Check the need to concat the rest into france\n")
            to_concat.append(e)
        print(len(e),e,"\n")

    all_ter_same_3_entries_danube = [elem for elem in dan_exist if elem.startswith("P1-BA-BATIMENT INDUSTRIEL")]
    all_ter_same_3_entries_bdnb = [elem for elem in listdir(folder_first_level) if
                                   "P1-BA-BATIMENT INDUSTRIEL" in elem]
    print("\nall_ter_same_3_entries_danube")
    for e in all_ter_same_3_entries_danube:
        print(e)
    print("\nall_ter_same_3_entries_bdnb")
    for e in all_ter_same_3_entries_bdnb:
        print(e)

    if len(to_concat) > 0:
        print("Attention: need to investigate cases to concatenate in P1")
    else:
        print("No need to concatenate other archetypes in P1")
    print('\nAfter investigation P1: \n '
          'There are too few cases of "P1-BA-BATIMENT INDUSTRIEL" in BDNB, there is no need to consider them')


def check_other_ter_france_p2p7_to_concat(p2plus_multiple_france, to_print=True):
    # check which archetypes still need to concat for territory france with multiple, but not all territories for P2-P7
    print("\nlength p2plus_multiple_france: ",len(p2plus_multiple_france))
    to_concat = []
    for e in p2plus_multiple_france:
        if len(e) != 3:
            if to_print:
                print("Attention - Check the need to assemble further")
                to_concat.append(e)
        else:
            if to_print:
                print("OK - Considering the 2 territories Ardoise and Tuile, the whole country is covered")
        if to_print:
            print(len(e),e,"\n")
    if len(to_concat) > 0:
        print("Attention: need to investigate cases to concatenate in P2-P7")
    else:
        print("No need to concatenate other archetypes in P2-P7")


def filter_zinc_directly_in_danube(folder, dan_exist):
    dan_exist_no_ceiling = {"_".join(e.split("_")[:-1]) for e in dan_exist if not e.endswith("FRANCE")}
    for root in dan_exist_no_ceiling:
        for file in listdir(folder):
            if (root in file) and ("ZINC" in file):
                print("\nYES")
                print(root, file)

                path_csv = folder / file
                df = pd.read_csv(path_csv)
                path_save = GPD_SORTING_OUTPUT_PATH / "concat_archetypes" / "by_category" / "paris_zinc_not_yet_in_danube" / file
                df.to_csv(path_save, index=False)

def copy_non_selected_files():
    folder_first_level = GPD_SORTING_OUTPUT_PATH / "concat_archetypes" / "all_first_level_concat"
    folder_all_selected = GPD_SORTING_OUTPUT_PATH / "concat_archetypes" / "final_selection" \
                          /"all_selected_before_assemble"

    all_files = listdir(folder_first_level)
    all_selected = listdir(folder_all_selected)
    not_selected = set(all_files) - set(all_selected)
    print("len all_files", len(all_files))
    print("len all_selected", len(all_selected))
    print("len not_selected", len(not_selected))

    for csv in not_selected:
        source = folder_first_level / csv
        folder_not_selected = GPD_SORTING_OUTPUT_PATH / "concat_archetypes" / "final_selection" / "all_not_selected_before assemble"
        destination = folder_not_selected / csv
        shutil.copy(source, destination)


def check_number_of_building_selected_or_not():
    folder_first_level = GPD_SORTING_OUTPUT_PATH / "concat_archetypes" / "all_first_level_concat"
    folder_all_selected = GPD_SORTING_OUTPUT_PATH / "concat_archetypes" / "final_selection" \
                          / "all_selected_before_assemble"

    all_files = listdir(folder_first_level)
    all_selected = listdir(folder_all_selected)
    not_selected = set(all_files) - set(all_selected)
    print("len all_files", len(all_files))
    print("len all_selected", len(all_selected))
    print("len not_selected", len(not_selected))

    all_files_lens = [int(file.split("-")[0].split("_")[1]) for file in all_files]
    all_selected_lens = [int(file.split("-")[0].split("_")[1]) for file in all_selected]
    not_selected_lens = [int(file.split("-")[0].split("_")[1]) for file in not_selected]

    print("\nall_files_lens: ",sum(all_files_lens)/1E6, "M")
    print("\nall_selected_lens: ",sum(all_selected_lens)/1E6, "M")
    print("\nnot_selected_lens: ",sum(not_selected_lens)/1E6, "M")
    print("\nall_selected_lens + not_selected_lens: ",(sum(all_selected_lens) + sum(not_selected_lens))/1E6, "M")


def main_file_selection(folder_first_level):
    catalogue, archs_danube = provide_danube_archs_from_catalogue(to_print=False)
    dan_exist, dan_not_analysed = select_possible_danube_to_be_analysed(folder_first_level, archs_danube, to_print=False)
    (archs_danu_territ_all_france,
     unique_france,
     p1_multiple_france,
     p2plus_multiple_france) = define_multiple_territories_and_france(dan_exist, to_print=False)

    # to comment, once done:

    # select the archetypes that have a direct correspondence between danube and the 4 entries
    filter_archs_directly_in_danube(folder_first_level, dan_exist)
    # concat the archetypes that have a unique correspondent territory france
    concat_unique_france(unique_france, folder_first_level)
    # check which territories need to concat for FRANCE_PIERRE_ARDOISE
    solve_case_pierre_ardoise(dan_exist, folder_first_level)
    # check other to concat to france
    check_other_ter_france_p1_to_concat(p1_multiple_france, dan_exist)
    check_other_ter_france_p2p7_to_concat(p2plus_multiple_france, to_print=False)
    # filter the cases with zinc that have a correspondence in the first 3 entries
    filter_zinc_directly_in_danube(folder_first_level, dan_exist)


####################################################################################################################

if __name__ == "__main__":
    folder_first_level = GPD_SORTING_OUTPUT_PATH / "concat_archetypes" / "all_first_level_concat"
    # main_file_selection(folder_first_level)
    # copy_non_selected_files()
    # check_number_of_building_selected_or_not()

    catalogue, archs_danube = provide_danube_archs_from_catalogue(to_print=False)
    print(len(set(archs_danube)))


    folder_archetype = r"C:\Users\ldecarva\Documents\data\working_data\gpd_sorting_output\concat_archetypes\final_selection\final_after_assemble"
    all_studied = ["-".join(el.split("-")[1:])[:-4] for el in listdir(folder_archetype)]

    print("all_studied",len(set(all_studied)))
    not_studied = set(archs_danube)-set(all_studied)
    print("not_studied",len(set(not_studied)))
    print(all_studied)

    {}






