import pandas as pd

from scripts.families.utils import LanguageFamily

CHIRILA_DIR = 'data/datasets/chirila'
CHIRILA_LANGUAGES_CSV = f'{CHIRILA_DIR}/languages.csv'


class PamaNyungan(LanguageFamily):
    name = 'PamaNyungan'
    n_sites = 18438
    n_concepts = 200

    def load_languages(self):
        all_languages = pd.read_csv(CHIRILA_LANGUAGES_CSV)
        self.glottocodes = list(all_languages.Glottocode)
        self.languages = list(all_languages.Name)
        self.languages_ascii = list(all_languages.ID)

    def patch(self):
        pass
        # see literature in parent: https://glottolog.org/resource/languoid/id/dier1241
        # self.set_language_glottocode('CoopersCreek', 'diye1234')
        # From https://en.wikipedia.org/wiki/Lower_Burdekin_languages
        # self.set_language_glottocode('LowerBurdekin', 'bind1234')
