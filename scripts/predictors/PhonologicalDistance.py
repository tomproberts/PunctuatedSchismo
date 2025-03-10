from statistics import median

from strsimpy.normalized_levenshtein import NormalizedLevenshtein

from scripts.families.IndoEuropean import Italic, IE_COR_FORM_COLUMN


def get_common_forms(family, lang1: str, lang2: str) -> (list[str], list[str]):
    forms1 = family.get_forms(lang1, extended=True)
    forms2 = family.get_forms(lang2, extended=True)

    common_cognates = list(set(forms1.Cognateset_ID) & set(forms2.Cognateset_ID))

    forms1 = list(
        forms1[forms1.Cognateset_ID.isin(common_cognates)].sort_values(by=['Parameter_ID'])[IE_COR_FORM_COLUMN])
    forms2 = list(
        forms2[forms2.Cognateset_ID.isin(common_cognates)].sort_values(by=['Parameter_ID'])[IE_COR_FORM_COLUMN])

    assert len(forms1) == len(forms2)
    return forms1, forms2


def calc_phon_distances(forms1: list[str], forms2: list[str]) -> list[float]:
    normalized_levenshtein = NormalizedLevenshtein()
    distances = []
    for f1, f2 in zip(forms1, forms2):
        distances.append(normalized_levenshtein.distance(f1, f2))
    return distances


def calc_phon_distance(forms1: list[str], forms2: list[str], fold=median) -> float:
    distances = calc_phon_distances(forms1, forms2)
    if len(distances) == 0:
        return 0
    return fold(distances)


if __name__ == '__main__':
    family = Italic()
    # family.language_ids = [17, 25, 39, 42, 56, 59, 62, 63, 68, 76, 112, 122, 130, 132, 189, 203, 204, 207, 209, 220, 281, 283, 289, 305, 311]
    pairs = [('stan1290', 'fran1269'), ('ital1282', 'neap1235'), ('ital1282', 'mila1243')]  # ('stan1295', 'swis1247')
    for lang1, lang2 in pairs:
        forms1, forms2 = get_common_forms(family, lang1, lang2)
        distance = calc_phon_distance(forms1, forms2)
        print(
            f"Levenshtein Distance between {family.get_language(lang1)} and {family.get_language(lang2)} is {distance}")
    print(family.get_forms('stan1290'))
