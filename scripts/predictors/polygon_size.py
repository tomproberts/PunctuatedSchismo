import pandas as pd

from scripts.families.indo_european import Italic
from scripts.predictors.polygons.glottography import Glottography
from scripts.predictors.utils import write_out_df

POLYGON_SIZE = 'area'

if __name__ == '__main__':
    glottography = Glottography()

    family = Italic()
    required_glottocodes = family.glottocodes

    df_glottocodes = []
    df_area = []
    for code in required_glottocodes:
        polygon = glottography.get_polygon(code)
        if polygon is not None:
            area = round(polygon.area.iloc[0], 0)
            # df_names.append(family.get_language(code))
            df_glottocodes.append(code)
            df_area.append(area)

    df = pd.DataFrame({'glottocode': df_glottocodes, 'area_cartesian': df_area})
    file_name = f'{family.name}.area'
    write_out_df(POLYGON_SIZE, file_name, df)
