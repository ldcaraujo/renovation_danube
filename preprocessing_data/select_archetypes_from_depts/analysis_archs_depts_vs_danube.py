from os import listdir

import pandas as pd
from time import time

# charge Danube data base
from access_files import DATA_PATH, GPD_SORTING_OUTPUT_PATH

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
# I modified manually the Danube database double entry, while waiting officially do it with Serge
# so then, there is no double entry and list and set have the same size
print(f"danube_archs set len of {len(set(archs_danube))}")

# charge archetypes from dept archs outputs
def depts_archetypes_names():
    arch_per_dept_paths = GPD_SORTING_OUTPUT_PATH / "archetypes_per_dept_tables"
    files_archs_depts = listdir(arch_per_dept_paths)
    print(files_archs_depts[:2])
    archs_depts = [
        "-".join(file_name.split("-")[:4]) for file_name in files_archs_depts
    ]
    print(f"archs_depts len of {len(archs_depts)}")
    print(archs_depts[:2])
    archs_depts_set = set(archs_depts)
    print(f"archs_depts_set len of {len(archs_depts_set)}\n")

    return archs_depts_set, archs_depts, files_archs_depts


archs_depts_set, archs_depts, files_archs_depts = depts_archetypes_names()

# check territories compatibility
print("*" * 50)
territ_danu_p1 = danube[danube["PERIODE"] == "P1"]["TERRITOIRE"].unique()
print("territ_danu_p1 \n", len(territ_danu_p1))
for e in territ_danu_p1:
    print(e)
territ_depts_p1 = {arch.split("-")[-1] for arch in archs_depts if "P1" in arch}
print("\nterrit_depts_p1 \n", len(territ_depts_p1))
for e in territ_depts_p1:
    print(e)
print(
    "territ_depts_p1 = territ_danu_p1 ",
    sorted(territ_depts_p1) == sorted(territ_danu_p1),
)
ter_dan_not_dept = sorted(list(set(territ_danu_p1) - set(territ_depts_p1)))
ter_dept_not_dan = sorted(list(set(territ_depts_p1) - set(territ_danu_p1)))

print("\nterrit_danu_p1 - territ_depts_p1 , len", len(ter_dan_not_dept))
for e in ter_dan_not_dept:
    print(e)
print("\nterrit_depts_p1 - territ_danu_p1 , length", len(ter_dept_not_dan))
for e in ter_dept_not_dan:
    print(e)

print(
    "\nall different territories P1 has length ",
    len(list(set(territ_danu_p1).symmetric_difference(set(territ_depts_p1)))),
    "\n ",
)

print("#" * 50)
archs_just_danube = []
for ter in ter_dan_not_dept[1:]:
    arch_just_dan = danube[danube["TERRITOIRE"] == ter]["archetype"]
    archs_just_danube.append(arch_just_dan)
    print("\nterritory just Danube", ter, "archetypes")
    for arch in arch_just_dan:
        print(arch)
print("#" * 50)

ter_pierre_and_ardoise = [
    ter for ter in territ_danu_p1 if ("PIERRE" in ter) and ("ARDOISE" in ter)
]
print("ter_pierre_and_ardoise :", ter_pierre_and_ardoise)

files_ter_dept_not_danu = []
for ter_just_dept in ter_dept_not_dan:
    files_1dept_not_dan = [file for file in files_archs_depts if ter_just_dept in file]
    print(
        "\nter_just_dept ",
        ter_just_dept,
        " len ",
        len(files_1dept_not_dan),
        ", associated files:",
    )
    for file in files_1dept_not_dan:
        print(file)
    files_ter_dept_not_danu.append(files_1dept_not_dan)
ter_dept_not_dan_joined_archs = [
    element for sublist in files_ter_dept_not_danu for element in sublist
]
len_files_ter_dept_not_danu = [
    int(ele.split("-")[-1][3:-4]) for ele in ter_dept_not_dan_joined_archs
]
print("len_files_ter_dept_not_danu: ", sum(len_files_ter_dept_not_danu))


# there is a problem between the territories defined in the QGIS file from mapuce territories and Danube definitions.
# we need to find the correspondence between them to be able to join the archetypes in the whole French territory.
territ_danu_p2plus = danube[danube["PERIODE"] != "P1"]["TERRITOIRE"].unique()
print("territ_danu_p2plus \n", territ_danu_p2plus)

territ_depts_p2plus = {arch.split("-")[-1] for arch in archs_depts if "P1" not in arch}
print("territ_depts_p2plus \n", territ_depts_p2plus, "\n")

print(
    f"{(set(territ_danu_p2plus) - territ_depts_p2plus)} are not in the dept territories, but are in Danube"
)
print("*" * 50)
# check how many danube archetypes are divided into
# having territories FRANCE_BRIQUE_TUILE in Dabube is a problem,
# cause this was not defined on the initial shapefile with the territories for joining in QGIS
# how to solve this problem ?
danube_groupedby_ter_per = danube.groupby(["TERRITOIRE", "PERIODE"]).count()[
    "archetype"
]
print(danube_groupedby_ter_per)

# check the cases in Danube that are not in depts
# FRANCE_BRIQUE_TUILE
archs_danu_territ_fbt = {arch for arch in archs_danube if "FRANCE_BRIQUE_TUILE" in arch}
print(f"len archs_danu_territ_fbt is {len(archs_danu_territ_fbt)}")
for e in sorted(archs_danu_territ_fbt):
    print(e)

# general FRANCE
archs_danu_territ_all_france = {arch for arch in archs_danube if "FRANCE_" not in arch}
print(f"len archs_danu_territ_all_france is {len(archs_danu_territ_all_france)}")
archs_danu_territ_all_france_3entries = [
    arch[:-7] for arch in archs_danu_territ_all_france
]
check_unicity_all_france = []
p1_p7_1france = []
p1_multiple_france = []
p2plus_2france = []
p2plus_3france = []

i = 1
j = 1
for arch_france in sorted(archs_danu_territ_all_france):
    list_one_arch_france = [arch for arch in archs_danube if arch_france in arch]
    # print(i)
    # print(arch_france)
    # print(list_one_arch_france)
    # print("*" * 50)
    i += 1
    if len(list_one_arch_france) == 1:
        p1_p7_1france.append(list_one_arch_france)
    else:
        print(arch_france, len(list_one_arch_france))
        print(list_one_arch_france)
        print("*" * 50)

        if not arch_france.startswith("P1"):
            if len(list_one_arch_france) == 2:
                p2plus_2france.append(list_one_arch_france)
            else:
                p2plus_3france.append(list_one_arch_france)
                j += 1
        else:
            p1_multiple_france.append(list_one_arch_france)

print(j)

# if len(list_one_arch_france) > 1:
#     list_one_arch_france.remove(arch_france)
#     check_unicity_all_france += list_one_arch_france
print(
    f"check_unicity_all_france len is of {len(check_unicity_all_france)} "
    f"- all these elements are present even though there is already the territory france defined"
)

print(f"\n p1_p7_1france len {len(p1_p7_1france)}")
for e in sorted(p1_p7_1france):
    print(e)
print(f"\n p2plus_2france len {len(p2plus_2france)}")
for e in sorted(p2plus_2france):
    print(e)
print(f"\n p2plus_3france len {len(p2plus_3france)}")
for e in sorted(p2plus_3france):
    print(e)
print(f"\n p1_multiple_france len {len(p1_multiple_france)}")
for e in sorted(p1_multiple_france):
    print(len(e), e)
# in many cases there are territories in Danube that are defined as France, but there is another smaller level for it.
# this can be a problem to define the limits of the archetypes, since their territorial limit is not clearly defined.
# what exactly means territory France? In the QGIS territories there was no France brique tuile (neither France of course).
# The dificulty is in defining the territorry for those cases
# France is not always for the whole country, but the rest of the country
# if there is another archetype of the same first entries
# France brique tuile is probably in the territory of france tuile, but where exactly?

# In the following cases for the period P2+ there is 3 defined territories, but one of them is France.
# If FrAr, FrTu and FrBrTu are exhaustive categories, France should not be used in case there are 3 description.
# It is not a consistent nomenclature. France should be used if it corresponds to the whole territory
# or to the ensemble of at least 2 territories.
# Ex: 20 P2-I-HABITAT-FRANCE
# ['P2-I-HABITAT-FRANCE_ARDOISE', 'P2-I-HABITAT-FRANCE_TUILE', 'P2-I-HABITAT-FRANCE']
# Shouldn't it be FrBrTu instead of France ?
# Ex: 23 P2-P-HABITAT-FRANCE
# ['P2-P-HABITAT-FRANCE_ARDOISE', 'P2-P-HABITAT-FRANCE_BRIQUE_TUILE', 'P2-P-HABITAT-FRANCE']
# Shouldn't it be FrTu instead of France ? etc...


concat_archs_folder = GPD_SORTING_OUTPUT_PATH / "archetypes_concatenated"
concat_archs_files = listdir(concat_archs_folder)
print(concat_archs_files[:2])


test = "P3-I-TERTIAIRE-FRANCE"
p1_p7_1france = [element for sublist in p1_p7_1france for element in sublist]

concat_need_1france = []

for france1 in p1_p7_1france:
    concat_need = [arch for arch in concat_archs_files if france1 in arch]
    print(f"\n All france1 - {france1} has {len(concat_need)} archetypes to concat:")
    for e in concat_need:
        print(e)
    concat_need_1france.append(concat_need)

concat_need_1france_ = [e for e in concat_need_1france if len(e) > 1]
a = 1
