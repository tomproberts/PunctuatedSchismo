import pandas as pd
import os

from scripts.families.utils import LanguageFamily


def check_dir_exists(dir_name):
    os.makedirs(dir_name, exist_ok=True)


def write_out_phonological_distance(
        family: LanguageFamily, cherries: list[(str, str)], distances: list[float]):
    lang1, lang2 = zip(*cherries)
    df = pd.DataFrame(data={'Language1': lang1, 'Language2': lang2, 'Distance': distances})
    dir_name = f'data/predictors/phono-distance'
    check_dir_exists(dir_name)
    file_name = f'{family.name}.levenshtein.csv'
    df.to_csv(f'{dir_name}/{file_name}', index=False, header=True)
