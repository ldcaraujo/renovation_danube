from time import time
import logging
import traceback

from access_files import GPD_SORTING_OUTPUT_PATH, QGIS_OUTPUT_NEW_TER # , QGIS_OUTPUT_PATH
from preprocessing_data.process_qgis_output.gdfs_utils import open_gdfs, pool_save_archetypes
from preprocessing_data.process_qgis_output.create_danube_entries import pool_create_danube_entries
from preprocessing_data.process_qgis_output.data_percentage import all_perc_typology

TEST = False

if TEST:
    QGIS_OUTPUT_NEW_TER, GPD_SORTING_OUTPUT_PATH = (
        path / "test" for path in (QGIS_OUTPUT_NEW_TER, GPD_SORTING_OUTPUT_PATH)
    )

# define log file
level    = logging.INFO
format   = '  %(message)s'
handlers = [logging.FileHandler('AppLog_main_preprocessing.log'), logging.StreamHandler()]
logging.basicConfig(level = level, format = format, handlers = handlers)


def timed_open_gdfs(dept_file_paths):
    start_time = time()
    loaded_gdfs = open_gdfs(dept_file_paths, processes=6)
    logging.info(f"open_gdfs executed in {(time() - start_time):.4f}s")
    return loaded_gdfs


def timed_format(gdfs):
    start_time = time()
    gdfs = pool_create_danube_entries(gdfs, processes=6)
    logging.info(f"pool_create_danube_entries executed in {(time() - start_time):.4f}s")
    return gdfs


def timed_save_archetypes(gdfs, output_path):
    start_time = time()
    pool_save_archetypes(gdfs, output_path)
    logging.info(f"pool_save_archetypes executed in {(time() - start_time):.4f}s")


def timed_data_percentage(gdfs, folder_save):
    start_time = time()
    perc = all_perc_typology(gdfs)
    # save percentage
    first_dept = sorted(gdfs)[0]
    last_dept = sorted(gdfs)[-1]
    name_perc_nb_depts_from_to = f"percent_depts_{first_dept}_to_{last_dept}.csv"
    perc.to_csv(rf"{folder_save}/{name_perc_nb_depts_from_to}")
    logging.info(f"data percentages executed in {(time() - start_time):.4f}s")


if __name__ == "__main__":
    start_time = time()

    # dept_files_path = QGIS_OUTPUT_PATH / "joined_per_dept"  # for SIG files
    dept_files_path = QGIS_OUTPUT_NEW_TER / "csvs_per_department"
    all_dept_file_paths = sorted(list(dept_files_path.iterdir()))
    file_start_nb = 0
    while file_start_nb < len(all_dept_file_paths):
        slice_size = 1

        dept_file_paths_slice = all_dept_file_paths[
            file_start_nb : min(file_start_nb + slice_size, len(all_dept_file_paths))
        ]
        file_start_nb += slice_size
        try:
            # read dept files
            loaded_gdfs_slice = timed_open_gdfs(dept_file_paths_slice)
            gdfs = loaded_gdfs_slice.copy()
            logging.info(f"loaded gdfs: {list(gdfs.keys())}")

            # Formatting
            gdfs = timed_format(gdfs)

            # save archetypes csv
            timed_save_archetypes(
                gdfs, GPD_SORTING_OUTPUT_PATH / "archetypes_per_dept_tables"
            )

            # percentage of non null data
            timed_data_percentage(
                gdfs, GPD_SORTING_OUTPUT_PATH / "percentage_of_data_tables"
            )


        except Exception as e:
            if hasattr(e, 'message'):
                logging.info("Problem to execute the process to this dept.\nError:")
                logging.info(e.message)
                logging.info(traceback.format_exc())

            else:
                logging.info("Problem to execute the process to this dept.\nError:")
                logging.info(e)
                logging.info(traceback.format_exc())


    logging.info(f"All files execution time: {(time() - start_time):.4f}s")
    logging.shutdown()
