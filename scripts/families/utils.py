from scripts.utils import asciify_alphanumeric, is_valid_identifier


class LanguageFamily:
    _name = None
    _family_glottocode = None

    def __init__(self):
        self._id_map = dict()  # {'lang_id': ('glottocode', 'language_name', 'language_ascii'),...}
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
        language_names = self.get_languages_from_glottocode(glottocode)
        if not language_names:
            raise GlottocodeNotFound(glottocode)
        if len(language_names) == 1:
            return language_names[0]
        raise DuplicateGlottocodes([glottocode])

    def get_languages_from_glottocode(self, glottocode):
        languages = []
        for (lang_glottocode, language_name, _) in self._id_map.values():
            if glottocode == lang_glottocode:
                languages.append(language_name)
        return languages

    def get_language_ascii_from_glottocode(self, glottocode):
        language_asciis = self.get_language_asciis_from_glottocode(glottocode)
        # Return
        if not language_asciis:
            raise GlottocodeNotFound(glottocode)
        if len(language_asciis) == 1:
            return language_asciis[0]
        raise DuplicateGlottocodes([glottocode])

    def get_language_asciis_from_glottocode(self, glottocode):
        self.check_and_generate_ascii_names()
        language_asciis = []
        for (lang_glottocode, lang_name, lang_ascii) in self._id_map.values():
            if glottocode == lang_glottocode:
                language_asciis.append(lang_ascii)
        return language_asciis

    def get_language_id_from_glottocode(self, glottocode):
        language_ids = self.get_language_ids_from_glottocode(glottocode)
        if not language_ids:
            raise GlottocodeNotFound(glottocode)
        if len(language_ids) == 1:
            return language_ids[0]
        raise DuplicateGlottocodes([glottocode])

    def get_language_ids_from_glottocode(self, glottocode):
        language_ids = []
        for key, (lang_glottocode, _, _) in self._id_map.items():
            if glottocode == lang_glottocode:
                language_ids.append(key)
        return language_ids

    @property
    def language_ids(self):
        return list(self._id_map.keys())

    @language_ids.setter
    def language_ids(self, value):
        # check for duplicates
        singles = []
        for new_id in value:
            if new_id not in singles:
                singles.append(new_id)
            else:
                raise DuplicateLanguageID(new_id)

        # if map is initialised
        if bool(self._id_map):
            self.verify_fit('language ids', value)
            new_map = {}
            for (old_lang_id, new_lang_id) in zip(self._id_map, value):
                new_map[verify_id(new_lang_id)] = self._id_map[old_lang_id]
            self._id_map = new_map
        else:
            for lang_id in value:
                self._id_map[verify_id(lang_id)] = (None, None, None)

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
            self.verify_fit('glottocodes', value)
            for (lang_id, glottocode) in zip(self._id_map, value):
                (_, lang_name, lang_ascii) = self._id_map[lang_id]
                self._id_map[lang_id] = (glottocode, lang_name, lang_ascii)
        else:
            for glottocode in value:
                key = glottocode
                while key in self._id_map:
                    key = f'{key}+'
                self._id_map[key] = (glottocode, None, None)

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
            self.verify_fit('languages', value)
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

    def check_and_generate_ascii_names(self):
        if bool(self._id_map):
            (_, _, sample_ascii) = next(iter(self._id_map.values()))
            if sample_ascii is None:
                self.languages_ascii = [asciify_alphanumeric(l) for l in self.languages]

    @languages_ascii.setter
    def languages_ascii(self, value):
        # if map is initialised
        if bool(self._id_map):
            self.verify_fit('asciis', value)
            for (lang_id, lang_ascii) in zip(self._id_map, value):
                (glottocode, lang_name, _) = self._id_map[lang_id]
                self._id_map[lang_id] = (glottocode, lang_name, lang_ascii)
        else:
            for lang_ascii in value:
                self._id_map[lang_ascii] = (None, lang_ascii, None)

    def load_languages(self):
        raise NotImplementedError('load_languages method not implemented')

    def get_duplicate_glottocodes(self):
        uniques = set()
        doubles = set()
        for (glottocode, language_name, _) in self._id_map.values():
            if type(glottocode) is str:
                (uniques if glottocode not in uniques else doubles).add(glottocode)
            else:
                print(f"Warning: no glottocode specified for language '{language_name}'")
        return doubles

    def verify_unique_glottocodes(self):
        duplicates = self.get_duplicate_glottocodes()
        if len(duplicates) > 0:
            print(f"Warning: duplicate glottocodes '{"','".join(duplicates)}' found, perhaps implement self.patch()?")
            # raise DuplicateGlottocodes(duplicates)

    def patch(self):
        pass

    def verify_fit(self, parameter_name, value):
        try:
            assert len(self._id_map) == len(value)
        except:
            print(f'id_map ({len(self._id_map)}): {self._id_map}')
            print(f'{parameter_name} ({len(value)}): {value}')
            raise AssertionError(f'id_map and {parameter_name} must have same length')

    def set_language_glottocode(self, language_name, glottocode):
        found = False
        for key, (_, match_name, lang_ascii) in self._id_map.items():
            if language_name == match_name:
                self._id_map[key] = (glottocode, language_name, lang_ascii)
                found = True
                break
        if not found:
            raise LanguageNotFound(language_name, self.name)


def verify_id(lang_id):
    lang_id = str(lang_id)
    if not is_valid_identifier(lang_id):
        raise InvalidLanguageID(lang_id)
    return lang_id


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


class DuplicateLanguageID(Exception):
    def __init__(self, language_id):
        super().__init__(f"Duplicate language ID '{language_id}', language ID's must be unique")


class InvalidLanguageID(Exception):
    def __init__(self, language_id):
        super().__init__(
            f"Invalid language ID '{language_id}', may only contain alpha-numeric characters and underscores")
