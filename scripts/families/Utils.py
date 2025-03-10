class LanguageFamily:
    def __init__(self):
        self.name = ''
        # TODO: reimplement as dictionary
        self.glottocodes = []
        self.languages = []
        self.load_languages()

    def __contains__(self, item):
        return item in self.glottocodes

    def get_language(self, glottocode):
        index = self.get_index(glottocode)
        return self.languages[index]

    def get_glottocodes(self):
        return self.glottocodes

    def get_index(self, glottocode):
        try:
            return self.glottocodes.index(glottocode)
        except ValueError:
            pass
        raise GlottocodeNotFound(glottocode, self.name)

    def load_languages(self):
        raise NotImplemented("load_languages method not implemented")


class GlottocodeNotFound(Exception):
    def __init__(self, glottocode, family=None):
        self.glottocode = glottocode
        if family is None:
            message = f"Could not find language with Glottocode '{glottocode}'"
        else:
            message = f"Could not find language with Glottocode '{glottocode}' in family {family}"
        super().__init__(message)
