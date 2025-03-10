import pandas as pd

from scripts.families.Utils import LanguageFamily

IE_COR_DIR = "data/datasets/ie-cor"

IE_COR_LANGUAGES_CSV = f'{IE_COR_DIR}/languages.csv'
IE_COR_FORMS_CSV = f'{IE_COR_DIR}/forms.csv'
IE_COR_COGNATES_CSV = f'{IE_COR_DIR}/cognates.csv'

IE_COR_FORM_COLUMN = 'Form'  # 'Phonemic'


class Italic(LanguageFamily):
    def __init__(self):
        super().__init__()
        self.name = 'Italic'
        self.language_ids = []
        self.all_forms = None
        self.all_cognates = None
        self.tmp1 = (None, None)
        self.tmp2 = (None, None)

    def load_languages(self):
        all_languages = pd.read_csv(IE_COR_LANGUAGES_CSV)
        italic_languages = all_languages[all_languages.Clade.str.startswith('Italic')]
        self.glottocodes = list(italic_languages.Glottocode)
        self.language_ids = list(italic_languages.ID)
        self.languages = list(italic_languages.Name)

    def get_language_id(self, glottocode):
        index = super().get_index(glottocode)
        return self.language_ids[index]

    def cache(self, glottocode, forms, first=True):
        if first:
            self.tmp1 = (glottocode, forms)
        else:
            self.tmp2 = (glottocode, forms)

    def get_from_cache(self, glottocode):
        g1, f1 = self.tmp1
        if g1 == glottocode:
            return f1
        g2, f2 = self.tmp2
        if g2 == glottocode:
            return f2
        return None

    def get_forms(self, glottocode):
        filtered = self.get_from_cache(glottocode)
        if filtered is None:
            lang_id = self.get_language_id(glottocode)
            all_forms = self.get_ie_cor_forms()
            filtered = all_forms[all_forms.Language_ID == lang_id][['ID', IE_COR_FORM_COLUMN, 'Parameter_ID']]
        filtered = filtered.sort_values(by=['Parameter_ID'])
        return list(filtered[IE_COR_FORM_COLUMN])

    def get_common_forms(self, lang1, lang2):
        merged1 = self.get_from_cache(lang1)
        if merged1 is None:
            lang1_id = self.get_language_id(lang1)
            all_forms = self.get_ie_cor_forms()
            all_forms1 = all_forms[all_forms.Language_ID == lang1_id][['ID', IE_COR_FORM_COLUMN, 'Parameter_ID']]
            all_cognates = self.get_ie_cor_cognates()
            merged1 = all_forms1.merge(all_cognates, left_on='ID', right_on='Form_ID', suffixes=('', 'y'))[
                ['ID', 'Parameter_ID', IE_COR_FORM_COLUMN, 'Cognateset_ID']]
            self.cache(lang1, merged1, True)
        merged2 = self.get_from_cache(lang2)
        if merged2 is None:
            lang2_id = self.get_language_id(lang2)
            all_forms = self.get_ie_cor_forms()
            all_forms2 = all_forms[all_forms.Language_ID == lang2_id][['ID', IE_COR_FORM_COLUMN, 'Parameter_ID']]
            all_cognates = self.get_ie_cor_cognates()
            merged2 = all_forms2.merge(all_cognates, left_on='ID', right_on='Form_ID', suffixes=('', 'y'))[
                ['ID', 'Parameter_ID', IE_COR_FORM_COLUMN, 'Cognateset_ID']]
            self.cache(lang2, merged2, first=False)

        common_cognates = list(set(merged1.Cognateset_ID) & set(merged2.Cognateset_ID))

        forms1 = list(
            merged1[merged1.Cognateset_ID.isin(common_cognates)].sort_values(by=['Parameter_ID'])[IE_COR_FORM_COLUMN])
        forms2 = list(
            merged2[merged2.Cognateset_ID.isin(common_cognates)].sort_values(by=['Parameter_ID'])[IE_COR_FORM_COLUMN])

        return forms1, forms2

    def get_ie_cor_forms(self):
        return pd.read_csv(IE_COR_FORMS_CSV) if self.all_forms is None else self.all_forms

    def get_ie_cor_cognates(self):
        return pd.read_csv(IE_COR_COGNATES_CSV) if self.all_cognates is None else self.all_cognates
