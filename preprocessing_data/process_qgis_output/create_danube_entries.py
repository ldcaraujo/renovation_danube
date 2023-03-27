from multiprocessing import Pool
from time import time

import numpy as np
import logging

from access_files import GPD_SORTING_OUTPUT_PATH


# Formatting

# period
def create_period(dep):
    """Transform BDNB 'cerffo2020_annee_construction' into Danube periods."""
    period_relations = {
        "P1": (dep["cerffo2020_annee_construction"] <= 1948),
        "P2": (dep["cerffo2020_annee_construction"] > 1948)
        & (dep["cerffo2020_annee_construction"] <= 1973),
        "P3": (dep["cerffo2020_annee_construction"] > 1973)
        & (dep["cerffo2020_annee_construction"] <= 1981),
        "P4": (dep["cerffo2020_annee_construction"] > 1981)
        & (dep["cerffo2020_annee_construction"] <= 1989),
        "P5": (dep["cerffo2020_annee_construction"] > 1989)
        & (dep["cerffo2020_annee_construction"] <= 2000),
        "P6": (dep["cerffo2020_annee_construction"] > 2000)
        & (dep["cerffo2020_annee_construction"] <= 2012),
        "P7": (dep["cerffo2020_annee_construction"] > 2012),
    }

    period_values = list(period_relations.keys())
    period_conditions = list(period_relations.values())

    dep["period"] = np.select(period_conditions, period_values, default=None)

    # put into first column
    first_column = dep.pop("period")
    dep.insert(0, "period", first_column)


# Territory


def create_territory_1dep(dep):
    dep["territory"] = dep.apply(
        lambda x: (
            None
            if x["period"] is None
            else x["territory_P1"]
            if x["period"] == "P1"
            else x["territory_P2_P7"]
        ),
        axis=1,
    )
    # put into first column
    first_column = dep.pop("territory")
    dep.insert(0, "territory", first_column)


# Usage


def create_usage_1dep(dep):
    """Transform BDNB Usages into Danube Usages.
    All usages in Danube are create with exception of the below:
                                                                    Usages_ignored = [
                                                                    'BATIMENT AGRICOLE',
                                                                    'BATIMENT RELIGIEUX',
                                                                    'CHATEAU',
                                                                    'LOCAL NON CHAUFFE']"""
    relations = {
        "BATIMENT INDUSTRIEL": (dep["cerffo2020_usage_niveau_2_txt"] == "Industrie")
        | (
            dep["cerffo2020_usage_niveau_3_txt"]
            == "Etablissement industriel autre que carrière"
        ),
        "SERRE AGRICOLE": (dep["cerffo2020_usage_niveau_3_txt"] == "Serre"),
        "BATIMENT D ENSEIGNEMENT": (
            dep["cerffo2020_usage_niveau_2_txt"] == "Enseignement"
        ),
        "BATIMENT DE SANTE": (
            dep["cerffo2020_usage_niveau_2_txt"] == "Centre de santé"
        ),
        "COMMERCE": (dep["cerffo2020_usage_niveau_2_txt"] == "Commerce"),
        "HABITAT": (dep["cerffo2020_usage_niveau_1_txt"] == "Résidentiel individuel")
        | (
            dep["cerffo2020_usage_niveau_1_txt"] == "Résidentiel collectif"
        )  # not described in BDNB methodology
        | (dep["cerffo2020_usage_niveau_3_txt"] == "Maison exceptionnelle"),
        "TERTIAIRE": (dep["cerffo2020_usage_niveau_2_txt"] == "Bureau")
        | (dep["cerffo2020_usage_niveau_2_txt"] == "Hôtel"),
        "BATIMENT SPORTIF": (dep["cerffo2020_usage_niveau_3_txt"] == "Espace sportif")
        | (dep["cerffo2020_usage_niveau_3_txt"] == "Espace loisir"),
    }

    usages = list(relations.keys())
    conditions = list(relations.values())

    dep["usage"] = np.select(conditions, usages, default=None)

    # put into first column
    first_column = dep.pop("usage")
    dep.insert(0, "usage", first_column)


# ### Typology

# #### Mapuce


# Should I take out the local? Or should I pass it to final typology? take it out
def create_typo_mapuce_S_1dep(dep):

    conditions_mapuce = [
        (dep["typologie_mapuce"] == "pcif")
        | (dep["typologie_mapuce"] == "pcio")
        | (dep["typologie_mapuce"] == "pd")
        | (dep["typologie_mapuce"] == "psc"),
        (dep["typologie_mapuce"] == "icif") | (dep["typologie_mapuce"] == "icio") | (dep["typologie_mapuce"] == "id"),
        (dep["typologie_mapuce"] == "ba"),
        (dep["typologie_mapuce"] == "bgh"),
        # (dep['typologie_mapuce'] == 'local')
    ]

    # values_mapuce = ['P', 'I', 'BA', 'IGH', "local"]
    values_mapuce = ["P", "I", "BA", "IGH"]

    dep["typologie_mapuce_sigle"] = np.select(conditions_mapuce, values_mapuce, default=None)


# #### BDNB


def create_typo_bdnb_S_1dep(dep):
    conditions_typo_bdnb = [
        (dep["cerffo2020_usage_niveau_2_txt"] == "Maison individuelle")
        | (dep["cerffo2020_usage_niveau_2_txt"] == "Maisons groupées")
        | (dep["cerffo2020_usage_niveau_2_txt"] == "Maison exceptionnelle"),
        (dep["cerffo2020_usage_niveau_2_txt"] == "Immeuble collectif")
        | (dep["cerffo2020_usage_niveau_2_txt"] == "Résidentiel collectif autre")
        | (dep["cerffo2020_usage_niveau_2_txt"] == "Hôtel")
        | (dep["cerffo2020_usage_niveau_2_txt"] == "Bureau")
        | (dep["cerffo2020_usage_niveau_2_txt"] == "Centre de santé")
        | (dep["cerffo2020_usage_niveau_2_txt"] == "Enseignement")
        | (
            dep["cerffo2020_usage_niveau_3_txt"]
            == "Magasin sans accès à la rue avec surface < 400m²"
        )
        | (
            dep["cerffo2020_usage_niveau_3_txt"]
            == "Magasin de centre commercial avec surface < 400m²"
        )
        | (
            dep["cerffo2020_usage_niveau_3_txt"]
            == "Magasin sur rue avec surface < 400m²"
        ),
        (dep["cerffo2020_usage_niveau_2_txt"] == "Industrie")
        | (
            dep["cerffo2020_usage_niveau_3_txt"]
            == "Magasin grande surface (entre 400m² et 2499m²)"
        )
        | (
            dep["cerffo2020_usage_niveau_3_txt"]
            == "Magasin très grande surface (> 2500m²)"
        )
        | (dep["cerffo2020_usage_niveau_3_txt"] == "Serre")
        | (dep["cerffo2020_usage_niveau_3_txt"] == "Espace sportif"),
        (dep["igntop202103_bat_hauteur"] >= 39),
    ]

    # create a list of the values we want to assign for each condition
    values_typo_bdnb = ["P", "I", "BA", "IGH"]

    dep["typologie_transf_BDNB"] = np.select(conditions_typo_bdnb, values_typo_bdnb, default=None)


# ### Combine both typos


def combine_typo_mapuce_bdnb(dep):
    dep["typology"] = np.where(
        dep.typologie_mapuce_sigle.notnull(),
        dep.typologie_mapuce_sigle,
        (np.where(dep.typologie_mapuce_sigle.isnull(), dep.typologie_transf_BDNB, None)),
    )
    #     dep.fillna(np.nan)

    # put into first column
    first_column = dep.pop("typology")
    dep.insert(0, "typology", first_column)


def create_archetype(df):
    cond_have_all_entries = (
        (df["period"].notnull())
        & (df["territory"].notnull())
        & (df["usage"].notnull())
        & (df["typology"].notnull())
    )

    df["archetype"] = np.where(
        cond_have_all_entries,
        (
            df["period"].astype(str)
            + "-"
            + df["typology"].astype(str)
            + "-"
            + df["usage"].astype(str)
            + "-"
            + df["territory"].astype(str)
        ),
        None,
    )


# ### Create columns to count the number of usages in each level for checking multiple usage
def create_col_num_multiple_usage(dep):
    def count_multiple_usage(col):
        return dep[col].str.split(",", expand=False).map(len)

    dep["count_usage_niv_1"] = count_multiple_usage("cerffo2020_l_usage_niveau_1_txt")
    dep["count_usage_niv_2"] = count_multiple_usage("cerffo2020_l_usage_niveau_2_txt")
    dep["count_usage_niv_3"] = count_multiple_usage("cerffo2020_l_usage_niveau_3_txt")


# # Create all entries


def create_danube_entries(tuple_dep):
    dept_nb = tuple_dep[0]
    dep = tuple_dep[1]

    start = time()
    create_period(dep)
    create_territory_1dep(dep)
    create_usage_1dep(dep)
    create_typo_mapuce_S_1dep(dep)
    create_typo_bdnb_S_1dep(dep)
    combine_typo_mapuce_bdnb(dep)
    create_archetype(dep)
    create_col_num_multiple_usage(dep)
    logging.info(f"create_danube_entries of {dept_nb} executed in {(time()-start):.2f}s")
    return dept_nb, dep


def pool_create_danube_entries(gdfs, processes=3):
    return dict(Pool(processes).map(create_danube_entries, gdfs.items()))
