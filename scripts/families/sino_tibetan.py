import pandas as pd

from scripts.families.utils import LanguageFamily

SINOTIBETAN_DIR = "data/datasets/sagartst"
SINOTIBETAN_LANGUAGES_CSV = f'{SINOTIBETAN_DIR}/languages.csv'


class SinoTibetan(LanguageFamily):
    name = 'SinoTibetan'
    family_glottocode = 'sino1245'
    n_sites = 3784
    n_concepts = 180

    def load_languages(self):
        all_languages = pd.read_csv(SINOTIBETAN_LANGUAGES_CSV)
        self.language_ids = list(all_languages.ID)
        self.glottocodes = list(all_languages.Glottocode)
        self.languages = list(all_languages.Name_in_Text)
