import re
import unicodedata


def asciify(string):
    # change extended characters to ascii, e.g. ç to c, ā to a
    return unicodedata.normalize('NFKD', string).encode('ASCII', 'ignore').decode('ASCII')


def asciify_alphanumeric(string):
    # same as above but also remove spaces
    return re.sub(r'[ -:.\(\)]', '', asciify(string))
