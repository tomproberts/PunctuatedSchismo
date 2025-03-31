import geopandas
import pandas as pd
from shapely.measurement import length

from scripts.families.indo_european import Italic
from scripts.predictors.utils import write_out_df

POLYGON_SIZE = 'area'

if __name__ == '__main__':
    glottocodes = pd.read_csv(
        '/home/thomas/gis/glottography-data/bouckaert2012indoeuropean/bouckaert2012indoeuropean_glottocode_to_polygons.csv',
        index_col=0)[['name', 'glottocode', 'year']]
    countries_gdf = geopandas.read_file(
        '/home/thomas/gis/glottography-data/bouckaert2012indoeuropean/bouckaert2012indoeuropean_raw.gpkg')

    family = Italic()
    italics = family.glottocodes
    polygon_glottocodes = list(glottocodes.glottocode)

    df_glottocodes = []
    df_area = []
    for code in italics:
        if code in polygon_glottocodes:
            row = glottocodes[glottocodes.glottocode == code]
            if len(row) > 1:
                print(f'{row}')
            id = row.index.values[0]
            area = round(countries_gdf[countries_gdf.polygon_id == id].area.iloc[0], 0)

            df_glottocodes.append(code)
            # df_names.append(family.get_language(code))
            df_area.append(area)

    df = pd.DataFrame({'glottocode': df_glottocodes, 'area_cartesian': df_area})
    file_name = f'{family.name}.area'
    write_out_df(POLYGON_SIZE, file_name, df)
