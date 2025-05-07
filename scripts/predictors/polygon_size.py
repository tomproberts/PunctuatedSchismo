import pandas as pd

from scripts.families.dravidian import Dravidian
from scripts.predictors.polygons.glottography import Glottography, LiterallyNoPolygonException
from scripts.predictors.polygons.glottography_config import get_config
from scripts.predictors.utils import write_out_df

POLYGON_SIZE = 'area'


def write_out_polygon_size(dataframe, family_name):
    file_name = f'{family_name}.cartesian'
    write_out_df(POLYGON_SIZE, file_name, dataframe)


def calculate_areas(glottography, required_glottocodes):
    df_glottocodes = []
    df_area = []
    for code in required_glottocodes:
        try:
            polygon = glottography.get_polygon(code)
            area = round(polygon.area.iloc[0], 0)
            df_glottocodes.append(code)
            df_area.append(area)
        except LiterallyNoPolygonException as e:
            print(f'{e} ({family.get_language_from_glottocode(code)})')

    # TODO: Include sources?
    return pd.DataFrame({'glottocode': df_glottocodes, 'area_cartesian': df_area})


if __name__ == '__main__':
    family = Dravidian()
    required_glottocodes = family.glottocodes

    glottography = Glottography(get_config(family.name))

    df = calculate_areas(glottography, required_glottocodes)
    # TODO: include language IDs
    write_out_polygon_size(df, family.name)
