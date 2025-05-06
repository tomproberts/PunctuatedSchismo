from scripts.families.utils import LanguageFamily


class Uralic(LanguageFamily):
    name = 'Uralic'

    def load_languages(self):
        self.glottocodes = []
        self.languages = []
        # self.languages_ascii = []
