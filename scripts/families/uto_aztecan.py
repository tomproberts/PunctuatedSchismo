import pandas as pd

from scripts.families.utils import LanguageFamily

UTO_DIR = "data/datasets/utoaztecan"
UTO_LANGUAGES_CSV = f'{UTO_DIR}/languages.csv'

UTO_AZTECAN_FAMILY = 'Uto-Aztecan'


class UtoAztecan(LanguageFamily):
    name = 'UtoAztecan'
    family_glottocode = 'utoa1244'

    def load_languages(self):
        all_languages = pd.read_csv(UTO_LANGUAGES_CSV)
        # all_languages = all_languages[all_languages.Family == UTO_AZTECAN_FAMILY]
        self.language_ids = list(all_languages.ID)
        self.glottocodes = list(all_languages.Glottocode)
        self.languages = list(all_languages.Name)
        self.languages_ascii = self.language_ids
