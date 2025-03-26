from scripts.utils import asciify_alphanumeric


class LanguageFamily:
    _name = None
    _family_glottocode = None
    _glottocodes = []
    _languages = []

    def __init__(self):
        # TODO: reimplement as dictionary
        self.load_languages()
        self.patch()
        self.verify_unique_glottocodes()

    @property
    def name(self):
        if self._name is None:
            raise NotImplementedError('self.name not provided')
        return self._name

    @property
    def family_glottocode(self):
        if self._family_glottocode is None:
            raise NotImplementedError('self.family_glottocode not provided')
        return self._family_glottocode

    @property
    def FORM_COLUMN(self):
        raise NotImplementedError('self.FORM_COLUMN not provided')

    @property
    def COGNACY_COLUMN(self):
        raise NotImplementedError('self.COGNACY_COLUMN not provided')

    @property
    def n_taxa(self):
        raise NotImplementedError('number of taxa not provided')

    @name.setter
    def name(self, name):
        self._name = name

    @family_glottocode.setter
    def family_glottocode(self, family_glottocode):
        self._family_glottocode = family_glottocode

    def get_forms_for_language(self, glottocode, extended=False):
        raise NotImplementedError(f'get_forms_for_language not implemented for {self.name}')

    def get_glottocode_from_ascii(self, glottocode, extended=False):
        raise NotImplementedError(f'get_glottocode_from_ascii not implemented for {self.name}')

    @property
    def cherries(self):
        raise NotImplementedError(f'Cherries not implemented for {self.name}')

    def __contains__(self, item):
        return item in self._glottocodes

    def get_language(self, glottocode):
        index = self.get_index(glottocode)
        return self.languages[index]

    def get_language_ascii(self, glottocode):
        l = self.get_language(glottocode)
        l = asciify_alphanumeric(l)
        return l

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
        raise NotImplemented('load_languages method not implemented')

    def verify_unique_glottocodes(self):
        uniques = set()
        doubles = set()
        for glottocode in self.glottocodes:
            (uniques if glottocode not in uniques else doubles).add(glottocode)
        if len(doubles) > 0:
            raise DuplicateGlottocodes(doubles)
            # print(f"Warning: duplicate glottocodes '{"','".join(doubles)}' found, perhaps implement self.patch()?")

    def patch(self):
        pass

    def set_language_glottocode(self, language_name, glottocode):
        try:
            i = self._languages.index(language_name)
            self._glottocodes[i] = glottocode
            return
        except ValueError:
            pass
        raise LanguageNotFound(language_name, self.name)


class GlottocodeNotFound(Exception):
    def __init__(self, glottocode, family=None):
        if family is None:
            message = f"Could not find language with Glottocode '{glottocode}'"
        else:
            message = f"Could not find language with Glottocode '{glottocode}' in family {family}"
        super().__init__(message)


class LanguageNotFound(Exception):
    def __init__(self, language, family=None):
        if family is None:
            message = f"Could not find language '{language}'"
        else:
            message = f"Could not find language '{language}' in family {family}"
        super().__init__(message)


class DuplicateGlottocodes(Exception):
    def __init__(self, glottocodes=None):
        message = f"Duplicate glottocodes '{"','".join(glottocodes)}' found, perhaps implement self.patch()?"
        super().__init__(message)
