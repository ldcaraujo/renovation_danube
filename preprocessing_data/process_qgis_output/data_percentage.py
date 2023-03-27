"""
Created on Tue Aug 16 14:19:54 2022

@author: laraujo
"""

import pandas as pd
from access_files import GPD_SORTING_OUTPUT_PATH

# Percentage of data


def dept_perc_typology(df):
    def percent_not_null(column_name):
        return df[column_name].notnull().sum() / len(df) * 100

    dict_perc = {
        "all_danube_entries": percent_not_null("archetype"),
        "period": percent_not_null("period"),
        "territory": percent_not_null("territory"),
        "usage": percent_not_null("usage"),
        "typology": percent_not_null("typology"),
        # "mapuce_typo_tot": percent_not_null("TYPO_count"),
        "mapuce_typo_uni": percent_not_null("typologie_mapuce"),
        "mapuce_typo_S": percent_not_null("typologie_mapuce_sigle"),
        "bdnb_usage_tot": percent_not_null("cerffo2020_usage_niveau_3_txt"),
        "bdnb_typo_S": percent_not_null("typologie_transf_BDNB"),  # ajouter usage
    }

    def percent_usage_multiple_indicators():
        usage_mult_ind = {}
        cond_mult = df["count_usage_niv_3"] > 1
        # all multiple usages in bdnb
        usage_mult_ind["bdnb_all_multiple_usage"] = len(df[cond_mult])

        # usage is defined even though there is multiple usages
        usage_mult_ind["mult_usage_OK"] = len(df[(cond_mult) & (df["usage"].notnull())])

        # usage is NOT defined ((because methodology does not follow logic) ou (ignored case)) and there is multiple usage
        usage_mult_ind["mult_usage_KO"] = len(df[(cond_mult) & (df["usage"].isnull())])

        # typology is defined even though there is multiple usages
        usage_mult_ind["mult_typo_OK"] = len(
            df[(cond_mult) & (df["typology"].notnull())]
        )

        # typology is NOT defined ((because methodology does not follow logic) ou (ignored case)) and there is multiple usage
        usage_mult_ind["mult_typo_KO"] = len(
            df[(cond_mult) & (df["typology"].isnull())]
        )
        usage_mult_ind = {k: v / len(df) * 100 for (k, v) in usage_mult_ind.items()}
        return usage_mult_ind

    usage_mult_ind = percent_usage_multiple_indicators()
    dict_perc.update(usage_mult_ind)

    percent_dpe = {
        dpe_indicator: percent_not_null(column_name)
        for dpe_indicator, column_name in {
            "dpe_classe_conso": "adedpe202006_logtype_classe_conso_ener",
            "dpe_mean_conso": "adedpe202006_mean_conso_ener",
            "dpe_baie_vitrage": "adedpe202006_logtype_baie_type_vitrage",
            "dpe_baie_u": "adedpe202006_logtype_baie_u",
            "dpe_mur_mat": "adedpe202006_logtype_mur_mat_ext",
            "dpe_mur_pos_is": "adedpe202006_logtype_mur_pos_isol_ext",
            "dpe_mur_u": "adedpe202006_logtype_mur_u_ext",
            "dpe_pb_mat": "adedpe202006_logtype_pb_mat",
            "dpe_pb_pos_is": "adedpe202006_logtype_pb_pos_isol",
            "dpe_pb_u": "adedpe202006_logtype_pb_u",
            "dpe_ph_mat": "adedpe202006_logtype_ph_mat",
            "dpe_ph_pos_is": "adedpe202006_logtype_ph_pos_isol",
            "dpe_ph_u": "adedpe202006_logtype_ph_u",
        }.items()
    }
    dict_perc.update(percent_dpe)

    perc_cases = pd.DataFrame.from_dict(dict_perc, orient="index")
    return perc_cases


def all_perc_typology(gdfs):
    perc_typologies = [
        dept_perc_typology(gdfs[one_gdf]).rename(columns={0: one_gdf})
        for one_gdf in gdfs
    ]
    all_perc_typologies = pd.concat(perc_typologies, axis=1)
    return all_perc_typologies


if __name__ == "__main__":
    folder_perc = GPD_SORTING_OUTPUT_PATH / "percentage_of_data_tables"
    all_perc_file_paths = sorted(list(folder_perc.iterdir()))
    all_perc_tables = [
        pd.read_csv(file_path, index_col=0) for file_path in all_perc_file_paths
    ]
    perc_table = pd.concat(all_perc_tables, axis=1)
    perc_table.to_csv(folder_perc / "all_depts.csv", float_format="%.2f")
    perc_description = perc_table.T.describe().T
    perc_description = perc_description[
        ["mean", "min", "max", "std", "25%", "50%", "75%", "count"]
    ]
    perc_description.to_csv(
        folder_perc / "all_description.csv",
        float_format="%.1f",
    )

    print(perc_table)
