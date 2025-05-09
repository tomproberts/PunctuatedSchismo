import pandas as pd
from tqdm import tqdm

from scripts.utils import asciify_alphanumeric

COGNATE_MATRIX_CSV = "data/datasets/uralex/cognate_matrix.csv"


def get_cognate_matrix():
    uralic_forms = pd.read_csv("data/datasets/uralex/forms.csv")
    uralic_forms.Language_ID = uralic_forms.Language_ID.astype(str)
    uralic_forms.Parameter_ID = uralic_forms.Parameter_ID.astype(str)
    uralic_forms.form_set = uralic_forms.form_set.astype(str)

    parameter_ids = uralic_forms.Parameter_ID.unique()

    uralic_languages = pd.read_csv("data/datasets/uralex/languages.csv", index_col=0)
    uralic_languages.index = uralic_languages.index.astype(str)
    uralic_languages.sort_index(inplace=True)
    languages = list(uralic_languages.index)
    names = [asciify_alphanumeric(l) for l in list(uralic_languages.Name)]

    n_langs = len(languages)
    all_params = {}

    for param in tqdm(parameter_ids):
        forms = uralic_forms[uralic_forms.Parameter_ID == param]
        forms = forms[['Language_ID', 'form_set']]

        forms = forms.groupby('Language_ID', as_index=False).agg({'form_set': ';'.join}).drop_duplicates(keep='first')

        if forms.shape[0] != n_langs:
            for lang in set(languages) - set(forms.Language_ID):
                forms.loc[-1] = [lang, '?']

        forms.set_index('Language_ID', inplace=True)
        forms = forms.sort_index()
        all_params[f'param{param}'] = list(forms['form_set'])

    cognate_matrix = pd.DataFrame(data={'ID': languages, 'Language': names, **all_params})
    cognate_matrix.set_index('ID', inplace=True)
    cognate_matrix.sort_index(inplace=True)
    # cognate_matrix.to_csv(COGNATE_MATRIX_CSV)
    return cognate_matrix


def make_binarised(cognate_matrix):
    for series_name, series in tqdm(cognate_matrix.items()):
        if not str(series_name).startswith('param'): continue
        series = series.astype(str)

        unique_cognate_sets = set((';'.join(series.values)).split(';')) - set('?')
        # Convert to binary
        pos_map = dict((j, i) for i, j in enumerate(sorted(unique_cognate_sets)))

        len1 = len(unique_cognate_sets)
        blank = '0' * len1
        missing_cognate = '?' * len1

        # Convert to binary
        binarised_all = []
        for v in series.values:
            binarised = blank
            required_sets = v.split(';')
            for s in required_sets:
                if s == '?':
                    binarised = missing_cognate
                else:
                    i = pos_map[s]
                    binarised = f'{binarised[:i]}1{binarised[i + 1:]}'
            binarised_all.append(binarised)

        assert len(series) == len(binarised_all)
        cognate_matrix[series_name] = binarised_all

    return cognate_matrix


if __name__ == "__main__":
    cognate_matrix = get_cognate_matrix()
    cognate_matrix = make_binarised(cognate_matrix)

    cognate_matrix.to_csv(COGNATE_MATRIX_CSV)
    print(f"Wrote cognate matrix to {COGNATE_MATRIX_CSV}")
