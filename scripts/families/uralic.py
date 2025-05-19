import pandas as pd

from scripts.families.utils import LanguageFamily

URALEX_DIR = "data/datasets/uralex"
URALEX_LANGUAGES_CSV = f'{URALEX_DIR}/languages.csv'


class Uralic(LanguageFamily):
    name = 'Uralic'
    family_glottocode = 'ural1272'
    n_sites = 3655

    def load_languages(self):
        all_languages = pd.read_csv(URALEX_LANGUAGES_CSV)
        self.language_ids = list(all_languages.ID)
        self.glottocodes = list(all_languages.Glottocode)
        self.languages = list(all_languages.Name)

    def patch(self):
        self.delete_language('Proto-Uralic*')
