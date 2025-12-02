import pandas as pd

from scripts.families.utils import LanguageFamily

URALEX_DIR = 'data/datasets/uralex'
URALEX_LANGUAGES_CSV = f'{URALEX_DIR}/languages.csv'


def uralic_ascii_names(lang_names):
    # Syrjänen's export uses ascii names present in raw/Languages.tsv but not in CLDF
    ascii_names = []
    for l_name in lang_names:
        if l_name == 'Karelian Proper':
            new_name = 'Karelian_Proper'
        elif l_name == 'Selkup':
            new_name = 'Selkup_Northern'
        else:
            new_name = str(l_name).split(' ')[-2:]
            new_name.reverse()
            new_name = '_'.join(new_name).replace('-', '_')
        ascii_names.append(new_name)
    return ascii_names


class Uralic(LanguageFamily):
    DEPRECATED = True
    name = 'Uralic'
    family_glottocode = 'ural1272'
    n_sites = 800
    n_concepts = 101

    def load_languages(self):
        all_languages = pd.read_csv(URALEX_LANGUAGES_CSV)
        self.language_ids = list(all_languages.ID)
        self.glottocodes = list(all_languages.Glottocode)
        self.languages = list(all_languages.Name)
        self.languages_ascii = uralic_ascii_names(all_languages.Name)

    def patch(self):
        self.delete_language('Proto-Uralic*')
