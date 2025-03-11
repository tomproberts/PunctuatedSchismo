from statistics import median

from strsimpy.normalized_levenshtein import NormalizedLevenshtein

from scripts.families.indo_european import Italic


def get_common_forms(family, lang1: str, lang2: str) -> (list[str], list[str]):
    # Get dataframe column names
    cognacy_column = family.COGNACY_COLUMN
    form_column = family.FORM_COLUMN

    # Get forms and corresponding cognate ids
    forms1 = family.get_forms(lang1, extended=True)
    forms2 = family.get_forms(lang2, extended=True)

    # Find common cognate ids and filter
    common_cognates = list(set(forms1[cognacy_column]) & set(forms2[cognacy_column]))
    filtered1 = list(forms1[forms1[cognacy_column].isin(common_cognates)][form_column])
    filtered2 = list(forms2[forms2[cognacy_column].isin(common_cognates)][form_column])

    assert len(filtered1) == len(filtered2)
    return filtered1, filtered2


def calc_phon_distances(forms1: list[str], forms2: list[str]) -> list[float]:
    # Calculate normalised levenshtein distances for each pair in aligned lists of cognate forms
    normalized_levenshtein = NormalizedLevenshtein()
    distances = []
    for f1, f2 in zip(forms1, forms2):
        distances.append(normalized_levenshtein.distance(f1, f2))
    return distances


def calc_phon_distance(forms1: list[str], forms2: list[str], average=median) -> float:
    # Calculate average normalised levenshtein distance between each pair in aligned lists of cognate forms
    distances = calc_phon_distances(forms1, forms2)
    if len(distances) == 0:
        return 0
    return average(distances)


def calculate_distances(family, pairs):
    # Calculate average phonological distance between pairs of languages (glottocodes)
    distances = []
    for lang1, lang2 in pairs:
        forms1, forms2 = get_common_forms(family, lang1, lang2)
        distance = calc_phon_distance(forms1, forms2)
        distances.append(distance)
    return distances


if __name__ == '__main__':
    family = Italic()
    # pairs can be calculated somewhere else since they're also needed for contact distances
    pairs = [('stan1290', 'fran1269'), ('ital1282', 'neap1235'), ('ital1282', 'mila1243')]  # ('stan1295', 'swis1247')
    distances = calculate_distances(family, pairs)

    forms1, forms2 = get_common_forms(family, 'stan1290', 'ital1282')
    print(forms1[0:20])
    print(forms2[0:20])
