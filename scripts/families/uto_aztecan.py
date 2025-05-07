import pandas as pd

from scripts.families.utils import LanguageFamily

UTO_DIR = "data/datasets/utoaztecan"
UTO_LANGUAGES_CSV = f'{UTO_DIR}/languages.csv'


class UtoAztecan(LanguageFamily):
    name = 'UtoAztecan'
    family_glottocode = 'utoa1244'

    def load_languages(self):
        all_languages = pd.read_csv(UTO_LANGUAGES_CSV)
        self.glottocodes = list(all_languages.Glottocode)
        self.languages = list(all_languages.Name)
