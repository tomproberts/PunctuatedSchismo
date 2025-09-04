import pandas as pd
from tqdm import tqdm

from scripts.families.indo_european import IndoEuropean
from scripts.predictors.polygons.glottography import Glottography, LiterallyNoPolygonException, MultiplePolygonException
from scripts.predictors.polygons.glottography_config import get_config
from scripts.predictors.utils import write_out_df

POLYGON_SIZE = 'area'


def write_out_polygon_size(dataframe, family_name, type):
    file_name = f'{family_name}.{type}'
    write_out_df(POLYGON_SIZE, file_name, dataframe)


def calculate_areas(glottography, asciis):
    df_ascii = []
    df_glottocodes = []
    df_area = []
    errors = []
    for lang in tqdm(asciis):
        code = family.get_glottocode_from_ascii(lang)
        try:
            polygon = glottography.get_polygon(code)
            area = round(polygon.area.iloc[0] / 1e6, 0)
            df_ascii.append(lang)
            df_glottocodes.append(code)
            df_area.append(area)
        except (LiterallyNoPolygonException, MultiplePolygonException) as e:
            errors.append(f'{e} ({family.get_language_from_ascii(lang)})')

    # display errors
    print('\n'.join(errors))

    # TODO: Include sources?
    return pd.DataFrame({'lang': df_ascii, 'glottocode': df_glottocodes, 'area': df_area})


if __name__ == '__main__':
    family = IndoEuropean()
    required_ascii = family.languages_ascii

    glottography = Glottography(get_config(family.name), geodesic=True)

    df = calculate_areas(glottography, required_ascii)
    write_out_polygon_size(df, family.name, type="geodesic")
    print(f'Wrote out polygon sizes for {family.name}')
