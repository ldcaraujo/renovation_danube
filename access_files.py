from pathlib import Path
import logging

ROOT_PATH = Path(__file__)
# DATA_PATH = ROOT_PATH.parent.parent / "data"
DATA_PATH =  Path(r"C:\Users\ldecarva\Documents\data")
WORKING_DATA_PATH = DATA_PATH / "working_data"

# INPUT_DATA_PATH = DATA_PATH / "input_data"
INPUT_DATA_PATH = Path(r"D:\_Paendora_DATA_no_space_pc\input_data")
QGIS_INPUT_PATH = INPUT_DATA_PATH / "qgis_input"

# QGIS_OUTPUT_PATH = DATA_PATH / QGIS /"qgis_output"
QGIS_OUTPUT_OLD_TER = WORKING_DATA_PATH / "qgis_output" / "france_old_territory"
QGIS_OUTPUT_NEW_TER = WORKING_DATA_PATH / "qgis_output" / "france_new_territory"

GPD_SORTING_OUTPUT_PATH = WORKING_DATA_PATH / "gpd_sorting_output"

ASSEMBLED_ARCHS_PATH = Path(r"U:\WORK\assembled_by_roof_and_rock_wall")
ANALYSIS_PATH = ROOT_PATH.parent / "data_analysis"

def define_log_file(log_name):
    level = logging.INFO
    format = '  %(message)s'
    handlers = [logging.FileHandler(log_name), logging.StreamHandler()]
    logging.basicConfig(level=level, format=format, handlers=handlers)