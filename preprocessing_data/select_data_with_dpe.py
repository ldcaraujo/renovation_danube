from pathlib import Path
from os import listdir
import pandas as pd

work_folder = Path(r"U:\WORK\assembled_same_U")
source_folder = work_folder / "assembled_by_roof_and_rock_wall"
root_save_folder = work_folder / "with_complete_dpe_data"

csv = r"len_30255-P1-I-HABITAT-FRANCE_TERRE_TUILE-uniq.csv"
path = source_folder / csv

for csv in listdir(source_folder):
    path = source_folder / csv
    df = pd.read_csv(path)
    print(path.stem)

    root_name = "-".join(path.stem.split("-")[1:])
    print(root_name)

    element_columns = {"wall": "adedpe202006_logtype_mur_u_ext",
                       "roof": "adedpe202006_logtype_ph_u",
                       "window": "adedpe202006_logtype_baie_type_vitrage"}

    # save dfs with not null values
    for element, col in element_columns.items():
        print(element,col)
        df_element =  df.loc[df[col].notnull()]
        save_name = f"dpe_{element}-len_{len(df_element)}-{root_name}.csv"
        print(save_name)
        df_element.to_csv(root_save_folder / element / save_name)

    cond_all_3_dpe = (df["adedpe202006_logtype_mur_u_ext"].notnull()) & (df["adedpe202006_logtype_ph_u"].notnull()) & (df["adedpe202006_logtype_baie_type_vitrage"].notnull())
    df_all = df.loc[cond_all_3_dpe]
    save_name_all = f"dpe_all3-len_{len(df_all)}-{root_name}.csv"
    df_all.to_csv(root_save_folder / "all" / save_name_all)


