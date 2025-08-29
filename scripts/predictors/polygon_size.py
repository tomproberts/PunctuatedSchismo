import pandas as pd

from scripts.families.indo_european import IndoEuropean
from scripts.predictors.polygons.glottography import Glottography, LiterallyNoPolygonException
from scripts.predictors.polygons.glottography_config import get_config
from scripts.predictors.utils import write_out_df

POLYGON_SIZE = 'area'


def write_out_polygon_size(dataframe, family_name, type):
    file_name = f'{family_name}.{type}'
    write_out_df(POLYGON_SIZE, file_name, dataframe)


def calculate_areas(glottography, required_glottocodes):
    df_glottocodes = []
    df_area = []
    for code in required_glottocodes:
        try:
            polygon = glottography.get_polygon(code)
            area = round(polygon.area.iloc[0] / 1e6, 0)
            df_glottocodes.append(code)
            df_area.append(area)
        except LiterallyNoPolygonException as e:
            language_name = family.get_languages_from_glottocode(code)
            language_name = language_name[0] if len(language_name) == 1 else ', '.join(language_name)
            print(f'{e} ({language_name})')

    # TODO: Include sources?
    return pd.DataFrame({'glottocode': df_glottocodes, 'area_geodesic': df_area})


if __name__ == '__main__':
    family = IndoEuropean()
    required_glottocodes = family.glottocodes

    glottography = Glottography(get_config(family.name), geodesic=True)

    df = calculate_areas(glottography, required_glottocodes)
    # TODO: include language IDs
    write_out_polygon_size(df, family.name, type="geodesic")
    print(f'Wrote out polygon sizes for {family.name}')
