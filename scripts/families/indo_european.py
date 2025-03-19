import pandas as pd

from scripts.families.utils import LanguageFamily

IE_COR_DIR = "data/datasets/ie-cor"

IE_COR_LANGUAGES_CSV = f'{IE_COR_DIR}/languages.csv'
IE_COR_FORMS_CSV = f'{IE_COR_DIR}/forms.csv'
IE_COR_COGNATES_CSV = f'{IE_COR_DIR}/cognates.csv'

IE_COR_ITALIC_CLADE = 'Italic'

IE_COR_ID_COLUMN = 'ID'
IE_COR_FORM_COLUMN = 'Form'  # 'Phonemic'
IE_COR_COGNATE_ID_COLUMN = 'Cognateset_ID'
IE_COR_PARAMETER_ID_COLUMN = 'Parameter_ID'
IE_COR_LANGUAGE_ID_COLUMN = 'Language_ID'


class IndoEuropean(LanguageFamily):
    FORM_COLUMN = IE_COR_FORM_COLUMN
    COGNACY_COLUMN = IE_COR_COGNATE_ID_COLUMN
    name = 'IndoEuropean'

    def __init__(self):
        super().__init__()
        self._language_ids = []
        self._all_forms = None
        self._cognates_merged = False

    def load_languages(self):
        all_languages = pd.read_csv(IE_COR_LANGUAGES_CSV)
        self.glottocodes = list(all_languages.Glottocode)
        self.languages = list(all_languages.Name)
        self._language_ids = list(all_languages.ID)

    # @property
    # def glottolog_cherries(self) -> list[(str, str)]:
    #     return []

    @property
    def language_ids(self):
        if len(self._language_ids) == 0:
            self.load_languages()
        return self._language_ids

    def get_language_id(self, glottocode):
        index = super().get_index(glottocode)
        return self.language_ids[index]

    def get_forms_for_language(self, glottocode, extended=False):
        all_forms = self.merge_on_cognate_ids() if extended else self.ie_cor_forms
        lang_id = self.get_language_id(glottocode)
        forms = all_forms[all_forms[IE_COR_LANGUAGE_ID_COLUMN] == lang_id]
        if extended:
            return forms
        return list(forms[IE_COR_FORM_COLUMN])

    def merge_on_cognate_ids(self):
        if not self._cognates_merged:
            all_forms = self.ie_cor_forms
            all_forms = all_forms[all_forms.Language_ID.isin(self.language_ids)][
                [IE_COR_ID_COLUMN, IE_COR_LANGUAGE_ID_COLUMN, IE_COR_FORM_COLUMN, IE_COR_PARAMETER_ID_COLUMN]]
            all_cognates = pd.read_csv(IE_COR_COGNATES_CSV)
            merged = all_forms.merge(all_cognates, left_on=IE_COR_ID_COLUMN, right_on='Form_ID', suffixes=('', 'y'))[
                [IE_COR_ID_COLUMN, IE_COR_LANGUAGE_ID_COLUMN, IE_COR_PARAMETER_ID_COLUMN, IE_COR_FORM_COLUMN,
                 IE_COR_COGNATE_ID_COLUMN]].sort_values(by=[IE_COR_PARAMETER_ID_COLUMN])
            self._all_forms = merged
            self._cognates_merged = True
        return self.ie_cor_forms

    @property
    def ie_cor_forms(self):
        if self._all_forms is None:
            self._all_forms = pd.read_csv(IE_COR_FORMS_CSV)
        return self._all_forms


class Italic(IndoEuropean):
    name = 'Italic'

    def load_languages(self):
        all_languages = pd.read_csv(IE_COR_LANGUAGES_CSV)
        italic_languages = all_languages[all_languages.Clade.str.startswith(IE_COR_ITALIC_CLADE)]
        self.glottocodes = list(italic_languages.Glottocode)
        self.languages = list(italic_languages.Name)
        self._language_ids = list(italic_languages.ID)

    @property
    def glottolog_cherries(self) -> list[(str, str)]:
        return [
            ('port1283', 'braz1246'),
            ('stan1288', 'olds1249'),
            ('oldc1251', 'stan1289'),
            ('stan1290', 'fran1269'),
            ('ladi1250', 'friu1240'),
            ('neap1235', 'ital1282'),
            ('sout2614', 'barb1262'),
            ('roma1327', 'megl1237'),
            ('umbr1253', 'osca1245')
        ]
