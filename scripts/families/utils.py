from scripts.utils import asciify_alphanumeric


class LanguageFamily:
    _name = None
    _family_glottocode = None
    _id_map = {}  # {'lang_id': ('glottocode', 'language_name', 'language_ascii'),...}

    def __init__(self):
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
    def n_sites(self):
        raise NotImplementedError('number of sites not provided')

    @name.setter
    def name(self, name):
        self._name = name

    @family_glottocode.setter
    def family_glottocode(self, family_glottocode):
        self._family_glottocode = family_glottocode

    def get_forms_for_language(self, glottocode, extended=False):
        raise NotImplementedError(f'get_forms_for_language not implemented for {self.name}')

    def get_glottocode_from_ascii(self, ascii_name):
        i = self.languages_ascii.index(ascii_name)
        return self.glottocodes[i]

    def __contains__(self, item):
        return item in self.glottocodes

    def get_language_from_glottocode(self, glottocode):
        for (lang_glottocode, language_name, _) in self._id_map:
            if glottocode == lang_glottocode:
                return language_name
        raise GlottocodeNotFound(glottocode)

    def get_language_ascii_from_glottocode(self, glottocode):
        for (lang_glottocode, lang_name, lang_ascii) in self._id_map:
            if glottocode == lang_glottocode:
                if lang_ascii is not None:
                    return lang_ascii
                return asciify_alphanumeric(lang_name)
        raise GlottocodeNotFound(glottocode)

    @property
    def glottocodes(self):
        # if map is initialised
        if bool(self._id_map):
            return [glottocode for (glottocode, _, _) in self._id_map.values()]
        return []

    @glottocodes.setter
    def glottocodes(self, value):
        # if map is initialised
        if bool(self._id_map):
            assert len(self._id_map) == len(value)
            for (lang_id, glottocode) in zip(self._id_map, value):
                (_, lang_name, lang_ascii) = self._id_map[lang_id]
                self._id_map[lang_id] = (glottocode, lang_name, lang_ascii)
        else:
            for glottocode in value:
                self._id_map[glottocode] = (glottocode, None, None)

    @property
    def languages(self):
        # if map is initialised
        if bool(self._id_map):
            return [lang_name for (_, lang_name, _) in self._id_map.values()]
        return []

    @languages.setter
    def languages(self, value):
        # if map is initialised
        if bool(self._id_map):
            assert len(self._id_map) == len(value)
            for (lang_id, lang_name) in zip(self._id_map, value):
                (glottocode, _, lang_ascii) = self._id_map[lang_id]
                self._id_map[lang_id] = (glottocode, lang_name, lang_ascii)
        else:
            for lang_name in value:
                self._id_map[lang_name] = (None, lang_name, None)

    @property
    def languages_ascii(self):
        self.check_and_generate_ascii_names()
        # if map is initialised
        if bool(self._id_map):
            return [lang_ascii for (_, _, lang_ascii) in self._id_map.values()]
        return []
        # self._tmp_languages_ascii = [asciify_alphanumeric(l) for l in self.languages]

    def check_and_generate_ascii_names(self):
        if bool(self._id_map):
            (_, _, sample_ascii) = next(iter(self._id_map.values()))
            if sample_ascii is None:
                self.languages_ascii = [asciify_alphanumeric(l) for l in self.languages]

    @languages_ascii.setter
    def languages_ascii(self, value):
        # if map is initialised
        if bool(self._id_map):
            assert len(self._id_map) == len(value)
            for (lang_id, lang_ascii) in zip(self._id_map, value):
                (glottocode, lang_name, _) = self._id_map[lang_id]
                self._id_map[lang_id] = (glottocode, lang_name, lang_ascii)
        else:
            for lang_ascii in value:
                self._id_map[lang_ascii] = (None, lang_ascii, None)

    def load_languages(self):
        raise NotImplementedError('load_languages method not implemented')

    def verify_unique_glottocodes(self):
        uniques = set()
        doubles = set()
        for glottocode in self.glottocodes:
            if type(glottocode) is str:
                (uniques if glottocode not in uniques else doubles).add(glottocode)
            # TODO: else, it's float.NAN, i.e. missing glottocode
        if len(doubles) > 0:
            raise DuplicateGlottocodes(doubles)
            # print(f"Warning: duplicate glottocodes '{"','".join(doubles)}' found, perhaps implement self.patch()?")

    def patch(self):
        pass

    def set_language_glottocode(self, language_name, glottocode):
        found = False
        for key, (_, match_name, lang_ascii) in self._id_map.items():
            if language_name == match_name:
                self._id_map[key] = (glottocode, language_name, lang_ascii)
                found = True
                break
        if not found:
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
