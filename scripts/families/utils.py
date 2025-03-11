class LanguageFamily:
    def __init__(self):
        # TODO: reimplement as dictionary
        self._name = None
        self._glottocodes = []
        self._languages = []
        self.load_languages()

    @property
    def name(self):
        if self._name is None:
            raise NotImplementedError('self.name not provided')
        return self._name

    @property
    def FORM_COLUMN(self):
        raise NotImplementedError('self.FORM_COLUMN not provided')

    @property
    def COGNACY_COLUMN(self):
        raise NotImplementedError('self.COGNACY_COLUMN not provided')

    @name.setter
    def name(self, name):
        self._name = name

    def get_forms_for_language(self, glottocode, extended=False):
        raise NotImplementedError(f'get_forms_for_language not implemented for {self.name}')

    @property
    def cherries(self):
        raise NotImplementedError(f'Cherries not implemented for {self.name}')

    def __contains__(self, item):
        return item in self._glottocodes

    def get_language(self, glottocode):
        index = self.get_index(glottocode)
        return self.languages[index]

    @property
    def glottocodes(self):
        return self._glottocodes

    @glottocodes.setter
    def glottocodes(self, value):
        self._glottocodes = value

    @property
    def languages(self):
        return self._languages

    @languages.setter
    def languages(self, value):
        self._languages = value

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
