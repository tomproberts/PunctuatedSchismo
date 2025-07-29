import pandas as pd
import re

from scripts.families.utils import LanguageFamily
from scripts.utils import asciify

PHILIPPINES_DIR = 'data/datasets/abvd_philippines'
PHILIPPINES_LANGUAGES_CSV = f'{PHILIPPINES_DIR}/languages.csv'


def to_abvd_link(language_ascii, family: LanguageFamily):
    id = family.get_language_id_from_ascii(language_ascii)
    return f'[{id}](https://abvd.eva.mpg.de/austronesian/language.php?id={id})'


def p_asciify(language):
    sub = asciify(language)
    sub = re.sub(r'[:\']', '', sub)
    sub = re.sub(r' - ', '_', sub)
    sub = re.sub(r'[,_ \(\)]+', '_', sub)
    if sub[-1] == '_': sub = sub[:-1]
    return sub


class Philippines(LanguageFamily):
    name = 'Philippines'

    def load_languages(self):
        all_languages = pd.read_csv(PHILIPPINES_LANGUAGES_CSV)
        self.language_ids = list(all_languages.ID)
        self.glottocodes = list(all_languages.Glottocode)
        self.languages = list(all_languages.Name)
        self.languages_ascii = [f'{p_asciify(l)}_{str(i)}' for l, i in zip(all_languages.Name, all_languages.ID)]
