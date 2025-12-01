import pandas as pd

from scripts.families.utils import LanguageFamily, LanguageNotFound

IE_COR_DIR = 'data/datasets/ie-cor'

IE_COR_LANGUAGES_CSV = f'{IE_COR_DIR}/languages.csv'
IE_COR_ITALIC_CLADE = 'Italic'


class IndoEuropean(LanguageFamily):
    name = 'IndoEuropean'
    family_glottocode = 'indo1319'
    n_sites = 4958
    n_concepts = 170
    clades = {}

    def load_languages(self):
        all_languages = pd.read_csv(IE_COR_LANGUAGES_CSV)
        self.language_ids = list(all_languages.ID)
        self.glottocodes = list(all_languages.Glottocode)
        self.languages = list(all_languages.Name)
        self.languages_ascii = list(all_languages.ascii_name)
        self.clades = dict(zip(self.languages_ascii, list(all_languages.clade_name)))

    def patch(self):
        self.set_language_glottocode('Old Polish', 'oldp1256')
        self.set_language_glottocode('Middle Cornish', 'midd1380')
        self.set_language_glottocode('Late Cornish', 'corn1251')
        self.set_language_glottocode('Old Swedish', 'olds1252')
        # No glottocode for early modern slovenian, set to something topologically equal
        self.set_language_glottocode('Old Czech', 'oldc1253')
        self.set_language_glottocode('Kurdish S.: Elami', 'feyl1238')
        self.set_language_glottocode('Kurdish S.: Qorveh', 'koly1245')
        # Both are south-eastern dialects but no finer granularity of course
        self.set_language_glottocode('Macedonian: Suho', 'sout3278')
        self.set_language_glottocode('Macedonian: Visoka', 'sout3278')
        # Sardinian dialects
        self.set_language_glottocode('Sardinian: Logudoro', 'logu1236')
        self.set_language_glottocode('Sardinian: Nuoro', 'nuor1238')

    def get_clades(self):
        return ['Germanic', 'Celtic', 'Italic', 'Balto-Slavic', 'Indo-Iranic']

    def get_clade_from_ascii(self, ascii):
        try:
            return self.clades[ascii]
        except KeyError:
            pass
        raise LanguageNotFound(ascii)


class Italic(IndoEuropean):
    name = 'Italic'

    def load_languages(self):
        all_languages = pd.read_csv(IE_COR_LANGUAGES_CSV)
        italic_languages = all_languages[all_languages.Clade.str.startswith(IE_COR_ITALIC_CLADE)]
        self.language_ids = list(italic_languages.ID)
        self.glottocodes = list(italic_languages.Glottocode)
        self.languages = list(italic_languages.Name)
        self.languages_ascii = list(italic_languages.ascii_name)

    def patch(self):
        pass
