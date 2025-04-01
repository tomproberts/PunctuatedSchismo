import pandas as pd

from scripts.families.indo_european import Italic, IndoEuropean
from scripts.predictors.polygons.glottography import Glottography, LiterallyNoPolygonException
from scripts.predictors.polygons.glottography_config import indoeuropean_config
from scripts.predictors.utils import write_out_df

POLYGON_SIZE = 'area'

if __name__ == '__main__':
    family = Italic()
    required_glottocodes = family.glottocodes

    glottography = Glottography(indoeuropean_config())

    df_glottocodes = []
    df_area = []
    for code in required_glottocodes:
        try:
            polygon = glottography.get_polygon(code)
            area = round(polygon.area.iloc[0], 0)
            # df_names.append()
            df_glottocodes.append(code)
            df_area.append(area)
        except LiterallyNoPolygonException as e:
            print(f'{e} ({family.get_language(code)})')

    df = pd.DataFrame({'glottocode': df_glottocodes, 'area_cartesian': df_area})
    file_name = f'{family.name}.area'
    write_out_df(POLYGON_SIZE, file_name, df)
