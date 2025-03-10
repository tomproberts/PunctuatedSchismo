from statistics import median
import pandas as pd

from strsimpy.normalized_levenshtein import NormalizedLevenshtein


def get_common_forms(lang1: str, lang2: str) -> (list[str], list[str]):
    form = 'Form'  # 'Phonemic'
    all_languages = pd.read_csv("data/datasets/ie-cor/languages.csv")
    lang1_id = all_languages[all_languages.Glottocode == lang1].ID.iat[0]
    lang2_id = all_languages[all_languages.Glottocode == lang2].ID.iat[0]

    all_forms = pd.read_csv("data/datasets/ie-cor/forms.csv")
    all_forms1 = all_forms[all_forms.Language_ID == lang1_id][['ID', form, 'Parameter_ID']]
    all_forms2 = all_forms[all_forms.Language_ID == lang2_id][['ID', form, 'Parameter_ID']]

    all_cognates = pd.read_csv("data/datasets/ie-cor/cognates.csv")
    merged1 = all_forms1.merge(all_cognates, left_on='ID', right_on='Form_ID', suffixes=('', 'y'))[
        ['ID', 'Parameter_ID', form, 'Cognateset_ID']]
    merged2 = all_forms2.merge(all_cognates, left_on='ID', right_on='Form_ID', suffixes=('', 'y'))[
        ['ID', 'Parameter_ID', form, 'Cognateset_ID']]

    common_cognates = list(set(merged1.Cognateset_ID) & set(merged2.Cognateset_ID))

    forms1 = list(merged1[merged1.Cognateset_ID.isin(common_cognates)].sort_values(by=['Parameter_ID'])[form])
    forms2 = list(merged2[merged2.Cognateset_ID.isin(common_cognates)].sort_values(by=['Parameter_ID'])[form])
    assert len(lang1) == len(lang2)
    return forms1, forms2


def calc_phon_distances(forms1: list[str], forms2: list[str]) -> list[float]:
    normalized_levenshtein = NormalizedLevenshtein()
    distances = []
    for f1, f2 in zip(forms1, forms2):
        distances.append(normalized_levenshtein.distance(f1, f2))
    return distances


def calc_phon_distance(forms1: list[str], forms2: list[str], fold=median) -> float:
    distances = calc_phon_distances(forms1, forms2)
    return fold(distances)


if __name__ == '__main__':
    pairs = [('stan1290', 'fran1269'), ('ital1282', 'neap1235'), ('ital1282', 'mila1243'), ('stan1295', 'swis1247')]
    for lang1, lang2 in pairs:
        forms1, forms2 = get_common_forms(lang1, lang2)
        distance = calc_phon_distance(forms1, forms2)
        print(f"Levenshtein Distance between {lang1} and {lang2} is {distance}")
