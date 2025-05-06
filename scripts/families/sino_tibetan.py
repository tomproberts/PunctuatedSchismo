import pandas as pd

from scripts.families.utils import LanguageFamily

SINOTIBETAN_DIR = "data/datasets/sagartst"
SINOTIBETAN_LANGUAGES_CSV = f'{SINOTIBETAN_DIR}/languages.csv'


class SinoTibetan(LanguageFamily):
    name = 'SinoTibetan'
    family_glottocode = 'sino1245'

    def load_languages(self):
        all_languages = pd.read_csv(SINOTIBETAN_LANGUAGES_CSV)
        self.glottocodes = list(all_languages.Glottocode)
        self.languages = list(all_languages.ID)

    def patch(self):
        # Both randomly assigned to similar place on topology, investigate later!
        self.set_language_glottocode('Alike', 'inno1234')
        self.set_language_glottocode('Xingning', 'yuet1238')
