import pandas as pd

from scripts.families.utils import LanguageFamily

BANTU_DIR = 'data/datasets/grollemund'
BANTU_LANGUAGES_CSV = f'{BANTU_DIR}/languages.csv'


class Bantu(LanguageFamily):
    name = 'Bantu'
    family_glottocode = 'bant1294'

    def load_languages(self):
        all_languages = pd.read_csv(BANTU_LANGUAGES_CSV)
        self.language_ids = list(all_languages.ID)
        self.glottocodes = list(all_languages.Glottocode)
        self.languages = list(all_languages.Name)
        self.languages_ascii = self.language_ids

    def get_clades(self):
        return ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'R', 'S']

    def get_clade_from_ascii(self, ascii):
        if ord('0') <= ord(ascii[1]) <= ord('a'):
            return ascii[0]
        return ''
