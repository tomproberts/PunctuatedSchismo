import pandas as pd

from scripts.families.utils import LanguageFamily

SINOTIBETAN_DIR = "data/datasets/sagartst"
SINOTIBETAN_LANGUAGES_CSV = f'{SINOTIBETAN_DIR}/languages.csv'


class SinoTibetan(LanguageFamily):
    name = 'SinoTibetan'
    family_glottocode = 'sino1245'
    n_sites = 3784
    n_concepts = 180
    clades = None

    def load_languages(self):
        all_languages = pd.read_csv(SINOTIBETAN_LANGUAGES_CSV)
        self.language_ids = list(all_languages.ID)
        self.glottocodes = list(all_languages.Glottocode)
        self.languages = list(all_languages.Name_in_Text)
        self.languages_ascii = [str(l).replace('_', '') for l in all_languages.Name]
        self.clades = dict(zip(self.languages_ascii, list(all_languages.SubGroup)))

    def get_clades(self):
        return ['Burmish', 'Tibetan', 'Sinitic', 'Kiranti', 'rGyalrong']

    def get_clade_from_ascii(self, ascii):
        return self.clades[ascii]
