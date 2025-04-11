import pandas as pd
from scripts.families.utils import LanguageFamily

DRAVLEX_DIR = "data/datasets/dravlex"
DRAVLEX_LANGUAGES_CSV = f'{DRAVLEX_DIR}/languages.csv'


class Dravidian(LanguageFamily):
    name = 'Dravidian'
    family_glottocode = 'drav1251'
    n_taxa = 877

    def __init__(self):
        self.languages_ascii = []
        super().__init__()

    def load_languages(self):
        all_languages = pd.read_csv(DRAVLEX_LANGUAGES_CSV)
        self.glottocodes = list(all_languages.Glottocode)
        self.languages = list(all_languages.Name)
        self.languages_ascii = list(all_languages.ID)
