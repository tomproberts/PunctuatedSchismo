import pandas
import pandas as pd
import os

from scripts.families.utils import LanguageFamily

PHONO_DISTANCE = 'phono-distance'
DATA_DIR = 'data'


def check_dir_exists(dir_name: str):
    # check that data dir exists
    if not os.path.exists(DATA_DIR):
        raise Exception('Data directory does not exist, are you running the script from the right location?')
    os.makedirs(dir_name, exist_ok=True)


def write_out_df(predictor: str, file_name_base: str, df: pandas.DataFrame):
    assert len(predictor) > 0
    dir_name = f'{DATA_DIR}/predictors/{predictor}/'
    check_dir_exists(dir_name)
    df.to_csv(f'{dir_name}{file_name_base}.csv', index=False, header=True)


def write_out_phonological_distance(
        family: LanguageFamily, cherries: list[(str, str)], distances: list[float]):
    lang1, lang2 = zip(*cherries)
    df = pd.DataFrame(data={'Language1': lang1, 'Language2': lang2, 'Distance': distances})
    file_name = f'{family.name}.levenshtein'
    write_out_df(PHONO_DISTANCE, file_name, df)
