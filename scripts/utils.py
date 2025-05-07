import re
import unicodedata


def asciify(string):
    # change extended characters to ascii, e.g. ç to c, ā to a
    return unicodedata.normalize('NFKD', string).encode('ASCII', 'ignore').decode('ASCII')


def asciify_alphanumeric(string):
    # same as above but also remove spaces
    return re.sub(r'[ -:.\(\)]', '', asciify(string))


def is_valid_identifier(id: str) -> bool:
    return id == re.sub(r'([a-zA-Z0-9_]+)', r'\1', id)
