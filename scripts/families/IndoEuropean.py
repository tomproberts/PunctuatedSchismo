import pandas as pd

from scripts.families.Utils import LanguageFamily

IE_COR_DIR = "data/datasets/ie-cor"

IE_COR_LANGUAGES_CSV = f'{IE_COR_DIR}/languages.csv'
IE_COR_FORMS_CSV = f'{IE_COR_DIR}/forms.csv'
IE_COR_COGNATES_CSV = f'{IE_COR_DIR}/cognates.csv'

IE_COR_FORM_COLUMN = 'Form'  # 'Phonemic'
IE_COR_COGNATE_ID_COLUMN = 'Cognateset_ID'


class Italic(LanguageFamily):
    def __init__(self):
        super().__init__()
        self.name = 'Italic'
        self.language_ids = []
        self.all_forms = None
        self.all_cognates = None
        self.already_merged = False
        self.FORM_COLUMN = IE_COR_FORM_COLUMN
        self.COGNACY_COLUMN = IE_COR_COGNATE_ID_COLUMN

    def load_languages(self):
        all_languages = pd.read_csv(IE_COR_LANGUAGES_CSV)
        italic_languages = all_languages[all_languages.Clade.str.startswith('Italic')]
        self.glottocodes = list(italic_languages.Glottocode)
        self.language_ids = list(italic_languages.ID)
        self.languages = list(italic_languages.Name)

    def get_language_ids(self):
        if len(self.language_ids) == 0:
            self.load_languages()
        return self.language_ids

    def get_language_id(self, glottocode):
        # TODO: replace with getters
        index = super().get_index(glottocode)
        return self.language_ids[index]

    def get_forms(self, glottocode, include_cognacy=False):
        all_forms = self.merge_on_cognate_ids()
        lang_id = self.get_language_id(glottocode)
        forms = all_forms[all_forms.Language_ID == lang_id]
        if include_cognacy:
            return forms
        return list(forms[IE_COR_FORM_COLUMN])

    def merge_on_cognate_ids(self):
        if not self.already_merged:
            all_forms = self.get_ie_cor_forms()
            all_forms = all_forms[all_forms.Language_ID.isin(self.get_language_ids())][
                ['ID', 'Language_ID', IE_COR_FORM_COLUMN, 'Parameter_ID']]
            all_cognates = self.get_ie_cor_cognates()
            merged = all_forms.merge(all_cognates, left_on='ID', right_on='Form_ID', suffixes=('', 'y'))[
                ['ID', 'Language_ID', 'Parameter_ID', IE_COR_FORM_COLUMN, 'Cognateset_ID']].sort_values(
                by=['Parameter_ID'])
            self.all_forms = merged
            self.already_merged = True
        return self.get_ie_cor_forms()

    def get_ie_cor_forms(self):
        if self.all_forms is None:
            self.all_forms = pd.read_csv(IE_COR_FORMS_CSV)
        return self.all_forms

    def get_ie_cor_cognates(self):
        if self.all_cognates is None:
            self.all_cognates = pd.read_csv(IE_COR_COGNATES_CSV)
        return self.all_cognates
